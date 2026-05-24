# Full Path Disclosure in Phabricator Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 143575 | https://hackerone.com/reports/143575
- **Submitted:** 2016-06-07
- **Reporter:** fnqgpc
- **Program:** Phabricator
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal Information Leak
- **CVEs:** None
- **Category:** web-api

## Summary
The /login/mustverify/ endpoint in Phabricator discloses the full server installation path when accessed by unauthenticated users. This information exposure could aid attackers in reconnaissance and planning targeted attacks against the Phabricator instance.

## Attack scenario
1. Attacker discovers a Phabricator instance and notes it requires authentication
2. Attacker navigates to /login/mustverify/ while logged out
3. Server responds with an error message containing the full filesystem path to the Phabricator installation directory
4. Attacker uses this path information to understand server structure and identify potential targets
5. Attacker cross-references the path with known vulnerabilities specific to that Phabricator version
6. Attacker leverages this information for targeted exploitation or social engineering

## Root cause
Error handling in the mustverify authentication page does not sanitize or redact filesystem paths in error messages returned to unauthenticated users. The application directly exposes exception stack traces or file paths in responses without filtering sensitive information.

## Attacker mindset
Reconnaissance-focused attacker gathering environmental intelligence. Path disclosure is valuable for understanding server topology, confirming software version/location, and identifying potential attack vectors. Low-hanging fruit for initial foothold planning.

## Defensive takeaways
- Implement centralized error handling that sanitizes all error messages before returning to clients
- Never expose filesystem paths, stack traces, or technical details in responses to unauthenticated users
- Use generic error messages for authentication failures (e.g., 'Invalid credentials' instead of path-specific errors)
- Apply the same security controls to all endpoints regardless of authentication status
- Regularly audit error messages and logs for unintended information disclosure
- Implement security headers and error page templating to prevent path leakage

## Variant hunting
Check other /login/* endpoints for similar path disclosure patterns
Test error conditions on authentication pages (invalid inputs, missing parameters)
Review exception handling in password reset, account verification, and two-factor authentication flows
Examine server logs and error pages for filesystem path patterns
Test with malformed requests to trigger error states

## MITRE ATT&CK
- T1598 - Phishing: Reconnaissance
- T1592 - Gather Victim Identity Information
- T1087 - Account Discovery
- T1046 - Network Service Discovery

## Notes
This is a classic information disclosure vulnerability commonly found in web applications with improper error handling. While severity is low, it's part of the reconnaissance chain and should be fixed as part of security hardening. The reporter provided a patch, indicating the fix is straightforward. Path disclosure is common in development/staging environments but should never occur in production.

## Full report
<details><summary>Expand</summary>

Mongoose. The full path of the phabricator install is shown if you go to /login/mustverify/ while being logged out. This could be seen as a server configuration issue, but I think I followed your installation guide closely.

Since I already wrote it I include a little patch, please feel free to ignore it if it's not what you need.

</details>

---
*Analysed by Claude on 2026-05-24*
