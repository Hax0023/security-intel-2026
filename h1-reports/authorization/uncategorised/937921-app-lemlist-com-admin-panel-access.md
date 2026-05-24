# Unprotected Admin Panel Access at app.lemlist.com

## Metadata
- **Source:** HackerOne
- **Report:** 937921 | https://hackerone.com/reports/937921
- **Submitted:** 2020-07-23
- **Reporter:** omarelfarsaoui
- **Program:** Lemlist
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Access Control, Insufficient Authorization Verification, Horizontal Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated or insufficiently authenticated user could directly access sensitive admin panel endpoints at app.lemlist.com/admin and related paths without proper authorization checks. This allows unauthorized users to view and potentially manipulate administrative functionality intended only for privileged accounts.

## Attack scenario
1. Attacker creates a normal user account or logs in with basic credentials
2. Attacker discovers admin endpoints through JavaScript file analysis or URL enumeration
3. Attacker navigates to /admin or /admin/mailboxes endpoints
4. Application fails to validate if user has admin privileges before rendering admin panel
5. Attacker gains access to admin dashboard and can perform unauthorized administrative actions
6. Attacker could modify settings, access sensitive data, or create rogue admin accounts

## Root cause
Client-side or insufficient server-side authorization checks. The application likely relies on client-side role validation or fails to verify admin privileges on backend endpoints, allowing direct URL access to bypass authorization controls.

## Attacker mindset
Opportunistic security researcher or malicious actor discovering overly permissive access controls through passive reconnaissance. The attacker systematically analyzed exposed JavaScript files to identify hidden endpoints, demonstrating methodical reconnaissance before exploitation.

## Defensive takeaways
- Implement server-side authorization checks on ALL protected endpoints, never rely solely on client-side validation
- Enforce role-based access control (RBAC) with explicit permission verification before serving admin content
- Use middleware to protect admin routes, requiring verified admin role tokens/sessions
- Implement proper authentication state validation and session management checks
- Avoid exposing sensitive endpoint paths in client-side code; if necessary, obfuscate or use dynamic path generation
- Conduct regular access control audits and penetration testing focused on privilege escalation
- Log and monitor unauthorized access attempts to admin endpoints
- Use HTTP security headers like X-Frame-Options to prevent clickjacking of admin panels

## Variant hunting
Check for similar unprotected admin paths: /admin/, /administrator/, /manage/, /dashboard/, /superadmin/
Test other sensitive endpoints: /api/admin/*, /admin-api/*, /settings/admin/
Attempt to access admin endpoints with expired or invalid session tokens
Test horizontal privilege escalation by accessing other users' admin contexts
Check if admin functionality is accessible through different subdomains or URL paths
Analyze JavaScript files for references to other protected routes missing authorization

## MITRE ATT&CK
- T1190
- T1566
- T1526
- T1087

## Notes
This is a classic broken access control vulnerability (OWASP Top 10 A01:2021). The discovery method (JavaScript analysis) is common and highlights the importance of secure coding practices. The multiple vulnerable endpoints (/admin, /admin/i18n, /admin/mailboxes) suggest a systemic authorization issue rather than isolated oversights. No evidence of authentication bypass; rather, authorization validation is missing entirely.

## Full report
<details><summary>Expand</summary>

hi team,

### Steps To Reproduce:
While doing some  analyse for javascript files in  [app.lemlist.com](https://app.lemlist.com) i found interesting endpoints . is the **admin** panal and is not protected , any normal user can access the panel .

## Steps To Reproduce:
(Add details for how we can reproduce the issue)

  1. Log into your account.
  1. visit on of the link below.

https://app.lemlist.com/admin
https://app.lemlist.com/admin/i18n
https://app.lemlist.com/admin/mailboxes/123

## Impact

Incorrect access restriction to the authorized interface.

Best Regards,
@omarelfarsaoui

</details>

---
*Analysed by Claude on 2026-05-24*
