# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** JasperReports
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Remote Code Execution, Arbitrary Code Execution, Unsafe Deserialization, Insecure Template Processing, Default Credentials
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated administrators to upload malicious JRXML report templates containing custom Scriptlets that execute arbitrary Java code on the server. Combined with default credentials (jasperadmin/jasperadmin), this enables trivial remote code execution. The vulnerability exists because the template processing engine instantiates and executes user-supplied Scriptlet classes without proper validation or sandboxing.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance exposed on the internet through port scanning or reconnaissance
2. Attacker attempts default credentials (jasperadmin/jasperadmin) against the administrative interface
3. Upon successful authentication, attacker navigates to the report creation/editing functionality
4. Attacker crafts a malicious JRXML template file that references a custom Scriptlet class with embedded shell/reverse shell code
5. Attacker uploads the template and triggers report generation/compilation
6. JasperReports instantiates the Scriptlet class and executes the attacker's code with application privileges

## Root cause
JasperReports designers prioritized flexibility by allowing custom Java Scriptlets in report templates, but failed to implement code execution controls or sandboxing. The template parser deserializes and instantiates arbitrary classes referenced in JRXML files without validation. Combined with default credentials remaining unchanged, this creates a direct path to RCE.

## Attacker mindset
An attacker recognizes that administrative interfaces frequently expose code execution paths. Upon finding JasperReports with default credentials, they systematically explore the application's capabilities and identify the Scriptlet feature as a built-in mechanism for arbitrary code execution. This is not a complex exploit—it's leveraging intended functionality with weak authentication.

## Defensive takeaways
- Enforce strong, unique credentials for all administrative accounts; disable or change default accounts immediately
- Implement code execution restrictions or sandboxing for user-supplied templates and Scriptlets
- Disable Scriptlet support if not required; provide configuration options to restrict dangerous features
- Validate and restrict the classes that can be instantiated from templates using whitelisting
- Do not expose administrative interfaces to the internet; require VPN or network segmentation
- Monitor for suspicious template uploads and compilation activities
- Apply principle of least privilege to JasperReports service accounts
- Regularly audit and update JasperReports versions for security patches

## Variant hunting
['Check other reporting tools (Pentaho, BIRT, Jasper Soft Studio) for similar template-based code injection', 'Investigate if unauthenticated template processing or guest report creation is possible', 'Examine if Scriptlets can be exploited through report parameters or data sources', 'Test if JRXML files can be uploaded via other interfaces (file upload, API endpoints)', 'Assess whether compiled reports (.jasper files) can be modified to inject malicious Scriptlets', 'Determine if expression injection in report fields can bypass Scriptlet restrictions', 'Check for Java deserialization gadgets that could be leveraged in template contexts']

## MITRE ATT&CK
- T1190
- T1078
- T1059
- T1203
- T1134
- T1570

## Notes
This is a classic example of how 'flexibility' in software design creates security liabilities. The Scriptlet feature itself is the vulnerability vector—not a bug or misconfiguration per se, but intentional functionality misused. Default credentials amplify the severity dramatically. The writeup is from 2016; organizations using unsupported or unpatched JasperReports versions likely remain vulnerable. The attack requires minimal sophistication and would be highly reliable in practice.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
