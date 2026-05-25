# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** JasperReports (self-hosted/client application)
- **Bounty:** Unknown - appears to be from penetration test, not bug bounty program
- **Severity:** critical
- **Vuln types:** Arbitrary Code Execution, Unsafe Deserialization, Scriptlet Injection, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload custom JRXML report templates containing malicious Scriptlets (Java code) that execute during report generation. Combined with default credentials (jasperadmin:jasperadmin) left exposed, this provides trivial remote code execution. The vulnerability stems from insufficient input validation on user-defined report templates and the unsafe execution of arbitrary Java code via Scriptlets.

## Attack scenario (step by step)
1. Attacker discovers JasperReports administrative interface exposed on internet-facing server
2. Attacker uses default credentials (jasperadmin/jasperadmin) to authenticate to admin panel
3. Attacker creates or modifies an existing JRXML report template to include a malicious Scriptlet reference
4. Scriptlet class references custom Java code (e.g., foxglove.shell.ShellScriptlet) containing payload logic
5. Attacker uploads/saves the modified template through the JasperReports UI
6. When report is executed/rendered, the Scriptlet code executes with application privileges, returning reverse shell or executing arbitrary commands

## Root cause
JasperReports architecture allows JRXML templates to reference and execute arbitrary Scriptlets (Java classes) during report generation without proper sandboxing or code validation. No mechanism prevents users from embedding malicious code. Additionally, default credentials were never changed post-deployment.

## Attacker mindset
Reconnaissance-focused: attacker identified exposed JasperReports instance, tested obvious default credentials, then methodically explored legitimate features (report editing/uploading) to identify code execution pathway. Leveraged intended functionality rather than exploiting coding bugs—classic 'feature abuse' approach.

## Defensive takeaways
- Change all default credentials immediately on deployment; enforce strong password policies for administrative accounts
- Disable or restrict Scriptlet functionality entirely if not required for business processes
- Implement code signing/validation for JRXML templates; whitelist approved Scriptlet classes
- Restrict report template upload/edit permissions to minimal necessary users; implement approval workflows
- Run JasperReports in sandboxed environment with minimal privileges; restrict Java permissions via SecurityManager
- Do not expose administrative interfaces to internet; gate behind VPN, bastion hosts, or WAF
- Implement file upload validation: scan JRXML for suspicious Scriptlet references before processing
- Monitor and audit all report template modifications; alert on execution of custom Scriptlets
- Apply security patches promptly; JasperReports has had multiple RCE issues over time

## Variant hunting
Search for similar 'feature abuse' vulnerabilities in reporting tools: Pentaho, Cognos, MicroStrategy, Tableau Server. Look for: (1) template upload mechanisms that execute user code, (2) expression language injection in report definitions, (3) data source connection strings allowing code execution, (4) similar default credentials in enterprise reporting software. Test for scriptlet execution via expression injection (e.g., Groovy, JEXL expressions) in report filters/parameters.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (default credentials)
- T1059 - Command and Scripting Interpreter (Java)
- T1203 - Exploitation for Client Execution
- T1105 - Ingress Tool Transfer (reverse shell)
- T1133 - External Remote Services

## Notes
This is a 2016 publication; JasperReports has evolved but similar issues persist. The vulnerability chain is simple but devastating: default credentials + feature abuse = unauthenticated RCE. No CVE assigned in writeup but likely corresponds to known JasperReports RCE vulnerabilities. Attack requires only basic Java knowledge to craft malicious class; no advanced exploitation needed. The 'hidden' aspect refers to Scriptlets being a documented but underutilized feature that many administrators overlook during security reviews.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
