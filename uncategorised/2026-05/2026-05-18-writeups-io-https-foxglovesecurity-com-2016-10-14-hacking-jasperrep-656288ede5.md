# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Arbitrary Code Execution, Unsafe Deserialization, Insecure Template Processing, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload malicious JRXML report templates containing custom Scriptlets that execute arbitrary Java code during report generation. Combined with default credentials (jasperadmin:jasperadmin), this enables unauthenticated remote code execution on internet-facing JasperReports instances. The vulnerability stems from the framework's design allowing arbitrary Java code execution through Scriptlet references in report templates.

## Attack scenario (step by step)
1. Attacker discovers internet-facing JasperReports instance through network reconnaissance
2. Attacker authenticates using default credentials (jasperadmin:jasperadmin)
3. Attacker creates or modifies a report template (JRXML file) to include reference to a malicious custom Scriptlet class
4. Attacker uploads the modified JRXML template through the JasperReports administrative interface
5. Attacker triggers report generation/execution, causing JasperReports to instantiate and execute the malicious Scriptlet
6. Malicious Scriptlet code executes with application privileges, delivering reverse shell or executing arbitrary commands

## Root cause
JasperReports design flaw allowing arbitrary Java code execution through custom Scriptlet classes referenced in JRXML templates. The framework does not adequately restrict or sandbox code execution, treating Scriptlet references as trusted components. Combined with weak default credentials and no rate limiting on authentication attempts.

## Attacker mindset
Penetration tester identifying that administrative interfaces typically lead to code execution. Recognition that report templating systems often support scripting/code execution features. Methodical approach: default credentials → upload malicious template → execute arbitrary code.

## Defensive takeaways
- Change default credentials immediately upon installation
- Disable or restrict administrative interfaces from internet-facing access
- Implement strict input validation and sandboxing for uploaded report templates
- Disable Scriptlet functionality if not required, or restrict to whitelisted classes
- Apply principle of least privilege to JasperReports service account
- Monitor and log all report template uploads and modifications
- Implement code signing or cryptographic verification for report templates
- Use Web Application Firewall (WAF) rules to detect suspicious JRXML uploads
- Restrict Java class loading to prevent instantiation of arbitrary classes
- Apply security patches and use hardened configurations

## Variant hunting
Search for other reporting engines with Scriptlet/macro support (Apache Velocity, Freemarker, Groovy templates). Investigate other Jaspersoft products (JasperServer, Jaspersoft Studio) for similar template injection vectors. Look for XXE vulnerabilities in JRXML XML parsing. Hunt for other Java applications allowing user-supplied templates with code execution capabilities.

## MITRE ATT&CK
- T1190
- T1059
- T1059.003
- T1570
- T1598
- T1078
- T1078.001
- T1105
- T1053

## Notes
This is a 2016 vulnerability disclosure that demonstrates a common pattern in report generation tools. JasperReports version 6.0.0 confirmed vulnerable. The vulnerability requires either default credentials or valid user account with report creation permissions. The writeup is educational and demonstrates practical exploitation methodology. Similar vulnerabilities have been identified in other Jaspersoft products.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
