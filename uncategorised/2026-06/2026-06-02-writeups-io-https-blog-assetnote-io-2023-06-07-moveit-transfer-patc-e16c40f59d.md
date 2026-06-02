# MOVEit Transfer RCE via SQL Injection and SSRF (CVE-2023-34362)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Server-Side Request Forgery (SSRF), Remote Code Execution, Arbitrary Session Variable Setting, Pre-Authentication RCE
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer allows remote code execution through a combination of arbitrary session variable injection via HTTP headers and SSRF to access internal ASP.NET pages. The vulnerability chains SQL injection with remote code execution, affecting versions prior to 2023.0.1, and was actively exploited in the wild.

## Attack scenario (step by step)
1. Attacker sends HTTP request with malicious headers to MOVEit Transfer public endpoint
2. Arbitrary session variables are set via unvalidated header input processed by vulnerable code
3. Attacker leverages SSRF capability to reach internal machine2.aspx page normally restricted to internal network
4. SQL injection payloads are crafted and sent through the internal endpoint
5. Injected SQL commands execute with database privileges
6. Remote code execution is achieved, granting full system compromise

## Root cause
The vulnerability stems from two primary issues: (1) MOVEitISAPI.dll and related components allow arbitrary session variables to be set based on unvalidated HTTP header input without proper authentication checks, and (2) the application architecture permits SSRF to internal ASP.NET pages like machine2.aspx which contain exploitable SQL injection points. The patched version removes the vulnerable code that sets session variables from headers.

## Attacker mindset
Opportunistic mass exploitation of publicly exposed MOVEit instances. Attackers recognized the pre-authentication nature of the vulnerability and the widespread deployment of MOVEit Transfer in enterprise environments, making it an ideal target for ransomware groups and APT actors seeking initial access. The active exploitation in the wild demonstrates commodity-level tooling being rapidly developed.

## Defensive takeaways
- Implement strict input validation on all HTTP headers and never trust them for session management
- Restrict internal-only endpoints with network-level controls rather than relying solely on application-level checks
- Audit all code paths that modify session state, especially those accepting external input
- Disable or restrict SSRF capabilities by implementing allowlist-based URL validation
- Apply parameterized queries/prepared statements for all database interactions to prevent SQL injection
- Require pre-authentication before exposing any functionality, especially administrative features
- Monitor for suspicious header patterns and SSRF attempts in HTTP traffic
- Implement web application firewall rules to detect SQL injection patterns in session data
- Maintain an inventory of critical software and establish rapid patching procedures
- Segment network to limit lateral movement even if RCE is achieved

## Variant hunting
['Search for other HTTP headers beyond those documented that may influence session state', 'Analyze other internal ASP.NET pages (.aspx files) in wwwroot for similar injection vulnerabilities', 'Check MOVEitISAPI.dll for additional SSRF gadgets or internal endpoint access methods', 'Review other Progress products that may share code patterns or architecture', 'Examine authentication bypass techniques in related file upload/transfer applications', 'Investigate if similar header-based session manipulation exists in other Ipswitch products', 'Test for unauthenticated access to other administrative or diagnostic endpoints']

## MITRE ATT&CK
- T1190
- T1190.004
- T1505
- T1190.001
- T1021.001
- T1190.002

## Notes
The researchers responsibly delayed PoC publication for 30 days post-patch to allow organizations time to remediate. The vulnerability was discovered through patch diffing by comparing DLL files between patched (2023.0.1) and unpatched (2023.0.0) versions. Key insight: the removed code snippet in the patched version directly pointed to the vulnerability mechanism. The blog post demonstrates advanced reverse engineering methodology including use of Ghidra for native binary analysis and ILSpy for .NET decompilation. This was a high-profile supply chain attack vector affecting thousands of enterprises globally.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
