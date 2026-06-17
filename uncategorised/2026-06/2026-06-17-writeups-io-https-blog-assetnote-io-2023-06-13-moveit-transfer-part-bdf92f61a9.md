# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the /MOVEitISAPI/MOVEitISAPI.dll endpoint. The vulnerability exists in the machine2.aspx handler which improperly processes user-supplied input from X-siLock-* headers without adequate sanitization, enabling attackers to execute arbitrary SQL commands and achieve code execution on the server.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request is forwarded to /machine2.aspx where CrackInput method extracts data from X-siLock-* headers
3. Attacker injects malicious SQL payload through insufficiently sanitized header parameters
4. SQL injection allows attacker to bypass authentication and extract database credentials or modify application logic
5. Attacker leverages escalated privileges to upload and execute malicious code through /api/v1/folders/{id}/files endpoints
6. Remote code execution is achieved on the MOVEit Transfer server with application privileges

## Root cause
The CrackInput method in SILMachine2 class extracts user-supplied data from HTTP headers (X-siLock-*) but applies insufficient input validation and sanitization before using the data in SQL queries. The header processing lacks parameterized query usage or proper escaping, allowing SQL injection through specially crafted header values.

## Attacker mindset
Opportunistic adversary targeting widely-deployed enterprise file transfer solution with zero-day capability. The attacker recognized that unauthenticated access to the /MOVEitISAPI endpoint combined with SQL injection in header processing creates a complete chain to unauthenticated RCE. Active exploitation suggests high-value targeting of financial, healthcare, and government organizations relying on MOVEit for secure file transfers.

## Defensive takeaways
- Implement strict input validation and use parameterized/prepared SQL statements for all database queries
- Avoid extracting and processing security-critical parameters from HTTP headers without validation
- Apply defense-in-depth: implement Web Application Firewall rules to detect SQL injection patterns in headers
- Conduct regular security code reviews focusing on data flow from external input to database queries
- Implement application-level authentication checks before processing requests to administrative endpoints
- Monitor for unusual X-siLock-Transaction header values and suspicious SQL patterns in logs
- Keep all enterprise software updated immediately when critical patches are released
- Segment file transfer servers on isolated networks to limit lateral movement impact

## Variant hunting
Search for similar authentication bypass vulnerabilities in other Progress Software products, particularly those using X-siLock-* header processing patterns. Examine any custom header processing in ISAPI DLL extensions. Look for SQL injection in other endpoint handlers that process machine2.aspx requests or similar transaction-based operations. Check for similar patterns in related file transfer applications that use transaction headers for session management.

## MITRE ATT&CK
- T1190
- T1589
- T1566
- T1567
- T1021
- T1059
- T1053

## Notes
The vulnerability was actively exploited in the wild before public disclosure. Researchers used Ghidra for binary analysis and BinDiff comparison between patched and unpatched versions, finding the vulnerability existed in managed .NET code (dnSpy analysis) rather than native DLL. The exploit chain required specific header values (X-siLock-Transaction: folder_add_by_path) to trigger the vulnerable code path. This represents a supply chain attack vector affecting thousands of organizations globally.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
