# MOVEit Transfer RCE - CVE-2023-34362: SQL Injection and Pre-Authentication Remote Code Execution

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Setting, Server-Side Request Forgery (SSRF), Pre-Authentication Vulnerability
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer allows unauthenticated attackers to execute arbitrary code through a combination of SQL injection and session variable manipulation. The vulnerability exploits unvalidated header input that sets session variables, leading to RCE via an SSRF chain through internal-only endpoints like machine2.aspx.

## Attack scenario (step by step)
1. Attacker sends a crafted HTTP request with malicious headers to the MOVEitISAPI.dll endpoint without authentication
2. The vulnerable code processes the header input and sets arbitrary session variables based on attacker-controlled data
3. Attacker leverages session variable manipulation to inject SQL commands into database queries
4. SQL injection payload executes within the database context, potentially retrieving sensitive data or modifying records
5. Attacker chains the exploit with SSRF to access internal endpoint machine2.aspx that should only be callable from internal network
6. SSRF combined with session manipulation results in code execution on the server

## Root cause
The application accepts and processes HTTP headers to set session variables without proper validation or sanitization. This unvalidated input directly influences SQL queries and internal request routing, allowing attackers to manipulate application state and execute arbitrary code pre-authentication.

## Attacker mindset
An attacker would recognize that pre-authentication vulnerabilities in file transfer software are high-value targets. By identifying that session variables are controllable via headers, they can chain multiple techniques (SQL injection + SSRF) to achieve unauthenticated RCE without needing valid credentials.

## Defensive takeaways
- Never trust HTTP headers for setting session state or security-critical variables without strict validation
- Implement allowlisting for any header values used in database queries or internal routing logic
- Apply input validation and parameterized queries to prevent SQL injection regardless of input source
- Enforce authentication boundaries - ensure internal-only endpoints cannot be accessed via SSRF chains
- Regularly perform patch diffing on security updates to understand what was being exploited
- Disable or restrict direct access to ISAPI handlers and DLL endpoints from untrusted networks

## Variant hunting
Search for other Progress MOVEit Transfer versions and features that accept HTTP headers for session management. Look for similar patterns where headers control SQL query construction or internal request routing. Examine other ISAPI DLL endpoints for similar session variable setting vulnerabilities. Check if other file transfer applications use similar header-based session initialization patterns.

## MITRE ATT&CK
- T1190
- T1190
- T1566
- T1595
- T1598
- T1039
- T1548

## Notes
This vulnerability was actively exploited in the wild before patches became widely available. The researchers demonstrated excellent methodology: obtaining both patched and unpatched versions through trial downloads and URL manipulation, performing binary diffing, decompiling .NET assemblies with ILSpy, and reverse engineering native DLLs with Ghidra. The vulnerability chains multiple weaknesses (header validation + SQL injection + SSRF) into a critical RCE. The responsible disclosure approach involved withholding full PoC details for 30 days to allow organizations time to patch.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
