# Missing Function Level Access Control in /cindex.php/widget/customize/

## Metadata
- **Source:** HackerOne
- **Report:** 30575 | https://hackerone.com/reports/30575
- **Submitted:** 2014-10-08
- **Reporter:** adrianomarcmont
- **Program:** BookFresh
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Missing Authentication, Broken Access Control, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /cindex.php/widget/customize/ endpoint lacks server-side authentication checks, allowing unauthenticated users to access administrative widget customization functionality. While the application may hide this functionality from the UI for non-authenticated users, the backend does not enforce authorization controls on the endpoint itself.

## Attack scenario
1. Attacker discovers the /cindex.php/widget/customize/ URL through directory enumeration, source code inspection, or JavaScript analysis
2. Attacker makes an HTTP request to the endpoint without providing valid authentication credentials
3. Server processes the request and returns the customize page/functionality without verifying the user's authentication status
4. Attacker gains access to widget customization features intended only for authenticated administrators
5. Attacker can modify application widgets, potentially injecting malicious content or altering user interface
6. Changes persist across the application affecting all users or specific user sessions

## Root cause
The application implements client-side or UI-level access control by hiding the customize functionality from unauthenticated users, but fails to implement server-side authentication/authorization checks on the endpoint. The backend does not verify user authentication status before processing requests to /cindex.php/widget/customize/.

## Attacker mindset
Recognizing that hiding functionality in the UI is insufficient protection, the attacker systematically probes for administrative or privileged endpoints that lack server-side access controls. This represents a common attack pattern of testing direct object references and administrative functions for missing authentication.

## Defensive takeaways
- Always implement server-side authentication and authorization checks before processing any privileged request, regardless of UI visibility
- Verify user identity and permissions on every endpoint, not just those accessible through normal application navigation
- Use a centralized authorization framework that applies consistently across all endpoints
- Implement role-based access control (RBAC) at the framework level to enforce permissions server-side
- Conduct thorough access control testing including unauthenticated and cross-role requests to all endpoints
- Disable direct access to administrative endpoints or implement strict authentication gates
- Apply the principle of deny-by-default: explicitly authorize access rather than assuming protection

## Variant hunting
Test other /cindex.php endpoints for missing authentication (e.g., /cindex.php/admin/*, /cindex.php/settings/*)
Check if other customization endpoints (/cindex.php/*/customize/) have the same vulnerability
Attempt to access widget customization with varying authentication methods (session tokens, API keys, etc.)
Test if the endpoint accepts parameters that reference other users' widgets (IDOR vulnerability)
Verify if customization changes affect global application state or individual user sessions
Check for similar patterns in other controller/action combinations using fuzzing

## MITRE ATT&CK
- T1190
- T1566
- T1548

## Notes
This is a classic broken access control vulnerability (OWASP A01:2021). The vulnerability demonstrates the critical importance of server-side validation. Even though the application likely has UI-level controls, the absence of backend validation creates an exploitable security gap. The /cindex.php pattern suggests a PHP-based application framework (possibly CodeIgniter-like structure). The 'widget/customize' endpoint likely manages application UI components, making unauthorized access particularly dangerous for defacement or social engineering attacks.

## Full report
<details><summary>Expand</summary>

Most web applications verify function level access rights before making that functionality visible in the UI. However, applications need to perform the same access control checks on the server when each function is accessed. If requests are not verified, attackers will be able to forge requests in order to access functionality without proper authorization.

The URL "https://www.bookfresh.com/cindex.php/widget/customize/" is accessible to anyone even without authentication. The page should only be accessible to authenticated users.

</details>

---
*Analysed by Claude on 2026-05-24*
