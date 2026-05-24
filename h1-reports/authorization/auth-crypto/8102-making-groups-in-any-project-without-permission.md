# Unauthorized Group Creation in Other Users' Projects via Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 8102 | https://hackerone.com/reports/8102
- **Submitted:** 2014-04-19
- **Reporter:** mickyd
- **Program:** Localize.io
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Insecure Direct Object Reference (IDOR), Missing Authorization Check
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An authenticated user can create groups in any public project they don't own by intercepting and modifying the project ID parameter in the group creation request. The application fails to validate that the requesting user has permission to modify the target project, allowing privilege escalation through direct object reference manipulation.

## Attack scenario
1. Attacker identifies a target public project owned by another user (e.g., project ID 8h)
2. Attacker creates a test group in their own project (project ID 3F) and intercepts the POST request
3. While intercepting, attacker modifies the project ID parameter from 3F to 8h (the target project)
4. Attacker forwards the modified request with the target project ID
5. The application processes the request without validating the attacker's permissions on project 8h
6. A group is successfully created in the victim's project without their authorization

## Root cause
The application performs authorization checks only on the client-side or assumes the project ID in the request parameter belongs to the authenticated user. Server-side validation fails to verify that the user has edit permissions on the specified project before processing the group creation request. The parameter is trusted implicitly without re-validating ownership.

## Attacker mindset
Opportunistic abuse of trust in client-supplied parameters. The attacker recognizes that authorization checks are missing between client submission and server processing, allowing simple parameter tampering to escalate privileges. This is classic IDOR exploitation using request interception.

## Defensive takeaways
- Implement server-side authorization checks before any resource modification, verifying the user has edit permissions on the target project
- Use indirect references (tokens/UUIDs) instead of direct object IDs where feasible, or enforce strict ownership validation
- Validate that the project ID in the request matches the user's session context and permissions
- Log and alert on authorization failures and suspicious cross-project modifications
- Apply the principle of least privilege: ensure all state-changing operations require explicit permission validation
- Use middleware or decorators to enforce authorization checks consistently across all endpoints

## Variant hunting
Test other state-changing operations (delete groups, modify settings) with similar parameter manipulation
Check if users can modify/delete resources in projects where they lack permissions
Verify if the vulnerability extends to private projects or projects requiring invitation
Test if attacker can enumerate valid project IDs through failed authorization attempts
Check if group membership/role changes can be applied to other users' projects
Test if the vulnerability works with other user roles (viewer, translator) trying to perform admin actions

## MITRE ATT&CK
- T1190
- T1566
- T1548

## Notes
Classic IDOR vulnerability discovered through manual testing and request interception. The simplicity of exploitation (basic parameter modification) combined with high impact (unauthorized project modification) makes this a critical authorization flaw. Public projects are particularly sensitive as they increase the attack surface. No CSRF token validation appears to have prevented this, suggesting the authorization layer is the only intended control.

## Full report
<details><summary>Expand</summary>

Something Interesting happening here !! ;)

Steps to reproduce :

1) Suppose User1 have Public Project called http://www.localize.io/v/8h
2) In public project any other user ll not have permissions to edit project 
3) Now User2 want to make a group in http://www.localize.io/v/8h which is unlikely not possible .
4) Soo what now ?? :P
5) User2 ll go to his any own project and edit the project like (http://www.localize.io/pages/create_project/3F) and he ll create a new group there , while creating the new group intercept the request and change it with http://www.localize.io/v/8h
6) Bang !! The group ll be created on User1 side .

Request (From User2 side) :

POST /pages/create_project/3F HTTP/1.1
Host: www.localize.io
User-Agent: Mozilla/5.0 (Windows NT 6.2; rv:28.0) Gecko/20100101 Firefox/28.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://www.localize.io/pages/create_project/82
Cookie: PHPSESSID=srdrqpfu6k679bna6e2rtrsrq7
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 84

CSRFToken=NTc4NTUxMjY1MzUxZTllOGIwYWM4MC4yMjE1MjUxNw%3D%3D&addGroup%5Bname%5D=Test

Now he ll change the POST /pages/create_project/3F with POST /pages/create_project/8h

and send the request and group ll be created on User1 side .

Take a look and lemme know if you need more info .

Daksh

</details>

---
*Analysed by Claude on 2026-05-24*
