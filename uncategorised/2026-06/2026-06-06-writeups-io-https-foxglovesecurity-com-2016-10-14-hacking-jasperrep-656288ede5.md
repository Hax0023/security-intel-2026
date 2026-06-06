# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Insecure Deserialization, Unsafe Template Processing
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload malicious JRXML report templates that reference custom Scriptlets containing arbitrary Java code. When the report is compiled and executed by the server, the malicious Scriptlet code runs with the privileges of the JasperReports application, enabling remote code execution. This vulnerability is particularly severe when combined with default credentials (jasperadmin/jasperadmin).

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet
2. Attacker uses default credentials (jasperadmin/jasperadmin) to authenticate as administrator
3. Attacker creates or modifies a JRXML report template to include a malicious Scriptlet class reference
4. Attacker uploads the modified template through the report creation/editing interface
5. JasperReports server compiles and executes the report, instantiating the malicious Scriptlet
6. Malicious Scriptlet code executes on the server with application privileges, establishing reverse shell or executing arbitrary commands

## Root cause
JasperReports allows report templates to reference and execute custom Java Scriptlets without proper validation or sandboxing. The application design prioritizes flexibility for data manipulation over security, permitting arbitrary code execution through template upload functionality. No restrictions are placed on the Java code that can be executed within Scriptlets.

## Attacker mindset
Penetration tester identifying a readily exploitable administrative interface that converts flexible design features into code execution primitives. The attacker recognizes that reporting systems often expose dangerous capabilities and leverages the combination of weak/default authentication with unsafe template processing to achieve system compromise.

## Defensive takeaways
- Never expose administrative interfaces to the internet; require VPN or bastion host access
- Change all default credentials immediately upon deployment
- Implement code sandboxing or restrict Scriptlet functionality to pre-approved, vetted code only
- Disable or remove the Scriptlet feature if not actively required
- Validate and sanitize all uploaded report templates before compilation
- Implement strict access controls limiting report creation/editing to trusted users
- Run JasperReports with minimal required privileges (principle of least privilege)
- Monitor and audit report template modifications and executions
- Implement application-level code signing for allowed Scriptlets
- Use Web Application Firewalls to detect suspicious report uploads

## Variant hunting
['Check for similar template injection vulnerabilities in other reporting engines (SSRS, Pentaho, SAP Crystal)', 'Investigate whether query fields or parameters in templates allow expression language injection', 'Test if reports can reference external Scriptlet classes from network locations or classloaders', 'Examine if compiled .jasper files can be directly uploaded and executed, bypassing JRXML parsing', 'Look for XXE vulnerabilities in JRXML XML parsing', 'Check if Scriptlet code can access restricted Java classes through reflection', 'Test report scheduling/batch processing for unauthenticated RCE']

## MITRE ATT&CK
- T1190
- T1568
- T1059
- T1046
- T1133
- T1078
- T1105

## Notes
This writeup demonstrates a critical vulnerability chain combining weak authentication (default credentials) with unsafe code execution capabilities. The flexibility of JasperReports' Scriptlet feature, designed for legitimate reporting customization, becomes a weaponized RCE vector. The vulnerability is particularly impactful due to the prevalence of default credentials left unchanged in production deployments and the triviality of exploitation once authenticated. Published in 2016, similar patterns have been identified in multiple JasperReports versions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
