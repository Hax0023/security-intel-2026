# Access to Administrative Resources via Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 1326352 | https://hackerone.com/reports/1326352
- **Submitted:** 2021-08-31
- **Reporter:** j4k3d
- **Program:** Not Disclosed
- **Bounty:** Not Disclosed
- **Severity:** Critical
- **Vuln:** Path Traversal, Broken Access Control, Authentication Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A path traversal vulnerability allows unauthenticated or low-privileged users to access administrative resources by directly navigating to admin directory paths. Authenticated users can bypass role-based access controls to access sensitive administrative pages containing system configurations, user credentials, and other sensitive data.

## Attack scenario
1. Attacker logs in with a standard user account or without authentication
2. Attacker directly accesses the /Saba/Web_wdk/ administrative path in the browser URL
3. Due to insufficient path validation, the application does not verify admin privileges before serving the resource
4. Attacker can access sensitive admin pages like systemMain.rdf and usersStatistics.rdf
5. Attacker exfiltrates sensitive data including system IPs, configurations, usernames, passwords, and email addresses
6. Attacker may modify administrative resources or execute remote code if upload/execution capabilities are present

## Root cause
The application fails to properly validate user privileges and enforce access controls on administrative resources. Path-based access control checks are insufficient or missing, allowing direct resource access by simply constructing the correct URL without verifying the user's administrative role.

## Attacker mindset
A path traversal vulnerability is attractive because it bypasses authentication/authorization layers entirely. An attacker sees that admin resources are accessible via predictable URL patterns and realizes the application may not be validating permissions on a per-request basis. The attacker exploits this by directly requesting admin endpoints, treating access control as a client-side concern rather than server-side validation.

## Defensive takeaways
- Implement server-side access control checks on every request before serving any resource, not just login pages
- Use role-based access control (RBAC) that is enforced at the application layer, not the URL layer
- Implement a whitelist of allowed paths for each user role and deny all others by default
- Do not rely on URL patterns or directory structures for security; validate permissions for each resource independently
- Use security frameworks that enforce authorization decorators/annotations on protected endpoints
- Implement comprehensive logging and monitoring to detect users accessing resources outside their role
- Perform security testing including forced browsing and path traversal tests during development
- Use principle of least privilege - grant users only the minimum access necessary

## Variant hunting
Test other administrative paths like /admin/, /system/, /config/, /settings/ with low-privilege accounts
Attempt directory traversal sequences (./../..) to bypass prefix-based access controls
Try URL encoding variations (%2e%2e, %252e) to bypass basic filters
Test different file extensions (.jsp, .rdf, .xml, .json) on admin paths
Check for API endpoints that may have the same access control weaknesses
Test with different HTTP methods (GET, POST, PUT, DELETE) on admin resources
Look for parameter manipulation that might change the user context or requested resource
Examine similar Saba platform installations for identical patterns

## MITRE ATT&CK
- T1190
- T1548
- T1566
- T1087
- T1526
- T1552
- T1538
- T1556

## Notes
This report affects Saba platform, likely an HR/LMS solution. The vulnerability is particularly severe because it allows complete bypass of authentication for admin access. The redacted content suggests a specific implementation detail that triggers the vulnerability. The attack works both for completely unauthenticated users and for privilege escalation by authenticated standard users. Critical that vendors audit ALL administrative endpoints for proper authorization checks.

## Full report
<details><summary>Expand</summary>

**Description:**
A user can login as an administrator without the need of an ██████████ account, or an authenticated user can access and manipulate administrative resources without needing to login as an administrator. An ████████ (███████) account is required.
## References

## Impact

Exfiltration of sensitive data (IPs, system configurations, passwords, usernames, email addresses, names), website defacing, denial of service, potential rce, deletion of data.

## System Host(s)
████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
If you do not have an ██████(██████████) account:

Navigate to https://██████/
Login using your ████████ account. 
When you login you should be at the page https://██████/Saba/██████/CustomLogin.jsp with the error "There was an error while processing your request.  Please try again. If the problem persists, please contact the help desk at ████████".
Navigate to https://█████████/home
Your account name should say "Samba administrator"

If you do have an █████████(███████) account:

Navigate to https://█████/
Login using your ███████ account. 
Navigate to a page in the admin directory i.e. https://███████/Saba/Web_wdk/████████/platform/system/admin/systemMain.rdf  or https://██████████/Saba/Web_wdk/███████/Platform/system/admin/usersStatistics.rdf

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
