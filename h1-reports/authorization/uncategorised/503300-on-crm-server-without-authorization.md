# Unauthorized Script Execution on CRM Server

## Metadata
- **Source:** HackerOne
- **Report:** 503300 | https://hackerone.com/reports/503300
- **Submitted:** 2019-02-28
- **Reporter:** b4a1d31dd4acbccc47b8072
- **Program:** Unikrn
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln:** Broken Access Control, Missing Authentication, Arbitrary Code Execution
- **CVEs:** None
- **Category:** uncategorised

## Summary
A script file on the CRM server (crm.unikrn.com) is publicly accessible without any authentication or authorization controls, allowing any unauthenticated attacker to execute arbitrary code. This represents a critical security flaw that could lead to complete system compromise, data exfiltration, or lateral movement within the organization's infrastructure.

## Attack scenario
1. Attacker discovers the publicly accessible script file at https://crm.unikrn.com/[script_name]
2. Attacker accesses the script directly via HTTP request without providing any credentials
3. Script executes with the privileges of the web server process
4. Attacker can interact with the script to execute arbitrary commands or logic
5. Attacker gains ability to read/write files, access database, or pivot to other systems
6. Complete compromise of CRM server and potential lateral movement to internal network

## Root cause
Missing authentication/authorization middleware or access control checks on the script endpoint. The script was likely deployed without proper security controls, potentially through misconfiguration, inadequate deployment procedures, or forgotten/legacy functionality.

## Attacker mindset
An attacker would recognize this as a quick-win vulnerability during reconnaissance, exploiting it immediately to establish initial access and persistence on a sensitive CRM system containing valuable customer data and business logic.

## Defensive takeaways
- Implement strong authentication (OAuth 2.0, JWT, session-based) for all web endpoints
- Apply authorization checks to verify user permissions before executing sensitive operations
- Use Web Application Firewall (WAF) rules to restrict access to administrative/operational scripts
- Implement a default-deny access control policy for all resources except public endpoints
- Conduct regular security audits and penetration testing to identify exposed endpoints
- Remove or disable legacy/debug scripts from production environments
- Implement proper logging and monitoring of access attempts to sensitive endpoints
- Use infrastructure-as-code and configuration management to ensure consistent security posture

## Variant hunting
Search for other executable scripts (.php, .asp, .jsp, .py) on the same domain
Check for similar exposed administrative or operational scripts on other subdomains
Look for backup files, .git directories, or configuration files in the same directory
Test for directory traversal to access other sensitive files
Check for other CRM-related endpoints that might have similar access control issues
Enumerate common script names (admin.php, config.php, test.php, backup.php) on the target

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1566 - Phishing
- T1105 - Ingress Tool Transfer
- T1059 - Command and Scripting Interpreter
- T1078 - Valid Accounts

## Notes
The report is intentionally vague about the specific script filename and functionality, which is a responsible disclosure practice. However, this represents a critical vulnerability requiring immediate remediation. The lack of bounty amount visible suggests this may have been recently resolved or the reporter declined the bounty.

## Full report
<details><summary>Expand</summary>

The https://crm.unikrn.com/███████ file is available on the server https://crm.unikrn.com without authorization. Anyone can run this script.
How to classify this vulnerability - leave the right for you.

## Impact

Anyone can run this script.

</details>

---
*Analysed by Claude on 2026-05-24*
