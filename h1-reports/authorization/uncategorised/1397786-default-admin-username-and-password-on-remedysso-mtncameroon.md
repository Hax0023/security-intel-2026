# Default Admin Credentials on Remedy SSO Server

## Metadata
- **Source:** HackerOne
- **Report:** 1397786 | https://hackerone.com/reports/1397786
- **Submitted:** 2021-11-10
- **Reporter:** dh0pe
- **Program:** MNT Group / Cameroon
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Use of Hard-coded Credentials, Weak Authentication, Default Credentials, Improper Access Control
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Remedy Single Sign-On (SSO) server at remedysso.mtncameroon.net was left with default administrative credentials (Admin/RSSO#Admin#), allowing unauthenticated access to the SSO administration panel. An attacker could leverage this access to modify SSO configurations, impersonate users, and exfiltrate sensitive organizational and user data.

## Attack scenario
1. Attacker discovers the remedysso.mtncameroon.net domain via reconnaissance or public scanning
2. Attacker navigates to the admin portal at /rsso/admin/#/
3. Attacker attempts login with default credentials (Admin/RSSO#Admin#)
4. Attacker gains administrative access to the SSO system
5. Attacker modifies SSO configurations, creates backdoor admin accounts, or extracts user credentials and organizational infrastructure details
6. Attacker uses SSO access to compromise downstream applications and user accounts

## Root cause
The Remedy SSO application was deployed to production without changing default administrative credentials from the installation/factory settings. This represents a failure in the deployment hardening process and lack of configuration management controls.

## Attacker mindset
An opportunistic attacker could exploit this misconfiguration to gain a foothold into the organization's identity infrastructure. SSO systems are highly valuable targets as they provide centralized authentication and authorization across multiple applications, making them ideal pivots for lateral movement and privilege escalation.

## Defensive takeaways
- Enforce mandatory password changes for all default accounts during initial deployment
- Implement deployment checklists that require verification of credential changes before production promotion
- Use secrets management systems to generate and rotate strong credentials during provisioning
- Conduct security hardening reviews of all identity and authentication systems
- Implement continuous monitoring and alerting for default credential usage
- Restrict administrative interface access via network segmentation and IP whitelisting
- Enable multi-factor authentication for SSO administrative accounts
- Audit and alert on privileged actions within the SSO system
- Implement automated scanning to detect services running with default credentials

## Variant hunting
Check for other Remedy SSO instances within the organization and verify credential changes
Scan for other SSO/identity management systems (OKTA, Ping, Azure AD) with default credentials
Review deployment procedures for other critical infrastructure components (databases, VPNs, firewalls)
Examine backup systems and disaster recovery instances for similar misconfigurations
Test other common default credentials for the Remedy SSO application

## MITRE ATT&CK
- T1078.001
- T1080
- T1190
- T1556
- T1110.001

## Notes
This is a textbook example of a critical misconfiguration vulnerability. The severity is maximum because SSO systems are security-critical infrastructure that protect organizational identity and access. Default credentials are among the easiest vulnerabilities to exploit and prevent, yet they remain common in real-world deployments. The 'RSSO#Admin#' default password suggests this is a known credential from Remedy's installation documentation, making it trivially exploitable.

## Full report
<details><summary>Expand</summary>

## Summary:
A Remedy Single Sign-On (Remedy SSO) Server is running at https://remedysso.mtncameroon.net/rsso/admin/#/.  
It is possible to access the application is using the default Administrator credentials.

## Steps To Reproduce:
Go to https://remedysso.mtncameroon.net/rsso/admin/#/ and login with credentials:
- Username: Admin
- Password: RSSO#Admin#

## Remediation
Change the password of the Admin user or disable the account.

## References
https://cwe.mitre.org/data/definitions/521.html

## Impact

A MNT Group Single Sign-On application was misconfigured in a manner that may have allowed a malicious user to login with the administrator user. The user is capable to perform any kind of configuration of the SSO system and retrieve sensitive information about organization users and infrastructure.

</details>

---
*Analysed by Claude on 2026-05-24*
