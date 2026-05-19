# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in MOVEit Transfer that allows unauthenticated remote code execution through the /machine2.aspx endpoint. The vulnerability exists in the CrackInput method which insufficiently sanitizes X-siLock-* headers passed through the /MOVEitISAPI/MOVEitISAPI.dll?action=m2 gateway endpoint, enabling attackers to inject arbitrary SQL commands.

## Attack scenario (step by step)
1. Attacker sends request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path' to bypass initial access controls
2. Request is routed to /machine2.aspx which processes the X-siLock-* headers via the CrackInput method
3. Attacker crafts malicious SQL payload in one of the X-siLock headers that are extracted but insufficiently sanitized
4. SQL injection payload executes against the backend database, allowing database manipulation or code execution
5. Attacker uses database access to escalate privileges or execute system commands
6. Attacker chains subsequent requests through /guestaccess.aspx, /api/v1/token, and file upload endpoints to maintain access and establish persistence

## Root cause
The CrackInput method in SILMachine2 class extracts data from X-siLock-* HTTP headers but applies insufficient input validation/sanitization before using these values in SQL queries. The header parsing logic fails to properly escape or parameterize user-supplied input, allowing SQL injection attacks to bypass authentication controls.

## Attacker mindset
Attackers identified the gateway endpoint pattern and reverse-engineered the required headers to reach the vulnerable code path. By analyzing logs of active exploitation and decompiling both patched and unpatched versions with Ghidra/BinDiff, attackers determined the vulnerability was not in the ISAPI DLL routing layer but in the downstream ASP.NET handler. The use of custom headers (X-siLock-*) provided a method to inject payloads that might evade simple WAF rules looking at POST body content.

## Defensive takeaways
- Implement comprehensive input validation on all HTTP headers, not just POST/GET parameters, as headers can be overlooked in security reviews
- Use parameterized queries or prepared statements for all database operations to prevent SQL injection regardless of input source
- Apply consistent sanitization across all custom header processing logic and avoid whitelisting approaches that may have gaps
- Require authentication before processing gateway/routing endpoints to prevent unauthenticated access to internal application handlers
- Use BinDiff analysis during patching to identify exact code changes and ensure patches address root causes, not just symptoms
- Implement network segmentation and monitor for suspicious request patterns to /MOVEitISAPI and /machine2.aspx endpoints
- Apply security headers and input length restrictions on all headers to limit injection attack surface

## Variant hunting
Search for other .aspx pages that use similar X-siLock-* header processing patterns, particularly those with CrackInput methods. Look for additional gateway endpoints in MOVEitISAPI.dll that route to other handlers. Examine other Progress products for similar authentication bypass patterns using custom headers. Search for SQL-building functions that concatenate header values without parameterization in other application modules.

## MITRE ATT&CK
- T1190
- T1027
- T1083
- T1005
- T1078
- T1055

## Notes
This vulnerability was actively exploited in the wild before public disclosure. The attack chain involves multiple endpoints (guestaccess.aspx, API token endpoint, file upload endpoints) suggesting attackers used SQL injection to either create valid credentials or bypass authentication entirely. The researchers' use of BinDiff on patched vs unpatched versions proved instrumental in narrowing down the vulnerable code location. The custom X-siLock-Transaction header requirement (set to 'folder_add_by_path') acts as a gating mechanism that must be understood for successful exploitation. BinDiff showing no differences between versions suggests the vulnerability may have existed for an extended period or the patch was minimal.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
