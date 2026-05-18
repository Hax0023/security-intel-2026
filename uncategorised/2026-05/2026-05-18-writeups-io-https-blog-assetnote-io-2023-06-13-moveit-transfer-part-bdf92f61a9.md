# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in Progress MOVEit Transfer that allows unauthenticated remote code execution through the /machine2.aspx endpoint. The vulnerability exists in the CrackInput method which insufficiently sanitizes X-siLock-* headers, enabling attackers to inject SQL commands and achieve RCE.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path' to bypass the initial transaction check
2. Request is forwarded to /machine2.aspx endpoint which calls Machine2Main method in SILMachine2 class
3. Attacker crafts malicious X-siLock-* headers containing SQL injection payload targeting the CrackInput method's insufficient sanitization
4. SQL injection payload executes through POST to /guestaccess.aspx or subsequent API endpoints
5. Attacker obtains authentication token via /api/v1/token endpoint using injected credentials
6. Attacker uploads and executes malicious file through /api/v1/folders/{id}/files resumable upload endpoints for RCE

## Root cause
The CrackInput method in SILMachine2 class insufficiently sanitizes user-controlled X-siLock-* headers before using them in SQL queries. The initial validation only checks for the X-siLock-Transaction header value 'folder_add_by_path' but does not properly validate subsequent header contents, allowing SQL injection through crafted header values.

## Attacker mindset
An attacker would recognize that the X-siLock-* header parsing logic is the gateway to the vulnerability. By identifying that the transaction type check is the only access control, they would focus on fuzzing header values to find injection points. The presence of multiple endpoints in the exploit chain suggests the attacker is chaining SQL injection with API abuse to achieve file upload and code execution.

## Defensive takeaways
- Implement parameterized queries/prepared statements for all database operations instead of string concatenation
- Apply input validation and sanitization consistently across all user-controlled inputs including HTTP headers
- Use allowlisting for expected header values rather than blocklisting dangerous patterns
- Implement proper authentication and authorization checks before processing file uploads
- Apply principle of least privilege to service accounts executing database queries
- Monitor for suspicious X-siLock-* header patterns and SQL error messages in logs
- Implement Web Application Firewall (WAF) rules to detect SQL injection patterns in headers
- Regular security testing including binary diffing of patched versions to understand vulnerability scope

## Variant hunting
Search for similar insufficient header validation in other ISAPI DLL endpoints, particularly those handling machine-to-machine communication. Examine other ASP.NET endpoints that parse custom headers without proper parameterized queries. Review any legacy code paths that may bypass the main /machine2.aspx validation logic. Check for similar vulnerabilities in other Progress products using ISAPI DLLs.

## MITRE ATT&CK
- T1190
- T1190.031
- T1589
- T1592
- T1098
- T1652

## Notes
This writeup documents the reverse engineering methodology used to understand an actively exploited vulnerability. The researchers used Ghidra for binary analysis and dnSpy for .NET decompilation. Binary diffing between patched and unpatched versions provided insights into the vulnerability location. The exploit chain involves multiple endpoints and requires careful header crafting to bypass initial validation checks. Public PoC availability enabled responsible disclosure of full technical details.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
