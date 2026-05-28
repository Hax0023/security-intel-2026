# MOVEit Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Setting, Server-Side Request Forgery, Pre-authentication Code Execution
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
Progress MOVEit Transfer contained a critical pre-authentication RCE vulnerability (CVE-2023-34362) allowing unauthenticated attackers to achieve remote code execution through a combination of SQL injection and SSRF. Assetnote reverse-engineered the vulnerability through patch diffing, identifying a code path that allowed arbitrary session variable manipulation via HTTP headers, which could be leveraged to bypass authentication controls.

## Attack scenario (step by step)
1. Attacker sends HTTP request with malicious headers to the MOVEit Transfer web application
2. Session variables are arbitrarily set based on user-controlled header input due to missing validation
3. Attacker exploits SSRF to call internal endpoint machine2.aspx from external context
4. Machine2.aspx endpoint is accessed with elevated privileges due to manipulated session variables
5. SQL injection payload is delivered through the now-accessible internal endpoint
6. Injected SQL commands execute with database context, leading to remote code execution on the server

## Root cause
Code that allowed arbitrary setting of session variables based on HTTP header input without proper validation or sanitization. This functionality was completely removed in the patched version. The vulnerability was compounded by insufficient access controls on internal endpoints like machine2.aspx that could be reached via SSRF.

## Attacker mindset
Opportunistic threat actors rapidly exploiting a freshly disclosed critical vulnerability affecting widely deployed file transfer software before patches could be applied. Focus on pre-authentication exploitation to maximize victim scope.

## Defensive takeaways
- Never allow user-controlled data to directly set session variables without strict validation and whitelisting
- Implement proper input sanitization and parameterized queries to prevent SQL injection
- Apply network-level access controls to internal endpoints and verify caller context
- Implement SSRF protections by validating and restricting outbound request destinations
- Enforce authentication on all sensitive endpoints regardless of perceived internal-only usage
- Maintain strict change control and security review processes for session management code
- Deploy WAF rules to detect and block exploitation patterns
- Prioritize patching critical vulnerabilities in internet-facing applications

## Variant hunting
Search for other instances where HTTP headers directly influence session state or authentication decisions. Review other web applications from Progress Software for similar patterns. Examine ASPX endpoints that perform internal operations without proper authorization checks.

## MITRE ATT&CK
- T1190
- T1021
- T1190
- T1005
- T1059
- T1021.001
- T1087

## Notes
This is a patch diffing case study demonstrating excellent reverse engineering methodology. The researchers obtained vulnerable and patched versions through CDN enumeration and serial key trial mechanism. The vulnerability required knowledge of internal endpoint structure (machine2.aspx) suggesting either public documentation or prior research. Active exploitation timeline indicates rapid weaponization. Researchers responsibly delayed full PoC disclosure pending patch deployment window.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
