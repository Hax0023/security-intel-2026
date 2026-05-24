# Able to Remove All Admin Access from Program via Group Management API

## Metadata
- **Source:** HackerOne
- **Report:** 141629 | https://hackerone.com/reports/141629
- **Submitted:** 2016-05-28
- **Reporter:** pardeepbattu02
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Business Logic Error, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A functional bug in HackerOne's group management API allowed an authenticated program owner to remove all administrators from their program by sending a PUT request to the groups endpoint with an empty or reduced team_member_ids array. This violated the critical business rule that every program must have at least one administrator, creating a program lockout situation.

## Attack scenario
1. Attacker authenticates to HackerOne as a program owner with administrative privileges
2. Attacker navigates to program group members management page and observes the group ID (12307)
3. Attacker crafts a PUT request to /sasas/groups/{groupId} with modified team_member_ids containing only non-admin members or empty array
4. Attacker sends the request with JSON payload removing all administrator user IDs from the group
5. Server processes the request without validation that at least one admin must remain
6. All admin access is revoked, leaving the program without any administrators

## Root cause
The API endpoint for updating group permissions lacked server-side validation to enforce the business rule that a program must always have at least one administrator. The system accepted modifications to team_member_ids without checking if the resulting state would leave the program without any admins.

## Attacker mindset
Opportunistic insider threat or disgruntled program owner seeking to sabotage program operations by locking out all administrators. Could also be used to deny other program stakeholders access before transferring/abandoning the program.

## Defensive takeaways
- Implement server-side validation on all group/permission modification endpoints to enforce critical business rules
- Require that at least one user with admin permissions must always exist before accepting group modification requests
- Add transaction checks: validate end-state permissions before committing changes
- Implement audit logging for all privilege modifications
- Require multi-step confirmation for removing final administrative access
- Add warnings when user attempts to remove themselves or the last admin
- Implement role-based access control validation at API layer, not just presentation layer

## Variant hunting
Similar validation bypass in user management endpoints where users can be removed from roles
Permission modification endpoints that don't validate minimum required role coverage
Organization/team management where all owners could potentially be removed
Project deletion when users remove all owners before deletion completes
Webhook or automation settings that could remove all notification recipients

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1531 - Account Access Removal

## Notes
This is a critical business logic vulnerability that could result in complete program lockout. The immutable flag on the group suggests it's a built-in admin group that should have had additional protections. The vulnerability demonstrates the importance of validating business invariants at the API layer rather than relying on client-side enforcement.

## Full report
<details><summary>Expand</summary>

Hey Jobert,


There is a functional bug in hackerone, using which i am able to make the my program admin free.
This shouldn't be happen in the program because atleast one admin be there in program.

Request:
PUT /sasas/groups/12307 HTTP/1.1
Host: hackerone.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:46.0) Gecko/20100101 Firefox/46.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Referer: https://hackerone.com/sasas/groups/12307/members/edit
Content-Length: 157
Cookie: 
Connection: close

{"id":12307,"name":"Admin","team_members_count":2,"permissions":["user_management","program_management"],"immutable":true,"team_member_ids":[{"id":"17940"}]}


Thanks & Regards,
Pardeep Battu


</details>

---
*Analysed by Claude on 2026-05-24*
