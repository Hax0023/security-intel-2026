# MOVEit Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Assignment, Server-Side Request Forgery (SSRF), Pre-authentication Vulnerability
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer allows attackers to exploit an arbitrary session variable assignment vulnerability combined with SQL injection and SSRF to achieve remote code execution. The vulnerability was discovered through patch diffing analysis by comparing vulnerable version 2023.0.0 with patched version 2023.0.1.

## Attack scenario (step by step)
1. Attacker identifies MOVEit Transfer instance exposed on the internet without authentication requirements
2. Attacker crafts malicious HTTP headers to set arbitrary session variables via the vulnerable code path that accepts header-based session variable assignment
3. Attacker leverages SSRF through machine2.aspx endpoint (normally restricted to internal network) to bypass access controls
4. Attacker injects SQL commands through the compromised session context to interact with the backend database
5. Attacker executes arbitrary SQL queries to escalate privileges or inject malicious payloads
6. Attacker achieves remote code execution on the MOVEit Transfer server, enabling full system compromise

## Root cause
The unpatched version contains code that allows arbitrary session variable assignment based on HTTP header input without proper validation. This code was removed in the patched version. The vulnerability exists in the ASP.NET application logic that processes user-supplied headers and assigns them to session objects without sanitization, combined with insufficient access controls on sensitive endpoints like machine2.aspx that can be reached via SSRF.

## Attacker mindset
Opportunistic exploitation of widely-deployed file transfer software. The attacker recognizes MOVEit as a high-value target used by enterprises for secure file handling. Pre-authentication nature allows mass exploitation without credential acquisition. Active exploitation suggests attackers quickly weaponized the vulnerability after discovery, likely through reverse engineering similar patch diffing techniques.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers before using them in session management or database queries
- Apply principle of least privilege to internal-only endpoints; validate request origin beyond endpoint URL routing
- Use parameterized queries/prepared statements exclusively to prevent SQL injection
- Implement SSRF protections by maintaining strict allowlists for URL targets and validating all redirect/proxy requests
- Maintain comprehensive patch management processes and prioritize critical pre-authentication vulnerabilities for immediate deployment
- Monitor access logs for requests to sensitive endpoints (MOVEitISAPI.dll, machine2.aspx) especially from external sources
- Implement Web Application Firewalls (WAF) rules to detect suspicious header manipulation attempts
- Apply defense-in-depth with network segmentation to isolate MOVEit instances from internet exposure

## Variant hunting
Search for similar header-to-session variable assignment patterns in other ASP.NET web applications. Investigate other Progress software products that may use similar vulnerable patterns. Look for SSRF vulnerabilities in other endpoints that bypass internal-only restrictions. Hunt for SQL injection vectors in applications accepting dynamic session context variables.

## MITRE ATT&CK
- T1190
- T1083
- T1087
- T1530
- T1562
- T1059
- T1021

## Notes
This analysis demonstrates the value of patch diffing for vulnerability discovery. The researchers obtained vulnerable software through trial downloads and publicly accessible CDN URLs. The exploitation occurred in the wild before PoC publication, indicating high attacker motivation. The vulnerability chain involved multiple attack vectors (session hijacking, SSRF, SQL injection, RCE), making it particularly critical. Researchers responsibly withheld PoC publication for 30 days to allow patching. The native binary MOVEitISAPI.dll required Ghidra reverse engineering, suggesting the complete exploit chain may be more complex than the ASP.NET components analyzed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
