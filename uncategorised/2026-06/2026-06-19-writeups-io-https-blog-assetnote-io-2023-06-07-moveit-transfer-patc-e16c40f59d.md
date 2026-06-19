# MOVEit Transfer RCE - CVE-2023-34362 Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Injection, Server-Side Request Forgery (SSRF), Pre-authentication RCE
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
Assetnote discovered a critical pre-authentication RCE vulnerability in Progress MOVEit Transfer (CVE-2023-34362) through patch diffing analysis. The vulnerability chain involves arbitrary session variable injection via request headers combined with SQL injection and SSRF to achieve remote code execution without authentication. The flaw existed in MOVEit Transfer 2023.0.0 and was patched in version 2023.0.1.

## Attack scenario (step by step)
1. Attacker obtains vulnerable MOVEit Transfer instance exposed to the internet (version 2023.0.0)
2. Attacker crafts malicious request headers to inject arbitrary session variables via the vulnerable code path
3. Injected session variables are used to bypass authentication checks or modify application state
4. Attacker exploits SQL injection vulnerability leveraging the modified session context
5. SQL injection is chained with SSRF to call internal endpoints like machine2.aspx
6. Internal endpoint execution combined with code execution primitives results in RCE

## Root cause
Code in MOVEit Transfer 2023.0.0 allowed arbitrary session variable assignment based on HTTP request headers without proper validation. This session manipulation could be chained with other vulnerabilities (SQL injection and SSRF) to achieve pre-authentication remote code execution. The vulnerable code was removed in the patched version 2023.0.1.

## Attacker mindset
Threat actors exploited this vulnerability actively in the wild to gain unauthorized access to MOVEit Transfer instances. The pre-authentication nature and ease of exploitation made it highly attractive for mass compromise campaigns. Attackers likely discovered the vulnerability through public information or security research, then rapidly weaponized it before patches were widely deployed.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers and request parameters
- Enforce strict session management controls - never allow client-controlled data to directly modify session state
- Apply principle of least privilege to internal endpoints - restrict access to machine2.aspx and similar internal functions from external requests
- Implement defense-in-depth: combine authentication, authorization, and input validation
- Prioritize patching critical pre-authentication vulnerabilities immediately
- Monitor for suspicious session variable assignments and SQL query patterns in logs
- Conduct regular patch diffing and code reviews to catch session handling vulnerabilities
- Use Web Application Firewalls (WAF) to detect and block requests attempting session injection

## Variant hunting
Security researchers should search for similar patterns in other Progress software products and web applications that allow header-based session manipulation. Look for code that directly assigns user-controlled input to session variables or uses request headers in security-sensitive operations. Check for other internal endpoints that may be accessible via SSRF or header-based access control bypasses.

## MITRE ATT&CK
- T1190
- T1190
- T1548
- T1578
- T1190

## Notes
Assetnote responsibly withheld the full proof of concept until either a public PoC became available or 30 days passed, giving organizations time to patch. The patch diffing methodology outlined (obtaining trial versions, using offline activation, binary diffing with DiffMerge, then decompiling .NET DLLs with ILSpy) provides a valuable template for reverse engineering vulnerabilities in commercial software. The vulnerability chain demonstrates the importance of securing internal-only endpoints and validating all input sources, not just obvious user input fields.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
