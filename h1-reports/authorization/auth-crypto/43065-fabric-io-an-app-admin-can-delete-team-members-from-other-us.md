# Fabric.io - App Admin Can Delete Team Members from Other User Apps via Insecure Direct Object Reference

## Metadata
- **Source:** HackerOne
- **Report:** 43065 | https://hackerone.com/reports/43065
- **Submitted:** 2015-01-09
- **Reporter:** satishb3
- **Program:** Fabric.io
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Horizontal Privilege Escalation, Denial of Service
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An authenticated app admin can delete team members from applications they don't have access to by manipulating account IDs and app IDs in DELETE requests. This allows cross-app team member removal and potential denial of service by deleting the sole admin from a victim application.

## Attack scenario
1. Attacker (Hackeradmin) logs into Fabric.io and navigates to their own app's team management settings
2. Attacker intercepts the DELETE request sent when removing a team member from their own app (HackerApp)
3. Attacker modifies the intercepted request by replacing the account ID and app ID with those from a victim's app (VictimApp) they shouldn't have access to
4. Attacker removes the admin parameter from the request to bypass potential authorization checks
5. Attacker sends the modified DELETE request, successfully removing a team member from VictimApp without authorization
6. If victim app has only one admin, attacker can delete that admin, rendering the app completely inaccessible and preventing password reset

## Root cause
Server-side authorization checks on the DELETE endpoint fail to verify that the authenticated user has admin privileges for the specified app before allowing team member deletion. The endpoint relies solely on the presence of valid IDs rather than enforcing app-level access control, making it vulnerable to IDOR attacks.

## Attacker mindset
A malicious app admin with access to Fabric.io could exploit this to sabotage competitor applications, lock out legitimate users, or cause organizational disruption by removing critical team members from apps they have no authorization to manage.

## Defensive takeaways
- Implement server-side authorization checks verifying the authenticated user has admin rights for the target app before allowing DELETE operations
- Validate that the app_id belongs to an app managed by the authenticated user
- Never rely on client-submitted IDs alone; enforce role-based access control at the API endpoint level
- Log all team member modifications with audit trails for forensic investigation
- Implement rate limiting on DELETE endpoints to prevent mass account removal
- Require additional confirmation (e.g., email verification) before removing the last admin from an application
- Sanitize and validate all ID parameters to prevent enumeration attacks
- Implement mandatory multi-factor authentication for sensitive operations like team member removal

## Variant hunting
Check other endpoints that modify user/team relationships (add member, change roles, update permissions) for similar IDOR vulnerabilities
Test if the vulnerability extends to organization-level operations or cross-organization tampering
Examine API endpoints for other resources (projects, APIs, organizations) that might have identical authorization flaws
Test if account deletion endpoint has the same vulnerability allowing account enumeration or deletion
Check if the vulnerability allows privilege escalation (changing admin to member or vice versa) across apps
Investigate whether app_id parameter is predictable or enumerable for brute force attacks

## MITRE ATT&CK
- T1190
- T1578
- T1531
- T1087

## Notes
This is a critical IDOR vulnerability enabling both horizontal and vertical privilege escalation. The DOS variant is particularly severe as it creates an unrecoverable state when the sole admin is deleted. The attacker requires knowledge of app_id and account_ids, which can be obtained through invitation responses or enumeration. The removal of the 'admin' parameter in the exploit suggests the application had minimal server-side validation of authorization context.

## Full report
<details><summary>Expand</summary>

It is possible for an app admin to delete all the team members from other apps for which he doesn't have access.

To reproduce the attack, create two apps and add different user roles as below, 

VictimApp  - Aliceadmin, Alicemember 

HackerApp - Hackeradmin, Hackermember

Before proceeding with the attack, log into fabric.io as Aliceadmin and grab the VictimApp id and account ids.

VictimApp id: 54ad5e03a25bb8136b000002
Aliceadmin id: 54aa4c616bb166b8f300134a
Alicemember id: 54af48304d8f5b12ff0000fd

Case 1:  Deleting other app team members

-> Log into fabric.io as Hackeradmin.
-> Navigate to settings->apps->HackerApp->Team member link.
-> Click on x symbol corresponding to Hackermember to remove him from HackerApp. Intercept this request using burp proxy.

	Proxy shows a similar request as below,

	DELETE /accounts/54aa37d8f61d7749430127ee?admin=true&app_id=54aeafc28bfc55053d000028 HTTP/1.1
	Host: fabric.io

-> In the intercepted request change the account id, app id to other app user and remove admin parameter.
 
For example, Alicemember - account id: 54aa4c616bb166b8f300134a, VictimApp id: 54ad5e03a25bb8136b000002

	Modified request is,

	DELETE /accounts/54aa4c616bb166b8f300134a?app_id=54ad5e03a25bb8136b000002 HTTP/1.1
	Host: fabric.io

-> Send the modified request to the server and it removes Alicemember from VictimApp.
-> To confirm, login as Aliceadmin and look at the VictimApp team members.

Though Hackeradmin does not have access to VictimApp, he successfully deleted VictimApp team member.

Case 2: DOS

Aliceadmin is the only user in VictimApp. If there is only one user in the app, fabric does not allow to leave the app. However, by following the steps provided above, it is possible to delete Aliceadmin account from the app. Now, VictimApp is not accessible to anyone and Aliceadmin can't log into Fabric with his password (Reset password also does not work - it shows success but does not send the reset link in email).

To successfully perform the attack, attacker has to know the app id and corresponding account ids. Possible scenarios are, 

-> Hackeradmin might be a member of VictimApp initially and later his access is removed. He might have noted down (or have some logs) VictimApp id and all other account ids.
-> Hackeradmin can obtain the victim account ids by sending an invitation to the victim email id (account id displayed in the response). Later, he can perform a bruteforce on the app id.


</details>

---
*Analysed by Claude on 2026-05-24*
