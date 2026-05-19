# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Unsafe Deserialization, Default Credentials, Insecure Template Processing
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload and execute arbitrary Java code through malicious JRXML report templates that reference custom Scriptlets. Combined with default credentials (jasperadmin/jasperadmin), this provides a direct path to remote code execution on the server.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet through reconnaissance
2. Attacker attempts default credentials (jasperadmin/jasperadmin) and gains administrative access
3. Attacker creates or modifies a JRXML report template to include a reference to a malicious custom Scriptlet class
4. Attacker uploads the malicious JRXML file through the JasperReports UI
5. Attacker triggers report generation/preview, causing the server to instantiate and execute the malicious Scriptlet
6. Attacker achieves remote code execution with the privileges of the JasperReports application server

## Root cause
JasperReports JRXML templates support arbitrary Java Scriptlet references for data manipulation flexibility. The application does not adequately restrict or sandbox Scriptlet execution, allowing instantiation of arbitrary classes. Combined with default credentials and lack of authentication enforcement, this creates a critical RCE vector.

## Attacker mindset
Low-hanging fruit mentality: identify exposed administrative interfaces, attempt default credentials, exploit intended flexibility features (Scriptlets) for unintended purposes (code execution). The attacker recognized that administrative interfaces typically lead to code execution and methodically exploited the feature chain from authentication through template upload to execution.

## Defensive takeaways
- Change default credentials immediately upon deployment; enforce strong password policies
- Implement network segmentation to restrict administrative interfaces from internet exposure
- Disable or strictly sandbox Scriptlet functionality if not required; whitelist allowed Scriptlet classes
- Apply principle of least privilege for report creation/editing capabilities
- Implement input validation and code review for uploaded JRXML templates
- Deploy Web Application Firewall (WAF) rules to detect malicious template uploads
- Monitor and audit report creation, modification, and execution activities
- Keep JasperReports patched to latest version with security fixes
- Implement request signing or integrity verification for JRXML files

## Variant hunting
Search for similar template injection vulnerabilities in other reporting engines (Pentaho, BIRT, Jasper Server variants). Investigate whether other custom code execution mechanisms exist in JasperReports (expressions, custom functions, data adapters). Check if unauthenticated users can access template upload functionality. Test for XXE injection in JRXML processing. Examine whether compiled reports (.jasper) can be reverse-engineered to extract embedded Scriptlets.

## MITRE ATT&CK
- T1190
- T1595
- T1566
- T1078
- T1059
- T1105
- T1046
- T1583

## Notes
This represents a well-documented case of chaining multiple vulnerabilities (default credentials + unsafe feature) for critical impact. The writeup demonstrates good security research methodology by documenting the attack chain with actual JRXML template examples. JasperReports and related Jaspersoft products have a history of RCE vulnerabilities. Organizations should treat this as a critical application requiring immediate security review if internet-exposed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
