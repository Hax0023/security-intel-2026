# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Insecure Deserialization, Default Credentials, Unsafe Template Processing
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated administrators to upload JRXML report templates that can reference custom malicious Scriptlets containing arbitrary Java code. When the report is compiled and executed, the embedded Java code runs with the privileges of the application server, enabling remote code execution. The vulnerability is exacerbated by default credentials (jasperadmin/jasperadmin) often being left unchanged.

## Attack scenario (step by step)
1. Identify exposed JasperReports instance on Internet-facing asset
2. Discover or brute-force default administrative credentials (jasperadmin/jasperadmin)
3. Authenticate to JasperReports administrative interface
4. Create or edit a report template (JRXML file) containing scriptlet reference to malicious Java class
5. Upload modified template and trigger report compilation/execution
6. Receive reverse shell with application server privileges

## Root cause
JasperReports design allows users with report creation/editing permissions to define custom Scriptlets as arbitrary Java code. The framework compiles and executes these Scriptlets without sufficient validation or sandboxing, treating user-supplied templates as trusted code.

## Attacker mindset
Reconnaissance-focused: penetration tester identifying small attack surface and leveraging administrative access to escalate privileges. Recognizes that flexible data processing features (Scriptlets) commonly hide RCE vectors and systematically exploits this pattern.

## Defensive takeaways
- Change default administrative credentials immediately after deployment
- Restrict report creation/editing permissions to trusted users only
- Disable or restrict Scriptlet functionality if not required
- Implement code review/approval workflows for report templates
- Run JasperReports with minimal required privileges (principle of least privilege)
- Use Web Application Firewall rules to detect suspicious JRXML uploads
- Regularly audit and monitor report template modifications
- Isolate JasperReports instances from public Internet exposure
- Update to patched versions and apply security controls for template validation

## Variant hunting
['Check for similar code execution vectors in other data processing frameworks (Pentaho, BIRT, Actuate)', 'Search for unauthenticated template upload endpoints or authentication bypass techniques', 'Investigate whether Expression Language (EL) injection exists in JRXML expression evaluation', 'Test for XXE (XML External Entity) vulnerabilities in JRXML parsing', 'Examine whether compiled report classes can be deserialized for gadget chain exploitation', 'Hunt for information disclosure via error messages revealing template compilation paths']

## MITRE ATT&CK
- T1190
- T1199
- T1078
- T1648
- T1203

## Notes
This writeup demonstrates a classic admin-to-RCE escalation pattern. The vulnerability fundamentally stems from allowing untrusted template uploads with arbitrary code execution capabilities. Published October 2016; likely patched in subsequent JasperReports versions but remains a critical finding when default credentials are present or admin access is obtained through other means.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
