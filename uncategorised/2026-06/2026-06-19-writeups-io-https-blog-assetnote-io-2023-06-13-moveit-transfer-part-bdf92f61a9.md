# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** CRITICAL
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the /machine2.aspx endpoint. The vulnerability exists in the CrackInput method which fails to properly sanitize user-supplied input from X-siLock-* headers, enabling attackers to bypass authentication and execute arbitrary SQL commands that ultimately lead to RCE.

## Attack scenario (step by step)
1. Attacker crafts a request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is forwarded to /machine2.aspx endpoint which instantiates SILMachine2 class and calls Machine2Main method
3. Attacker supplies malicious SQL injection payload in X-siLock-* headers
4. CrackInput method extracts headers but fails to properly sanitize the injected payload
5. SQL injection is executed against the backend database via improperly parameterized queries
6. Attacker achieves remote code execution through SQL Server xp_cmdshell or CLR integration

## Root cause
The CrackInput method in the SILMachine2 class extracts user-controlled data from X-siLock-* HTTP headers and passes it to SQL queries without proper input validation or parameterized statements. The security check requiring X-siLock-Transaction header value to equal 'folder_add_by_path' provides insufficient protection as it only validates header presence, not content sanitization of subsequent injection vectors.

## Attacker mindset
Attacker identified that MOVEit Transfer was actively being exploited and conducted binary diffing between patched and unpatched DLLs to locate the vulnerability. They used static analysis and reverse engineering to map the request chain, identify the vulnerable code path through the /machine2.aspx handler, and discover the SQL injection in the CrackInput method which processes unsanitized headers.

## Defensive takeaways
- Always use parameterized queries or prepared statements for all database operations, never concatenate user input into SQL strings
- Implement defense-in-depth: validate header presence AND sanitize/validate header content separately
- Conduct regular security code reviews specifically targeting header handling, input validation, and database query construction
- Use static analysis tools and binary diffing on security patches to understand vulnerability root causes
- Apply principle of least privilege to service accounts executing database queries
- Implement Web Application Firewall (WAF) rules to detect SQL injection patterns in HTTP headers
- Monitor and log suspicious header patterns and database query execution anomalies

## Variant hunting
Search for similar patterns in other Progress products using X-siLock headers; examine other ASPX handlers that accept X-siLock-* headers; review CrackInput implementations across codebase; identify other endpoints that forward requests through machine2.aspx; look for similar header-based authentication bypass patterns in ShareFile and other file transfer products

## MITRE ATT&CK
- T1190
- T1083
- T1059
- T1021
- T1569

## Notes
This is the second part of Assetnote's MOVEit research where they declined to publish the full exploit chain during active exploitation. Binary diffing between patched/unpatched versions revealed no differences in MOVEitISAPI.dll, indicating the vulnerability was in downstream .NET code (machine2.aspx). The X-siLock-Transaction header requirement is a weak access control mechanism. Public POCs were released after their initial post, allowing them to publish detailed reversing methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
