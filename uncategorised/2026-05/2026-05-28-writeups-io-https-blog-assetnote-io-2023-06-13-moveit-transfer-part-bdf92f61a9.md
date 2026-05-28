# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
A SQL injection vulnerability in MOVEit Transfer's machine2.aspx endpoint allows unauthenticated attackers to execute arbitrary code. The vulnerability exists in the X-siLock-Transaction header processing chain which accepts 'folder_add_by_path' transactions without proper input validation, leading to SQL injection in database queries.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is forwarded to /machine2.aspx which calls Machine2Main on SILMachine2 class
3. CrackInput method extracts headers but insufficiently sanitizes SQL injection payloads in certain parameters
4. Attacker crafts malicious SQL injection payload in X-siLock-* headers to manipulate database queries
5. SQL injection allows attacker to execute arbitrary database commands or extract sensitive data
6. Combined with file upload endpoints (/api/v1/folders/{id}/files?uploadType=resumable), attacker achieves RCE

## Root cause
Insufficient input validation and sanitization of X-siLock-* headers in the CrackInput method of SILMachine2.Machine2Main. The application accepts 'folder_add_by_path' transactions without proper parameterization of SQL queries, allowing injection of arbitrary SQL syntax.

## Attacker mindset
Exploit unauthenticated access to machine2.aspx endpoint by leveraging transaction type validation bypass. Craft headers that pass basic security checks but inject SQL when processed by database layer. Chain SQL injection with resumable file upload API to achieve code execution on the server.

## Defensive takeaways
- Use parameterized queries/prepared statements for all SQL operations regardless of header source
- Implement strict input validation on all X-siLock-* headers with whitelisting rather than blacklisting
- Apply authentication and authorization checks before processing any transaction types
- Separate validation logic in CrackInput from database query execution with clear data boundaries
- Conduct security code review of ISAPI handler and all authentication bypass paths
- Implement Web Application Firewall (WAF) rules to detect SQL injection patterns in headers
- Regular binary diffing between patched and vulnerable versions to identify subtle fixes
- Monitor for requests to /MOVEitISAPI/MOVEitISAPI.dll with folder_add_by_path transactions

## Variant hunting
Search for similar unauthenticated endpoints in Progress products that accept transaction-type headers. Examine other X-siLock-* header handling in different .aspx pages. Look for similar SQL injection patterns in other file transfer or folder management operations. Check for other transaction types beyond 'folder_add_by_path' that may bypass authentication.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1027 - Obfuscated Files or Information (SQL injection obfuscation)
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts (authentication bypass)
- T1505 - Server Software Component
- T1059 - Command and Scripting Interpreter

## Notes
This is the second part of a two-part analysis. Researchers initially withheld full exploit details due to active exploitation. The vulnerability requires reverse engineering of both the ISAPI DLL and .NET assemblies using Ghidra and dnSpy. The attack chain involves multiple endpoints and header manipulation. BinDiff showed no discernible differences between patched and unpatched MOVEitISAPI.dll, suggesting the patch may be in other components. The X-siLock-Transaction header validation is the key bypass mechanism.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
