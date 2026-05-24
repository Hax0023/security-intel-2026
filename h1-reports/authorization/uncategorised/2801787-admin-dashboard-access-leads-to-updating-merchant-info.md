# Unauthorized Admin Dashboard Access via Missing Authentication Controls

## Metadata
- **Source:** HackerOne
- **Report:** 2801787 | https://hackerone.com/reports/2801787
- **Submitted:** 2024-10-24
- **Reporter:** tinopreter
- **Program:** ████████ (Payment/Merchant Processing Platform)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln:** Broken Authentication, Broken Access Control, Missing Authorization Checks, Privilege Escalation, Insecure Direct Object References (IDOR)
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated user could register for an admin account despite the UI indicating admin registration was disabled, gaining full access to the admin dashboard. Once authenticated, the attacker could view and modify sensitive merchant, supervisor, cashier, and station data including account credentials, banking information, and passcodes.

## Attack scenario
1. Attacker discovers hidden admin registration endpoint not exposed in UI at ████████
2. Attacker creates admin account via registration endpoint and logs in successfully
3. Attacker is redirected to admin dashboard with full administrative privileges
4. Attacker accesses merchant list at ███████ and modifies merchant account details
5. Attacker changes merchant account numbers to attacker-controlled bank accounts, redirecting payments
6. Attacker also accesses and modifies supervisor/cashier/station accounts and retrieves passcodes

## Root cause
The application implements role-based access control only on the UI layer by hiding registration options, but fails to enforce authorization checks on backend endpoints. The admin registration endpoint lacks proper authentication middleware, allowing any user to create admin accounts. Resource endpoints for merchants, supervisors, cashiers, and stations do not validate user permissions before allowing modifications.

## Attacker mindset
An opportunistic attacker performing reconnaissance discovered the hidden registration endpoint through endpoint enumeration, API inspection, or reverse engineering. Recognizing the complete absence of backend authorization, the attacker escalated from user to admin, then systematically explored available admin functions to identify high-impact targets like merchant financial accounts and supervisor credentials for maximum damage and potential payment fraud.

## Defensive takeaways
- Never rely on UI-level access controls; enforce authorization checks on every backend endpoint
- Implement proper authentication middleware that validates user identity on all protected routes
- Use principle of least privilege - admin accounts should only be created through secure administrative processes, not public registration endpoints
- Implement role-based access control (RBAC) in the backend that verifies user role/permissions for each resource operation
- Audit all user-facing endpoints to identify hidden or undocumented registration/admin functions
- Implement proper access logs and monitoring for sensitive operations like credential changes and account modifications
- Use secure credential transmission - never expose passcodes or sensitive data in plaintext responses
- Implement rate limiting and anomaly detection on sensitive endpoints to catch bulk modifications

## Variant hunting
Search for other role registration endpoints (cashier, supervisor) that might lack proper validation
Test for horizontal privilege escalation by attempting to modify other admin accounts
Check for predictable admin IDs/usernames that could allow direct object reference attacks
Examine API endpoints for missing authorization headers or tokens on sensitive operations
Test account takeover by modifying email/phone associated with merchant accounts
Look for similar patterns in other user management sections (reports, transactions, audit logs)
Test bulk operation endpoints for lack of permission validation
Check for API version endpoints (/api/v1/ vs /api/v2/) that might have weaker security

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (privilege escalation via account creation)
- T1531 - Account Access Removal (ability to disable/delete accounts)
- T1020 - Automated Exfiltration (potential for bulk data access)
- T1098 - Account Manipulation (modifying merchant account details)
- T1580 - Cloud Infrastructure Discovery (identifying sensitive endpoints)

## Notes
This is a classic case of 'security through obscurity' where developers assumed hiding UI controls was sufficient for access control. The writeup demonstrates scope creep - attacker initially focused on merchants but discovered the vulnerability affected all user classes. The ability to modify bank account numbers directly for payment redirection represents extremely high financial impact. The exposure of supervisor passcodes suggests additional poor credential management practices. The fact that basic CRUD operations on sensitive objects lack authorization is indicative of systemic architectural security failures rather than isolated bugs.

## Full report
<details><summary>Expand</summary>

## Summary:
The ███████ application provides access to 3(Merchant, Supervisor, Admin) classes of users. Looking at the Admin side, its clear only permitted admins can login to the portal since nothing on the UI indicates a register feature. However I was able to find a registration endpoint to sign up. Now I have access to the Admin dashboard. Based on the functionalities there, it's evident an outsider shouldn't have access to this.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Visit ████████ and signup
  2. Login at ██████ and you will be redirected to the admin dashboard where you can approve or decline transactions.
██████   
  3. At ███████, you can see a list of registered Merchant accounts in the application.    
███████  

  You can edit their data, 
`Change their account credentials`
`change their account number to an attacker's: thereby 
  receiving payments made to them`,  
`disable` or `delete` their account, etc.  
██████    
█████████

##!EDIT

Initially my report focused on the merchants, however it affects, Cashiers, Stations and Supervisors also. You can edit and delete their data also by navigating the the URLs below:  

███████
█████████
█████████   

#IMPORTANT
You can see the passcode for various supervisor accounts at
███   
█████████

## Impact

Direct access to admin functionalities, where an attacker can modify merchant financial account information, disable and delete account of MTN clients. An outsider like myself shouldn't have access to this.

</details>

---
*Analysed by Claude on 2026-05-24*
