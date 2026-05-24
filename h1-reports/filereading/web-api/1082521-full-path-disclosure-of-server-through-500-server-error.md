# Full Path Disclosure of Server through 500 Server Error

## Metadata
- **Source:** HackerOne
- **Report:** 1082521 | https://hackerone.com/reports/1082521
- **Submitted:** 2021-01-20
- **Reporter:** basant0x01
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Error-based Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
A Laravel application discloses the full server file path through a 500 Server Error when an account verification link is used twice. The error message reveals the absolute path to the application's Laravel Blade template file, exposing internal server structure information.

## Attack scenario
1. Attacker receives or intercepts an account verification email containing a verification link
2. Attacker clicks the verification link once to verify their account successfully
3. Attacker clicks the same verification link a second time
4. Application throws a 500 Server Error due to attempting to re-verify an already verified account
5. Error message in page title or body displays full path: /usr/share/ngnix/website/resources/view/auth/create_password.blade.php
6. Attacker gains information about server file structure, application framework (Laravel), and absolute path location

## Root cause
The application lacks proper error handling and input validation on the account verification endpoint. When attempting to process an already-used verification token, the application throws an unhandled exception that exposes the full file path in the error message instead of displaying a user-friendly error page.

## Attacker mindset
An attacker would view this as reconnaissance information useful for planning more sophisticated attacks. Knowing the exact file structure and path allows for better understanding of the application architecture, identifying potential other vulnerabilities, and crafting targeted payloads.

## Defensive takeaways
- Implement comprehensive error handling to catch exceptions and display generic error messages to end users
- Configure custom error pages for 5xx errors that do not expose sensitive path information
- Log detailed error information server-side only, not in client-facing responses
- Validate verification tokens and implement proper state management to prevent token reuse
- Set appropriate HTTP headers to prevent information leakage
- Implement rate limiting on verification endpoints to detect and block abuse attempts
- Use Laravel's built-in error handling configuration to suppress debug information in production

## Variant hunting
Check for similar path disclosure in password reset endpoints
Test other idempotent operations with repeated requests (email confirmation, token validation)
Look for path disclosure in other error conditions (file uploads, form submissions)
Test API endpoints for similar information disclosure in error responses
Examine all publicly accessible endpoints that process user-submitted tokens
Check for path disclosure in different error states across authentication workflows

## MITRE ATT&CK
- T1592
- T1526
- T1217

## Notes
This is a low-severity vulnerability as it requires specific conditions to trigger and the information disclosed, while useful for reconnaissance, does not directly lead to compromise. However, it represents a common configuration weakness where applications leak sensitive information through improper error handling. The vulnerability is easily fixable through proper error handling configuration in Laravel.

## Full report
<details><summary>Expand</summary>

Hello team,

EXPLANATION
============
I found a interesting vulnerability into your site that it unexpected disclosing the server path where the PHP files are being hosted. When application sends account verification links in email then if anyone tries to verify his account with that link at a twice then on the title of the website the whole server path is disclosing through 500 Server Error.

Vulnerable Path :
---------------
`/usr/share/ngnix/website/resources/view/auth/create_password.blade.php`


I have added a POC .

## Impact

1. Server Information Disclosure

</details>

---
*Analysed by Claude on 2026-05-24*
