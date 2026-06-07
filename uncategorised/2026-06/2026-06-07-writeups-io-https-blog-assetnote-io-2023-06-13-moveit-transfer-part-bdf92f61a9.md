# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
A critical SQL injection vulnerability in MOVEit Transfer's machine2.aspx endpoint allows unauthenticated remote code execution through crafted X-siLock-* headers. The vulnerability exists in the CrackInput method's header parsing and sanitization logic, enabling attackers to execute arbitrary SQL commands and achieve full system compromise.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is routed to /machine2.aspx handler which instantiates SILMachine2 class and calls Machine2Main method
3. Machine2Main processes request through CrackInput method which extracts and sanitizes X-siLock-* headers
4. Attacker injects SQL payload in unsanitized header field that bypasses sanitization logic
5. SQL injection executes in database context, allowing data exfiltration or stored procedure execution
6. Attacker escalates to RCE through SQL Server xp_cmdshell or similar stored procedures

## Root cause
Insufficient input validation and sanitization in the CrackInput method when processing X-siLock-* headers. While headers were supposedly sanitized, the sanitization logic contained bypasses or inconsistencies that allowed SQL injection payloads to reach the database query construction code.

## Attacker mindset
Opportunistic attacker exploiting publicly documented endpoints and header structures. Initial reconnaissance identified the request chain from public logs, then used binary diffing to understand the vulnerability mechanics rather than relying on patch analysis. The attacker leveraged legitimate application headers as injection vectors to evade basic security filters.

## Defensive takeaways
- Use parameterized queries and prepared statements exclusively; never concatenate user input into SQL
- Implement input validation as a whitelist of allowed characters rather than blacklist of dangerous ones
- Apply input sanitization at the earliest point of entry and validate consistently across all code paths
- Use binary diffing on patched vs unpatched versions to identify attack surface when direct vulnerability analysis fails
- Restrict HTTP headers to expected values and reject requests with unexpected header contents
- Implement rate limiting and WAF rules to detect SQL injection patterns in HTTP headers
- Apply least privilege principles to database accounts to limit damage from successful SQL injection
- Monitor for suspicious header patterns and unusual database activity

## Variant hunting
Search for similar unauthenticated endpoints that route through ISAPI filters to ASP.NET handlers. Examine other X-siLock-* header processing code for similar sanitization bypasses. Look for other Machine2 or similar internal transfer mechanism endpoints. Test other action parameters besides 'm2' in the ISAPI endpoint. Examine if similar patterns exist in other Progress products.

## MITRE ATT&CK
- T1190
- T1040
- T1057
- T1005
- T1021

## Notes
This writeup demonstrates sophisticated vulnerability analysis through binary diffing and code review rather than simple fuzzing. The researchers methodically traced execution flow from public log evidence to identify the attack chain. The vulnerability required understanding legitimate application architecture (X-siLock headers, folder_add_by_path transaction type) to craft valid requests. At time of publication, the vulnerability was already being actively exploited in the wild, making responsible disclosure challenging. The SQL injection was not in the native DLL but in the .NET ASP.NET layer (dnSpy analysis), showing attackers must examine multiple code layers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
