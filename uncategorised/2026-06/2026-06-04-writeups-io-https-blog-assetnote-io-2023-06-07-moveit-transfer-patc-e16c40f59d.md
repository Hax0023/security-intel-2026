# MOVEIt Transfer RCE - CVE-2023-34362: Patch Diffing Analysis and Exploit Chain Discovery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Progress MOVEIt Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Assignment, Server-Side Request Forgery (SSRF)
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
Assetnote reverse-engineered CVE-2023-34362, a critical pre-authentication RCE vulnerability in Progress MOVEIt Transfer, through systematic patch diffing between vulnerable (2023.0.0) and patched (2023.0.1) versions. The vulnerability chain involves arbitrary session variable assignment via request headers, SSRF to call internal endpoints, SQL injection, and ultimately remote code execution. The researchers identified the vulnerable code removal in patched DLLs and traced the exploitation path through machine2.aspx and MOVEitISAPI.dll.

## Attack scenario (step by step)
1. Attacker sends crafted HTTP request with malicious headers to publicly accessible MOVEIt Transfer instance
2. Vulnerable code in patched-out function allows arbitrary session variable assignment from request headers
3. Attacker leverages SSRF vulnerability to call internal machine2.aspx endpoint that is normally restricted
4. SQL injection payload is injected through the established session context
5. Malicious SQL query executes on the backend database
6. Remote code execution is achieved through SQL injection, allowing arbitrary command execution on the server

## Root cause
Code in the wwwroot/bin DLL files allowed arbitrary assignment of session variables based on request header input without proper validation or authentication checks. This unsafe session variable assignment, combined with SSRF capability and downstream SQL injection in machine2.aspx, created a pre-authentication RCE vulnerability.

## Attacker mindset
Exploit critical pre-authentication vulnerabilities affecting widely-deployed software for maximum impact and speed. The attacker likely used public indicators (exploitation logs referencing MOVEitISAPI.dll) and quickly weaponized the vulnerability once disclosed, exploiting organizations before patches could be deployed.

## Defensive takeaways
- Implement strict input validation for all request headers and never use them to directly set session variables
- Apply defense-in-depth controls: validate session variable assignments, restrict internal endpoints with proper authentication, and sanitize all database inputs
- Monitor for SSRF patterns in web applications and restrict outbound connections from web application processes
- Conduct comprehensive code review and security testing of session management mechanisms
- Deploy network segmentation to prevent exploitation chains that rely on accessing internal endpoints
- Prioritize patching of critical pre-authentication RCE vulnerabilities immediately
- Implement Web Application Firewalls with rules detecting session variable injection attempts

## Variant hunting
Researchers should examine other Progress software products for similar session variable assignment patterns in request header processing. Look for other endpoints with weak SSRF protections that could be chained with session manipulation. Check for similar SQL injection points downstream from session variable usage.

## MITRE ATT&CK
- T1190
- T1190: Exploit Public-Facing Application
- T1021.1: Remote Services - RDP
- T1090.2: Proxy - External Proxy
- T1570: Lateral Tool Transfer
- T1505: Server Software Component
- T1505.001: Server Software Component - Web Shell

## Notes
This was an active 0-day being exploited in-the-wild. Assetnote responsibly withheld PoC release for 30 days to allow organizations patching time. The vulnerability demonstrates the value of patch diffing as a vulnerability research technique. The researchers leveraged publicly available software trials and accessible CDN URLs to obtain both vulnerable and patched versions. The exploitation chain is multi-stage: unauthenticated session hijacking → SSRF → SQL injection → RCE.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
