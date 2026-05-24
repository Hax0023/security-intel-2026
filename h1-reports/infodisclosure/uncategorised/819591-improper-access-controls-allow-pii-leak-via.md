# Improper Access Controls Allow PII Leak via Dashboard Widgets

## Metadata
- **Source:** HackerOne
- **Report:** 819591 | https://hackerone.com/reports/819591
- **Submitted:** 2020-03-15
- **Reporter:** z32
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Information Disclosure, Unauthorized Data Modification
- **CVEs:** None
- **Category:** uncategorised

## Summary
Dashboard widgets in the target application lack proper access controls, allowing any authenticated user to view and modify sensitive data including PII, configuration items, and system diagnostics. An adversary can easily create an account and gain access to full names, email addresses, physical addresses, phone numbers, and other sensitive information belonging to other users.

## Attack scenario
1. Attacker creates a new account on the platform through an easily-accessible account creation process
2. After email verification, attacker navigates to the dashboard creation page
3. Attacker uses 'Add Widgets' feature to discover available data sources without authorization restrictions
4. Attacker identifies widgets containing PII and configuration information accessible to all users
5. Attacker clicks on data aggregation points (e.g., 'All(22)') to view and enumerate sensitive configuration items and user records
6. Attacker modifies fields within configuration items and views PII including names, emails, addresses, and phone numbers of other users

## Root cause
The application implements widget functionality on dashboards without proper authorization checks. Access controls fail to restrict which widgets can be added and what data they can display based on user role or permissions. The backend does not validate user privileges before serving sensitive data through these widgets.

## Attacker mindset
An attacker recognizes that the account creation process is trivial and that default dashboard functionality provides unauthorized access to valuable data. The attacker explores the 'Add Widgets' feature as a discovery mechanism, realizing it serves as a window into sensitive backend data sources without authorization enforcement.

## Defensive takeaways
- Implement role-based access control (RBAC) for all dashboard widgets and ensure only authorized users can add specific widgets
- Validate user permissions on the backend before returning any data through widget APIs
- Restrict PII and diagnostic data visibility based on user role; most users should not see other users' personal information
- Implement data filtering at the API level to exclude sensitive fields for unauthorized users
- Enforce authorization checks for both read (viewing data) and write (modifying configuration) operations
- Audit default permissions granted to newly created accounts and remove unnecessary data access
- Implement principle of least privilege for account creation flows
- Add access logging for sensitive data queries through widget functionality

## Variant hunting
Check other dashboard-like interfaces for similar widget-based data disclosure
Test API endpoints that serve widget data directly for missing authorization checks
Enumerate all widget types and their underlying data sources for unauthorized access patterns
Test if users can modify configuration items they created or only view them
Check if there are export/download features on widgets that also lack access controls
Test cross-tenant or cross-organization data leakage through widgets if multi-tenant
Analyze whether admin-only widgets can be added by regular users through parameter manipulation

## MITRE ATT&CK
- T1190
- T1199
- T1526
- T1087
- T1083
- T1087.001
- T1580

## Notes
This report demonstrates a critical flaw in the principle of least privilege. The ease of account creation combined with overly permissive dashboard functionality creates a severe information disclosure vulnerability. The ability to also modify configuration items compounds the severity. The redacted nature of the original report suggests this was filed against a commercial SaaS product with a responsible disclosure process.

## Full report
<details><summary>Expand</summary>

**Summary:**
Dashboards in `██████████` allow a user to add widgets and obtain large amounts of information to include PII and diagnostic information. Additionally, a user is able to make changes to certain catalogs via these widgets.

**Description:**

## Impact
An adversary can gain access to PII to include full names, e-mail addresses, physical addresses, phone numbers, etc., as well as modifying fields within the underlying system. Additionally, the adversary could identify information such as the number/type of incidents, as well as diagnostic information such as memory usage.

## Step-by-step Reproduction Instructions

1. Create an account on `███████/` and browse to `███████` once your account has been verified. 
██████
2. If this is your first time accessing this page, you will need to create a dashboard.
██████
3. Using the `Add Widgets` feature, an adversary can gain access to various information as shown in the picture below. This is just a small glimpse of what an adversary has access to through this panel.
████
4. Clicking on the `All(22)` text in the third widget above, an adversary can access various configuration items.
██████████
5. These can then be modified by the adversary as shown below:
████
6. If an adversary browses to `███/home`, they get a slightly different interface:
████
7. By clicking `Add Content` in the top left corner, the adversary can add widgets similar to before. This dashboard seems to contain a little more functionality..
████████
8. By adding `███████`, the adversary can access PII of many of the users of the website.
█████
█████
9. The `███` account shown below does not contain much sensitive information, but the fields for the other accounts are highly populated. The ████████ account was used instead in effort to prevent showing real user information.
████████

## Suggested Mitigation/Remediation Actions
Restrict access to these widgets to only those users that need this functionality. Regular users should not have access to this data, especially when the account creation process is so easy.

## Impact

An adversary can gain access to PII to include full names, e-mail addresses, physical addresses, phone numbers, etc., as well as modifying fields within the underlying system. Additionally, the adversary could identify information such as the number/type of incidents, as well as diagnostic information such as memory usage.

</details>

---
*Analysed by Claude on 2026-05-24*
