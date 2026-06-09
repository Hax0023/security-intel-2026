# MOVEit Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Setting, SSRF, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer (CVE-2023-34362) allows remote code execution through a combination of SQL injection and arbitrary session variable manipulation. The vulnerability was identified through patch diffing analysis by comparing unpatched version 2023.0.0 with patched version 2023.0.1, revealing removed code that allowed setting session variables from request headers.

## Attack scenario (step by step)
1. Attacker crafts HTTP request targeting publicly exposed MOVEit Transfer instance with malicious headers
2. Request is processed through MOVEitISAPI.dll which accepts arbitrary session variable setting from headers
3. Session variables are manipulated to bypass authentication or escalate privileges
4. Attacker leverages SSRF vulnerability to call internal machine2.aspx endpoint normally restricted to internal network
5. SQL injection payload is injected through the SSRF to execute arbitrary database commands
6. RCE is achieved through SQL injection executing system commands on the server

## Root cause
The vulnerable code allowed arbitrary session variables to be set directly from HTTP request headers without proper validation or sanitization. This was removed in the patch, indicating developers failed to implement proper input validation and session management controls in the initial release.

## Attacker mindset
Active exploitation in the wild suggests attackers reverse-engineered the vulnerability before patches were available. They target the pre-authentication nature of the flaw to achieve RCE without credentials, making it attractive for mass exploitation and lateral movement in supply chain attacks.

## Defensive takeaways
- Never allow direct setting of session variables from untrusted request headers
- Implement strict input validation and sanitization for all user-controlled data
- Use allowlists for session variable names rather than blocklists
- Require authentication before processing sensitive operations like machine2.aspx
- Apply defense-in-depth: validate at multiple layers (header parsing, session management, SQL queries)
- Patch critical vulnerabilities immediately given active exploitation
- Monitor for suspicious session variable patterns in logs
- Implement SSRF protections including URL validation and internal network restrictions

## Variant hunting
Researchers should examine other Progress software products (MOVEit Managed File Transfer, MOVEit Central) for similar session variable handling patterns. Additionally, search for other ASPX endpoints that may have similar authentication bypass mechanisms. Check for variants where other HTTP headers are parsed into session variables (X-Forwarded headers, custom headers, etc.). Analyze other versions between 2022.1.1 and 2023.0.1 for intermediate vulnerable builds.

## MITRE ATT&CK
- T1190
- T1190
- T1598
- T1566
- T1190
- T1190
- T1195
- T1199
- T1021

## Notes
This writeup focuses on patch diffing methodology rather than full exploit details, with responsible disclosure practice deferring PoC release. The exploitation chain combines multiple vectors (header manipulation, SSRF, SQL injection) showing sophisticated attack complexity. The active exploitation in the wild during disclosure indicates zero-day nature at time of discovery. Researchers successfully obtained trial licenses and older versions through public CDN enumeration, demonstrating practical reverse engineering techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
