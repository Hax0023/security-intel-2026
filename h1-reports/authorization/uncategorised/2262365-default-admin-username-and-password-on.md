# Default Admin Credentials Exposed on DoD Geoportal Application

## Metadata
- **Source:** HackerOne
- **Report:** 2262365 | https://hackerone.com/reports/2262365
- **Submitted:** 2023-11-23
- **Reporter:** maskedpersian
- **Program:** Department of Defense
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln:** Use of Hard-coded Credentials, Insufficient Access Control, Weak Authentication, Default Credentials
- **CVEs:** None
- **Category:** uncategorised

## Summary
A Department of Defense geoportal application was accessible using default administrator credentials (admin/admin and admin/gptadmin), allowing unauthorized administrative access. An attacker with these credentials could modify website content, delete posts, and perform other administrative functions.

## Attack scenario
1. Attacker discovers the geoportal URL at https://███/geoportal/
2. Attacker attempts common default credentials starting with 'admin'
3. Attacker successfully authenticates using admin/admin credentials
4. Attacker gains full administrator access to the application
5. Attacker exploits administrative privileges to delete posts and modify website content
6. Attacker causes data loss and reputational damage to the DoD organization

## Root cause
Application deployed with default credentials unchanged from installation. No forced credential rotation or enforcement of strong passwords during initial setup. Lack of secure-by-default configuration practices.

## Attacker mindset
Low-effort reconnaissance and exploitation. Attacker performs basic enumeration of common paths (/geoportal/) and tests well-known default credentials. Once authenticated, attacker leverages administrative privileges for maximum impact without needing sophisticated techniques.

## Defensive takeaways
- Force mandatory password change on first login for all default accounts
- Implement account lockout policies after failed authentication attempts
- Disable or rename default administrative accounts entirely
- Conduct security configuration reviews before production deployment
- Implement monitoring and alerting for default credential usage attempts
- Require multi-factor authentication for administrative accounts
- Regular security scanning for exposed default credentials
- Include credential management in deployment checklists with mandatory verification

## Variant hunting
Check for other default credentials (gptadmin/gptadmin, admin/admin123, admin/password)
Scan other URLs on same domain for similar patterns (/admin/, /portal/, /dashboard/)
Test for weak password policies allowing simple credentials
Review other DoD or government contractor applications for same pattern
Check version-specific default credentials for identified geoportal software
Attempt credential stuffing with common DoD naming conventions
Look for exposed credentials in git repositories or configuration files

## MITRE ATT&CK
- T1190
- T1589
- T1199
- T1078
- T1592

## Notes
This is a critical infrastructure vulnerability affecting U.S. Department of Defense systems. The ease of exploitation combined with high-impact consequences (administrative access to DoD systems) makes this extremely severe. The fact that this was deployed in production on a government system represents a significant security governance failure. Video proof-of-concept was provided to validate the vulnerability.

## Full report
<details><summary>Expand</summary>

It is possible to access the application is using the default username and password 
Steps To Reproduce:
1-Go to https://███/geoportal/ and login with credentials:
user and password: admin
user and password: gptadmin
Poc video attached

## Impact

A Department of Defense website was misconfigured in a manner that may have allowed a malicious user to login with administrator for the default organization account credentials and delete posts , edit website

## System Host(s)
███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
POC video

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
