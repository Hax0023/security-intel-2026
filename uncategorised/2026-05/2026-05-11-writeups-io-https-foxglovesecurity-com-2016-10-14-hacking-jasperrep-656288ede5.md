# Hacking JasperReports - The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln types:** Remote Code Execution (RCE), Arbitrary Code Execution, Scriptlet Injection, Default Credentials, Insecure Deserialization
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload custom JRXML report templates containing malicious Java Scriptlets that execute arbitrary code on the server. Combined with default credentials (jasperadmin/jasperadmin), this vulnerability enables unauthenticated remote code execution and full system compromise.

## Attack scenario (step by step)
1. Attacker discovers JasperReports server exposed on the internet
2. Attacker attempts default credentials jasperadmin:jasperadmin and gains administrative access
3. Attacker creates or modifies a JRXML report template to include a custom Scriptlet reference
4. Attacker embeds malicious Java code in the Scriptlet class (e.g., reverse shell payload)
5. Attacker uploads the modified template and triggers report generation
6. JasperReports compiles and executes the Scriptlet code with application privileges, granting attacker shell access

## Root cause
JasperReports allows arbitrary Java code execution through Scriptlets without proper validation. The application trusts uploaded JRXML templates and executes referenced Scriptlet classes. Combined with weak default credentials and no access controls, this creates a direct path to RCE.

## Attacker mindset
Penetration tester or adversary identifying internet-exposed administrative interfaces, testing default credentials as a primary access vector, then leveraging application features designed for extensibility (Scriptlets) to achieve code execution.

## Defensive takeaways
- Enforce strong, non-default credentials on all administrative accounts and disable default accounts entirely
- Implement strict code review and sandboxing for dynamically loaded code or templates
- Restrict JRXML template uploads to trusted sources and implement code signing/verification
- Disable Scriptlet functionality if not required; use safer alternatives for data manipulation
- Apply principle of least privilege - run JasperReports with minimal required permissions
- Implement network segmentation to prevent internet-facing exposure of administrative interfaces
- Monitor and audit template uploads and report execution activities
- Apply all security patches and keep JasperReports updated

## Variant hunting
['Check for other data processing tools (Pentaho, BIRT, etc.) with similar template injection issues', 'Investigate whether other report fields or expressions allow code injection beyond Scriptlets', 'Test if unauthenticated users can access report creation/editing functionality', 'Examine datasource configurations for JNDI injection or expression language injection vulnerabilities', 'Search for other default credential combinations across JasperReports versions', 'Test XML External Entity (XXE) injection in JRXML file uploads']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1078 - Valid Accounts
- T1059 - Command and Scripting Interpreter
- T1651 - Defense Evasion
- T1053 - Scheduled Task/Job
- T1218 - System Binary Proxy Execution

## Notes
This vulnerability chain combines multiple weaknesses: (1) default credentials, (2) internet exposure, (3) unsafe dynamic code execution via Scriptlets. The flexibility of JasperReports for report customization becomes a critical vulnerability when combined with weak authentication. The attack requires only knowledge of default credentials and basic understanding of JRXML structure, making it a high-risk 'easy win' for attackers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
