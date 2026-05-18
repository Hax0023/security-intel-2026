# MOVEit Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Server-Side Request Forgery (SSRF), Arbitrary Session Variable Injection
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer allows attackers to execute arbitrary code through a combination of SQL injection and session variable manipulation. The vulnerability stems from improper handling of user-supplied headers that can arbitrarily set session variables, which are subsequently used in unsafe SQL queries.

## Attack scenario (step by step)
1. Attacker discovers MOVEit Transfer exposed on external internet without authentication required
2. Attacker crafts malicious HTTP request with specially crafted headers to inject arbitrary session variables
3. Session variables are set without proper validation or sanitization of user input
4. Injected session variables are used in SQL queries without parameterization, enabling SQL injection
5. SQL injection payload executes system commands or modifies database records to achieve code execution
6. Attacker gains remote code execution on the MOVEit Transfer server with application privileges

## Root cause
The application accepts and processes arbitrary session variables from user-supplied HTTP headers without validation. These unvalidated session variables are subsequently used in SQL queries without proper parameterization or prepared statements, enabling SQL injection attacks that can lead to RCE.

## Attacker mindset
Opportunistic attacker targeting widely-deployed file transfer software with pre-authentication access. The simplicity of the exploitation vector (header manipulation) combined with critical impact (RCE) makes this highly attractive for mass exploitation campaigns.

## Defensive takeaways
- Never accept session variables or security-critical parameters from user-supplied input (headers, query strings, cookies)
- Always use parameterized queries and prepared statements for all database operations
- Implement strict input validation and sanitization for all external inputs
- Apply principle of least privilege - restrict access to sensitive functionality and validate authentication on all endpoints
- Monitor for suspicious header manipulation and session variable modifications in security logs
- Maintain an inventory of critical software and implement rapid patching processes
- Implement network segmentation to isolate file transfer services from direct internet exposure

## Variant hunting
Search for similar patterns in other Progress products and file transfer applications: Check for unauthenticated endpoints accepting headers that influence session state; Look for unsafe use of session variables in SQL queries across codebase; Examine ASPX pages for improper access controls; Audit custom header processing in web applications

## MITRE ATT&CK
- T1190
- T1190 - Exploit Public-Facing Application
- T1190 - SQL Injection
- T1548 - Abuse Elevation Control Mechanism
- T1552 - Unsecured Credentials

## Notes
Active exploitation observed in the wild during research. Patch diffing methodology used: install vulnerable and patched versions, compare DLL changes via DiffMerge, decompile with ILSpy, reverse engineer native binaries with Ghidra. Researchers noted the vulnerability chain involved MOVEitISAPI.dll (native binary), machine2.aspx (internal network bypass), and SSRF component. Responsible disclosure timeline: 30 days before public PoC release or until public PoC available. The vulnerability is pre-authentication, making it wormable and suitable for rapid automated exploitation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
