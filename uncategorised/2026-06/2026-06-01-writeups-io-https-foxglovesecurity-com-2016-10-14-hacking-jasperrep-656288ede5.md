# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** JasperReports (open-source reporting tool)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Insecure Deserialization, Authentication Bypass, Privilege Escalation
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates that can reference malicious custom Scriptlets written in Java. By crafting a template that invokes a malicious Scriptlet class during report execution, attackers can achieve arbitrary code execution on the server. Combined with default credentials (jasperadmin/jasperadmin), this becomes a trivial remote code execution vulnerability.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet
2. Attacker logs in using default credentials (jasperadmin/jasperadmin)
3. Attacker creates or edits an existing JRXML report template file
4. Attacker adds a malicious scriptlet reference in the template XML pointing to custom Java class
5. Attacker uploads the modified template and triggers report execution
6. Server compiles and executes the malicious Scriptlet code, providing reverse shell or command execution

## Root cause
JasperReports design flaw allowing arbitrary Java code execution through Scriptlets in JRXML templates without proper sandboxing. The feature was intended for legitimate data manipulation but provides no restrictions on what code can be executed. Combined with default credentials and lack of input validation on template uploads.

## Attacker mindset
Reconnaissance-focused attacker identifies JasperReports as a high-value target due to its reporting functionality. The attacker recognizes that administrative report-building features typically lead to code execution. Default credentials provide immediate access, and the Scriptlet feature is discovered through template analysis and documentation review. The attack is straightforward once credentials are obtained.

## Defensive takeaways
- Never deploy applications with default credentials; enforce strong password policies at installation
- Implement strict code sandboxing for user-provided templates and scripts
- Disable or restrict Scriptlet functionality if not required; use configuration management
- Apply principle of least privilege - limit report editing to necessary users
- Implement code review processes for uploaded templates before execution
- Use security scanning tools to detect dangerous patterns in JRXML files
- Segment reporting servers from critical infrastructure
- Monitor and log all report template uploads and modifications
- Apply patches promptly and keep JasperReports updated
- Consider using expression sandboxing or restricting expression languages

## Variant hunting
Search for similar patterns in other Java-based reporting tools (BIRT, Pentaho, Crystal Reports) that support custom expressions or plugins. Look for template injection vulnerabilities in other XML-based configuration systems. Investigate other features in JasperReports that accept Java code (expressions, formatters, validators). Check for server-side template injection in PDF/report generation services.

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1203
- T1598
- T1110

## Notes
This vulnerability exemplifies a common pattern: feature-rich administrative interfaces with default credentials and unsafe code execution capabilities create a 'perfect storm' for exploitation. The writeup's practical approach (modifying existing templates rather than creating new ones) demonstrates real-world attack methodology. The vulnerability likely affects multiple JasperReports versions and deployments, particularly those facing the internet with default configurations. The research was conducted by Foxglove Security (@breenmachine) during a legitimate penetration test engagement.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
