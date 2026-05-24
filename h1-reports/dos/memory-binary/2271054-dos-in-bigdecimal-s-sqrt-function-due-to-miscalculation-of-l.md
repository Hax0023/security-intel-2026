# DoS in BigDecimal#sqrt due to Inverted Loop Iteration Limit Check

## Metadata
- **Source:** HackerOne
- **Report:** 2271054 | https://hackerone.com/reports/2271054
- **Submitted:** 2023-12-04
- **Reporter:** z2_
- **Program:** Ruby (bigdecimal extension)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Resource Exhaustion, Logic Error
- **CVEs:** None
- **Category:** memory-binary

## Summary
The BigDecimal#sqrt function in Ruby's bigdecimal extension contains a logic error where the iteration limit check uses 'less than' instead of 'greater than', allowing attackers to force up to 10,000 iterations instead of the intended maximum of 100. This causes the Ruby interpreter to hang indefinitely, blocking all event processing and requiring SIGKILL to terminate.

## Attack scenario
1. Attacker identifies a Ruby application that calls BigDecimal#sqrt with user-controlled precision parameter
2. Attacker supplies a large precision value (e.g., 10000) and a large decimal number (e.g., 6E19) to the sqrt function
3. The inverted comparison (n < maxnr instead of n > maxnr) fails to cap iterations at 100
4. The loop executes 10,000 iterations instead of 100, consuming significant CPU time
5. The native C loop blocks the entire Ruby interpreter, preventing signal delivery and event processing
6. Application becomes unresponsive; legitimate users experience service unavailability until process is forcefully killed

## Root cause
Logic error in ext/bigdecimal/bigdecimal.c line 7220: comparison operator uses '<' instead of '>', treating maxnr (100) as a lower bound rather than upper bound for iteration count 'n'. The calculation sets n = y_prec * BASE_FIG, which can be arbitrarily large; the buggy check only forces n to maxnr if n is already below maxnr, allowing user-supplied precision parameters to bypass the intended safety limit.

## Attacker mindset
An attacker exploits this to achieve application-level denial of service by triggering computationally expensive iterations. The ease of exploitation (single function call with controlled parameters) combined with the interpreter-wide blocking makes this an attractive attack vector against Ruby services that expose BigDecimal arithmetic operations to untrusted input.

## Defensive takeaways
- Implement strict input validation and sanitization on precision parameters for cryptographic and numerical operations, with hard caps enforced regardless of user input
- Use unsigned/bounded integer types and explicit range checks to prevent parameter-driven resource exhaustion in C extensions
- Conduct thorough code review of boundary condition logic, particularly comparison operators that enforce limits (< vs > vs <=  vs >=)
- Add fuzz testing and performance regression tests for mathematical functions with user-controllable iteration counts
- Implement timeouts or iteration budgets in long-running C extension functions to prevent interpreter-wide blocking
- Document and validate the semantics of limit-checking logic with unit tests covering both under and over-limit scenarios

## Variant hunting
Search for similar inverted comparison logic in other cryptographic or numerical C extensions (OpenSSL, GMP, MPFR bindings). Examine iteration loops in bignum implementations, matrix operations, and transcendental function approximations. Check for other uses of maxnr constant and similar bounded-iteration patterns that may have copy-pasted the same bug. Review precision/scale parameter handling in financial or scientific computing libraries.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service

## Notes
The fix is minimal (single character change from < to >) and all existing tests pass, indicating this was a simple typo rather than intentional design. The vulnerability is trivial to trigger and has been present since at least version 3.2.2. The blocking nature of the C loop (inability to receive SIGTERM, requiring SIGKILL) suggests Ruby's GIL/interpreter lock prevents signal handlers from executing during native extension code. This pattern should be searched for in other Ruby C extensions.

## Full report
<details><summary>Expand</summary>

# Vulnerability
__Affected Product__: `bigdecimal` extension in https://github.com/ruby/ruby
__Affected Versions__: At least version 3.2.2, I didn't test any previous versions

The current implementation of `BigDecimal#sqrt` in `ext/bigdecimal/bigdecimal.c` erroneously checks its parameter
and allows users of the function to control how long it will run. This may lead to
a DoS if the parameter to the function can be controlled by an attacker.

The implementation of `BigDecimal#sqrt` involves a loop that iteratively calculates
the value of the square root:
```c
do {
    y->MaxPrec *= 2;
    if (y->MaxPrec > y_prec) y->MaxPrec = y_prec;
    f->MaxPrec = y->MaxPrec;
    VpDivd(f, r, x, y);        /* f = x/y    */
    VpAddSub(r, f, y, -1);     /* r = f - y  */
    VpMult(f, VpConstPt5, r);  /* f = 0.5*r  */
    if (VpIsZero(f))
        goto converge;
    VpAddSub(r, f, y, 1);      /* r = y + f  */
    VpAsgn(y, r, 1);           /* y = r      */
} while (++nr < n);
```
The number of iterations is determined by the number `n`, which is derived from the
parameter of the `sqrt` function.
The application tries to impose a limit on the number of iterations, as can be seen
in line 4659:
```c
#define maxnr 100UL    /* Maximum iterations for calculating sqrt. */
```
However, the calculation of `n` is erroneous and uses `maxnr` as a _lower_ bound and not
an upper bound for `n` as can be seen in line 7220:
```c
if (n < (SIGNED_VALUE)maxnr) n = (SIGNED_VALUE)maxnr;
```
This may cause the program to have more iterations than originally intended.

# Proof of Concept
The following ruby program iterates 10000 times instead of 100 and takes longer than 10 min to complete on my machine:
```rb
require 'bigdecimal'
BigDecimal("6E19").sqrt(10000)
```
Furthermore, it can be observed the ruby interpreter stalls completely. The program has to be killed with SIGKILL.

# Solution
The following patch resolves the error:
```diff
diff --git a/ext/bigdecimal/bigdecimal.c b/ext/bigdecimal/bigdecimal.c
index 07c2bcf0b5..31e5574574 100644
--- a/ext/bigdecimal/bigdecimal.c
+++ b/ext/bigdecimal/bigdecimal.c
@@ -7217,7 +7217,7 @@ VpSqrt(Real *y, Real *x)
     y->MaxPrec = Min((size_t)n , y_prec);
     f->MaxPrec = y->MaxPrec + 1;
     n = (SIGNED_VALUE)(y_prec * BASE_FIG);
-    if (n < (SIGNED_VALUE)maxnr) n = (SIGNED_VALUE)maxnr;
+    if (n > (SIGNED_VALUE)maxnr) n = (SIGNED_VALUE)maxnr;

     /*
      * Perform: y_{n+1} = (y_n - x/y_n) / 2
```
This change maintains the correctness of the implementation. 
I have checked this against the test suite from https://github.com/ruby/bigdecimal and all the tests still pass.

## Impact

If an attacker can control the parameter to `BigDecimal#sqrt` he/she can cause a ruby program to hang
for a long time.
Furtermore, since the loop is inside of a function of an extension it blocks the interpreter / execution engine
as a whole hindering the delivery of events or signals.
As seen above, a ruby program that is caught up in such a loop can only be interrupted by a SIGKILL signal.
Since the bug is
1. Easy to trigger if the necessary conditions are met
2. Has a huge effect for relatively small input values

I chose the severity medium.

</details>

---
*Analysed by Claude on 2026-05-24*
