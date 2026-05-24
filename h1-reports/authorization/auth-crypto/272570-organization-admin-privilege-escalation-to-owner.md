# Organization Admin Privilege Escalation To Owner

## Metadata
- **Source:** HackerOne
- **Report:** 272570 | https://hackerone.com/reports/272570
- **Submitted:** 2017-09-28
- **Reporter:** rhynorater
- **Program:** Unknown
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln:** Privilege Escalation, Horizontal Privilege Escalation, Insecure Direct Object References (IDOR), Authorization Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An organization admin can escalate their own privileges to owner level through the user edit functionality, effectively taking complete control of the organization and removing the original owner. This vulnerability allows complete organizational takeover with no additional authentication or approval required.

## Attack scenario
1. Attacker creates or obtains admin role within a target organization
2. Attacker navigates to organization user management and selects their own user profile for editing
3. Attacker modifies their role field from 'admin' to 'owner' via the API or web interface
4. System processes the request without validating authorization, allowing the privilege escalation
5. Attacker now has owner-level permissions and can modify other users
6. Attacker removes original owner from the organization, completing the takeover

## Root cause
The application fails to implement proper authorization checks when modifying user roles. The backend accepts role modification requests from admins without verifying that the requester has sufficient permissions to grant owner-level privileges, likely checking only that a user is authenticated rather than validating their actual authorization level for that specific action.

## Attacker mindset
An insider threat or compromised admin account seeking to gain complete control of an organization's resources, data, and settings. The attacker exploits the trust relationship granted by admin status to escalate beyond intended permissions with minimal effort, indicating either careless permission logic or an assumption that admins wouldn't abuse their role.

## Defensive takeaways
- Implement strict authorization checks that verify a user cannot grant themselves or others privileges higher than their own role
- Use role-based access control (RBAC) with explicit deny rules for privilege escalation attempts
- Require additional authentication (MFA, approval workflow) for sensitive role changes, especially to owner level
- Audit and log all role modification attempts and changes, including failed attempts
- Enforce the principle of least privilege and separate owner functionality from admin functionality
- Implement immutable owner transitions that require multiple stakeholders to approve
- Add validation that prevents users from modifying their own permissions or those of higher-privileged users
- Conduct regular security reviews of authorization logic, especially around role management

## Variant hunting
Test if admins can modify other admins' roles or escalate them to owners
Check if moderators or lower roles can escalate through API endpoints not protected in UI
Verify if bulk user import/modification endpoints have the same authorization checks
Test if role changes persist across session boundaries or are reverted on logout/login
Check if organization transfer functionality has similar escalation vulnerabilities
Look for permission checks that use role names instead of numeric/immutable role IDs
Test if admins can create new owners or modify owner permissions through API calls with missing parameters

## MITRE ATT&CK
- T1548
- T1548.002
- T1087
- T1110
- T1190

## Notes
The reporter also requests IP whitelisting due to rate limiting/blacklisting issues during testing. This is a critical privilege escalation requiring immediate patching. The vulnerability is trivial to exploit and has severe impact on organization security.

## Full report
<details><summary>Expand</summary>

##Summary
It seems there is an issue with your roles which allows an admin to escalate his own privileges to owner and takeover the organization. 

##Reproduce
1. Create an account, accountA
2. Create another account, accountB
3. Create an organization under accountA and invite accountB to that organization as admin
4. Accept invitation with accountB and log out
5. Confirm accountB for the organization on accountA
6. Log in with accountB
7. Navigate to the organization -> invite users -> edit accountB user and change to owner
8. See that the change worked and accountB is now owner. 
9. To proceed with organization takeover, remove the original owner
10. Note that (after login and logout) the original owner no longer is in the organization

##Impact
Anyone who is an admin on an organization can take total control of the organization and kick the original owner out. 

##Request
Could you please whitelist ip 173.167.43.57 and ip 54.197.209.98 so that I can keep reporting? It is very hard to fully test the application while I am constantly getting blacklisted and having to use my phone as a hotspot :P If not, that's cool, just figured I'd ask :)


Thanks,
Justin Gardner

</details>

---
*Analysed by Claude on 2026-05-24*
