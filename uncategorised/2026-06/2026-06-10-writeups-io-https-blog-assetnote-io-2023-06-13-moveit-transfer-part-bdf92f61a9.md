# MOVEit Transfer RCE Part Two (CVE-2023-34362) - SQL Injection via machine2.aspx

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
A critical SQL injection vulnerability exists in the MOVEit Transfer /machine2.aspx endpoint that allows unauthenticated remote code execution. Attackers can exploit improper sanitization of X-siLock-* headers by crafting malicious requests through the /MOVEitISAPI/MOVEitISAPI.dll?action=m2 handler to achieve RCE on the target system.

## Attack scenario (step by step)
1. Attacker sends initial request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is forwarded to /machine2.aspx which calls Machine2Main on SILMachine2 class
3. CrackInput method extracts and attempts to sanitize X-siLock-* headers, but sanitization is insufficient
4. Attacker injects SQL payload into a header parameter that bypasses sanitization checks
5. SQL query executes with attacker-controlled input, allowing database manipulation or command execution
6. Attacker chains requests to /guestaccess.aspx, /api/v1/token, and file upload endpoints to achieve RCE

## Root cause
The CrackInput method in Machine2Main class performs inadequate sanitization of X-siLock-* headers extracted from HTTP requests. While headers are processed through a sanitization routine, the implementation fails to properly escape or parameterize SQL queries constructed from user-supplied header values, allowing SQL injection attacks.

## Attacker mindset
Attacker reverse-engineered the patched vs unpatched DLL versions using BinDiff, identified the critical endpoint routing through MOVEitISAPI.dll, discovered the required X-siLock-Transaction header value through log analysis, and systematically traced through decompiled code to locate the vulnerable CrackInput method. This demonstrates methodical binary analysis combined with exploit chain construction for maximum impact.

## Defensive takeaways
- Use parameterized queries and prepared statements for all database operations instead of string concatenation
- Implement comprehensive input validation with whitelist-based sanitization for all HTTP headers
- Apply defense-in-depth: use ORM frameworks that prevent SQL injection by design
- Employ Web Application Firewalls (WAF) to detect and block SQL injection patterns in headers
- Conduct security code review of all custom sanitization functions - built-in framework methods are preferred
- Implement request signing/HMAC validation for critical transaction headers like X-siLock-*
- Apply principle of least privilege to database accounts used by application
- Monitor for suspicious X-siLock header patterns and folder_add_by_path transaction types

## Variant hunting
Search for similar custom header validation in other Progress products, examine other CrackInput-style functions across codebase, review all endpoints that construct SQL from X-siLock-* headers, test other transaction types beyond 'folder_add_by_path' for similar vulnerabilities, examine error handling in Machine2Main for information disclosure vulnerabilities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1083 - File and Directory Discovery
- T1087 - Account Discovery
- T1078 - Valid Accounts
- T1020 - Automated Exfiltration

## Notes
This is Part Two of a multi-part analysis series. The vulnerability was actively exploited in the wild before PoC disclosure. BinDiff comparison between patched/unpatched versions showed no differences in MOVEitISAPI.dll, indicating the vulnerability lies in machine2.aspx/.NET code rather than native DLL. The X-siLock-Transaction header appears to be a custom authentication/authorization mechanism that was bypassed. The exploit chain involves multiple endpoints suggesting file upload capabilities were leveraged for code execution. As of the writeup date, public PoCs existed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
