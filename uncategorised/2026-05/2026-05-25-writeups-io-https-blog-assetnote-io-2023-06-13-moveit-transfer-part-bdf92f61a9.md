# MOVEit Transfer RCE Part Two (CVE-2023-34362) - SQL Injection via machine2.aspx

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer's machine2.aspx endpoint that allows unauthenticated remote code execution. The vulnerability exists in the X-siLock-Transaction header processing with the 'folder_add_by_path' transaction type, bypassing authentication and enabling arbitrary SQL queries to be executed against the database.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is forwarded to /machine2.aspx endpoint which processes the transaction type
3. Attacker crafts malicious SQL injection payload in X-siLock-* headers, bypassing input validation in CrackInput method
4. SQL injection payload is passed to backend database query without proper parameterization
5. Attacker uses stacked queries or UNION-based injection to execute arbitrary SQL commands
6. Attacker achieves remote code execution through SQL Server extended stored procedures or CLR integration

## Root cause
Insufficient input validation and sanitization in the CrackInput method of SILMachine2 class combined with the use of dynamic SQL queries instead of parameterized queries. The X-siLock-Transaction header validation only checks for specific transaction type strings but does not properly validate subsequent header parameters used in SQL operations.

## Attacker mindset
An attacker would recognize that unauthenticated endpoints processing transaction headers with special types like 'folder_add_by_path' could bypass authentication. By analyzing the header processing logic through binary diffing between patched/unpatched versions and reverse engineering the DLL, they would identify that input validation is insufficient for X-siLock-* headers and that these values flow directly into SQL queries without proper parameterization, enabling injection attacks.

## Defensive takeaways
- Always use parameterized queries/prepared statements for all database operations, never construct dynamic SQL strings
- Implement strict input validation on all headers, especially those used in backend queries - validate type, length, and character sets
- Apply defense-in-depth: validate at multiple layers and ensure unauthenticated endpoints do not bypass security controls
- Conduct binary diffing and code review between patched and unpatched versions to ensure all instances of vulnerable patterns are fixed
- Implement least privilege database accounts that restrict stored procedure execution and file system access
- Monitor for suspicious SQL patterns in logs, particularly those containing UNION, stacked queries, or extended stored procedure calls
- Use Web Application Firewalls to block common SQL injection patterns in headers

## Variant hunting
Search for other endpoints accepting X-siLock-* headers in MOVEitISAPI.dll and other .NET components. Examine other transaction types beyond 'folder_add_by_path' that may have similar SQL injection vulnerabilities. Review all user-controlled input flowing into database queries in machine2.aspx and related modules. Check for similar patterns in other Progress products using the MOVEit framework.

## MITRE ATT&CK
- T1190
- T1059
- T1021
- T1106
- T1547

## Notes
This vulnerability was actively exploited in the wild before the public POC was released. The researchers used binary diffing to compare patched and unpatched DLLs but found no differences in MOVEitISAPI.dll, correctly deducing the vulnerability was in machine2.aspx/.NET components instead. The bypass of authentication through the folder_add_by_path transaction type is particularly notable as it allows completely unauthenticated SQL injection. The use of Ghidra for native code analysis and dnSpy for .NET decompilation demonstrates a comprehensive reverse engineering approach.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
