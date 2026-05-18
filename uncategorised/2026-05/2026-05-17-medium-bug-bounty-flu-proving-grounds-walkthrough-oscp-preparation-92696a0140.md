# CVE-2022-26134: Confluence OGNL Injection RCE Exploitation

## Metadata
- **Source:** Medium Bug Bounty
- **Date:** 2026-05-17
- **Author:** SilentExploit
- **Program:** Atlassian Confluence
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Object-Graph Navigation Language (OGNL) Injection, Remote Code Execution, Unauthenticated Arbitrary Code Execution
- **Category:** uncategorised
- **Writeup:** https://medium.com/@SilentExploit/flu-proving-grounds-walkthrough-oscp-preparation-a5b2c75b11b6?source=rss------bug_bounty_writeup-5

## Summary
CVE-2022-26134 is a critical unauthenticated RCE vulnerability in Atlassian Confluence Server and Data Center that allows remote attackers to execute arbitrary code by injecting malicious OGNL expressions into HTTP request URLs. The vulnerability affects Confluence 7.13.6 and other versions, enabling complete system compromise without authentication.

## Attack scenario (step by step)
1. Attacker performs reconnaissance and identifies Confluence 7.13.6 running on port 8090 via nmap and service enumeration
2. Attacker determines the target is vulnerable to CVE-2022-26134 by checking the version number against public vulnerability databases
3. Attacker crafts a malicious HTTP request containing OGNL injection payloads in the URL parameters
4. Attacker exploits the vulnerability to read sensitive files (e.g., /etc/passwd) to gather system information
5. Attacker escalates the exploit to achieve remote code execution by injecting command execution OGNL expressions
6. Attacker gains shell access and establishes persistence or moves laterally within the network

## Root cause
Confluence fails to properly validate and sanitize user-supplied input in HTTP request URLs before passing them to the OGNL expression evaluator. The application directly processes OGNL expressions without sufficient input validation, allowing injection of arbitrary code.

## Attacker mindset
An attacker recognizes that Confluence instances are commonly exposed on the internet and often run without authentication requirements on initial setup. By identifying the specific vulnerable version, the attacker can leverage a well-documented critical vulnerability to achieve unauthenticated RCE, allowing them to compromise the entire server and potentially the infrastructure it serves.

## Defensive takeaways
- Immediately patch Confluence to a patched version addressing CVE-2022-26134
- Implement strict input validation and output encoding for all user-supplied data, especially URL parameters
- Disable or restrict OGNL expression evaluation in untrusted contexts
- Implement Web Application Firewall (WAF) rules to detect and block OGNL injection attempts
- Require authentication and implement access controls before allowing access to Confluence administration features
- Monitor for suspicious HTTP requests containing OGNL syntax patterns in URLs and logs
- Conduct regular vulnerability scanning and version audits of all Atlassian products
- Network segmentation: restrict direct internet exposure of Confluence instances
- Implement principle of least privilege for the service account running Confluence

## Variant hunting
Look for similar OGNL injection vulnerabilities in other Atlassian products (Jira, Bitbucket). Search for expression language injection patterns in other Java-based applications using template engines or dynamic expression evaluators. Investigate whether other endpoints in Confluence versions accept OGNL expressions beyond the identified attack vector.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1210 - Exploitation of Remote Services
- T1592 - Gather Victim Host Information
- T1526 - Scan for Accessible Content

## Notes
This writeup demonstrates a real-world exploitation of CVE-2022-26134 in a controlled OSCP preparation environment. The vulnerability requires no authentication and allows immediate system compromise. The exploit tool 'through_the_wire.py' by jbaines-r7 is publicly available and highly effective. Organizations should treat this as a critical incident if found in production environments. The vulnerability affects multiple Confluence versions and requires immediate patching.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
