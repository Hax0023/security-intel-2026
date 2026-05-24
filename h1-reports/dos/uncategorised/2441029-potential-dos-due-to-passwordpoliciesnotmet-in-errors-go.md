# Denial of Service via Unbounded PasswordPoliciesNotMet Error Collection

## Metadata
- **Source:** HackerOne
- **Report:** 2441029 | https://hackerone.com/reports/2441029
- **Submitted:** 2024-03-29
- **Reporter:** sinic
- **Program:** Unknown
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Denial of Service, Resource Exhaustion, Memory Exhaustion, Uncontrolled Resource Allocation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The PasswordPoliciesNotMet struct in errors.go accumulates an unbounded number of PasswordPolicyError instances without limits, allowing an attacker to trigger multiple password policy violations simultaneously and cause excessive memory consumption or system crashes. The Error() method converts all collected errors into a single string, amplifying memory usage through string allocations and concatenations.

## Attack scenario
1. Attacker identifies a password validation endpoint that checks multiple password policies (complexity, length, history, etc.)
2. Attacker crafts a password that violates numerous password policies simultaneously
3. Attacker submits multiple rapid requests with policy-violating passwords to accumulate PasswordPolicyError instances
4. Each failed validation adds another PasswordPolicyError to the UnMetPasswordPolicies slice without limits
5. The Error() method allocates strings and joins them, consuming heap memory proportionally to the number of errors
6. Continued requests cause memory exhaustion, leading to performance degradation, OOM errors, or service denial

## Root cause
Lack of bounds checking on the UnMetPasswordPolicies slice. The error collection mechanism has no maximum size limit, allowing the slice to grow unbounded. Additionally, the Error() method materializes all errors into memory simultaneously when converting to string representation.

## Attacker mindset
An attacker would recognize that password validation is typically a user-facing endpoint with rate limiting applied at HTTP layer but not at business logic layer. By triggering validation failures with policies that aggregate multiple errors, the attacker exploits the assumption that error handling is lightweight and can be scaled without bounds.

## Defensive takeaways
- Implement a maximum cap on error collection (e.g., max 10-20 policy errors per validation attempt)
- Use early exit strategies when critical policy failures occur rather than collecting all failures
- Lazy-evaluate error strings instead of materializing all errors at once in Error() method
- Implement rate limiting at validation layer, not just HTTP layer
- Monitor memory consumption patterns during validation failures
- Consider returning only the first N policy violations to callers rather than all violations
- Add resource limits and circuit breakers for error object creation
- Test error handling paths with fuzzing and resource exhaustion scenarios

## Variant hunting
Search for other error structs with unbounded slice fields that call Error() methods during error handling
Look for validation endpoints that accumulate errors in loops without size checks (validation chains, multiple validators)
Identify error aggregators in form validation, schema validation, or rule engines
Check for similar patterns in error collection within batch processing or multi-step validation workflows
Hunt for string.Join() or repeated Sprintf() calls on unbounded error slices
Review error handling in multi-field validation forms or complex object validation

## MITRE ATT&CK
- T1190
- T1499

## Notes
This is a classic resource exhaustion vulnerability that exploits the assumption of 'one request = one error'. The vulnerability is particularly dangerous because it occurs at the application logic layer where rate limiting may not apply. The fix should prioritize capping error collection while maintaining sufficient error reporting for legitimate debugging purposes. Similar patterns should be audited across the codebase wherever errors are collected in loops or aggregated structures.

## Full report
<details><summary>Expand</summary>

## Summary:
Possible DoS depending on amount of `PasswordPolicyError` instances that can be created in a short time

```
type PasswordPoliciesNotMet struct {
	UnMetPasswordPolicies []PasswordPolicyError
}

func (e PasswordPoliciesNotMet) Error() string {
	errorStrs := make([]string, 0, len(e.UnMetPasswordPolicies))
	for _, ppe := range e.UnMetPasswordPolicies {
		errorStrs = append(errorStrs, ppe.Error())
	}
	return fmt.Sprintf("Password policies not met due to: %s", strings.Join(errorStrs, ", "))
}
```

## Bug:
The possible vulnerability is in the `PasswordPoliciesNotMet` struct. This struct collects all errors when password policies fail. But it does not limit the number of errors it can collect. If multiple instance of policies fail together, the struct will have huge number of errors. This can make system use lot of memory or even crash due to flood of errors.

## Fix:
To fix this, we need to make sure the `PasswordPoliciesNotMet` struct doesn't collect an unlimited number of errors. Set a limit on how many errors it can store or find some other way to handle a large number of errors in better way.

## Impact

Can lead to lot of memory consumption or denial of service(DoS) attack if many policies fail together.

</details>

---
*Analysed by Claude on 2026-05-24*
