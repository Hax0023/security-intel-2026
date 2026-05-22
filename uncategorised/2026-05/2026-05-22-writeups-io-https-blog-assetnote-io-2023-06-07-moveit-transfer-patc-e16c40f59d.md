# MOVEIt Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Progress MOVEIt Transfer
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Manipulation, Server-Side Request Forgery (SSRF), Pre-authentication Vulnerability
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEIt Transfer (CVE-2023-34362) allows unauthenticated attackers to execute arbitrary code through a combination of SQL injection and session variable manipulation. Assetnote reverse-engineered the full exploit chain by patch diffing vulnerable (2023.0.0) and patched (2023.0.1) versions, discovering code that allowed arbitrary session variable setting via request headers.

## Attack scenario (step by step)
1. Attacker identifies MOVEIt Transfer instance exposed to the internet without authentication requirements
2. Attacker crafts HTTP request with malicious headers to set arbitrary session variables via the vulnerable code path
3. Vulnerability allows session variable manipulation to bypass authentication or authorization checks
4. Attacker leverages SSRF through machine2.aspx endpoint (internally callable) to access restricted functionality
5. Attacker injects SQL payload through session variable to execute arbitrary database commands
6. Attacker achieves remote code execution on the MOVEIt Transfer server

## Root cause
The patched version removed code that allowed arbitrary session variable setting based on HTTP header input without proper validation or authentication. This code was accessible pre-authentication, enabling attackers to manipulate application state and bypass security controls. The SSRF through machine2.aspx combined with SQL injection in the manipulated session context created the RCE vector.

## Attacker mindset
Opportunistic exploitation of unpatched internet-facing file transfer appliances. Once the vulnerability became public knowledge through exploitation in the wild, attackers quickly identified and compromised vulnerable instances. The attacker understood the application architecture well enough to chain SSRF with SQL injection for code execution.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers, especially those influencing session state
- Never trust or manipulate session variables based on user-supplied headers without cryptographic verification
- Enforce pre-authentication checks on all endpoints, including internal-only ones, to prevent SSRF bypass
- Use parameterized queries and prepared statements to prevent SQL injection
- Implement network segmentation to limit internet exposure of critical file transfer appliances
- Maintain inventory of all MOVEIt Transfer instances and prioritize patching of pre-authentication RCE vulnerabilities
- Monitor for exploitation attempts targeting machine2.aspx and MOVEitISAPI.dll endpoints
- Apply patches immediately for pre-authentication critical vulnerabilities
- Implement Web Application Firewall (WAF) rules blocking requests with suspicious session manipulation headers

## Variant hunting
Researchers should examine other Progress products for similar session variable manipulation vulnerabilities. The SSRF-to-internal-endpoint pattern should be searched for in other web-based file transfer solutions. Native DLL files like MOVEitISAPI.dll warrant additional reverse engineering to identify other potential code execution vectors or authentication bypass mechanisms. Look for similar pre-authentication endpoints that might accept header-based session manipulation in other versions or related products.

## MITRE ATT&CK
- T1190
- T1190
- T1190
- T1556
- T1548
- T1078
- T1190
- T1021

## Notes
The researchers responsibly withheld the full proof-of-concept until either public disclosure occurred or 30 days had passed to allow organizations time to patch. Patch diffing proved highly effective for vulnerability analysis in .NET applications using ILSpy decompilation. The challenge of obtaining unpatched versions was overcome through historical CDN enumeration. Native binary components (MOVEitISAPI.dll) required Ghidra for reverse engineering, indicating a multi-tool approach was necessary. This vulnerability was actively exploited in the wild during the research, demonstrating the high-value nature of pre-authentication RCE in enterprise appliances.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
