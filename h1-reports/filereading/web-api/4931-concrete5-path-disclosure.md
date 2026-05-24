# Concrete5 Path Disclosure via Cookie Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 4931 | https://hackerone.com/reports/4931
- **Submitted:** 2014-03-27
- **Reporter:** smiegles
- **Program:** Concrete5
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Path Disclosure, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
Emptying or manipulating the CONCRETE5 session cookie triggers unhandled PHP warnings that disclose the full file system path to the application installation directory. The application fails to validate the session ID format before processing it, causing session_start() to emit verbose error messages that leak sensitive path information.

## Attack scenario
1. Attacker identifies a Concrete5 installation on the target domain
2. Attacker clears, deletes, or sets the CONCRETE5 cookie to an invalid value containing special characters
3. Upon the next page request, the application attempts to start a session with the malformed cookie value
4. PHP's session_start() function rejects the invalid session ID and outputs warning messages
5. Error messages are displayed to the attacker revealing full file paths like /home/c5host/msm_versions/012312/concrete/
6. Attacker uses disclosed paths for further reconnaissance and targeted exploitation

## Root cause
The application does not validate or sanitize the CONCRETE5 cookie value before passing it to session_start(). Additionally, PHP error reporting is configured to display warnings, and proper input validation on session IDs is missing. The code at session.php line 22 calls session_start() without prior validation of the session ID format.

## Attacker mindset
Information gathering and reconnaissance - an attacker would manipulate cookies as a basic reconnaissance technique to map the application's directory structure and identify the exact installation path, version information, and file organization. This facilitates further targeted attacks.

## Defensive takeaways
- Implement strict input validation on all session identifiers before processing
- Validate session ID format (a-z, A-Z, 0-9, hyphen only) before calling session_start()
- Configure PHP to suppress or log errors rather than display them to users
- Set php.ini display_errors=off and log_errors=on in production environments
- Implement a custom session handler that validates session IDs early
- Use error suppression operators or try-catch blocks around session handling code
- Implement global error handling to catch and sanitize error messages before display

## Variant hunting
Test other framework session/cookie handling mechanisms for similar path disclosure
Check for similar issues in startup routines of other PHP frameworks
Fuzz cookie values with special characters across different Concrete5 versions
Review other initialization files that may call session_start() without validation
Test for path disclosure in error logs and exception handlers

## MITRE ATT&CK
- T1526 - Reconnaissance
- T1598 - Phishing
- T1592 - Gather Victim Host Information

## Notes
This is a relatively straightforward information disclosure vulnerability. While the bounty amount is not specified in the report, path disclosure vulnerabilities typically receive low to medium severity ratings. The fix is simple - validate session IDs before use. The vulnerability demonstrates the importance of secure defaults in error handling and the danger of displaying system paths in error messages to end users.

## Full report
<details><summary>Expand</summary>

Hi,

When you emtpy the cookie `CONCRETE5` it will throw the following error on the page :

`Warning: session_start() [function.session-start]: The session id contains illegal characters, valid characters are a-z, A-Z, 0-9 and '-,' in /home/c5host/msm_versions/012312/concrete/startup/session.php on line 22
Warning: session_start() [function.session-start]: Cannot send session cookie - headers already sent by (output started at /home/c5host/msm_versions/012312/concrete/startup/session.php:22) in /home/c5host/msm_versions/012312/concrete/startup/session.php on line 22`
`Warning: session_start() [function.session-start]: Cannot send session cache limiter - headers already sent (output started at /home/c5host/msm_versions/012312/concrete/startup/session.php:22) in /home/c5host/msm_versions/012312/concrete/startup/session.php on line 22
Warning: Cannot modify header information - headers already sent by (output started at /home/c5host/msm_versions/012312/concrete/startup/session.php:22) in /home/c5host/msm_versions/012312/concrete/libraries/view.php on line 841`

Best regards,

Olivier Beg

</details>

---
*Analysed by Claude on 2026-05-24*
