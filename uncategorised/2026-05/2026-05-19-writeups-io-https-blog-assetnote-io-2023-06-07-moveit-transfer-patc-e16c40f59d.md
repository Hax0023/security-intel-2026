# MOVEit Transfer RCE via SQL Injection and SSRF Chain (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Unknown (appears to be internal security research, not traditional bug bounty)
- **Severity:** critical
- **Vuln types:** SQL Injection, Server-Side Request Forgery (SSRF), Remote Code Execution, Improper Input Validation, Arbitrary Session Variable Setting
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer (CVE-2023-34362) allows remote attackers to achieve unauthenticated remote code execution through a combination of SQL injection and SSRF attacks. The vulnerability stems from removed input validation code that previously prevented arbitrary session variable manipulation via HTTP headers, enabling attackers to bypass authentication and execute arbitrary commands on affected systems.

## Attack scenario (step by step)
1. Attacker crafts malicious HTTP request containing injected session variables via custom headers targeting exposed MOVEit Transfer instance
2. Vulnerable code accepts and sets arbitrary session variables without validation, bypassing authentication mechanisms
3. Attacker leverages SSRF vulnerability to trigger internal requests to restricted resources like machine2.aspx that are normally only accessible from internal network
4. Through SSRF chain, attacker injects SQL payload into application that processes the forged internal request
5. SQL injection executes arbitrary database commands with application privileges, allowing data exfiltration or command execution hooks
6. Attacker achieves remote code execution on the server, gaining full system compromise

## Root cause
Patch diffing analysis revealed that the patched version removed code that was arbitrarily setting session variables based on HTTP header input without validation. The unpatched version allowed attackers to manipulate session state pre-authentication, combined with SSRF capabilities that could access internal-only endpoints like machine2.aspx, which then became vulnerable to SQL injection attacks.

## Attacker mindset
Opportunistic exploitation of critical pre-authentication vulnerability in widely-deployed enterprise file transfer software. Attackers actively exploited this in-the-wild with intent to establish persistent access, exfiltrate data, and potentially pivot within target networks. The vulnerability's pre-authentication nature and ease of exploitation made it attractive for mass scanning and compromise.

## Defensive takeaways
- Never trust HTTP headers for security-sensitive operations like session variable assignment without strict whitelist validation
- Implement robust input validation and sanitization for all user-controlled data, especially in ASP.NET header processing
- Apply principle of least privilege to internal endpoints - do not assume internal-only resources are safe from external attack chains
- Validate and sanitize all SQL queries; use parameterized queries to prevent SQL injection regardless of input source
- Implement SSRF protections including URL validation, hostname resolution verification, and blocking private IP ranges
- Prioritize patching of pre-authentication vulnerabilities in externally-facing services within 24-48 hours
- Monitor for exploitation patterns including requests to unusual internal endpoints and malformed header injection attempts
- Conduct thorough patch diffing analysis for critical fixes to understand root causes and identify variant vulnerabilities

## Variant hunting
Researchers should investigate: (1) Other Progress products using similar session variable handling mechanisms; (2) Alternative SSRF entry points in MOVEit Transfer that could chain with SQL injection; (3) Other HTTP header injection points in ASP.NET applications that may allow session manipulation; (4) Similar pre-authentication bypass patterns in competing file transfer solutions; (5) Other instances where removed validation code suggests security patches addressing input sanitization

## MITRE ATT&CK
- T1190
- T1190 - Exploit Public-Facing Application
- T1190 - CVE-2023-34362
- T1089 - Service Stop
- T1043 - Exfiltration Over Alternative Protocol
- T1566 - Phishing
- T1570 - Lateral Tool Transfer
- T1021 - Remote Services
- T1055 - Process Injection
- T1047 - Windows Management Instrumentation

## Notes
This writeup demonstrates advanced patch diffing methodology for vulnerability analysis. Key research technique: obtaining trial software and older versions through CDN enumeration, then using DiffMerge to identify removed security code. The vulnerability chain combines session hijacking, SSRF, and SQL injection - a sophisticated attack requiring multiple layers. Researchers responsibly delayed public PoC release by 30 days to allow organizations time to patch. The vulnerability was actively exploited in the wild before patches were available, making this post-incident analysis critical for threat intelligence. The native binary MOVEitISAPI.dll required Ghidra analysis, demonstrating need for mixed tooling approaches in comprehensive patch analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
