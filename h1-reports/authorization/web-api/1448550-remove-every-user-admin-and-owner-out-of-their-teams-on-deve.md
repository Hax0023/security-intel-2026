# Remove Every User, Admin, And Owner Out Of Their Teams on developers.mtn.com via IDOR + Information Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 1448550 | https://hackerone.com/reports/1448550
- **Submitted:** 2022-01-13
- **Reporter:** wallotry
- **Program:** MTN (developers.mtn.com)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Information Disclosure, Broken Access Control, Insufficient Authorization Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A critical IDOR vulnerability in the team member removal functionality allows any authenticated user to remove arbitrary users from any team by manipulating team_id and user_id parameters in API requests. The vulnerability exposes sensitive user and team information, and can be weaponized at scale to remove all users from all teams within 12-20 hours through brute-force attacks on 4-digit numeric IDs.

## Attack scenario
1. Attacker creates account A on developers.mtn.com and gains a valid session token
2. Attacker intercepts and analyzes the HTTP request used to remove a team member (contains team_id and user_id parameters)
3. Attacker modifies the request by replacing team_id and user_id with values from other teams/users they don't control
4. Server processes the request without verifying the attacker has authorization over the target team, removing the user and disclosing team/user names in response
5. Attacker automates brute-force attacks using Burp Intruder or custom scripts, cycling through all possible 4-digit team_id and user_id combinations (10,000 x 10,000 = 100M combinations)
6. System removes users from teams at scale, including admins and owners, within hours

## Root cause
The application fails to validate object-level access control on the user removal endpoint. The server accepts team_id and user_id as direct parameters without verifying: (1) the requesting user has permission to manage the target team, (2) the target user actually belongs to the target team, or (3) the user is authorized to perform removal actions on that specific team.

## Attacker mindset
An attacker with basic account access recognizes that numeric IDs in removal requests are predictable and not validated against the requester's permissions. They realize that by simply changing two parameters, they can impact any team or user. The brute-force angle suggests lateral thinking about automation to scale the impact from removing one user to removing all users system-wide.

## Defensive takeaways
- Implement session-based authorization checks: verify the requesting user has explicit permissions (owner/admin role) on the target team before allowing removal operations
- Validate object ownership: ensure the target team_id belongs to the authenticated user's accessible teams
- Implement indirect object references (UUIDs instead of sequential numeric IDs) to prevent enumeration and reduce brute-force feasibility
- Add rate limiting on user removal endpoints to prevent large-scale brute-force automation
- Audit all object removal endpoints for similar IDOR patterns; this vulnerability likely exists in other team management functions
- Minimize information disclosure by not returning user/team names in successful removal responses, or only return them if already visible to requester
- Log all user removal actions with requester details for forensic analysis and anomaly detection
- Implement approval workflows or confirmation steps for removing team owners/admins

## Variant hunting
Test team creation, update, and deletion endpoints with foreign team_id values
Check team invitation acceptance/rejection with modified team_id or user_id
Test team role modification (promote/demote to admin/owner) with unauthorized IDs
Review all user profile update endpoints (settings, permissions) for similar IDOR patterns
Check team settings modifications (name, description, privacy) with unauthorized team_id
Test team message/channel access with invalid team_id parameters
Review any endpoint returning sensitive user/team data in responses for information leakage

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (IDOR vulnerability exploitation)
- T1078 - Valid Accounts (using legitimate authenticated account)
- T1087 - Account Discovery (enumerating user and team IDs)
- T1526 - Reconnaissance (discovering accessible teams and users)
- T1531 - Account Access Removal (removing users from teams at scale)

## Notes
The report demonstrates professional vulnerability research by: (1) clearly explaining the vulnerability with a realistic mental model, (2) providing step-by-step reproduction, (3) demonstrating both manual and automated attack vectors, (4) quantifying impact (12-20 hour brute-force timeline), and (5) proposing specific remediations. The numeric ID scheme (4 digits = 10,000 possibilities) enables the brute-force aspect; changing to UUIDs would significantly reduce attack feasibility. The information disclosure component (leaking usernames and team names) makes this more exploitable as reconnaissance. Reference to report #1448475 suggests a related vulnerability in the same application.

## Full report
<details><summary>Expand</summary>

Hello world,

This vulnerability is too involved with regular users, in order for us to prevent any damage, we need 3 different user accounts we own. 
This gives us specific "user_id" and "team_id" to work with.
There's an Information Disclosure as a side effect of this vulnerability. User and team names are disclosed in the response from the server.

## Steps To Reproduce(POC)

==First, let's paint a mental picture of this vulnerability and the required conditions using accounts with imaginary user_id & team_id.
The vulnerability and conditions are realistic, the only imaginary thing is the user_id and team_id.==

 1. Create 3 accounts on developers.mtn.com(Account A, B, and C)

==My imaginary accounts:==
- A: First Account(imaginary user_id=1111 & team_id=0001)
- B: Second Account(imaginary user_id=1112 & team_id=0002)
- C: Third Account(imaginary user_id=1113 & team_id=0003)
 2. Login to A, Invite B to your Team A
 3. Login to B, Invite C to your team B
 4. Open Burp Suite
 5. Login to A, Remove B(Please Intercept This Request)
 6. Send the Intercepted request to the repeater tab
 7. Modify the request(Our Goal is to remove C from Team B, which we don't have access or permissions to.)
 8. Replace the team_id with Team B's team_id. Replace the user_id with C's user_id.
 9. Send the Request. (This Request will disclose C's username And Team B's name. Making this an information disclosure. PII)

{F1577574}

 10. C will be removed from B's Team B.
 11. C will receive an email from MTN telling him/her that he/she has been removed from Team B.

{F1577544}

## Steps To Reproduce(Removing Every User)

==This can be done with a custom script/code without the need for Burp Suite==
 1. Intercept the request for removing a user, and send it to the Burp Suite intercept tab.
 2. Config your settings to brute-force through every team_id and user_id. This part is not that hard because every user_id and team_id has only 4 digits.
 3. Run the intruder request. When there's a successful user_id and team_id match, the user whose ID has been matched, will be removed.
 4. If my calculations are correct, it should take 12 Hours to remove every user from every group they're in, the maximum being 20 Hours. The faster the internet speed, the faster the computer, the shorter the time it'll take to brute-force through every user_id and team_id.

## Exploitability
- Anyone with an account on developers.mtn.com can exploit this vulnerability
- All you need is a user_id and a team_id to remove a user from his/her team.(Their privileges don't matter, even the owner is vulnerable)

## Remediation
- Ensure proper session management and object-level user access control checks.
- Apply access control mechanisms such as permissions to certain action.
- Validation of access to a team_id.
- You should always check if a user submitting the request isn't tampering and isn't submitting any ID's that do not belong to his/her account.

## Reference
#1448475

## Impact

A low level user can remove his Admin and Owner from the team.
Every user will be removed from every team they are in, including owners and admins.

</details>

---
*Analysed by Claude on 2026-05-24*
