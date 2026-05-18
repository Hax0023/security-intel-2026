# Authentication Bypass Using Empty Parameters

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Undisclosed Pen-Testing Client
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Logic Flaw, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://eslam3kl.gitbook.io/blog/bug-hunting-findings/authentication-bypass-using-empty-parameters.

## Summary
A custom framework's login function fails to properly terminate execution when authentication checks fail, allowing attackers to bypass authentication by sending empty or malformed JSON credentials. The vulnerability exists in inadequately configured IF statement logic that continues execution instead of terminating when credential validation fails.

## Attack scenario (step by step)
1. Attacker intercepts normal login request containing JSON credentials
2. Attacker modifies the request to send empty parameters or removes credential fields entirely
3. Backend IF statement conditions evaluate to false but execution continues instead of terminating
4. Processing falls through to default user assignment logic
5. Attacker gains authenticated access as the default admin user
6. Attacker achieves unauthorized access to restricted functionality

## Root cause
Improperly configured conditional logic in custom authentication framework where failed authentication conditions do not terminate the login process. The code lacks proper exit/return statements after validation failure, causing execution to continue to default case handling.

## Attacker mindset
Methodical fuzzing and parameter manipulation to discover edge cases in authentication logic. Attacker tested multiple bypass techniques (XXE, JSON manipulation) before identifying the core issue of missing validation termination conditions.

## Defensive takeaways
- Always explicitly terminate execution with return/throw statements after failed authentication checks
- Implement whitelist-based validation rather than blacklist approach for credentials
- Validate that all required parameters are present and non-empty before processing
- Use security-focused frameworks instead of custom authentication implementations
- Implement comprehensive logging and alerting for failed authentication attempts
- Conduct thorough code review focusing on control flow in authentication pathways
- Apply principle of fail-secure: deny access by default unless all conditions pass
- Test authentication logic with empty, null, and missing parameters as part of security testing

## Variant hunting
['Test other endpoints using custom framework for similar control flow issues', 'Attempt authorization bypass with empty or missing role parameters', 'Try sending null values instead of empty strings in authentication parameters', 'Test for similar issues in password reset and session management functions', 'Fuzz parameter names and test case sensitivity in authentication handlers', 'Check for default user/admin assignments in error handling paths', 'Test multi-stage authentication processes for incomplete validation chains']

## MITRE ATT&CK
- T1190
- T1078
- T1556

## Notes
The vulnerability demonstrates importance of secure coding practices in authentication systems. The attacker's methodical approach of testing multiple bypass techniques before identifying the root cause is instructive. The use of custom frameworks without proper security controls significantly increases risk. Collaboration with team members facilitated deeper analysis and root cause identification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
