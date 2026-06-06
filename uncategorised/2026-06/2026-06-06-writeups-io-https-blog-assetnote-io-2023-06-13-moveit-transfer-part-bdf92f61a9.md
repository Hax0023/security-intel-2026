# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Unsafe Deserialization
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the /MOVEitISAPI/MOVEitISAPI.dll endpoint. The vulnerability exists in the machine2.aspx handler where user-supplied input from X-siLock-* headers is improperly sanitized before being used in SQL queries.

## Attack scenario (step by step)
1. Attacker sends initial request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction: folder_add_by_path header
2. Request is passed through to /machine2.aspx handler which processes the X-siLock-* headers via CrackInput method
3. Attacker crafts malicious SQL injection payload in unsanitized header parameters
4. SQL injection is executed against the database, allowing data extraction or further exploitation
5. Attacker chains exploitation with file upload endpoints (/api/v1/folders/{id}/files?uploadType=resumable) to achieve RCE
6. Attacker gains code execution on the MOVEit Transfer server

## Root cause
The CrackInput method in SILMachine2 class extracts user-supplied data from X-siLock-* HTTP headers and uses them in SQL queries without proper parameterization or sanitization. The vulnerability is in /machine2.aspx handler which processes these headers unsafely.

## Attacker mindset
Attacker identified an unauthenticated entry point through the ISAPI interface that could be leveraged to bypass authentication. By chaining SQL injection with file upload capabilities, complete server compromise becomes achievable without any credentials.

## Defensive takeaways
- Always use parameterized queries or prepared statements for all database operations
- Validate and sanitize all HTTP headers, not just common ones
- Implement whitelist-based header validation rather than relying on blacklist approaches
- Perform binary diffing between patched and unpatched versions to identify subtle changes
- Apply principle of least privilege to unauthenticated endpoints
- Monitor for requests with X-siLock-* headers and folder_add_by_path transactions
- Implement Web Application Firewall rules to detect SQL injection patterns in HTTP headers

## Variant hunting
Similar SQL injection vulnerabilities likely exist in other ASPX handlers that process X-siLock-* headers. Review all handlers that call CrackInput or similar header parsing methods. Check for other unauthenticated ISAPI endpoints that bypass authentication controls. Examine file upload mechanisms for chaining opportunities.

## MITRE ATT&CK
- T1190
- T1059
- T1190
- T1055
- T1083
- T1020

## Notes
This is Part Two of MOVEit Transfer vulnerability research. The exploit chain requires multiple endpoints working together. BinDiff comparison between patched/unpatched versions showed no obvious differences in MOVEitISAPI.dll, suggesting the vulnerability was in a different assembly. The X-siLock-Transaction header with folder_add_by_path value is a critical requirement to reach vulnerable code path. Public PoC became available before full details were published, allowing this detailed analysis.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
