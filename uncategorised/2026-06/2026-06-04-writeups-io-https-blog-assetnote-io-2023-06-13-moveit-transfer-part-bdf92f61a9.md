# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical remote code execution vulnerability in MOVEit Transfer that leverages SQL injection through the /machine2.aspx endpoint. The vulnerability allows unauthenticated attackers to execute arbitrary SQL commands and achieve remote code execution by crafting malicious requests with specific X-siLock headers.

## Attack scenario (step by step)
1. Attacker sends initial request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 endpoint with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request passes through to /machine2.aspx which processes X-siLock-* headers via CrackInput method
3. Attacker crafts SQL injection payload in one of the extracted header parameters that bypasses sanitization checks
4. Injected SQL command is executed against the backend database, allowing data exfiltration or database modification
5. Attacker leverages database access to upload malicious files through /api/v1/folders/{id}/files endpoints
6. Uploaded files achieve remote code execution on the MOVEit Transfer server

## Root cause
Insufficient input validation and sanitization in the CrackInput method of SILMachine2 class when processing X-siLock-* headers. The machine2.aspx endpoint fails to properly sanitize user-supplied data before incorporating it into SQL queries, allowing SQL injection attacks.

## Attacker mindset
Methodical reverse engineering approach: identify entry points via endpoint analysis, use binary diffing to locate vulnerability source, decompile .NET assemblies with dnSpy to trace data flow, and identify sanitization bypass in header processing. Attacker seeks pre-authentication RCE for maximum impact on widely-deployed software.

## Defensive takeaways
- Implement parameterized queries/prepared statements for all database operations to prevent SQL injection
- Apply whitelist-based input validation for all HTTP headers, not just blacklist approaches
- Use binary diffing and comparison of patched vs unpatched versions during security updates
- Implement proper authentication checks before processing sensitive operations like folder/file management
- Apply defense-in-depth: even if one sanitization is bypassed, subsequent layers should catch attacks
- Monitor and log all requests to /machine2.aspx endpoint for suspicious X-siLock header patterns
- Conduct thorough code review of custom protocol handlers and header processing logic
- Use Web Application Firewall (WAF) rules to detect SQL injection patterns in HTTP headers

## Variant hunting
Search for similar custom header processing in other Progress products; examine other ASP.NET endpoints with X-* header parsing; look for CrackInput-like methods in other managed code assemblies; search for folder_add_by_path string across codebase for related functionality; test other transaction types beyond folder_add_by_path for similar bypass techniques

## MITRE ATT&CK
- T1190
- T1071
- T1087
- T1078
- T1020
- T1105
- T1486

## Notes
This is Part Two of Assetnote's analysis released after public PoC disclosure. The vulnerability required reverse engineering both native (Ghidra) and managed (.NET/dnSpy) code. Initial investigation ruled out MOVEitISAPI.dll through BinDiff comparison, leading researchers to focus on machine2.aspx. The X-siLock-Transaction header value 'folder_add_by_path' is a critical requirement to reach vulnerable code path. This was an actively exploited vulnerability in the wild before detailed analysis was published.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
