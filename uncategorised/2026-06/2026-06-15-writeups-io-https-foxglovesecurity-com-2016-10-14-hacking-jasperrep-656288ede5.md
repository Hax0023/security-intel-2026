# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Authentication Bypass, Unsafe Deserialization, Template Injection
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload malicious JRXML report templates containing custom Java Scriptlets that execute arbitrary code on the server. Combined with default credentials (jasperadmin/jasperadmin), this provides trivial remote code execution to unauthenticated attackers.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet
2. Attacker logs in using default credentials jasperadmin/jasperadmin
3. Attacker creates or modifies an existing JRXML report template
4. Attacker inserts a malicious Scriptlet class reference pointing to custom Java code
5. Attacker uploads the template and triggers report generation
6. Malicious Scriptlet executes with server privileges, providing reverse shell or code execution

## Root cause
JasperReports design allows arbitrary Java code execution through Scriptlets for data manipulation flexibility. The application fails to validate Scriptlet class references or restrict their capabilities. Combined with default credentials left unchanged, this creates an unauthenticated RCE pathway.

## Attacker mindset
The attacker recognized that administrative interfaces typically lead to code execution and systematically exploited JasperReports' template feature. They leveraged the flexibility mechanism (Scriptlets) intended for legitimate use to inject malicious Java code, understanding that report generation would execute their payload.

## Defensive takeaways
- Change all default credentials immediately upon installation
- Disable or restrict Scriptlet functionality if not required
- Implement strict code review and validation for uploaded JRXML templates
- Use Java sandboxing or SecurityManager to restrict Scriptlet capabilities
- Apply principle of least privilege to service accounts running JasperReports
- Implement network segmentation to restrict internet exposure of administrative interfaces
- Enable audit logging for template uploads and modifications
- Keep JasperReports patched and updated
- Use allowlists for permitted Scriptlet classes if custom code is required

## Variant hunting
Hunt for other reporting engines with code injection via templates (Pentaho, BIRT, Tableau); Java-based services accepting user-supplied templates; Other applications using Scriptlets or expression language evaluation; Services with default credentials exposed to network; Upload functionality in administrative interfaces that processes markup/template languages

## MITRE ATT&CK
- T1190
- T1200
- T1059
- T1059.003
- T1078
- T1078.001
- T1570

## Notes
This vulnerability chain demonstrates the critical importance of default credential hygiene. JasperReports' Scriptlet feature is a powerful design choice for legitimate use cases but becomes dangerous without proper access controls. The vulnerability was reported by Foxglove Security in October 2016. This type of code execution through template injection is endemic to flexible reporting engines and similar patterns appear across multiple platforms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
