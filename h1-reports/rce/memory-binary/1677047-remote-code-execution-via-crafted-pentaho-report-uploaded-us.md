# Remote Code Execution via Malicious Pentaho Report Upload with Default Credentials

## Metadata
- **Source:** HackerOne
- **Report:** 1677047 | https://hackerone.com/reports/1677047
- **Submitted:** 2022-08-22
- **Reporter:** zer0code
- **Program:** MTN Cameroon (mtn.ci)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Remote Code Execution (RCE), Authentication Bypass, Insecure Deserialization, Arbitrary File Upload
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical RCE vulnerability exists in Pentaho Business Server accessible at sm.mtn.ci:8888/pentaho due to unchanged default credentials (admin/password). An unauthenticated attacker can login and upload malicious PRPT report files containing BeanShell, JavaScript, or Java code that executes with server privileges during report rendering.

## Attack scenario
1. Attacker performs reconnaissance and discovers Pentaho Business Server instance at sm.mtn.ci:8888/pentaho
2. Attacker accesses login portal and authenticates using default credentials admin/password
3. Attacker uses Pentaho Report Designer to craft a malicious .prpt file embedding BeanShell, JavaScript, or Java code
4. Attacker uploads the malicious PRPT file to the server through the report management interface
5. Attacker triggers report execution/rendering through the web UI or by scheduling the report
6. Malicious code within the report executes with server privileges, allowing full system compromise

## Root cause
Multiple security failures: (1) Default credentials never changed in production, (2) Pentaho Report Designer allows arbitrary code execution via BeanShell/Java expressions in reports, (3) No input validation or sandboxing of uploaded report files, (4) Report execution engine processes untrusted code without restrictions

## Attacker mindset
Reconnaissance-focused attacker systematically testing common services for default credentials. Once low-hanging fruit (defaults) accessed, chained with application-specific code execution vectors (PRPT report design capabilities) to achieve RCE. Likely seeking initial access for lateral movement or data exfiltration.

## Defensive takeaways
- Enforce strong unique credentials on all services during deployment; disable or remove default accounts entirely
- Implement code execution restrictions in report designers using sandboxing, allowlists, or disabling dangerous expression languages (BeanShell)
- Validate, sanitize, and scan uploaded files for malicious content before storing/executing
- Apply principle of least privilege to report execution contexts (dedicated unprivileged service accounts)
- Implement Web Application Firewall (WAF) rules to detect/block report file uploads with suspicious payloads
- Conduct regular security audits of development/reporting tools for code injection vectors
- Enforce MFA for administrative console access
- Monitor report execution logs for suspicious activity and uncommon expressions

## Variant hunting
Test other Pentaho installations for similar default credential exposure
Check if other report formats (PDF, XLSX, etc.) support code execution via formulas or expressions
Investigate if scheduled report execution bypasses additional security controls
Hunt for other services using default credentials in same environment (Tomcat, database backends)
Test if file upload restrictions can be bypassed via MIME type manipulation or polyglot files
Examine if report parameters are injectable with code payloads
Check for similar RCE in other Pentaho components (Kettle ETL, metadata repositories)

## MITRE ATT&CK
- T1190
- T1566.002
- T1595.002
- T1078.001
- T1190
- T1059.005

## Notes
This vulnerability demonstrates the dangerous combination of weak authentication with application-level code execution capabilities. Pentaho's reporting engine treating expressions as executable code without sandboxing is the core architectural issue. The exposure was easily discoverable via default credential testing, suggesting this was likely a prototype/test instance exposed to internet with minimal security hardening.

## Full report
<details><summary>Expand</summary>

## Summary:
Good day,
                      While I do recon for mtn.ci domain I found  Pentaho business server at https://sm.mtn.ci:8888/pentaho with default credentials admin/password ,then I figured that I can upload  prpt reports to server which could use some beanshell,js and java to achieve RCE

## Steps To Reproduce:
1. Login to https://sm.mtn.ci:8888/pentaho admin/password  
{F1878259}
2. Use Pentaho report designer to create malicious report file  
{F1878260}
3. Upload and run the report   
{F1878261}  
{F1878262}

## Impact

The impact of an RCE vulnerability can range from malware execution to an attacker gaining full control over a compromised server.

</details>

---
*Analysed by Claude on 2026-05-11*
