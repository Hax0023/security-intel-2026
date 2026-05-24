# Fabric.io: Ex-admin of an organization can delete team members

## Metadata
- **Source:** HackerOne
- **Report:** 55670 | https://hackerone.com/reports/55670
- **Submitted:** 2015-04-10
- **Reporter:** satishb3
- **Program:** Fabric.io
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization, Privilege Escalation, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** auth-crypto

## Summary
When an administrator is removed from an organization, their API access rights are not properly revoked, allowing them to continue performing privileged actions such as deleting team members. An ex-admin can manipulate API requests to remove any organization member despite no longer having administrative privileges.

## Attack scenario
1. Attacker is invited to a target organization as an administrator and records the organization ID and victim member ID
2. Attacker's admin role is revoked and they are removed from the organization
3. Attacker logs back into fabric.io with their account credentials
4. Attacker intercepts a legitimate team member removal request from their own organization
5. Attacker modifies the API request by replacing their organization/account IDs with the target organization and victim member IDs
6. Attacker sends the crafted DELETE request to /api/v3/accounts/{victim_id}/organizations/{target_org_id}/leave, successfully removing the victim from the target organization

## Root cause
The API endpoint lacks proper authorization validation. The server fails to verify that the authenticated user still has active admin privileges in the target organization before processing member removal requests. Authorization checks likely rely solely on authentication token validity rather than validating current organizational membership and role status.

## Attacker mindset
An insider threat or disgruntled former admin leveraging residual access to disrupt organizational operations by removing team members without authorization, causing workflow disruption and potential data loss.

## Defensive takeaways
- Implement server-side authorization checks on every API endpoint verifying the user's current role and membership status in the target organization
- Revoke all API tokens/sessions immediately upon removal of user from an organization
- Audit all privileged API endpoints (/api/v3/accounts/*/organizations/*/leave) for IDOR vulnerabilities
- Require explicit permission verification at request time rather than caching authorization decisions
- Implement comprehensive audit logging for all member removal operations including requester identity and authorization context
- Apply principle of least privilege - ensure API endpoints validate both authentication AND authorization for the specific resource being modified

## Variant hunting
Check if ex-admins can perform other privileged actions (modify org settings, export data, change org name)
Test if ex-members with lower privileges can also manipulate requests to perform admin-only actions
Verify if role downgrade (admin to member) also fails to revoke elevated API privileges
Check if similar vulnerabilities exist in other endpoints accepting organization/account ID parameters
Test invitation endpoints to see if ex-admins can re-invite themselves or create new admins

## MITRE ATT&CK
- T1190
- T1548
- T1078
- T1556

## Notes
This is a classic IDOR combined with inadequate authorization revocation. The vulnerability is particularly dangerous as it allows insider threats to persist after offboarding. The fix should involve token revocation and stateful authorization checks rather than relying on cached permissions.

## Full report
<details><summary>Expand</summary>

When an admin is deleted from an organization, his access rights are not removed properly. This allows an ex-admin to delete team members from the organization.

Before proceeding with attack,

1. Create an organization with two accounts.  Lets say,  VictimOrg - Victimadmin, Victimmember

2. Invite Hackeradmin to VictimOrg and change his role to admin. At this point Hackeradmin can login and grab VictimOrg & Victimmember ids.

     VictimOrg id:54af7e07b8568e8c6a0001e
     Victimmember id:552787195127ae16b8000987

3. Delete Hackeradmin from VictimOrg. Now, Hakeradmin is not a member of VictimOrg anymore. Ideally, he does not have rights to access/make changes to VictimOrg. However, he can still delete team members from the VictimOrg.


Steps listed below shows that Hackeradmin can delete Victimmember from VictimOrg:

1. Log into fabric.io as Hackeradmin.
2. Navigate to settings->organizations->HackerOrg->Team member link.
3. Click on x symbol corresponding to Hackermember to remove him from HackerOrg. Intercept this request using burp proxy.

    Proxy shows a similar request as below,
	
	DELETE /api/v3/accounts/54c1e78b9ea696b3cb00026a/organizations/54aa36e3937ae35559011d17/leave HTTP/1.1
	Host: fabric.io

4. In the intercepted request replace the account id with Victimmember id and org id with VictimOrg id.

	Modified request is,
	
	DELETE /api/v3/accounts/552787195127ae16b8000987/organizations/54af7e07b8568e8c6a0001e/leave HTTP/1.1
	Host: fabric.io

5. Send the modified request to the server and it removes Victimmember from VictimOrg. 
6. To confirm, login as Victimadmin and look at the VictimOrg team members. 


</details>

---
*Analysed by Claude on 2026-05-24*
