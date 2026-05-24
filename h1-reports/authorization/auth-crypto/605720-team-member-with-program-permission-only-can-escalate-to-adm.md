# Privilege Escalation via Direct URL Access to Group Management - Broken Authorization on /groups Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 605720 | https://hackerone.com/reports/605720
- **Submitted:** 2019-06-10
- **Reporter:** metnew
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Access Control, Privilege Escalation, Broken Role-Based Access Control (RBAC), Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A team member with only 'Program' permission can directly access the group management endpoint (/TEAM/groups) despite the UI not displaying Group Management or User Management menus, allowing arbitrary privilege escalation to Admin. Additionally, the /TEAM/groups.json endpoint leaks sensitive group membership and permission data to any user with at least one valid permission.

## Attack scenario
1. Attacker is assigned to a team with limited 'Program' permission only
2. Attacker navigates directly to https://hackerone.com/TEAM/groups bypassing UI restrictions
3. Server accepts the request despite authorization checks failing (likely due to frontend-only permission hiding)
4. Attacker selects their own user group from the group management interface
5. Attacker modifies group permissions by adding 'Admin' or other elevated permissions
6. Attacker gains full administrative control of the team through escalated privileges

## Root cause
Authorization is enforced only at the UI/frontend level (hiding menu items) rather than enforcing server-side authorization checks on the /groups endpoint. The application relies on security through obscurity by not displaying menu options, but fails to validate user permissions when the endpoint is accessed directly. The JSON endpoint also lacks proper data filtering based on user permissions.

## Attacker mindset
An insider threat or compromised low-privilege account can easily escalate to admin by recognizing that authorization is frontend-only. The attacker would use browser developer tools or direct URL manipulation to bypass menu restrictions. The information disclosure of groups.json provides reconnaissance data to identify which permissions to escalate to.

## Defensive takeaways
- Implement server-side authorization checks on ALL endpoints, not just UI menu visibility
- Enforce least privilege principle: validate user permissions before processing any state-changing operations
- Apply authorization filters to JSON endpoints to exclude sensitive data based on user role
- Separate authentication (who you are) from authorization (what you can do) - validate both at the API level
- Implement consistent permission validation across all endpoints returning group/user management data
- Use middleware/interceptors to enforce RBAC on protected routes before business logic execution
- Log and alert on suspicious permission modification attempts or direct access to restricted endpoints

## Variant hunting
Check other management endpoints (/users, /permissions, /audit-logs, /settings) for same direct access bypass
Test /TEAM/groups.json with different role levels to map data exposure across permission tiers
Attempt permission escalation via other group management operations (create group, delete user, modify existing permissions)
Test if other state-changing operations rely on frontend-only authorization (organization settings, policy changes)
Check API endpoints for similar IDOR vulnerabilities where resource IDs can be enumerated
Investigate if readonly permission actually filters data or just hides UI elements
Look for similar patterns in other SaaS applications with team/group management

## MITRE ATT&CK
- T1190
- T1548
- T1087
- T1526
- T1552

## Notes
This is a classic authorization bypass due to separation of concerns failure. The reporter correctly identified that the real root cause is broken RBAC implementation. The fact that identical data is served on /teams.json (with restrictions) vs /TEAM/groups.json (without proper filtering) suggests inconsistent authorization logic. This vulnerability likely existed because the engineering team implemented authorization on read-only endpoints but forgot to implement the same checks on write/administrative endpoints. The presence of both vulnerabilities in one endpoint set (privilege escalation + information disclosure) indicates systemic authorization framework issues rather than isolated bugs.

## Full report
<details><summary>Expand</summary>

## Summary

`https://hackerone.com/TEAM/groups` URL is accessible to team members with Program permission, even when "Group Management" and "User Management" menus aren't visible.

I didn't research this further, however, I was able to grant all permissions to the user assigned to a group with `Program` permission.

## PoC

> Tested on a user assigned to a group with Program permissions

1. Go to `https://hackerone.com/TEAM/groups`
2. Select the current user's group
3. Add arbitrary permission (e.g. Admin)

## Additional information disclosure

I noticed that `hackerone.com/teams.json` is accessible to users with "read-only" permission, but `https://hackerone.com/TEAM/groups.json` is accessible to users with at least 1 valid permission. 

That's strange because the data is *identical* and **allows disclosing user ids, assigned groups, groups permissions**.

Reporting 2 issues in one report, because it's hard to understand the real root cause of the broken RBAC.

## Impact

- A team member with 1 valid permission (except "readonly", e.g. Program) can escalate own permissions in the team to arbitrary permissions.
- "readonly" team member can disclose the team's groups, assigned users, groups' permissions and ids/names.

</details>

---
*Analysed by Claude on 2026-05-24*
