# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the /MOVEitISAPI/MOVEitISAPI.dll endpoint. The vulnerability exists in the machine2.aspx page handler where user-supplied input from X-siLock-* headers is inadequately sanitized before being used in SQL queries.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request passes validation checks and is forwarded to /machine2.aspx endpoint
3. Machine2Main method processes the request and extracts user-supplied data via CrackInput method from X-siLock-* headers
4. Despite sanitization attempts in CrackInput, malicious SQL payload in headers bypasses validation filters
5. SQL injection payload is executed in database query, allowing attacker to extract data or escalate privileges
6. Attacker chains SQL injection with file upload endpoints to achieve remote code execution on the server

## Root cause
The CrackInput method in SILMachine2 class implements insufficient input validation and sanitization of X-siLock-* headers. Although header values are extracted and processed, the sanitization logic contains bypasses that allow SQL injection payloads to reach database queries without proper parameterization or escaping.

## Attacker mindset
Opportunistic vulnerability researcher/APT identifying unauthenticated RCE in widely-deployed file transfer software. The active exploitation in the wild prior to public disclosure indicates sophisticated threat actors leveraging this for initial access and lateral movement in enterprise environments.

## Defensive takeaways
- Use parameterized queries and prepared statements exclusively for all database operations to prevent SQL injection
- Implement allowlist-based validation for critical headers rather than blacklist-based sanitization
- Apply defense-in-depth: validate input, use stored procedures with minimal privileges, and implement database activity monitoring
- Maintain strict separation between authentication/authorization checks and data processing logic
- Conduct binary diffing during patching to identify and review changed code paths comprehensively
- Implement Web Application Firewall (WAF) rules to detect and block X-siLock-* header abuse patterns
- Deploy network segmentation to limit impact of RCE on file transfer systems

## Variant hunting
Search for similar patterns in other Progress products and ISAPI-based applications. Hunt for other endpoints using X-siLock-* header validation. Examine all transaction types in SILMachine2 for similar SQL injection patterns. Review other .aspx page handlers that call legacy machine code through ISAPI bridges. Check for similar header-extraction patterns in other DLL modules.

## MITRE ATT&CK
- T1190
- T1190
- T1037
- T1547
- T1071
- T1087
- T1583

## Notes
The researchers were unable to find differences between patched and unpatched MOVEitISAPI.dll versions using BinDiff, indicating the SQL injection likely resides in managed .NET code (SILMachine2) rather than native code. The exploitation chain required reverse engineering both native and managed components. This vulnerability became widely exploited (ALPHV/BlackCat, Cl0p) and was a major supply-chain attack vector in 2023. The X-siLock-Transaction header validation using string comparison for 'folder_add_by_path' was a critical control that determined code path execution.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
