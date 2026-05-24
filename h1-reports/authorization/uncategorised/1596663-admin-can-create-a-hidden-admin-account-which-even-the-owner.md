# Hidden Admin Account Creation via Multiple Role Invitations on Reddit Ads

## Metadata
- **Source:** HackerOne
- **Report:** 1596663 | https://hackerone.com/reports/1596663
- **Submitted:** 2022-06-10
- **Reporter:** 41bin
- **Program:** Reddit (HackerOne)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Authentication Bypass, Authorization Flaw, Account Manipulation, Session Token Abuse
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker with admin privileges on Reddit Ads can invite a malicious account multiple times with different roles, then remove the visible invitation while retaining an active authorization token that allows continued administrative actions. This creates an undetectable hidden admin account that even the organization owner cannot locate or remove from the members list.

## Attack scenario
1. Admin invites a malicious email address with 'admin' role and attacker accepts the invitation
2. Admin invites the same email address again with a different role (e.g., 'analyst') to generate a new invitation
3. Attacker accepts the second invitation while logged into the malicious account
4. Attacker extracts the authorization token from the second role's session via network interception
5. Admin removes the malicious user from organization, deleting the visible account record
6. Attacker reuses the extracted token to make API calls (invite users, remove members) despite being removed from the member list

## Root cause
The application fails to invalidate previously issued authorization tokens when a user's role is removed or changed. Additionally, the system allows duplicate invitations for the same email address across different roles, and the backend does not properly validate that an authenticated request's user still maintains valid organizational membership before executing privileged operations.

## Attacker mindset
A malicious admin seeks to maintain persistent hidden access after being demoted or removed by the owner. By exploiting the multi-role invitation mechanism and token management flaws, they can preserve administrative capabilities while remaining invisible in the UI, enabling further sabotage or lateral movement.

## Defensive takeaways
- Invalidate all issued tokens when a user's role is changed or removed from an organization
- Implement backend membership validation on every API request requiring organizational privileges
- Prevent duplicate active invitations for the same email address within a single organization
- Enforce single-role-per-user per organization; reject or replace prior invitations when new ones are issued
- Log all token generation, usage, and invalidation events for audit trails
- Implement token rotation and short expiration times for sensitive operations
- Add UI indicators showing all active sessions and roles, especially those with elevated permissions
- Require explicit confirmation when revoking user permissions with clear indication of immediate token revocation

## Variant hunting
Check if other role-based systems allow multiple simultaneous role assignments for same user/org
Test whether tokens from revoked roles continue to work across other API endpoints
Investigate if the issue affects other endpoints beyond invitation creation
Examine whether the vulnerability exists in other multi-tenant applications using similar permission models
Test if role downgrade (admin to analyst) creates similar token persistence issues
Check if organization removal/deletion properly invalidates all member tokens

## MITRE ATT&CK
- T1190
- T1098
- T1078
- T1556
- T1555
- T1550

## Notes
This is a sophisticated privilege escalation exploiting race conditions in token lifecycle management. The writeup demonstrates excellent methodical reproduction steps. The core issue is that the application trusts authorization tokens without validating current organizational membership status. This affects confidentiality, integrity, and availability of the organization's ad account. The use of Burp Suite for token extraction shows attacker capability assessment. The vulnerability requires existing admin access to initiate but results in persistent compromise beyond the attacker's assigned permissions.

## Full report
<details><summary>Expand</summary>

ads.reddit.com is an ads creating and managing application for reddit. The application has the feature to invite other members to the organization and give different roles at ad management.
Testing around the role management functionalities, I have noticed that a user with the same email can get invited to the same organization multiple times if the user is assigned with different roles.
So, taking advantage of this behavior I found the admin as an attacker can create an `undetectable/hidden admin account` and do administrative actions on the organization like remove other users and invite other users. Since this malicious account information  can not be seen in the `members` section, even the `owner` of the organization can not detect and remove this malicious user from the organization.

**Steps to reproduce:**
1) Login as admin from https://ads.reddit.com/
```
I know creating an owner account and then creating an admin account with in a limited time is  little-bit painful.
You can use the following credentials to login as admin

        email :██████████
        name: ███████
        password : ██████████
```
2) Go to https://ads.reddit.com/account/███/permissions and invite a user (malicious hidden user) by giving the role as `admin`
3) login to that account (malicious hidden user) from a different browser and accept the invite. 
4) Same as the second step, go to the admin account and invite the same malicious user by giving the role as `Analyst`.
5) Now go to the malicious user account and then go to https://ads.reddit.com/accounts.
6) You will see the new invitation arrived with the `Analyst` role. Accept the invitation.
7) From this account (malicious) go to https://ads.reddit.com/account/████████/billing while intercepting  the requests using burpsuite.
8) Look at the burp history and find out the `Authorization token` used by the account and copy it. (see `copy-the-auth-token.png`)
9) Now go to the normal admin account and change the permission of this malicious account to `None`   (It removes malicious account from the organization) and refresh the page to confirm that the malicious user is removed.
10) Using burpsuite repeater, change the email and send the following request by replacing the token which you copied from the 8'th step.
```
POST /api/v2.0/accounts/█████████/invitations HTTP/2
Host: ads-api.reddit.com
Content-Length: 87
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="102"
Accept: application/json
Content-Type: application/json
Authorization: ██████
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.5005.61 Safari/537.36
Sec-Ch-Ua-Platform: "Linux"
Origin: https://ads.reddit.com
Sec-Fetch-Site: same-site
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://ads.reddit.com/
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8

{"data":{"recipient_email":"█████████","type":"ADMIN"}}

```
11) Now you are able to invite other users to the organization even though you are not a member of that organization.

## Impact

Let me explain the `impact` with different scenarios as an example.

1)
-  The owner invites an admin to the organization and the admin who knows about this issue creates an account in this way.
- Latter, the owner decide to change the role of this admin to `analyst`  or remove this admin from the organization due to some reasons
- Now the `admin as the malicious user`, can do sensitive actions in the organization like inviting or removing other users.
- When the `owner` goes to the `members` section, he will not find the malicious account there and even he `can not remove` that malicious account from the organization.

2)
- It also happens when the owner or admin invites other users accidentally in this way.  
- It is not complicated, the vulnerability arises when a user accepts multiple invitations assigned with different roles from a single organization.

</details>

---
*Analysed by Claude on 2026-05-24*
