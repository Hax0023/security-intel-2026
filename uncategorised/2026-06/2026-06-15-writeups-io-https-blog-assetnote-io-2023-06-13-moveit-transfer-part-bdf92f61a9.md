# MOVEit Transfer RCE Part Two (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Authentication Bypass
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/13/moveit-transfer-part-two/

## Summary
CVE-2023-34362 is a critical SQL injection vulnerability in Progress MOVEit Transfer that allows unauthenticated remote code execution through the /machine2.aspx endpoint. Attackers can craft malicious requests with specially crafted X-siLock-* headers to execute arbitrary SQL commands and achieve RCE on the server.

## Attack scenario (step by step)
1. Attacker sends POST request to /MOVEitISAPI/MOVEitISAPI.dll?action=m2 with X-siLock-Transaction header set to 'folder_add_by_path'
2. Request bypasses authentication checks and is forwarded to /machine2.aspx endpoint via CrackInput method
3. Attacker crafts malicious SQL injection payload in X-siLock-* headers that bypass sanitization
4. SQL injection executes in database context, allowing data exfiltration or command execution
5. Attacker leverages subsequent API calls to /api/v1/token and /api/v1/folders to escalate privileges
6. Attacker uploads malicious file through /api/v1/folders/{id}/files endpoint to achieve RCE

## Root cause
Insufficient input validation and sanitization of X-siLock-* headers in the CrackInput method of SILMachine2.Machine2Main function. The CrackInput method attempted to sanitize headers but failed to properly validate SQL query parameters, allowing injection payloads to reach database queries executed by the application.

## Attacker mindset
Attackers exploited this vulnerability to gain unauthorized access to MOVEit Transfer instances, exfiltrate sensitive data, and establish persistent backdoors. The active exploitation and subsequent public PoC release indicated high-value target interest. Attackers leveraged the unauthenticated nature of the vulnerability to bypass all security controls.

## Defensive takeaways
- Implement strict input validation using allowlists rather than blacklists for all user-controlled inputs
- Use parameterized queries and prepared statements exclusively to prevent SQL injection
- Apply principle of least privilege to database accounts used by application
- Implement Web Application Firewall (WAF) rules to detect and block SQL injection patterns
- Monitor and log all requests to sensitive endpoints like /MOVEitISAPI/ and /machine2.aspx
- Segment network access to MOVEit Transfer instances and restrict exposure
- Keep all software dependencies and frameworks patched to latest versions
- Conduct regular security code reviews and binary diffing between versions to identify patches

## Variant hunting
Researchers should examine other Progress products using similar ISAPI DLL patterns and X-siLock header handling. Search for similar transaction-type headers in other endpoints that might bypass authentication. Analyze other .aspx page handlers that call Machine2Main or similar entry points. Review historical versions to identify when sanitization was introduced but bypassed.

## MITRE ATT&CK
- T1190
- T1059
- T1505
- T1078
- T1083
- T1020

## Notes
The researchers used Ghidra for binary analysis and dnSpy for .NET decompilation. Notably, BinDiff comparison between patched and unpatched versions showed no discernible differences in MOVEitISAPI.dll, suggesting the vulnerability lay elsewhere in the application logic. The vulnerability was actively exploited in the wild before detailed analysis was published. The X-siLock-Transaction header with value 'folder_add_by_path' was a critical requirement to trigger the vulnerable code path.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
