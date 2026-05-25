# MOVEit Transfer RCE via SQL Injection and Arbitrary Session Variable Setting (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Arbitrary Session Variable Setting, Server-Side Request Forgery (SSRF), Remote Code Execution, Pre-authentication vulnerability
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in MOVEit Transfer allows unauthenticated attackers to achieve remote code execution through a combination of SQL injection and arbitrary session variable manipulation. The vulnerability chain leverages SSRF to call an internal-only endpoint (machine2.aspx) and exploits unvalidated header inputs to set arbitrary session variables, ultimately leading to code execution.

## Attack scenario (step by step)
1. Attacker identifies MOVEit Transfer instance exposed on the internet
2. Attacker crafts HTTP request with malicious headers targeting the session variable setting functionality
3. Attacker uses SSRF technique to invoke the internal machine2.aspx endpoint
4. Arbitrary session variables are set via unvalidated header inputs without authentication
5. Attacker leverages SQL injection through manipulated session context
6. SQL injection payload leads to remote code execution on the server

## Root cause
The patched code reveals that the vulnerability stems from a function that allowed arbitrary setting of session variables based directly on HTTP header input without validation. The code removed in the patch shows this dangerous pattern. Combined with SSRF to bypass internal-only restrictions on machine2.aspx and SQL injection vectors, attackers can execute arbitrary code pre-authentication.

## Attacker mindset
Attackers exploited this vulnerability in the wild immediately upon discovery, indicating either advanced threat actor knowledge or rapid weaponization post-disclosure. The pre-authentication nature and ease of exploitation made it an attractive target for mass compromise campaigns.

## Defensive takeaways
- Never trust HTTP headers for session variable assignment without strict validation and sanitization
- Implement proper authentication checks on all endpoints, even those intended for internal use only
- Apply input validation and parameterized queries to prevent SQL injection attacks
- Use allowlists for session variable names and types rather than accepting arbitrary values
- Implement SSRF protections and network segmentation to prevent internal endpoint abuse
- Prioritize patching critical pre-authentication RCE vulnerabilities immediately
- Monitor for suspicious header patterns and session variable manipulation attempts
- Conduct thorough patch diffing analysis on security updates to understand root causes

## Variant hunting
Similar patterns should be hunted in other web applications that: (1) Accept session configuration via HTTP headers, (2) Have endpoints intended for internal use accessible via SSRF, (3) Use user-controlled input in SQL queries without parameterization, (4) Mix session handling with database queries without proper isolation. Check other Progress products and similar file transfer solutions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1190 - Pre-authentication RCE
- T1190 - SQL Injection
- T1557 - Man-in-the-Middle
- T1021.5 - Remote Services via SSRF
- T1505.004 - Web Shell

## Notes
This analysis is based on reverse engineering and patch diffing rather than public PoC code. Assetnote responsibly withheld full PoC disclosure (30-day embargo) to allow organizations time to patch. The vulnerability demonstrates the power of systematic patch diffing: removing session variable assignment code was the actual fix, pinpointing the vulnerability. The SSRF + internal endpoint bypass component was crucial to understanding the full attack chain. This is a sophisticated vulnerability combining multiple attack vectors (header injection, SSRF, SQL injection, RCE).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
