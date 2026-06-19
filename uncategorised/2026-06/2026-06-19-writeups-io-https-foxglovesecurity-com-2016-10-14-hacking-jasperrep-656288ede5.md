# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Arbitrary Code Execution, Remote Code Execution (RCE), Unsafe Deserialization, Weak Default Credentials, Unsafe Template Processing
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates containing malicious Scriptlets, which are arbitrary Java code executed server-side during report generation. Default credentials (jasperadmin/jasperadmin) combined with this Scriptlet feature enable unauthenticated remote code execution. This vulnerability transforms JasperReports into an easily exploitable command execution platform when exposed to the internet.

## Attack scenario (step by step)
1. Attacker discovers internet-facing JasperReports server
2. Attacker attempts default credentials (jasperadmin/jasperadmin) and gains administrative access
3. Attacker creates or edits an JRXML report template to include a custom Scriptlet class reference (e.g., foxglove.shell.ShellScriptlet)
4. Attacker uploads the malicious JRXML template through the administrative interface
5. Attacker triggers report generation, causing JasperReports to instantiate and execute the Scriptlet class
6. Attacker achieves arbitrary code execution with JasperReports process privileges and receives reverse shell

## Root cause
JasperReports design allows JRXML templates to reference arbitrary Scriptlet classes that are compiled and executed as Java code. The application does not adequately restrict which classes can be instantiated or validate Scriptlet sources. Combined with default credentials and no built-in rate limiting, this creates a trivial exploitation path.

## Attacker mindset
Identify high-value targets with small attack surfaces (e.g., administrative interfaces). Recognize that flexible data manipulation features in business tools often introduce code execution risks. Leverage default credentials as entry points and weaponize template/configuration upload features to achieve RCE. This represents 'easy wins' for penetration testers.

## Defensive takeaways
- Force immediate password changes from default credentials on all accounts, especially administrative ones
- Implement strong access controls and never expose administrative interfaces to the internet without VPN/bastion host protection
- Disable or restrict Scriptlet functionality in JRXML templates; implement allowlists for permitted Scriptlet classes if customization is required
- Sandbox JasperReports execution environments with least privilege and restrict network access
- Implement strict input validation and template sanitization to prevent malicious Scriptlet references
- Deploy Web Application Firewalls (WAF) to detect suspicious JRXML uploads
- Monitor for suspicious template uploads and Scriptlet instantiations in application logs
- Regularly audit and version control all report templates

## Variant hunting
Look for similar vulnerabilities in other reporting engines (BIRT, Pentaho, Cognos) that support custom code execution. Investigate similar default credential issues in other Jaspersoft products. Hunt for template injection vulnerabilities in any system accepting user-defined data transformation logic. Check for XML External Entity (XXE) vulnerabilities in JRXML parsing.

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1105
- T1570

## Notes
This vulnerability exemplifies why administrative interfaces should never be internet-facing and why flexible code execution features in data processing tools require extreme caution. The 2016 publication date suggests this was a known issue, yet deployment patterns indicate continued real-world exposure. JasperReports versions allowing Scriptlet execution in uploaded templates are vulnerable; patching and architectural changes (disabling Scriptlets) are necessary.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
