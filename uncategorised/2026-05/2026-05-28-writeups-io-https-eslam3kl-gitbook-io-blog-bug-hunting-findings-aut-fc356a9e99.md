# Authentication Bypass Using Empty Parameters

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Pentest Client (Undisclosed)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Logic Error, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://eslam3kl.gitbook.io/blog/bug-hunting-findings/authentication-bypass-using-empty-parameters.

## Summary
A custom framework's login function contains improper conditional logic that fails to terminate authentication flow when credentials are invalid or empty, allowing attackers to bypass authentication by submitting empty parameters. The vulnerability stems from IF statements that don't properly exit the function when conditions are false, allowing execution to continue and potentially authenticate as a default user (possibly admin).

## Attack scenario (step by step)
1. Attacker intercepts the login request containing JSON credentials
2. Attacker modifies the JSON payload to remove or empty the username/password parameters
3. Attacker sends the modified request with empty/missing credential values
4. Server-side IF statements fail to properly validate and reject empty parameters
5. Authentication logic continues execution instead of terminating
6. Attacker gains access, potentially authenticated as a default admin user

## Root cause
Custom framework's login function uses improper conditional logic where IF statements checking credential validity do not explicitly return/exit on false conditions, allowing subsequent authentication code to execute regardless of validation failures. The function likely defaults to authenticating a default user (admin) when credential parameters are empty or malformed.

## Attacker mindset
Fuzzing input parameters to identify edge cases where validation logic breaks. Testing with empty values and parameter manipulation to bypass business logic. Analyzing custom framework behavior to identify non-standard error handling patterns.

## Defensive takeaways
- Implement explicit exit/return statements after failed authentication checks; never rely on conditional flow alone
- Validate that all required authentication parameters are present and non-empty before any processing
- Use deny-by-default approach: require explicit success conditions rather than allowing execution to continue on failures
- Implement comprehensive input validation that rejects empty or null credential parameters
- Add rate limiting and account lockout mechanisms to detect brute force attempts
- Log and alert on suspicious authentication patterns including empty parameter submissions
- Use established authentication libraries rather than custom implementations prone to logic errors
- Implement defensive coding practices requiring explicit null/empty checks with clear error handling

## Variant hunting
['Test other authentication endpoints (password reset, account recovery) for similar logic flaws', 'Submit null values instead of empty strings to see if validation differs', 'Test with partial credential submission (username only, no password)', 'Attempt to authenticate with whitespace-only parameters', 'Test other JSON endpoints for similar conditional logic vulnerabilities', 'Check if other user roles can be targeted besides admin through parameter manipulation', 'Examine if the framework has similar vulnerabilities in authorization checks post-authentication']

## MITRE ATT&CK
- T1190
- T1078
- T1556

## Notes
The writeup demonstrates the importance of testing edge cases with empty/null values. The discovery process (attempting XXE conversion, then JSON manipulation) shows methodical security testing. Custom frameworks are particularly vulnerable to logic errors compared to established libraries. The involvement of multiple researchers suggests this required collaborative debugging to understand the non-obvious conditional flow issue.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
