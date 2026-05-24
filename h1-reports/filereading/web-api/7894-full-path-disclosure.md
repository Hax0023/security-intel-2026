# Full Path Disclosure via Verification Link Error

## Metadata
- **Source:** HackerOne
- **Report:** 7894 | https://hackerone.com/reports/7894
- **Submitted:** 2014-04-17
- **Reporter:** siddiki
- **Program:** Localize.io
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Full Path Disclosure, Error-based Information Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
The application's verification link handler fails to catch exceptions properly, resulting in verbose PHP error messages that disclose the full server filesystem path. An attacker can trigger this error by visiting a verification link with an invalid or non-existent token, revealing sensitive infrastructure information.

## Attack scenario
1. Attacker signs up for an account and receives a verification email with a token link
2. Attacker modifies the token in the URL to an invalid value
3. Attacker visits the modified verification link
4. The application fails to validate the token and crashes with an uncaught exception
5. PHP displays a fatal error message containing the full server path `/var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php`
6. Attacker gathers intelligence about server structure and hosting provider for further reconnaissance

## Root cause
Missing error handling and exception catching in the verification endpoint. The application calls `setEmail_lastVerificationAttempt()` on an object that is null or undefined when token validation fails, and PHP error reporting is set to display errors instead of logging them securely.

## Attacker mindset
An attacker performing reconnaissance would use path disclosure to understand the application architecture, identify the hosting provider (HostEurope), server OS (Linux), and web root structure. This information aids in planning subsequent attacks such as directory traversal, file inclusion, or targeted exploitation of known vulnerabilities in identified components.

## Defensive takeaways
- Implement comprehensive try-catch blocks around all database queries and object method calls
- Set `display_errors = Off` in production PHP configuration and log errors to files instead
- Return generic user-facing error messages (e.g., 'Invalid or expired verification link') without technical details
- Implement proper input validation for tokens before attempting to process them
- Use custom error handlers to control error output and ensure sensitive paths are never exposed
- Enable security headers and implement a Web Application Firewall (WAF) to detect error-based reconnaissance attempts

## Variant hunting
Check all authentication-related endpoints (password reset, email change, two-factor setup) for similar error disclosures
Test API endpoints with malformed requests to identify unhandled exceptions
Attempt SQL injection in token parameters to trigger database errors with path disclosure
Fuzz all user-facing forms and endpoints with invalid input to discover error handling gaps
Review logs and error pages for other instances of path disclosure across the application

## MITRE ATT&CK
- T1592
- T1592.004

## Notes
Full path disclosure is a low-severity vulnerability but valuable for attackers during the reconnaissance phase. Combined with other information gathering techniques, it significantly reduces the effort required to identify exploitable vulnerabilities. The vulnerability was triggered via a simple invalid token, making it easily discoverable. The specific path revealed hosting provider and server configuration details that could be used in targeted attacks.

## Full report
<details><summary>Expand</summary>

I signed up for localize with haxorsistz@gmail.com, and localize sent me a verification link which was:
`http://www.localize.io/verify/e6be646b24pdd3w6d5c27ppa9a267ee7`
When I visited that link I found it was showing the following error:
`Fatal error: Call to a member function setEmail_lastVerificationAttempt() on a non-object in /var/www/vhosts/lvps178-77-99-228.dedicated.hosteurope.de/httpdocs_localize/index.php on line 120 `
which includes the full path of the website.This should be mitigated.

</details>

---
*Analysed by Claude on 2026-05-24*
