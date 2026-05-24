# Unauthorized PII Access including CAC User IDs for U.S. Military Personnel via Unauthenticated Account Creation

## Metadata
- **Source:** HackerOne
- **Report:** 900137 | https://hackerone.com/reports/900137
- **Submitted:** 2020-06-17
- **Reporter:** 5050thepiguy
- **Program:** Undisclosed (U.S. Military/Defense-related organization)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Access Control, Insufficient Authorization, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A web application at the login portal allowed any user to self-register an account and immediately access sensitive PII including CAC User IDs, emails, phone numbers, and full names for a vast majority of U.S. military personnel without proper authorization controls. The sensitive data was marked 'For Official Use Only - Privacy Sensitive' and could be easily exported to PDF, CSV, or XLS formats, enabling rapid data exfiltration.

## Attack scenario
1. Attacker navigates to the login portal and selects 'Request New Account'
2. Attacker completes account registration with arbitrary credentials from the open internet
3. Attacker logs into the newly created account
4. Attacker navigates to Administration -> User -> Users menu
5. Attacker observes complete user directory containing PII for military personnel including CAC User IDs
6. Attacker exports the entire dataset to CSV/PDF/XLS and exfiltrates the information

## Root cause
Absence of role-based access control (RBAC) enforcement on the user directory viewing functionality. The application failed to restrict the 'Users' administration panel to authorized administrators only, instead granting access to any authenticated user regardless of their role or authorization level.

## Attacker mindset
An adversary could leverage this vulnerability for identity theft, targeted social engineering attacks against military personnel, espionage, or sale of PII on dark web markets. The ease of data export and lack of audit controls enable rapid, large-scale exploitation without detection.

## Defensive takeaways
- Implement strict role-based access control (RBAC) for all sensitive data views, particularly administration panels
- Require explicit authorization levels (e.g., 'Administrator' role) before granting access to user directories containing PII
- Disable or restrict export functionality for sensitive datasets to authorized roles only
- Implement principle of least privilege for all user accounts, default to restrictive permissions
- Add comprehensive audit logging for access to PII and data exports with alerting on bulk exports
- Conduct regular access control testing and privilege escalation assessments
- Implement data masking for sensitive fields (CAC IDs, SSN portions) in non-admin views
- Require multi-factor authentication for accounts accessing 'Official Use Only' data

## Variant hunting
Check for similar broken access control in other administration panels (Reports, Analytics, Settings)
Test whether self-registered users can access other sensitive areas marked 'For Official Use Only'
Verify if account creation itself requires proper vetting or authorization
Check if API endpoints for user data lack authorization checks
Test for horizontal privilege escalation by accessing other users' personal/profile data
Verify if deleted or disabled accounts can still be viewed
Check for verbose error messages that leak additional PII
Test if guest or unauthenticated users can access any sensitive endpoints

## MITRE ATT&CK
- T1087
- T1589
- T1190
- T1199
- T1526
- T1530

## Notes
This report indicates a prior similar vulnerability (#808338) was previously reported, suggesting inadequate remediation or multiple independent instances. The involvement of U.S. military personnel data elevates this to a national security concern. The 'For Official Use Only' classification indicates the organization understood the sensitivity but failed to implement corresponding controls. The reporter's identification of CAC User ID exposure suggests potential follow-on attacks targeting military authentication systems.

## Full report
<details><summary>Expand</summary>

**Summary:**
An attacker can create an account on https://█████/pages/login.aspx and gain access to a wealth of PII for practically every member that is registered on the website. This information that the attacker has access to includes usernames, CAC User ID's, e-mail addresses, telephone numbers, first/middle/last name, and other information about a vast majority of U.S. military personnel. The portal also clearly indicates "For Official Use Only - Privacy Sensitive". Additionally, an attacker conveniently has access to export this data as a pdf, csv, or xls file, which makes data exfiltration easy. Note that this vulnerability appears to be very similar to report #808338. Please see the attached PoC videos (note that there are 2 videos because after I made the first video I realized I could scroll across and see the user's CAC User ID information, which seems very important in terms of logging into U.S. military systems). I believe this is a critical vulnerability based on the CVSS scale.

## Impact
An adversary can sign up for an account on https://█████████/pages/login.aspx to gather a vast amount of PII related to a large portion of U.S. military personnel. This can be used for many purposes and should not be accessible by a regular user.

## Step-by-step Reproduction Instructions

1. Go to https://██████████/pages/login.aspx
2. Select 'Request New Account' and log into your account
3. Once logged in go to Administration -> User -> Users
4. Observe all the information about different users on the platform

## Product, Version, and Configuration (If applicable)
https://██████/pages/login.aspx

## Suggested Mitigation/Remediation Actions
Limit this function to administrators only, as regular users should not be able to access this type of data (especially when any user can sign up from the open internet.

##References
Please see the attached PoC videos.

## Impact

An attacker can sign up for an account on https://█████████/pages/login.aspx to gather a vast amount of PII related to a large portion of U.S. military personnel. This information can then be used for various malicious purposes and should not be accessible by a regular user.

</details>

---
*Analysed by Claude on 2026-05-24*
