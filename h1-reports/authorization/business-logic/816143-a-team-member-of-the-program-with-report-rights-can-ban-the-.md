# Team Member with Report Permission Can Ban Admin User

## Metadata
- **Source:** HackerOne
- **Report:** 816143 | https://hackerone.com/reports/816143
- **Submitted:** 2020-03-10
- **Reporter:** haxta4ok00
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Privilege Escalation, Insufficient Permission Validation
- **CVEs:** None
- **Category:** business-logic

## Summary
A team member with only 'Report' permission can ban users with 'Admin' rights from the program, despite having insufficient privileges for this action. This allows an unprivileged user to perform administrative actions and effectively disable administrators from creating reports.

## Attack scenario
1. Attacker joins a program as a team member with 'Report' permission only
2. Admin submits a new report in the program
3. Attacker accesses the 'Ban reporters' panel within the report view
4. Attacker selects the Admin user and executes a ban action
5. System applies the ban without validating that attacker lacks permission to ban admins
6. Admin is now prevented from creating new reports, losing core functionality

## Root cause
The application fails to validate permission levels before executing the 'ban reporter' action. It checks if a user can access the ban panel but does not verify that the user has authority to ban users of equal or higher privilege levels (Admin).

## Attacker mindset
A disgruntled team member or insider threat seeking to disrupt program operations by removing administrative access, potentially motivated by competitive advantage or malice toward specific admins.

## Defensive takeaways
- Implement hierarchical permission validation - users should only be able to ban those with equal or lower privilege levels
- Enforce role-based access control (RBAC) with explicit permission checks before sensitive actions
- Add audit logging for ban operations including who performed the action and on whom
- Implement approval workflows for actions that affect high-privilege users
- Validate both source and target user permissions in the same transaction
- Add alerts/notifications when admin users are banned or restricted

## Variant hunting
Check if other sensitive admin actions are accessible to low-privilege users (delete, modify, suspend)
Test if 'Report' permission members can modify admin settings or configurations
Verify if privilege escalation occurs in other team management operations
Check if bans can be applied cross-program by team members
Test whether admins can ban other admins (should be restricted or require approval)

## MITRE ATT&CK
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts
- T1136 - Create Account (or in this case, remove access)
- T1531 - Account Access Removal

## Notes
This is a critical insider threat vulnerability that allows privilege escalation through insufficient authorization checks. The logical inconsistency (low-privilege user banning admin) should have been caught during authorization layer design. The vulnerability suggests the ban panel checks view permission but not action permission.

## Full report
<details><summary>Expand</summary>

## Summary:
Our team has conducted a number of studies (tests) in the field of permission `Report`. We noticed that a team member of the program with such permission can ban a member with `Admin` rights

## Steps To Reproduce:
1) Admin submit new report in program
2) A team member with Report rights can use the 'Ban reporters ' panel via their report

my group - `one_permission` have permission `Report`

{F743466}
█████

3) After `ban` , admin can't create new report in program (it's not logical)

{F743464}

## Impact

Ban the Admin in program

</details>

---
*Analysed by Claude on 2026-05-24*
