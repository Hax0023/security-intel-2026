# Unauthorized Group Deletion via Sequential ID Prediction and CSRF Token Reuse

## Metadata
- **Source:** HackerOne
- **Report:** 8104 | https://hackerone.com/reports/8104
- **Submitted:** 2014-04-19
- **Reporter:** mickyd
- **Program:** Localize.io
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Broken Access Control, Insecure Direct Object References (IDOR), CSRF Token Reuse/Validation Bypass, Insufficient Authorization Checks
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An authenticated user can delete groups in any project without proper authorization by using the same POST method as group creation, combined with sequential ID guessing and CSRF token reuse. The application fails to validate whether the user has permission to delete groups in target projects or verify CSRF tokens are single-use.

## Attack scenario
1. Attacker creates a group in their own project to observe the deleteGroup request structure and CSRF token format
2. Attacker identifies that group IDs are sequential integers (e.g., 95, 96, 97, 98) with no randomization
3. Attacker captures a valid CSRF token from their own group deletion request
4. Attacker modifies the POST request to target a different project (changing 3F to 8h) while keeping the same CSRF token
5. Attacker increments deleteGroup[id] values to target groups in other projects owned by different users
6. Attacker successfully deletes arbitrary groups across the platform, causing data loss for other users

## Root cause
The application implements insufficient authorization checks by failing to verify that the authenticated user has permission to delete groups in the target project before processing the deleteGroup request. Additionally, CSRF tokens are not validated as single-use or project-specific, and no rate limiting prevents sequential ID enumeration.

## Attacker mindset
The attacker demonstrates opportunistic vulnerability discovery by recognizing that if group creation is accessible, the inverse operation (deletion) may also lack proper controls. The use of sequential ID guessing reflects lazy security implementation assumptions and tests basic authorization assumptions across different projects.

## Defensive takeaways
- Implement strict authorization checks verifying user has delete permissions for the specific group in the target project before processing requests
- Use cryptographically random, non-sequential identifiers for sensitive resources instead of predictable integer IDs
- Enforce CSRF token validation with single-use tokens that are bound to specific users, sessions, and operations
- Implement proper access control lists (ACLs) that explicitly check project membership and role permissions
- Log and monitor group deletion operations across all projects for suspicious patterns
- Add rate limiting and alerting for failed authorization attempts
- Use framework-provided CSRF protection mechanisms that validate token freshness and binding

## Variant hunting
Test creation/read/update/delete operations on other resource types using same sequential ID prediction
Attempt to perform administrative actions (change ownership, permissions) on groups without authorization
Test whether CSRF tokens from one operation can be reused for different operation types
Check if project ID prediction (3F → 8h) allows unauthorized access to other projects' resources
Enumerate whether user IDs are sequential and if groups can be accessed/deleted across user boundaries
Test if direct API endpoints bypass the web interface authorization checks

## MITRE ATT&CK
- T1190
- T1566
- T1087
- T1550

## Notes
This is a classic IDOR vulnerability combined with weak CSRF protection. The researcher (Daksh) demonstrates good security intuition by recognizing the permission model inconsistency. The vulnerability likely affects data integrity across the entire platform. The report lacks specific project IDs and group IDs actually exploited, suggesting either responsible disclosure or early-stage reporting. The vulnerability appears to have been submitted relatively early in bug bounty program history (Report ID 8104).

## Full report
<details><summary>Expand</summary>

If you can make a group then why can't you delete the group :P 

With same method of creating the group you can delete the group 
But have some restrictions :/ :

1) in any project you ll not get to know the deleteGroup[id] 
2) May be I'm only one who is making groups now so i can assume the deleteGroup[id] like 96,97,98 :P

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
Content-Length: 81

CSRFToken=NTc4NTUxMjY1MzUxZTllOGIwYWM4MC4yMjE1MjUxNw%3D%3D&deleteGroup%5Bid%5D=95

Now he ll change the POST /pages/create_project/3F with POST /pages/create_project/8h and the deleteGroup[id] .

and send the request and group ll be deleted.

Take a look and lemme know if you need more info .

Daksh


</details>

---
*Analysed by Claude on 2026-05-24*
