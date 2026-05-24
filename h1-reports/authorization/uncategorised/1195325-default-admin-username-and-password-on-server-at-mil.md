# Default Admin Credentials on Department of Defense Server

## Metadata
- **Source:** HackerOne
- **Report:** 1195325 | https://hackerone.com/reports/1195325
- **Submitted:** 2021-05-13
- **Reporter:** the_boschko
- **Program:** Department of Defense Bug Bounty Program (HackerOne)
- **Bounty:** Not disclosed in writeup
- **Severity:** Critical
- **Vuln:** Use of Hard-coded Credentials, Weak Authentication, Insufficient Access Control, Default Credentials
- **CVEs:** None
- **Category:** uncategorised

## Summary
A publicly accessible Department of Defense web application was running with default administrator credentials for the default organization account, allowing any user to gain full administrative access without authentication. The vulnerability existed on a production server accessible via standard HTTP/HTTPS protocols with no additional security controls.

## Attack scenario
1. Attacker discovers the vulnerable DoD web application endpoint through reconnaissance or public disclosure
2. Attacker navigates to the login page at the identified URL
3. Attacker enters well-known default credentials (Administrator username and associated password)
4. Authentication succeeds, granting attacker full administrator privileges for the default organization
5. Attacker gains access to sensitive DoD systems, configurations, data, and administrative functions
6. Attacker can modify settings, extract data, create backdoor accounts, or escalate privileges further

## Root cause
The application was deployed to production with default credentials never changed from installation defaults. No forced password change policy, account lockout, or credential rotation was implemented during initial deployment.

## Attacker mindset
Low-effort, high-impact opportunistic attack. Attackers routinely test applications for default credentials as a basic reconnaissance technique. Default credentials provide immediate administrative access without exploitation complexity.

## Defensive takeaways
- Mandate credential changes from defaults as part of deployment checklist before any production environment access
- Implement forced password change policies on first login for all accounts
- Disable or remove default accounts entirely if not required
- Implement account lockout policies after failed login attempts
- Conduct pre-deployment security assessments including default credential scanning
- Enforce multi-factor authentication for all administrative accounts
- Regular security audits of production systems for unchanged default configurations
- Implement centralized credential management and avoid storing credentials in code or documentation

## Variant hunting
Search for other DoD subdomains with similar application patterns
Test other services on same host/network for default credentials
Check for related applications (staging, development, administrative portals) with similar configurations
Enumerate accounts on the compromised system for other default credentials
Test API endpoints for unauthenticated access or default token usage
Scan for backup configuration files or documentation containing default credentials
Check version control repositories for exposed default credentials

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1110 - Brute Force
- T1021 - Remote Services
- T1059 - Command and Scripting Interpreter

## Notes
This report involves a DoD military domain (.mil) representing a critical security failure. Default credentials represent CWE-521 (Weak Password Requirements) and CWE-798 (Use of Hard-coded Credentials). The vulnerability's severity is amplified by the government sector nature and potential access to classified or sensitive defense information. The redacted content suggests operational security was maintained in the public report. Prompt remediation was critical due to public disclosure vector.

## Full report
<details><summary>Expand</summary>

**Description:**
A ██████ Server is running at https://███mil you can access the login at https://████mil/█████████ the application is using the default "Administrator for the default organization" credentials 

#POC 
Go to  https://███mil/████████ and login with *█████*

██████████

████

████

## How to remediate the vulnerability

Change the password of the user or disable the account 

## References
█████
https://cwe.mitre.org/data/definitions/521.html


##EXTRA

If you have any questions or concerns regarding the above let me know!

Cheers,

## Impact

A Department of Defense website was misconfigured in a manner that may have allowed a malicious user to login with administrator for the default organization account credentials.

## System Host(s)
████mil

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Read the POC

## Suggested Mitigation/Remediation Actions
Change the password of the user or disable the account



</details>

---
*Analysed by Claude on 2026-05-24*
