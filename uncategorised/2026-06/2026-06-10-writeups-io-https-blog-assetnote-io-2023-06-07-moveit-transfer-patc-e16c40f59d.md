# MOVEIt Transfer RCE via SQL Injection and Arbitrary Session Variable Setting (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Progress MOVEIt Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Arbitrary Session Variable Setting, Server-Side Request Forgery (SSRF), Remote Code Execution, Pre-authentication RCE
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
CVE-2023-34362 is a critical pre-authentication RCE vulnerability in Progress MOVEIt Transfer affecting versions prior to 2023.0.1. The vulnerability chain involves arbitrary session variable manipulation via request headers combined with SSRF to access internal pages and SQL injection, ultimately leading to remote code execution. Assetnote reverse-engineered the exploit chain through patch diffing analysis.

## Attack scenario (step by step)
1. Attacker sends HTTP request with malicious headers to MOVEIt Transfer instance
2. Request headers are used to set arbitrary session variables in the application
3. Attacker exploits SSRF to call internal machine2.aspx page that should only be accessible internally
4. Internal page interaction allows attacker to inject SQL payloads
5. SQL injection queries execute on the backend database
6. RCE payload is executed through database interactions or subsequent code execution

## Root cause
The patched version removed vulnerable code that allowed arbitrary session variables to be set based on HTTP request headers. Combined with insufficient access controls on internal pages and improper SQL query parameterization, this created an exploitation chain from pre-authentication to RCE.

## Attacker mindset
Threat actors likely discovered the session variable manipulation capability during reconnaissance or vulnerability scanning, recognized it could bypass authentication constraints via SSRF, and chained it with SQL injection to achieve database and system-level code execution without requiring valid credentials.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers, especially those that affect session management
- Enforce proper access controls on internal-only pages; do not rely solely on network segmentation
- Use parameterized queries and prepared statements for all database interactions to prevent SQL injection
- Apply principle of least privilege to application service accounts and database permissions
- Disable or restrict SSRF-prone functionality; validate and whitelist all URL destinations
- Implement Web Application Firewall (WAF) rules to detect suspicious header patterns and SQL injection attempts
- Require authentication for all endpoints, including those intended for internal use
- Maintain security patching cadence and monitor for patch releases closely

## Variant hunting
Researchers should examine: (1) Other Progress products for similar session variable manipulation patterns, (2) Different request header injection vectors in MOVEIt, (3) Alternative SSRF entry points or internal pages not yet discovered, (4) Related SQL injection patterns in database interaction layers, (5) Version-specific differences in access control implementations across MOVEIt releases

## MITRE ATT&CK
- T1190
- T1190
- T1052
- T1105
- T1059
- T1555
- T1219
- T1598

## Notes
This vulnerability was actively exploited in the wild at the time of disclosure (June 2023). Assetnote responsibly withheld proof-of-concept code for 30 days to allow organizations time to patch. The vulnerability required sophisticated patch diffing and reverse engineering using tools like DiffMerge, ILSpy, and Ghidra. The exploitation chain demonstrates how multiple moderate vulnerabilities can be chained to create critical impact. The native binary MOVEitISAPI.dll component required Ghidra analysis, suggesting potential additional complexity not fully detailed in this writeup.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
