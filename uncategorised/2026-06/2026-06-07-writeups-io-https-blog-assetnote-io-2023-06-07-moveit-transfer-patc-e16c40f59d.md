# MOVEit Transfer RCE (CVE-2023-34362) - Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Assignment, Server-Side Request Forgery (SSRF), Pre-authentication Code Execution
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer (CVE-2023-34362) allows remote attackers to execute arbitrary code through a combination of SQL injection and SSRF attacks. The vulnerability stems from improper session variable handling that allows arbitrary headers to set internal session variables, which can be leveraged to bypass authentication and achieve code execution.

## Attack scenario (step by step)
1. Attacker identifies unpatched MOVEit Transfer instance accessible from the internet
2. Attacker crafts HTTP request with malicious header values designed to set arbitrary session variables
3. Session variable manipulation allows attacker to bypass authentication checks or modify request context
4. Attacker exploits SSRF vulnerability to trigger internal requests to restricted endpoints (e.g., machine2.aspx)
5. Internal request execution leads to SQL injection payload being processed with elevated privileges
6. SQL injection payload results in arbitrary code execution on the MOVEit server

## Root cause
The patched version removed code that allowed arbitrary session variable assignment based on HTTP headers in request processing. The vulnerable code failed to properly validate or sanitize header inputs before using them to set internal session variables, enabling authentication bypass and subsequent exploitation of downstream SQL injection vulnerabilities.

## Attacker mindset
Exploit critical pre-authentication vulnerabilities in widely-deployed file transfer software to establish initial access. Chain multiple vulnerability classes (header injection → SSRF → SQL injection → RCE) to overcome layered controls. Target organizations with internet-exposed instances that haven't patched immediately upon disclosure.

## Defensive takeaways
- Implement strict input validation on all HTTP headers before using them to populate session or application state
- Enforce authentication checks at the earliest possible point in request processing, before any session variable manipulation
- Use allowlists for session variable assignment rather than accepting arbitrary header values
- Disable or heavily restrict SSRF-prone functionality (internal request handling) unless absolutely necessary
- Monitor for suspicious header patterns and session variable modifications in access logs
- Implement Web Application Firewall (WAF) rules to detect SQL injection patterns and unusual header values
- Maintain rapid patch deployment processes for critical vulnerabilities in externally-facing applications
- Segment network access to restrict internal endpoints like machine2.aspx to localhost only

## Variant hunting
Search for similar header-to-session-variable assignment patterns in other legacy web applications, particularly those written in ASP.NET. Look for other endpoints that may have SSRF-like behavior or internal-only restrictions that can be bypassed through header manipulation. Examine other MOVEit modules and related Progress products for similar authentication bypass mechanisms.

## MITRE ATT&CK
- T1190
- T1598
- T1056
- T1001
- T1021
- T1133

## Notes
Assetnote responsibly disclosed this vulnerability with a 30-day embargo before public PoC release to allow organizations time to patch. The research methodology of obtaining trial versions and performing patch diffing at the binary level provided complete exploit chain visibility. The vulnerability was actively exploited in the wild before patches were widely deployed, demonstrating the critical nature of immediate patching for pre-authentication RCE issues.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
