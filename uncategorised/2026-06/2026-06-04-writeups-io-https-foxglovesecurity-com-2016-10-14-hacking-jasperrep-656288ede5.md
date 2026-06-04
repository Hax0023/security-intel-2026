# Hacking JasperReports – The Hidden Shell Feature

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** JasperReports (Open Source)
- **Bounty:** Not specified (Penetration Test Finding)
- **Severity:** CRITICAL
- **Vuln types:** Remote Code Execution (RCE), Arbitrary Code Execution, Unsafe Deserialization, Insecure Template Processing
- **Category:** uncategorised
- **Writeup:** https://foxglovesecurity.com/2016/10/14/hacking-jasperreports-the-hidden-shell-feature/

## Summary
JasperReports allows authenticated users to upload malicious JRXML report templates containing custom Scriptlets that execute arbitrary Java code. By editing or creating a report template with a reference to a malicious Scriptlet class, attackers can achieve unauthenticated remote code execution when the report is compiled and executed by the server.

## Attack scenario (step by step)
1. Attacker discovers JasperReports instance with default credentials (jasperadmin/jasperadmin)
2. Attacker logs into administrative interface and accesses report creation/editing functionality
3. Attacker crafts malicious JRXML file containing <scriptlet> element referencing custom Java class
4. Attacker uploads JRXML file or modifies existing template to include scriptlet reference
5. When report is generated, JasperReports compiles and instantiates the Scriptlet class
6. Custom Scriptlet code executes with JasperReports application privileges, delivering reverse shell

## Root cause
JasperReports design allows arbitrary Java code execution through Scriptlets for 'flexibility' in data manipulation. The framework compiles and instantiates user-supplied Scriptlet classes without proper validation or sandboxing, combined with weak default credentials and exposed administrative interfaces.

## Attacker mindset
Penetration tester recognized that administrative interfaces typically lead to code execution. Investigated template processing mechanism, discovered Scriptlet feature as legitimate functionality designed for extensibility, and weaponized it by injecting malicious Java code disguised as legitimate report customization.

## Defensive takeaways
- Disable or remove default credentials immediately; enforce strong password policies for all administrative accounts
- Restrict network access to JasperReports administrative interfaces (non-Internet facing, VPN/firewall rules)
- Implement code signing or whitelisting for Scriptlets to prevent arbitrary class loading
- Disable Scriptlet functionality entirely if not required for business operations
- Apply principle of least privilege - restrict report creation/editing to trusted users only
- Monitor and audit report template uploads and modifications
- Keep JasperReports patched to latest security releases
- Use Java security manager to restrict what administrative Java code can execute
- Implement input validation and sandboxing for template processing

## Variant hunting
Search for similar vulnerabilities in other reporting engines (Crystal Reports, Apache OFBiz, Apache Cocoon). Look for template injection in configuration management tools, workflow engines, and any system allowing user-supplied code execution through 'plugins' or 'extensions'. Investigate other JasperReports features that might accept serialized Java objects or expressions (e.g., expression evaluation in fields, parameters, or conditional formatting).

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (default credentials)
- T1059 - Command and Scripting Interpreter (Java)
- T1203 - Exploitation for Client Execution
- T1648 - Serverless Execution

## Notes
This vulnerability is particularly dangerous because: (1) JasperReports is commonly deployed in enterprise environments, (2) default credentials are frequently left unchanged, (3) the vulnerability exploits a documented feature designed for legitimate use, making detection difficult, (4) the attack requires only report creation privileges, not direct code access. The write-up demonstrates excellent penetration testing methodology by identifying weak credentials, exploring application functionality, and weaponizing legitimate features. This became a well-known 'easy win' vulnerability in the security community post-publication.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
