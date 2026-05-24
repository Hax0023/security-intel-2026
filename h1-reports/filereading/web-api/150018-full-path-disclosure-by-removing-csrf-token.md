# Full Path Disclosure via Missing CSRF Token

## Metadata
- **Source:** HackerOne
- **Report:** 150018 | https://hackerone.com/reports/150018
- **Submitted:** 2016-07-08
- **Reporter:** velby
- **Program:** HackerOne (Report #150018)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Full Path Disclosure, Improper Error Handling, CSRF Token Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
Removing the CSRF token from POST requests causes the application to throw unhandled exceptions that leak the full file system path and sensitive error details. The CSRF validation mechanism fails to gracefully handle missing tokens, exposing the application's directory structure and internal error information.

## Attack scenario
1. Attacker intercepts a legitimate POST request (e.g., login, user data modification)
2. Attacker removes the _CSRF_TOKEN parameter entirely from the request
3. Application processes the POST request without proper CSRF token validation
4. Missing token variable causes undefined variable error in PHP code
5. Exception handler fails to catch the error properly, returning raw PHP error output
6. Full file path (/var/www/csprng/src/public/index.php) and line numbers are disclosed to attacker

## Root cause
The application's CSRF token validation is either missing or fails to properly validate token presence before processing requests. When the token is missing, the code attempts to access an undefined variable without proper error handling or try-catch blocks, causing PHP notices and fatal errors that expose internal debugging information.

## Attacker mindset
An attacker would recognize this as an opportunity to enumerate the application's directory structure and identify the technology stack. This information could be used for further reconnaissance, vulnerability research, or social engineering. The disclosure of file paths helps attackers understand the application architecture and potential attack surface.

## Defensive takeaways
- Implement proper CSRF token validation that checks for token presence before processing POST requests
- Use try-catch blocks or conditional checks to handle missing/invalid CSRF tokens gracefully
- Disable PHP error display in production environments (display_errors = Off in php.ini)
- Log errors to files instead of displaying them to users
- Implement a custom error handler that returns generic error messages without path disclosure
- Set appropriate HTTP status codes (400/403) when CSRF tokens are missing or invalid
- Use a Web Application Firewall (WAF) to detect and block requests with missing expected parameters

## Variant hunting
Test other security-critical parameters for removal (authentication tokens, session identifiers)
Check if other form-based actions (password reset, file upload, admin functions) have similar issues
Attempt to manipulate or modify CSRF token values instead of removing them
Test API endpoints for similar error handling weaknesses
Look for similar path disclosure vulnerabilities in error pages, 404 pages, and exception handlers
Test for bypass techniques like null values, empty strings, or special characters in CSRF field

## MITRE ATT&CK
- T1592.004 - Gather Victim Host Information: Software
- T1592.003 - Gather Victim Host Information: Client Configurations
- T1598 - Phishing for Information
- T1526 - Enumerate Cloud Resources

## Notes
This vulnerability represents a chaining of two weaknesses: weak CSRF validation and improper error handling. While full path disclosure alone is typically low severity, it becomes more valuable when combined with other reconnaissance techniques. The vulnerability suggests the application may lack proper input validation and exception handling frameworks throughout the codebase.

## Full report
<details><summary>Expand</summary>

Hello, you can get an error and full path disclosure by following these steps:
on any user generated POST request (such as during login, or changing user data) remove the CSRF token from the post request entirely. For example, on the login POST request,

_CSRF_TOKEN=WqXB7vmysdM06gBarWZiNfnZ%3AOMznb0rVagzWr41P_h_N2Qj50LwPV2HZxKyJxR17lB6b&username=zrgzrgzerg&passphrase=sergsergsergrg&two_factor=

Becomes

username=zrgzrgzerg&passphrase=sergsergsergrg&two_factor=

We get the following error with a full path disclosure:

<br />
<b>Notice</b>:  Undefined variable: ex in <b>/var/www/csprng/src/public/index.php</b> on line <b>160</b><br />
<br />
<b>Fatal error</b>:  Uncaught Error: Call to a member function getMessage() on null in /var/www/csprng/src/public/index.php:160
Stack trace:
0 {main}
  thrown in <b>/var/www/csprng/src/public/index.php</b> on line <b>160</b><br />


</details>

---
*Analysed by Claude on 2026-05-24*
