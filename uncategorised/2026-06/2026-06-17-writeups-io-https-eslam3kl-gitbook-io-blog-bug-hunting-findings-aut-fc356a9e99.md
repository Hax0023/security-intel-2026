# Authentication Bypass Using Empty Parameters

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Pentesting Client (Undisclosed)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Improper Input Validation, Logic Error in Conditional Statements
- **Category:** uncategorised
- **Writeup:** https://eslam3kl.gitbook.io/blog/bug-hunting-findings/authentication-bypass-using-empty-parameters.

## Summary
A custom framework's login function contained improperly configured conditional statements that failed to terminate execution when authentication checks returned false. By submitting empty or malformed JSON parameters in the login request, the function continued processing and authenticated users as the default admin account.

## Attack scenario (step by step)
1. Attacker identifies the login endpoint that accepts JSON credentials (username/password)
2. Attacker intercepts the login POST request and examines the JSON structure
3. Attacker modifies the JSON payload to contain empty parameters instead of valid credentials
4. Due to missing else-return logic, the conditional checks fail but execution continues
5. The application proceeds to set the user session to a default admin user account
6. Attacker successfully logs in with elevated privileges without providing valid credentials

## Root cause
The custom framework's login function used IF statements without proper termination logic (missing else-return or exit conditions). When credential validation failed, the code did not halt execution, allowing the function to continue and authenticate the user as a default account.

## Attacker mindset
The attacker systematically tested input manipulation techniques (XXE conversion attempts) before discovering the logic flaw. Rather than accepting initial failures, they collaborated with peers to analyze how input format changes affected server behavior, ultimately revealing the broken conditional logic in the authentication handler.

## Defensive takeaways
- Always include explicit exit/return statements in authentication conditional logic to prevent fallthrough execution
- Implement proper else-branches that deny access by default rather than relying on incomplete if-chains
- Use security frameworks instead of custom authentication implementations to leverage battle-tested logic
- Validate all input parameters are non-empty and meet expected formats before processing
- Perform code review specifically checking for missing termination conditions in authentication flows
- Test authentication with empty, null, and malformed parameters as part of security testing
- Implement centralized error handling that denies access on any validation failure

## Variant hunting
['Test other sensitive endpoints that use similar custom frameworks for missing return/exit statements', 'Attempt parameter omission attacks on password reset, account recovery, and permission-checking functions', 'Try sending JSON with null values, empty strings, or missing fields entirely to trigger fallthrough logic', 'Look for other endpoints that process conditional authentication checks without explicit denial paths', 'Test API endpoints that may use the same vulnerable authentication pattern across different functions']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1556 - Modify Authentication Process

## Notes
The vulnerability hinged on code logic rather than cryptographic or protocol weaknesses. The author initially pursued XXE exploitation before recognizing the underlying conditional logic flaw through systematic testing and peer collaboration. This demonstrates the importance of iterative analysis and team discussion in vulnerability research. The exact target and bounty amount were not disclosed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
