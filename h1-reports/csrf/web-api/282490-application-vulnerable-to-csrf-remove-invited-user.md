# Application Vulnerable to CSRF - Remove Invited user

## Metadata
- **Source:** HackerOne
- **Report:** 282490 | https://hackerone.com/reports/282490
- **Submitted:** 2017-10-24
- **Reporter:** ramakanthk35
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
POC:

1. Login to the application with a business account.
2. Go to Manage teams, where we can send invites to a team member. Send a Invite to a team member
3. After the invite is sent to a user, the admin has option to Remove User.
4. While trying to remove the user, capture the request in burp , do not forward the request, send to repeater and drop the request
5. Now, from repeater , copy the ur

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

POC:

1. Login to the application with a business account.
2. Go to Manage teams, where we can send invites to a team member. Send a Invite to a team member
3. After the invite is sent to a user, the admin has option to Remove User.
4. While trying to remove the user, capture the request in burp , do not forward the request, send to repeater and drop the request
5. Now, from repeater , copy the url and put it in a new tab of authenticated admin browser, the user removal is successful

The user removal URL would look like https://infogram.com/api/team/cancel-invitation/c535cc62-9586-4f4b-8306-9381dcdbc815?teamId=16537204&_=1508852073697

</details>

---
*Analysed by Claude on 2026-05-24*
