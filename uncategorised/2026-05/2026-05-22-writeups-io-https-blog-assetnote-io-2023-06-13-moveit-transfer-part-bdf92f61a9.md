# MOVEit Transfer RCE (CVE-2023-34362) - Part Two: Reverse Engineering & SQL Injection Discovery

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Progress Software MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass, Improper Input Validation
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
Asetnote researchers reverse-engineered the CVE-2023-34362 RCE vulnerability in MOVEit Transfer by analyzing both patched and unpatched DLL versions using Ghidra and dnSpy. The vulnerability exists in the /machine2.aspx endpoint where user-supplied input passed through X-siLock-* headers is inadequately sanitized before being used in SQL queries. By crafting a malicious request with the folder_add_by_path transaction header, an unauthenticated attacker can inject arbitrary SQL commands and achieve remote code execution.

## Attack scenario (step by step)
1. Attacker sends initial request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to folder_add_by_path
2. Request is forwarded to /machine2.aspx endpoint which instantiates SILMachine2 class and calls Machine2Main method
3. The CrackInput method extracts and processes X-siLock-* headers, but fails to properly sanitize user-controlled input
4. Attacker injects SQL commands through unsanitized header values that are concatenated into database queries
5. SQL injection payload is executed, potentially allowing database enumeration, modification, or code execution
6. Attacker leverages database access to execute system commands via SQL Server features (xp_cmdshell) or write files to achieve RCE

## Root cause
The CrackInput method in the SILMachine2 class extracts user-controlled data from X-siLock-* headers and applies insufficient input validation/sanitization before using these values in SQL queries. The developers assumed that data passed through custom headers would be trusted, creating a blind spot in the security validation logic.

## Attacker mindset
An attacker analyzing publicly available POCs and server logs would identify the request chain and work backwards through decompiled code to find the injection point. By comparing patched vs unpatched DLL versions and examining the message "Passing along user's request to machine2", they would systematically trace the data flow to locate where headers are processed without proper escaping, enabling SQL injection attacks.

## Defensive takeaways
- Never assume custom headers are inherently safe—apply the same input validation to all user-controlled input regardless of source
- Use parameterized queries/prepared statements for all database operations to prevent SQL injection
- Implement input validation whitelisting rather than blacklisting for security-critical operations
- Apply defense-in-depth: validate at multiple layers (HTTP handler, business logic, database driver)
- Regularly diff patched vs unpatched code to identify what security flaws were fixed and ensure complete remediation
- Monitor for unusual X-siLock-* header usage patterns in web logs as an indicator of exploitation attempts
- Restrict database user permissions to minimize damage from SQL injection (principle of least privilege)

## Variant hunting
Search for other endpoints using X-siLock-* headers without proper sanitization; examine other ASPX page handlers that process custom headers; look for similar patterns where HTTP headers are directly concatenated into SQL queries; review other transaction types beyond folder_add_by_path that may have the same vulnerability; check if other Progress products use similar header-based parameter passing mechanisms

## MITRE ATT&CK
- T1190
- T1098
- T1565
- T1005
- T1021

## Notes
This vulnerability was actively exploited in the wild before public POCs were released. The use of BinDiff to compare patched and unpatched DLLs was a key technique that helped rule out MOVEitISAPI.dll as the vulnerability location. The researchers demonstrate excellent reverse engineering methodology: starting with known endpoints from logs, using string analysis to find relevant code sections, and tracing data flow through decompilation tools. The vulnerability's criticality stems from pre-authentication RCE capability with no user interaction required.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
