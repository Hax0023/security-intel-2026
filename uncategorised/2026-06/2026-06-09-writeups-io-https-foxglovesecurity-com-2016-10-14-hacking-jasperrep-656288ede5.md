# Hacking JasperReports - The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Authentication Bypass, Insecure Deserialization
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates containing references to malicious Java Scriptlets, enabling arbitrary code execution on the server. Combined with default credentials (jasperadmin/jasperadmin), an attacker can gain complete remote code execution without authentication.

## Attack scenario (step by step)
1. Attacker discovers JasperReports server exposed on the internet
2. Attacker uses default credentials (jasperadmin/jasperadmin) to authenticate to administrative interface
3. Attacker crafts malicious JRXML report template referencing a custom Scriptlet class with shell payload
4. Attacker uploads the template through the report creation/editing functionality
5. Attacker executes the report through the server interface
6. Malicious Scriptlet executes arbitrary Java code, providing reverse shell or command execution

## Root cause
JasperReports design allows users with report creation privileges to define custom Scriptlets (arbitrary Java code) within JRXML templates. The server compiles and executes these Scriptlets during report generation without sufficient validation or sandboxing, combined with weak default credentials.

## Attacker mindset
Penetration tester seeking low-hanging fruit on internet-facing services; recognizes that administrative interfaces frequently lead to code execution; uses default credentials as entry point; leverages flexible template system as execution vector.

## Defensive takeaways
- Immediately change all default credentials on JasperReports instances
- Restrict network access to JasperReports administrative interfaces (firewall/VPN only)
- Disable Scriptlet functionality if not required; whitelist allowed Scriptlet classes
- Implement strict input validation and sandboxing for uploaded report templates
- Apply principle of least privilege; separate report creation from report execution roles
- Monitor and log report template uploads and executions
- Keep JasperReports patched to latest security updates
- Use code signing or integrity verification for report templates

## Variant hunting
['Check for similar vulnerabilities in other reporting engines (BIRT, Pentaho, Actuate)', 'Investigate whether other template upload features support code execution', 'Test if Scriptlets can be injected through other input vectors (API parameters, data sources)', 'Determine if compiled reports (.jasper files) can contain malicious Scriptlets', 'Assess if Expression Language (EL) injection exists in report fields/parameters', 'Check for Java deserialization vulnerabilities in report data handling']

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1543
- T1105

## Notes
This vulnerability represents a complete compromise chain: weak default credentials + privileged feature + unsafe code execution. The lack of prior public research on this specific attack vector made it a valuable 'easy win' for penetration testers. JasperReports' design philosophy prioritized flexibility over security. The vulnerability affects both on-premises and cloud deployments. Organizations running JasperReports should treat this as a critical risk requiring immediate remediation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
