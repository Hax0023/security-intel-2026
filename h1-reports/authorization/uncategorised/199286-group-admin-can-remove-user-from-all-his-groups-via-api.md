# Group Admin Can Remove User From All Groups Via API

## Metadata
- **Source:** HackerOne
- **Report:** 199286 | https://hackerone.com/reports/199286
- **Submitted:** 2017-01-18
- **Reporter:** nickvergessen
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Broken Access Control, Horizontal Privilege Escalation, API Security Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
A group admin could remove users from groups they don't administer by replaying API requests with modified group parameters, bypassing UI-level restrictions. This allowed group admins to exceed their authorization scope and remove users from groups outside their administrative purview.

## Attack scenario
1. Admin grants user1 group admin privileges for only group1 and group2
2. Attacker (user1) creates a new user2 and adds them to group3 (which user1 doesn't manage)
3. Attacker captures the togglegroup.php API request that removes user2 from group2
4. Attacker modifies the request to target group3 instead of group2 using curl
5. API processes the request without validating the admin's authorization scope
6. User2 is removed from group3, exceeding the attacker's intended administrative boundaries

## Root cause
Access control validation was implemented only in the UI layer, not enforced at the API endpoint level. The togglegroup.php and provisioning_api endpoints failed to verify that the requesting group admin had authorization over the target group before processing removal requests.

## Attacker mindset
A malicious group admin seeking to expand their influence by managing users outside their designated groups, or intentionally disrupting the organization by removing users from groups they shouldn't control.

## Defensive takeaways
- Always enforce authorization checks at the API endpoint level, never rely solely on UI restrictions
- Implement server-side validation of admin scope before processing group membership changes
- Verify that the requesting user has explicit permissions over the target group before executing togglegroup operations
- Apply consistent authorization logic across all interfaces (UI, API, provisioning endpoints)
- Use role-based access control (RBAC) matrix to track which admins can modify which groups
- Log all group membership changes with details of the requesting admin for audit purposes

## Variant hunting
Check for similar broken access control in: user creation endpoints (can non-scoped admins create users?), group creation endpoints (can admins create groups outside their scope?), group settings modification (can admins modify groups they don't manage?), bulk user operations (are batch removals validated per-group?), delegation APIs, and any other endpoints accepting group identifiers as parameters.

## MITRE ATT&CK
- T1078 - Valid Accounts
- T1531 - Account Access Removal
- T1087 - Account Discovery

## Notes
This is a classic case of security logic bypass where UI-level restrictions provide a false sense of security. The vulnerability demonstrates that authorization must be enforced at the data processing layer (API/backend), not presentation layer (UI). The mention of 'provisioning_api' indicates the issue affects multiple attack vectors, increasing severity.

## Full report
<details><summary>Expand</summary>

### Steps
1. As admin make user1 group admin for group1 and group2
2. As user1 create a new user user2
3. As user1 try to remove the user from both groups via the UI
4. Take the first `togglegroup.php` request and replay it with `group2` on curl

### Expected
Should not work

### Actual
The group-admin can escape his groups and create users that are not part of his groups.

Also possible via the provisioning_api.

Either the restriction should be enforced on the api endpoints (not only in the UI), or the restriction in the UI should be removed.


</details>

---
*Analysed by Claude on 2026-05-24*
