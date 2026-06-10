# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Arbitrary Code Execution, Insecure Deserialization, Unsafe Template Processing, Default Credentials
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates that can reference custom Java Scriptlets, enabling arbitrary code execution on the server. Combined with default credentials (jasperadmin/jasperadmin), an attacker can gain complete system compromise. The vulnerability exists because JasperReports prioritizes flexibility in report generation over security boundaries.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on internet via port scanning or reconnaissance
2. Attacker obtains default credentials (jasperadmin/jasperadmin) or weak administrative credentials through brute force
3. Attacker logs into JasperReports administrative interface
4. Attacker creates or modifies a JRXML report template to include a malicious Scriptlet class reference
5. Attacker uploads the crafted template and executes the report
6. Malicious Scriptlet code executes with JasperReports process privileges, allowing shell spawning or data exfiltration

## Root cause
JasperReports design allows arbitrary Java code execution through Scriptlet references in JRXML templates without sufficient validation or sandboxing. The developers prioritized flexibility for legitimate custom report processing over security isolation. Additionally, default credentials were not forced to change during initial deployment.

## Attacker mindset
Penetration tester looking for easy wins on administrative interfaces. After gaining default admin access, systematically explores application features to find code execution paths. Recognizes that business logic features (report templating) often have less security hardening than authentication layers.

## Defensive takeaways
- Never expose administrative interfaces to the internet; use VPN/bastion hosts
- Force immediate change of default credentials on first login with strong password requirements
- Disable or restrict Scriptlet functionality if not required; implement allowlist of permitted Scriptlet classes
- Implement strict input validation and sandboxing for JRXML template uploads
- Apply principle of least privilege to JasperReports service account (no shell access, minimal OS permissions)
- Monitor and audit report template creation/modification activities
- Keep JasperReports updated with security patches
- Implement code signing requirements for custom Scriptlets
- Use Web Application Firewall (WAF) rules to restrict administrative access

## Variant hunting
Similar vulnerabilities likely exist in other business intelligence/reporting platforms that support custom code execution (Pentaho, QlikView, Tableau extensions). Search for: template injection in report generators, scriptlet/macro functionality in data processing tools, Java deserialization in document upload features, unsafe reflection in template engines.

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1203
- T1566

## Notes
This represents a classic combination attack: default credentials + feature abuse for code execution. The writeup is from 2016, indicating this was a known issue for years. JasperReports is commonly deployed in enterprise environments; this vulnerability likely affected many organizations. The Scriptlet feature is documented but its security implications were not adequately communicated to users. This case study demonstrates why administrative interfaces must be treated as high-value targets and why default credentials remain a critical vulnerability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
