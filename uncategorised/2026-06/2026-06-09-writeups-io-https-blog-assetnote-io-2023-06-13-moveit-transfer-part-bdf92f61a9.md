# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the machine2.aspx endpoint. The vulnerability exists in the X-siLock-* header processing where user input is insufficiently sanitized before being used in SQL queries.

## Attack scenario (step by step)
1. Attacker crafts a request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 endpoint with X-siLock-Transaction header set to 'folder_add_by_path'
2. The ISAPI handler validates the transaction type and routes the request to /machine2.aspx without proper validation
3. Attacker submits a POST request to /machine2.aspx with malicious SQL injection payload embedded in X-siLock-* headers
4. The CrackInput method extracts headers but fails to properly sanitize the injected SQL payload
5. The unsanitized input is concatenated into an SQL query and executed against the backend database
6. Attacker achieves code execution through SQL injection, potentially uploading webshells via the file upload endpoints

## Root cause
Insufficient input validation and sanitization of X-siLock-* headers in the CrackInput method of the SILMachine2 class. While the code shows header extraction logic, the actual SQL query construction uses these headers without proper parameterized queries or escaping, allowing SQL injection.

## Attacker mindset
Attackers exploited a pre-authentication entry point in a widely deployed enterprise file transfer application. By analyzing the request chain from public logs, they identified the vulnerable parameter handling in custom headers and leveraged SQL injection for unauthenticated RCE, making this a high-value target for mass exploitation.

## Defensive takeaways
- Always use parameterized queries/prepared statements for all database operations, never concatenate user input directly into SQL
- Implement strict input validation on all HTTP headers, not just body parameters
- Apply defense-in-depth: validate at multiple layers (ISAPI filter, ASP.NET, database)
- Use allowlists for transaction types and header names rather than blacklists
- Implement Web Application Firewall (WAF) rules to detect SQL injection patterns in custom headers
- Conduct binary diffing between patched and unpatched versions during security reviews
- Sanitize all user-controlled input even when passed through internal APIs

## Variant hunting
Search for similar custom header processing in other Progress products (MOVEit Automation, MOVEit Central). Look for other ISAPI filters or ASP.NET handlers that extract data from X-siLock-* or similar proprietary headers and pass to database queries. Examine any endpoints that accept transaction type parameters without strict validation.

## MITRE ATT&CK
- T1190
- T1059
- T1057
- T1105
- T1133
- T1003

## Notes
This vulnerability was actively exploited in the wild before public PoC disclosure. The researchers used binary diffing between patched/unpatched versions of MOVEitISAPI.dll to narrow down the vulnerability location. The attack chain involves multiple endpoints working together, with the initial entry point at the ISAPI filter level bypassing authentication. The use of custom X-siLock-* headers suggests this is security-through-obscurity rather than proper security controls. Reverse engineering via Ghidra and dnSpy was critical to understanding the exploitation path.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
