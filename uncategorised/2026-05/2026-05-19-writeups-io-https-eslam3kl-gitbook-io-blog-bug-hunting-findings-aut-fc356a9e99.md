# Authentication Bypass Using Empty Parameters

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Undisclosed Pen-Testing Client
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Logic Error, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://eslam3kl.gitbook.io/blog/bug-hunting-findings/authentication-bypass-using-empty-parameters.

## Summary
A custom framework's login function failed to properly validate JSON credentials due to flawed conditional logic that did not terminate execution when authentication checks failed. By sending empty or malformed JSON parameters, attackers could bypass authentication and gain unauthorized access, including admin privileges.

## Attack scenario (step by step)
1. Attacker identifies login endpoint accepts JSON formatted credentials
2. Attacker intercepts legitimate login request to analyze request/response structure
3. Attacker modifies JSON payload by removing or emptying credential parameters
4. Due to improper IF statement logic, failed validation conditions allow execution to continue
5. Application processes request without credentials and falls back to default user (admin)
6. Attacker gains authenticated session as administrator without valid credentials

## Root cause
The custom authentication framework used incomplete IF statement conditions that failed to properly terminate execution when authentication checks were false, allowing subsequent code to execute and authenticate with default/empty values.

## Attacker mindset
Methodical testing of input handling - attempting XXE exploitation first, then identifying that JSON structure manipulation (including empty parameters) could trigger authentication bypass through logic flaws in the framework.

## Defensive takeaways
- Implement explicit authentication success/failure logic with proper execution termination
- Validate all required authentication parameters are present and non-empty before processing
- Use positive security model - explicitly allow only valid states rather than checking for invalid ones
- Implement comprehensive logging and monitoring of authentication attempts
- Never rely on default values or fallback users during authentication
- Apply security testing to custom frameworks equivalent to third-party dependencies
- Use code review and static analysis to identify control flow issues in authentication logic

## Variant hunting
Search for similar logic errors in custom authentication frameworks; test endpoints that accept multiple input formats (JSON, XML, form data); attempt parameter stripping/emptying on all authentication mechanisms; look for implicit default user assignments when primary authentication fails.

## MITRE ATT&CK
- T1190
- T1556
- T1110

## Notes
The vulnerability was discovered through iterative testing and format manipulation (JSON to XML conversion). The writeup demonstrates importance of understanding application behavior changes rather than relying on standard exploitation techniques. Custom frameworks present higher risk due to non-standard implementation of security controls.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
