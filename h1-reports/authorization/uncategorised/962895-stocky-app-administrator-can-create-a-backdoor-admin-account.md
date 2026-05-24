# Stocky App Administrator Can Create Backdoor Admin Account via POS User Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 962895 | https://hackerone.com/reports/962895
- **Submitted:** 2020-08-20
- **Reporter:** imgnotfound
- **Program:** Shopify Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Broken Access Control, Insecure Direct Object Reference (IDOR), Missing UI Control Validation, Insufficient Authorization Checks
- **CVEs:** None
- **Category:** uncategorised

## Summary
An administrator in the Stocky app can escalate a POS user account to administrator privileges by accessing a hidden edit endpoint and injecting an admin parameter into the request payload. The vulnerability exploits the discrepancy between UI restrictions (no visible POS user editing) and backend authorization controls, allowing privilege escalation without proper validation.

## Attack scenario
1. Attacker gains Administrator role in Stocky App by being granted legitimate staff member access
2. Attacker identifies a POS User account by inspecting the delete button element to extract the user ID
3. Attacker directly navigates to the hidden /users/{user_id}/edit endpoint which lacks proper authorization checks
4. Attacker modifies the POS user's email address to one under their control and captures the request
5. Attacker injects user[admin]=1 parameter into the request payload before submission
6. Attacker now possesses a backdoor administrator account that persists even if their original administrator role is revoked

## Root cause
The application implements UI-level access control (hiding edit functionality from the user management interface) but fails to enforce corresponding backend authorization checks. The /users/{user_id}/edit endpoint does not verify that only legitimate administrator creation flows can set the admin flag, allowing arbitrary parameter injection. Additionally, the admin privilege parameter is accepted in the request without proper validation.

## Attacker mindset
A disgruntled or malicious staff member with temporary administrator privileges seeks to establish persistent unauthorized access. By exploiting the gap between UI restrictions and backend validation, the attacker creates a hidden backdoor account that allows them to maintain administrative access even after their legitimate privileges are revoked. This represents a calculated persistence mechanism.

## Defensive takeaways
- Implement server-side authorization checks for all privilege-modifying operations, not relying on UI hiding
- Validate and whitelist all modifiable user attributes; reject unexpected parameters like user[admin] from unauthorized sources
- Enforce principle of least privilege: only specific admin creation endpoints should accept admin flag parameters
- Audit access to hidden or undocumented endpoints; implement comprehensive logging for privilege changes
- Use consistent authorization middleware across all routes rather than endpoint-specific checks
- Display user roles prominently in the UI for all user types to enable detection of unauthorized privilege changes
- Implement role-based access control (RBAC) that prevents privilege escalation through parameter injection
- Require multi-step approval workflows for administrator account creation or privilege escalation
- Monitor for suspicious POS user account modifications, particularly email address changes paired with privilege escalation

## Variant hunting
Test other user management endpoints for similar parameter injection vulnerabilities (user[superadmin], user[moderator])
Check if other hidden CRUD endpoints exist for different entity types (stores, permissions, configurations)
Investigate whether the same vulnerability exists in account settings where users might modify their own privileges
Search for other parameters that might control access levels: user[role], user[permissions], user[access_level]
Test if the vulnerability applies to different user types (Staff vs POS vs API users)
Examine bulk user import/export functionality for batch privilege escalation
Check if role changes can be made through API endpoints not exposed in the UI

## MITRE ATT&CK
- T1548.002 - Abuse Elevation Control Mechanism: Bypass User Account Control
- T1556.001 - Modify Authentication Process: Domain Controller Modification (equivalent: privilege escalation through parameter manipulation)
- T1078.001 - Valid Accounts: Default Accounts (leveraging existing POS user)
- T1098.002 - Account Manipulation: Exchange Email Delegate Permissions (modifying account properties)
- T1550.001 - Use Alternate Authentication Material: Application Access Token (using backdoor admin account)
- T1199 - Trusted Relationship (exploiting staff member access)
- T1087 - Account Discovery (enumerating POS users via inspect element)

## Notes
The vulnerability requires an attacker to already have some level of administrative access, which somewhat limits the impact scope. However, the persistence aspect is significant: the attacker can maintain access even after losing their original administrator role, making this a valuable persistence mechanism. The use of inspection tools to discover user IDs indicates the report also identifies information disclosure concerns. The fact that the Shopify app ecosystem has these security implications suggests this may be a platform-wide issue if similar patterns exist in other apps.

## Full report
<details><summary>Expand</summary>

## Details
The Stocky App has POS Users that are being created once a POS Staff logs in into the application from the Point Of Sale application on a mobile device.

From the users management page located at https://stocky.shopifyapps.com/users there's no visible way to edit those POS users. Although, it is possible to edit them by inspecting their user id from the `delete` button and then opening `https://stocky.shopifyapps.com/users/{user_id}/edit` endpoint. Furthermore, you can even make that user an admin by adding `user[admin]` to the request being sent once you save their profile. As the UI doesn't show an admin column for POS users, it becomes a bit transparent to any other admins that a POS User does have an actual account and what roles he's assigned to.

The thing is that to access the Stocky APP, it requires an actual staff member with the App permission so this is reducing the impact here. Still, that flaw could be abused by a Staff Member whom was granted once the **Administrator** role within the app and took the opportunity to create a backdoor admin user from an already existing POS user and/or creating one for himself if he also had access to the Point Of Sale app. He could then be using that backdoor account at some point later if he does lose  its `Administrator` role from the app (assuming he still has the App permission).

## Steps to reproduce
1. From the Point Of Sale mobile application, open the Stocky Application with a POS User. (This is to create a POS User into the Stocky App - not sure if there's any other way)
2. As a Staff Member with Stocky App `Administrator` permission, open https://stocky.shopifyapps.com/preferences/users and inspect the user ID of that POS User by mouse hovering its delete button.
3. Open `https://stocky.shopifyapps.com/users/{user_id}/edit` by taking care of replacing the `{user_id}` placeholder with the one from previous step
4. Set an email address field to an email that you own, so you can actually use it to set the account password. To make it real the attacker user could be creating one with the actual POS User Firstname/LastName so it looks more real.
5. Intercept the request once you save the profile and add `user[admin]=1` to the payload

The POS user now has an actual account he can use to login as an admin (Still requires Stocky App permission).

## Demo (Step 1 excluded)
{F956014}

## Impact

Create a backdoor admin user from a POS user account

</details>

---
*Analysed by Claude on 2026-05-24*
