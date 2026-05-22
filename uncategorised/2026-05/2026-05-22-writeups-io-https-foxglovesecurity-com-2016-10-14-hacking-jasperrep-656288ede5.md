# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** Arbitrary Code Execution, Insecure Deserialization, Unsafe Template Processing, Default Credentials
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload JRXML report templates that can reference malicious custom Scriptlets, which are arbitrary Java classes executed during report generation. Combined with default credentials (jasperadmin/jasperadmin), an attacker can gain remote code execution on the server.

## Attack scenario (step by step)
1. Identify JasperReports server exposed on the internet
2. Obtain access using default credentials (jasperadmin/jasperadmin)
3. Create or edit a report template (JRXML file)
4. Inject references to a malicious custom Scriptlet class in the JRXML
5. Upload the malicious template through the administrative interface
6. Trigger report generation, causing the Scriptlet to execute arbitrary Java code with server privileges

## Root cause
JasperReports' design allows arbitrary Java Scriptlets to be referenced and executed during report processing without proper validation or sandboxing. The feature was intended for data manipulation flexibility but provides no restrictions on what code can be executed.

## Attacker mindset
An attacker seeks low-hanging fruit on exposed administrative interfaces. The presence of default credentials combined with a feature designed for extensibility (Scriptlets) creates a direct path to code execution—a classic 'feature-as-vulnerability' scenario that administrative panels often present.

## Defensive takeaways
- Change all default credentials immediately upon deployment
- Restrict JasperReports administrative access to internal networks only
- Disable or restrict Scriptlet functionality if not required
- Implement strict validation and sandboxing for any user-uploaded templates
- Apply principle of least privilege to service accounts running JasperReports
- Monitor and audit report template uploads and modifications
- Keep JasperReports patched to the latest version

## Variant hunting
Look for similar report generation or data processing tools that allow custom code/plugins (e.g., Pentaho, BIRT, commercial BI platforms). Search for other Java-based templating systems that permit arbitrary class references. Investigate whether JasperReports has fixes for this in later versions and whether patch bypasses exist.

## MITRE ATT&CK
- T1190
- T1133
- T1078
- T1059

## Notes
This writeup demonstrates a real-world engagement where the combination of weak authentication and unsafe templating features led to RCE. The 'hidden shell feature' title is somewhat tongue-in-cheek—the Scriptlet functionality was never hidden, just underestimated as a security risk by users. The vulnerability requires authentication, but default credentials made it trivial to exploit. This is a excellent teaching example of how flexibility in software design can become a security liability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
