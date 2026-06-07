# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** JasperReports (various implementations)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Arbitrary Code Execution, Unsafe Deserialization, Authentication Bypass, Insecure Default Credentials
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated administrators to upload JRXML report templates containing malicious Scriptlets that execute arbitrary Java code. Combined with default credentials (jasperadmin:jasperadmin), this provides direct remote code execution on the server. The vulnerability stems from the framework's design allowing custom Java code execution within report templates.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet via port scanning or enumeration
2. Attacker attempts default credentials (jasperadmin:jasperadmin) and successfully authenticates to administrative interface
3. Attacker creates or edits a report template (JRXML file) to include a malicious Scriptlet class reference
4. Attacker uploads the modified JRXML template through the report creation/editing functionality
5. When the report is executed, JasperReports compiles and instantiates the Scriptlet class, executing arbitrary Java code
6. Attacker achieves remote code execution with application server privileges and establishes reverse shell or persistence mechanism

## Root cause
JasperReports architects designed the framework to allow custom Java Scriptlets for flexible data manipulation within reports. This feature, combined with no validation of Scriptlet class references and default credentials being widely known, creates an exploitable attack surface. The framework trusts authenticated users completely and does not sandbox or restrict code execution.

## Attacker mindset
Attackers recognize that administrative interfaces frequently lead to code execution. They leverage known default credentials and the framework's legitimate flexibility features (Scriptlets) as an unintended attack vector. The attacker understands Java compilation and report template structure, demonstrating intermediate technical sophistication.

## Defensive takeaways
- Never rely on default credentials; immediately change all default administrative accounts and enforce strong passwords
- Restrict network exposure of administrative interfaces; segregate report management systems behind VPNs or internal networks only
- Implement code review and validation for report templates before deployment; sanitize or sandbox Scriptlet references
- Apply principle of least privilege; limit which users can create/edit reports and define what code can be executed
- Monitor and log report template uploads and modifications for suspicious activity
- Keep JasperReports patched to the latest version; check vendor security advisories regularly
- Consider disabling Scriptlet functionality entirely if not required for business operations
- Implement file integrity monitoring on JRXML files in production environments

## Variant hunting
['Check for other template-injection vulnerabilities in similar reporting tools (Pentaho, BIRT, Stimulsoft)', 'Investigate if other Jasper products (JasperServer, JasperStudio) have similar issues with deserializing untrusted data', 'Look for bypass techniques around any Scriptlet restrictions or whitelists that may have been implemented', 'Test whether unauthenticated users can upload templates or if lower-privilege users can inject code', 'Examine if report parameters can be manipulated to inject malicious Scriptlet class names', 'Research Expression Language (EL) injection vectors in JRXML expressions themselves as alternative RCE method']

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1203
- T1105

## Notes
This vulnerability chain is particularly dangerous because it combines ease of exploitation (default credentials) with maximum impact (code execution). The post demonstrates practical exploitation and weaponization. Published in 2016, this highlights how long administrative interface defaults can persist in enterprise software. The vulnerability exemplifies how legitimate flexibility features become security liabilities when access controls are weak.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
