# Staff Members Without Domain Access Can Bypass Permissions via Direct URL

## Metadata
- **Source:** HackerOne
- **Report:** 96855 | https://hackerone.com/reports/96855
- **Submitted:** 2015-10-30
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Broken Access Control, Horizontal Privilege Escalation, Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Staff members without explicit domain access permissions can circumvent access controls by directly navigating to the domains settings page URL. While the UI correctly disables the domains menu item based on assigned permissions, the backend lacks proper authorization checks, allowing unauthorized modification of domains.

## Attack scenario
1. Administrator creates a new staff account with limited permissions (settings access only, no domain access)
2. Staff member logs in and verifies the domains tab is disabled in the sidebar menu
3. Staff member manually constructs and navigates to /admin/settings/domains URL
4. Backend fails to validate user permissions for the domains resource
5. Staff member successfully accesses the domains management page
6. Staff member can add, delete, or modify domains without authorization

## Root cause
Client-side permission enforcement via UI menu disabling without corresponding server-side authorization validation. The application relies on hiding menu items rather than implementing proper backend access controls on protected endpoints.

## Attacker mindset
A malicious insider or compromised low-privilege staff account recognizes that UI restrictions are merely cosmetic. By directly accessing the URL path, they test whether backend authorization checks exist, discovering the application trusts client-side permission enforcement.

## Defensive takeaways
- Implement server-side authorization checks on all protected endpoints before processing requests
- Never rely solely on UI/menu disabling for enforcing access control
- Validate user permissions for every domain-related operation (add, delete, modify)
- Use consistent permission checking across all entry points to sensitive resources
- Log and audit access attempts to sensitive resources for detection of unauthorized access
- Apply defense-in-depth: combine UI restrictions with robust backend authorization

## Variant hunting
Check other settings pages (/admin/settings/checkout, /admin/settings/notifications, etc.) for similar authorization bypass via direct URL access
Test other admin sections with granular permissions to identify similar client-side-only enforcement patterns
Attempt to access resources by manipulating URL parameters or IDs when user has partial permissions
Review other Shopify admin endpoints for authorization checks performed only on client side

## MITRE ATT&CK
- T1190
- T1548
- T1087

## Notes
Classic authorization bypass vulnerability exploiting the disconnect between presentation layer (disabled menu) and application logic layer (missing backend checks). This is a fundamental security design flaw common in applications that implement role-based access control incompletely. The vulnerability allows privilege escalation within the same user tier and could enable domain hijacking, DNS spoofing, or SSL certificate manipulation.

## Full report
<details><summary>Expand</summary>

Hi , I have found that if a staff member has a permission to access settings but has no permissions to access domains he can bypass this by just going to: `*store.myshopify.com/admin/settings/domains` .

in the side menu the `domains` tab will be disabled and the user shouldn't be able to access it,but he can access it by just going the domains page url.

#Steps to reproduce:
1. Add a new staff member and limit his access o `settings` only , and don't check the `domains` option , so the member should only have access to settings and shouldn't have access to domains.
2. Logout then login with the staff member and go to: `*yourstore.myshopify.com/admin/settings/domains` and you'll be able to add , delete and modify domains.

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
