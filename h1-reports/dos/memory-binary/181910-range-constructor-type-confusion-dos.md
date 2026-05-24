# Range constructor type confusion DoS

## Metadata
- **Source:** HackerOne
- **Report:** 181910 | https://hackerone.com/reports/181910
- **Submitted:** 2016-11-13
- **Reporter:** h72
- **Program:** mruby
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** type confusion, use-after-free, denial of service, memory corruption
- **CVEs:** None
- **Category:** memory-binary

## Summary
A type confusion vulnerability in mruby's Range class constructor allows an attacker to crash the interpreter by redefining the Range constant to point to a different class, then using range literal syntax. The vulnerability arises from runtime constant lookup that fails to validate the returned object's type, causing memory layout confusion between RRange and other struct types.

## Attack scenario
1. Attacker identifies that mruby performs runtime constant lookup for the Range class during range literal creation
2. Attacker redefines the global Range constant to point to the Array class or another incompatible class
3. Attacker triggers range literal syntax (e.g., (1..2)) which invokes mrb_range_new
4. mrb_range_new allocates memory using the redefined class's layout expectations
5. A subsequent instance method call (e.g., .inspect) attempts to access RRange::edges field
6. The field offset corresponds to a different struct member in the actual object, causing segmentation fault or potential memory corruption

## Root cause
The mrb_range_new function uses dynamic runtime constant lookup to find the Range class rather than caching a reference to the canonical Range class in mrb_state. When the Range constant is redefined to reference an incompatible class, the function proceeds to create an object with RRange memory layout expectations, but the runtime expects a different struct layout, causing field offset misalignment.

## Attacker mindset
An attacker exploiting this would be motivated by denial of service attacks against mruby-based applications. The vulnerability is trivial to trigger and requires no special privileges. While the researcher notes potential RCE possibilities, the primary impact is reliable DoS through interpreter crashes.

## Defensive takeaways
- Cache references to core builtin classes in the interpreter state rather than performing runtime constant lookups during object construction
- Validate class compatibility before creating instances with expected memory layouts
- Implement type checks when constructing objects that rely on specific struct layouts
- Consider making core class definitions immutable or protected from user redefinition
- Add assertions or runtime checks to verify struct field offsets match expected values
- Audit all builtin type constructors for similar constant lookup vulnerabilities

## Variant hunting
Search for other builtin class constructors that perform runtime constant lookups (Hash, String, Array, etc.). Check for any object construction paths that assume specific struct layouts without validating the class actually uses that layout. Look for similar patterns in other Ruby implementations (CRuby, JRuby) and other dynamically typed languages.

## MITRE ATT&CK
- T1190
- T1499

## Notes
The researcher provided a patch implementing the fix by adding a range_class field to mrb_state, mirroring the pattern already used for other core classes in mruby. This suggests the vulnerability was an oversight in the Range class implementation while other core classes had already been hardened. The vulnerability is particularly interesting because it demonstrates type confusion at the C struct level in an interpreter, where high-level language semantics (redefining Range) directly cause low-level memory corruption.

## Full report
<details><summary>Expand</summary>

It's possible to crash mruby by redefining the `Range` class and then using the range literal syntax:

    Range = Array
    (1..2).inspect

The `mrb_range_new` function allocates and initializes a range object backed by the `RRange` struct, however it uses runtime constant lookup to find the `Range` class object. Redefining the `Range` constant to point to a different class and calling an instance method causes a segfault, as the `RRange::edges` field is confused for the `iv` field on other structs.

It may be possible to achieve RCE through this vulnerability, but there are significant complicating factors and I have not spent the time trying to develop an RCE PoC.

I have attached a patch which fixes this bug. My patch adds a `range_class` field to `mrb_state`, following the pattern other core classes use to avoid runtime constant lookups.

</details>

---
*Analysed by Claude on 2026-05-24*
