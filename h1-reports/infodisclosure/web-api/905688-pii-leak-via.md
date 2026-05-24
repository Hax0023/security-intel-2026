# PII Disclosure via Unrestricted ServiceNow Email Notification Preview

## Metadata
- **Source:** HackerOne
- **Report:** 905688 | https://hackerone.com/reports/905688
- **Submitted:** 2020-06-22
- **Reporter:** z32
- **Program:** ServiceNow
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Information Disclosure, Missing Authorization Check
- **CVEs:** None
- **Category:** web-api

## Summary
An unauthenticated or inadequately authenticated attacker can access ServiceNow email notification preview functionality to enumerate and view sensitive Personally Identifiable Information (PII) of all users including full names, ranks, organizations, email addresses, physical addresses, and phone numbers. The vulnerability exists due to missing or insufficient access controls on the notification preview module endpoints.

## Attack scenario
1. Attacker discovers or guesses the URL path to the email notification modules endpoint
2. Attacker navigates to the vulnerable endpoint without proper authorization checks blocking access
3. Attacker clicks on notification names to access the notification menu interface
4. Attacker selects 'Preview Notification' option to trigger the user lookup functionality
5. Attacker uses the user search/query field to enumerate and identify target users
6. Attacker clicks information icons to view and exfiltrate complete PII profiles for enumerated users

## Root cause
Missing or improperly implemented authorization controls on the email notification preview and sysevent_email_action modules. The application fails to verify that the authenticated user has permission to access these administrative modules, and does not restrict user enumeration or PII disclosure through the preview functionality.

## Attacker mindset
An attacker seeking to collect employee intelligence and PII for social engineering, targeted phishing, identity theft, or corporate reconnaissance would systematically enumerate all users in the target organization and harvest their contact details and organizational hierarchy information through this easily accessible interface.

## Defensive takeaways
- Implement robust role-based access control (RBAC) on all administrative and notification management modules
- Require explicit authorization checks before allowing access to notification preview functionality
- Implement rate limiting and logging on user enumeration endpoints to detect abuse
- Mask or redact sensitive PII fields in preview/debug interfaces, or restrict them to authorized personnel only
- Apply principle of least privilege to email notification modules - restrict access to only necessary administrators
- Audit all ServiceNow modules that expose user directory information for similar authorization bypasses
- Implement API-level access controls separate from UI controls to prevent bypass

## Variant hunting
Check other ServiceNow modules that preview or display user data (user profiles, directory search, org charts)
Test other email/notification management endpoints (sysevent_email_*, notification.do, etc.) for similar flaws
Review all administrative modules for missing authorization checks on data preview/export functions
Test whether authentication is required at all to access the affected endpoints
Check if other user enumeration vectors exist (search fields, autocomplete, batch operations)
Examine whether the vulnerability allows privilege escalation beyond PII disclosure

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1526: Enumerate Cloud Resources (user directory enumeration)
- T1087: Account Discovery (user enumeration)
- T1589: Gather Victim Identity Information
- T1538: Cloud Service Discovery
- T1566: Phishing (social engineering with harvested PII)

## Notes
The report redacts specific endpoint names and user group details, suggesting sensitivity around organizational structure. The vulnerability is straightforward to exploit requiring only navigation and clicks. ServiceNow instances commonly contain sensitive organizational data, making such PII disclosure high-impact. The fix is straightforward (access control implementation) but may have been missed due to assumptions about who can access notification modules or failure to secure all code paths to sensitive data.

## Full report
<details><summary>Expand</summary>

**Summary:**
An attacker is able to access ServiceNow e-mail notification modules via █████/██████████. Once on this page, the attacker can click any of the notifications, select `Preview Notification`, and choose a user to view their profile data to include Full Name, rank, organization, e-mail address, physical address, and phone number.

## Step-by-step Reproduction Instructions

1. Browse to ██████ and create an account or sign in.
2. Browse to █████████/███████.
3. Click on any of the notification names. Once the notification menu appears, click `Preview Notification` in the top right corner of the screen.
4. The `████` field can now be used to query a user. Once a user is identified, the `(i)` icon can be clicked to view the users PII.
██████

## Suggested Mitigation/Remediation Actions
Restrict access to the █████ and sysevent_email_action.do modules to prevent unauthorized viewing of PII.

## Impact

An adversary can gather PII of all `███████` users via this endpoint.

</details>

---
*Analysed by Claude on 2026-05-24*
