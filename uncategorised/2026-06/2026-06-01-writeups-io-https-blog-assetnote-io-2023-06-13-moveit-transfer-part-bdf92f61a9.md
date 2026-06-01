# MOVEIt Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Progress MOVEIt Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEIt Transfer that allows unauthenticated remote code execution through the /machine2.aspx endpoint. The vulnerability exists in the X-siLock-Transaction header processing which fails to properly sanitize user input before constructing SQL queries, enabling attackers to execute arbitrary code on the server.

## Attack scenario (step by step)
1. Attacker sends request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is routed to /machine2.aspx endpoint which passes through SILMachine2.Machine2Main handler
3. CrackInput method extracts and attempts to sanitize X-siLock-* headers, but sanitization is insufficient
4. Attacker injects malicious SQL payload into header values that bypass sanitization checks
5. SQL injection in database query allows execution of arbitrary commands or authentication bypass
6. Attacker uploads malicious file via /api/v1/folders/{id}/files endpoints to achieve remote code execution

## Root cause
The CrackInput method in SILMachine2 class performs incomplete input sanitization on X-siLock-* headers. While headers are extracted and some sanitization is applied, the validation logic fails to prevent SQL injection payloads from reaching the database query construction layer. The application trusts user-supplied header values without proper parameterized query usage or comprehensive input validation.

## Attacker mindset
Attacker recognized that the X-siLock-Transaction header is critical to reaching vulnerable code paths and focused on identifying which header values bypass initial checks ('folder_add_by_path'). By comparing patched vs unpatched DLL versions and reverse engineering the validation logic, the attacker discovered that sanitization was incomplete, allowing SQL injection through header manipulation to achieve unauthenticated RCE.

## Defensive takeaways
- Always use parameterized queries/prepared statements instead of string concatenation for SQL
- Implement comprehensive input validation on all user-supplied data including headers, with whitelist-based validation where possible
- Apply consistent sanitization across all code paths; partial sanitization provides false security
- Require authentication before processing requests that modify server state (folder creation, file uploads)
- Use code review and static analysis tools to identify SQL injection patterns in decompiled code
- Test both patched and unpatched versions side-by-side to identify what was actually fixed
- Implement web application firewalls to detect and block SQL injection patterns in headers

## Variant hunting
Search for similar vulnerable patterns in other endpoints that: (1) process X-siLock-* or similar custom headers, (2) route requests through intermediary handlers like Machine2Main, (3) have CrackInput or similar extraction/sanitization methods with incomplete validation, (4) construct dynamic SQL without parameterization. Check other ASPX pages in MOVEIt Transfer that handle administrative operations, particularly those dealing with folders, files, or machine-to-machine communication.

## MITRE ATT&CK
- T1190
- T1021
- T1566
- T1105
- T1059

## Notes
The researchers declined to publish the full exploit chain initially due to active exploitation. The vulnerability affected multiple endpoints in sequence (/guestaccess.aspx → /api/v1/token → /api/v1/folders → upload endpoints), indicating a chain of compromises. Reverse engineering with Ghidra and dnSpy combined with BinDiff comparison proved effective for identifying the vulnerability location when binary differences were minimal. The X-siLock-Transaction header value 'folder_add_by_path' was the critical bypass required to reach vulnerable code.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
