# Authentication Bypass Using Empty Parameters

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Undisclosed Penetration Testing Client
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Improper Input Validation, Logic Flaw
- **Category:** uncategorised
- **Writeup:** https://eslam3kl.gitbook.io/blog/bug-hunting-findings/authentication-bypass-using-empty-parameters.

## Summary
A custom web application framework contained flawed conditional logic in the login function that failed to terminate execution when authentication checks returned false, allowing attackers to bypass authentication by sending empty or malformed JSON parameters. By manipulating the request structure, an unauthenticated user could gain access as the default/admin account.

## Attack scenario (step by step)
1. Attacker sends initial login attempt with valid credentials to observe JSON request/response structure
2. Attacker intercepts login POST request and modifies JSON payload to remove or empty credential parameters
3. Application's IF statement conditions evaluate to false due to missing/empty parameters
4. Execution flow fails to terminate and continues to default user initialization code
5. Application returns authentication token or session for default/admin user without proper credential validation
6. Attacker uses obtained session to access application with elevated privileges

## Root cause
The custom framework's login function used improper conditional logic where failed authentication checks (IF statements returning false) did not halt execution. Instead, the process continued to a default case that authenticated the user, likely due to missing return statements or break statements after failed authentication conditions.

## Attacker mindset
Methodical testing approach starting with credential validation, then attempting XXE injection, then observing request structure changes, and finally identifying that empty/missing parameters could bypass logic gates rather than being properly rejected.

## Defensive takeaways
- Always use explicit return/exit statements after failed authentication checks to prevent execution flow continuation
- Implement whitelist validation for all required authentication parameters with mandatory field checks
- Default to DENY rather than ALLOW when authentication conditions fail
- Ensure all code paths in authentication logic terminate correctly and don't fall through to default cases
- Use security-focused code review and static analysis tools to identify authentication logic flaws
- Implement comprehensive logging and monitoring of authentication attempts, especially those with missing parameters

## Variant hunting
Search for similar custom framework implementations where: (1) conditional authentication checks lack proper termination, (2) default user accounts are initialized in fallback code paths, (3) empty/null parameters are processed but not rejected, (4) multiple authentication pathways exist without proper state management, (5) JSON/XML parameter handling has inconsistent validation logic

## MITRE ATT&CK
- T1190
- T1556
- T1111

## Notes
The vulnerability demonstrates the danger of custom authentication frameworks without proper security review. The attacker's iterative approach (XXE → format conversion → parameter manipulation) shows effective reconnaissance. The root cause was insufficient input validation combined with improper control flow in the authentication function. This finding emphasizes the importance of security audits for bespoke authentication implementations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
