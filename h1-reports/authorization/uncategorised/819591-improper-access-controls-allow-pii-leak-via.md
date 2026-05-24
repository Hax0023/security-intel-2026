# Improper Access Controls Allow PII Leak via Dashboard Widgets

## Metadata
- **Source:** HackerOne
- **Report:** 819591 | https://hackerone.com/reports/819591
- **Submitted:** 2020-03-15
- **Reporter:** z32
- **Program:** Undisclosed
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Access Control, Improper Authorization, Information Disclosure, Insufficient Access Control, Unauthorized Data Access
- **CVEs:** None
- **Category:** uncategorised

## Summary
Dashboard widgets in the application allow any authenticated user to view and access sensitive Personally Identifiable Information (PII) including names, emails, physical addresses, and phone numbers, as well as modify configuration items and diagnostic data. The vulnerability stems from inadequate access controls that fail to restrict widget visibility and modification capabilities to only authorized users.

## Attack scenario
1. Attacker creates a low-privilege user account on the vulnerable application
2. Attacker navigates to the dashboard creation interface after account verification
3. Attacker uses the 'Add Widgets' feature to display PII widgets containing user data (names, emails, addresses, phone numbers)
4. Attacker clicks on data aggregation links (e.g., 'All(22)') to access and view configuration items belonging to other users
5. Attacker modifies accessible configuration fields within these widgets to alter system state
6. Attacker explores alternative dashboard interface via /home path and adds additional content widgets revealing even more sensitive user information

## Root cause
The application implements dashboard widgets without proper authorization checks, allowing any authenticated user to add widgets that expose sensitive data and configuration options regardless of their role or permissions. Access controls fail to validate whether users should have visibility into PII, system diagnostics, or modification capabilities for configuration items.

## Attacker mindset
Opportunistic account creator seeking to exploit easy registration mechanisms to gain unauthorized access to sensitive user data and system configuration. The attacker recognizes that dashboard functionality is insufficiently gated and systematically explores available widgets to maximize intelligence gathering on user information and system state.

## Defensive takeaways
- Implement role-based access control (RBAC) to restrict dashboard widget availability based on user permissions
- Never expose PII or sensitive configuration data through default or user-addable widgets without explicit authorization checks
- Enforce principle of least privilege - default dashboards should contain minimal data, not maximum
- Validate authorization at both widget rendering and data retrieval layers
- Implement data masking or redaction for PII when displayed in shared dashboard contexts
- Audit and restrict modification capabilities on configuration items to only authorized administrators
- Add comprehensive logging and monitoring for access to sensitive data widgets
- Implement rate limiting and monitoring for suspicious dashboard widget enumeration patterns
- Require strong authentication and verification before granting access to sensitive dashboards
- Regularly audit accessible widgets and the scope of data they expose across all user roles

## Variant hunting
Check other dashboard-like features or reporting interfaces for similar authorization bypass
Test API endpoints that power widget data retrieval for missing authorization checks
Examine export/download functionality for dashboards to see if it respects access controls
Look for stored dashboard configurations that could be shared and accessed by unauthorized users
Test for privilege escalation via widget modification that could grant higher permissions
Search for other content addition features similar to 'Add Content' that may have the same flaw
Check for cross-tenant data exposure if the application is multi-tenant
Test anonymous or guest user access to dashboard features
Look for IDOR vulnerabilities in widget parameter manipulation

## MITRE ATT&CK
- T1190
- T1592
- T1087
- T1526
- T1538
- T1566

## Notes
Report contains significant redactions of sensitive company/product information. The vulnerability demonstrates a critical failure in authorization architecture where widgets serve as a direct pathway to expose comprehensive PII and system information. The ease of account creation combined with unrestricted widget access creates a severe risk. The ability to modify configuration items suggests potential for lateral movement or privilege escalation beyond simple data exfiltration.

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
