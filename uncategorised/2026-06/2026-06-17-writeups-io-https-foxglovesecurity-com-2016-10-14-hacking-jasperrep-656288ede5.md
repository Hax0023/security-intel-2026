# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Arbitrary Code Execution, Unsafe Deserialization, Default Credentials, Template Injection
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates that can reference custom malicious Scriptlets (Java code) executed server-side. Combined with weak default credentials (jasperadmin/jasperadmin), this enables immediate remote code execution. The vulnerability demonstrates how report generation features can be weaponized when combined with administrative access.

## Attack scenario (step by step)
1. Attacker discovers JasperReports server exposed on internet
2. Attacker uses default credentials (jasperadmin/jasperadmin) to gain administrative access
3. Attacker creates or modifies a JRXML report template to reference a malicious Scriptlet class
4. Malicious Scriptlet contains arbitrary Java code (e.g., reverse shell payload)
5. Attacker uploads/saves the modified template through the JasperReports UI
6. When the report is executed/rendered, the Scriptlet code runs with application privileges, providing code execution

## Root cause
JasperReports intentionally allows custom Scriptlets (Java code) in report templates for flexibility in data manipulation, but fails to restrict Scriptlet functionality or validate template contents. The JRXML parsing and execution mechanism compiles and executes arbitrary Java code without sufficient sandboxing. Combined with default credentials remaining unchanged in deployments, this creates an exploitable code execution path.

## Attacker mindset
Penetration tester performing reconnaissance on internet-facing services. Recognizes that administrative interfaces typically lead to code execution. Understands that template-based systems often support dynamic code for flexibility, and exploits that design decision. Leverages well-known default credentials as the entry point to reach the dangerous functionality.

## Defensive takeaways
- Change default credentials immediately upon deployment and enforce strong authentication
- Disable or restrict Scriptlet functionality if not required; implement whitelist of allowed classes
- Sandbox Scriptlet execution with restricted permissions (no Runtime.exec, file access, network access)
- Implement code signing/validation for uploaded JRXML templates
- Apply principle of least privilege to JasperReports application user accounts
- Do not expose JasperReports administrative interfaces to untrusted networks
- Monitor and log report creation/modification and template uploads
- Consider using static report templates only, eliminating Scriptlet support entirely
- Implement template content inspection before execution (AST analysis, dangerous API detection)

## Variant hunting
['Look for other reporting engines with similar Scriptlet/expression features (Pentaho, BIRT, etc.)', 'Search for other JasperReports versions with different Scriptlet access mechanisms', 'Investigate if Scriptlets can be injected through other parameters (expressions, styles, conditional formatting)', 'Check if unauthenticated users can access any report rendering endpoints that execute Scriptlets', 'Look for XXE vulnerabilities in JRXML parsing that could lead to code execution', 'Examine if custom class loaders or datasources can be abused for code execution', 'Check if reports can include external JRXML files that could contain malicious Scriptlets']

## MITRE ATT&CK
- T1190
- T1199
- T1078
- T1059
- T1203

## Notes
This is a well-documented practical demonstration from 2016 showing how design flexibility for legitimate purposes becomes an attack surface. The vulnerability requires admin access, but default credentials make this trivial. The JRXML file format is XML-based and human-editable, allowing straightforward weaponization. This demonstrates the importance of secure-by-default configurations and restricting dangerous features at the architecture level rather than relying on runtime checks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
