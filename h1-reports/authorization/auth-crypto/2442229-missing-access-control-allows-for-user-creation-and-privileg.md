# Missing Access Control Allows Unauthenticated User Creation and Administrator Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 2442229 | https://hackerone.com/reports/2442229
- **Submitted:** 2024-03-31
- **Reporter:** bulldawg
- **Program:** RSI Test Environment (Oracle APEX Application)
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Missing Access Control, Broken Authentication, Privilege Escalation, Unauthorized Administrative Access
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An unauthenticated user can access the user management endpoint (page 842:9) without any access controls, allowing creation of arbitrary user accounts and assignment of administrator privileges. This enables complete unauthorized administrative access to the application and unrestricted access to sensitive USG data.

## Attack scenario
1. Attacker discovers the user management endpoint URL at /ords/f?p=842:9 through enumeration or documentation
2. Attacker navigates to the endpoint without authentication and finds the 'Add New User' form is accessible
3. Attacker creates a new user account by entering email, first name, last name, and agency information
4. Attacker assigns the administrator role to the newly created user through the role assignment interface
5. Attacker receives credentials sent to the email address and logs into the main application at /ords/f?p=303
6. Attacker gains full administrative access and can view, modify, delete sensitive data, and manage other users

## Root cause
The application fails to implement authentication and authorization checks on the user management page (APEX page 842, page 9). The endpoint is directly accessible without verifying user identity or role-based permissions, allowing any unauthenticated actor to perform administrative functions.

## Attacker mindset
An attacker would recognize this as a trivial privilege escalation path requiring minimal sophistication. The direct exposure of administrative functionality without authentication suggests either development/test environment misconfiguration or fundamental security architecture failures. An attacker could exploit this to establish persistent administrative access, exfiltrate sensitive USG data, or sabotage system integrity.

## Defensive takeaways
- Implement mandatory authentication checks on all application endpoints, especially administrative functions
- Apply role-based access control (RBAC) to enforce that only authenticated administrators can access user management features
- Validate that APEX page security settings (Authorization Schemes) are properly configured and enforced
- Segregate test/development environments from production and ensure they are not internet-accessible
- Conduct security review of all administrative endpoints and ensure consistent access control implementation
- Implement audit logging for user creation and role assignment operations
- Use Web Application Firewall (WAF) rules to restrict access to known administrative pages
- Perform regular access control testing as part of security testing lifecycle

## Variant hunting
Search for similar patterns in Oracle APEX applications: other unprotected pages handling sensitive operations (data export, system configuration, account management), ORDS endpoints without authentication, authorization scheme bypasses in APEX, direct parameter manipulation on privileged pages, and other applications using the same infrastructure potentially sharing the vulnerability.

## MITRE ATT&CK
- T1190
- T1078
- T1078.001
- T1548
- T1199

## Notes
This is a critical finding in a government-facing application (USG authorization required per disclaimer). The vulnerability is trivial to exploit and requires no technical sophistication. The presence of email-based credential delivery suggests the attacker can use any accessible email address to establish access. The application appears to be an Oracle APEX (ORDS) application, making it likely that similar access control issues may exist on other pages. The masking of URLs in the report suggests sensitive infrastructure details.

## Full report
<details><summary>Expand</summary>

Hello,

The RSI Test Environment application at https://███████████████/ords/f?p=842:1 does not enforce access controls on the user management endpoint. This allows any unauthenticated person to both create new users as well as give them the administrator role. This then provides access to https://███████████████/ords/f?p=303 as an administrator.

The user management endpoint can be accessed at https://████████████/ords/f?p=842:9:::::: 

I have attached screenshots which show this misconfiguration.

If there are any questions or concerns please let me know as I am more than happy to provide additional information!

## Impact

This is a critical security issue which poses risk to the confidentiality and integrity of data within the ███████████████ application. An attacker would be able to view, modify, and/or delete the restricted information and documents within the application as well as manage other user accounts. This provides unauthorized access that is otherwise restricted to USG-authorized individuals per the disclaimer.

## System Host(s)
█████████████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Visit https://█████████████████/ords/f?p=842:9, which is the user management endpoint for the environment.
2. Under "Add New User", enter an email address, first name, last name, and select an Agency.
3. Under "Assign User Roles", select the newly created user and apply the administrator role.
4. Retrieve the credentials for the new account that were sent to the email address entered.
5. Go to https://███████████/ords/f?p=303 and login using the credentials.
6. Change to a new password on prompt.
7. View the logged in username in the top right with the Administrator role.

## Suggested Mitigation/Remediation Actions
Enforce access controls on page 9 of the application with an ID of 842.



</details>

---
*Analysed by Claude on 2026-05-24*
