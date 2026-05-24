# Privilege Escalation in BuddyPress Group Management - Moderator to Administrator

## Metadata
- **Source:** HackerOne
- **Report:** 837018 | https://hackerone.com/reports/837018
- **Submitted:** 2020-04-02
- **Reporter:** hoangkien1020
- **Program:** BuddyPress
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Privilege Escalation, Broken Access Control, Insufficient Input Validation, Insecure Direct Object Reference (IDOR)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
BuddyPress core contains a privilege escalation vulnerability in the group management module that allows a moderator to elevate their privileges to administrator in a group they do not own. By manipulating the group member promotion API endpoint, an attacker can change their role from moderator to admin, gaining full control over any group where they hold moderator status.

## Attack scenario
1. Attacker creates Account A and Account B with separate groups
2. Attacker uses Account A to create Group ABC and adds both users
3. Attacker promotes Account B to Moderator role in Group ABC
4. Attacker creates a separate Group XYZ using only Account B
5. Attacker accesses the manage-members endpoint and captures a role change request
6. Attacker replays the request against Group ABC's API endpoint, changing their role to admin and gaining full control

## Root cause
The BuddyPress REST API endpoint (/wp-json/buddypress/v1/groups/[group_id]/members/[user_id]) fails to properly validate user permissions before processing role promotion requests. The application trusts the client-side role parameter without verifying the requesting user has authorization to promote members in the target group.

## Attacker mindset
An attacker with moderator access in a group recognizes the API lacks proper authorization checks and attempts to escalate privileges by directly modifying the promotion request to target the group they moderate. They capture legitimate requests to understand the API structure, then replay modified requests against other groups.

## Defensive takeaways
- Implement server-side authorization checks before processing any role changes - verify the requesting user has admin rights in the target group
- Validate that role promotion requests originate from group administrators only, not moderators
- Use capability-based access control (not just role-based) to determine if a user can promote other users
- Implement CSRF tokens on state-changing API operations
- Log all privilege escalation attempts for audit trails
- Add rate limiting on administrative actions
- Implement principle of least privilege - moderators should only have permissions explicitly granted, not inherit admin capabilities
- Use nonces/tokens tied to specific users and groups to prevent request replay

## Variant hunting
Check if similar privilege escalation exists in other BuddyPress modules (xprofile, messaging, etc.)
Investigate if other role transitions (moderator to admin, member to admin) bypass authorization
Test if users can promote themselves in any group where they have any role
Check if group ownership can be transferred via the same vulnerability
Examine if the vulnerability affects bulk member operations
Test if the vulnerability works cross-group (promoting users in groups the attacker doesn't belong to)
Investigate API token/session handling for authorization bypass scenarios

## MITRE ATT&CK
- T1190
- T1548
- T1578
- T1134

## Notes
This is a classic authorization bypass vulnerability where server-side permission checks are missing. The attacker leverages legitimate moderator access in one group to gain unauthorized admin access in another group by manipulating API parameters. The vulnerability requires low privilege (moderator role) but yields high impact (administrator control). Video PoC was provided but not included in this analysis. BuddyPress maintainers should audit all admin-related API endpoints for similar authorization failures.

## Full report
<details><summary>Expand</summary>

## Description:

BuddyPress core allows Moderate to Administrator in Manage Group Members module

## Steps To Reproduce:

Step 1 : Create two account with two groups
Step 2 : In account A, create group abc with this two users.
Step 3 : Administrator in group abc promote account B to Moderator
Step 4 : In account B, create own group(without account A), only account B.
Step 5: In account B, access quick link here:
domain/groups/[group_name]/admin/manage-members/ 
Change your B's group.
There are  Edit | Ban | Remove for you to select. Focusing to admin(When you are admin, all thing belongs you).
Therefore, I select Edit. Change to Moderate(To capture this request)
Change such as here:
In POST method: 
POST /wp-json/buddypress/v1/groups/[group_A_id]/members/[id_user] HTTP/1.1
In body/data:
action=promote&role=admin
Note: change [group_A_id] to group you are moderator and [id_user]- your id
Step 6: Done, you are admin's group A. You can do anything.

Poc with video

## Recommendations
Valid user with their roles

## Impact

User will takeover group, do anything such as, edit roles,remove, ban, delelte group,..... (Perform as administrator)

</details>

---
*Analysed by Claude on 2026-05-24*
