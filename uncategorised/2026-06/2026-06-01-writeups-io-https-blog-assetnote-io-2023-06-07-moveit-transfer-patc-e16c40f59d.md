# MOVEit Transfer RCE - CVE-2023-34362: SQL Injection and Arbitrary Session Variable Setting

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** SQL Injection, Arbitrary Session Variable Setting, Server-Side Request Forgery (SSRF), Remote Code Execution, Pre-authentication RCE
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
A critical pre-authentication vulnerability in Progress MOVEit Transfer allows attackers to execute remote code by exploiting SQL injection and arbitrary session variable setting. The vulnerability chains an SSRF attack through machine2.aspx (accessible internally) with session variable manipulation to achieve unauthenticated RCE on vulnerable versions prior to 2023.0.1.

## Attack scenario (step by step)
1. Attacker discovers that machine2.aspx can be accessed via SSRF despite being designed for internal-only access
2. Attacker identifies code that allows arbitrary session variables to be set via request headers in the unpatched version
3. Attacker crafts HTTP request with malicious headers to set session variables without authentication
4. Attacker leverages session variables to inject SQL commands or manipulate application logic
5. Attacker uses the established session context to execute arbitrary code on the server
6. RCE is achieved pre-authentication, allowing full system compromise

## Root cause
The vulnerability stems from two main issues: (1) insecure session variable handling that allows arbitrary values to be set from user-supplied headers without proper validation, and (2) insufficient access controls on the machine2.aspx endpoint that should have been restricted to internal network access. The combination enables unauthenticated attackers to bypass security controls.

## Attacker mindset
Threat actors likely performed reconnaissance on the MOVEit Transfer product, identifying it as a high-value target used by many organizations. Upon discovering the pre-authentication SSRF vector, they systematically explored internal endpoints and tested for session manipulation vulnerabilities. The active exploitation in the wild suggests attackers recognized the broad attack surface and lack of authentication requirements.

## Defensive takeaways
- Implement strict input validation and sanitization for all HTTP headers, especially those used to set session variables
- Never trust client-supplied data for session state management; use server-side session stores with cryptographic tokens
- Apply principle of least privilege - internal endpoints must not be accessible via SSRF even if marked as internal-only
- Conduct regular patch diffing analysis to detect security fixes and proactively identify vulnerabilities before active exploitation
- Monitor for unusual header patterns and session variable modifications in logs as an immediate detection method
- Implement network segmentation to limit damage from pre-authentication RCE vulnerabilities
- Use Web Application Firewalls to detect and block requests with suspicious header patterns targeting session manipulation

## Variant hunting
Researchers should examine other Progress products for similar session handling patterns, particularly in ASPX-based applications. Look for other endpoints marked as internal-only that may be accessible via SSRF. Test for header-based session variable injection in other web applications, especially those handling file transfers or similar high-value operations. Examine other versions of MOVEit Transfer to identify when this vulnerable code was introduced.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1078 - Valid Accounts (session hijacking)
- T1190 - SQL Injection
- T1021 - Remote Services
- T1021.001 - Remote Services: Remote Service Session Hijacking

## Notes
This vulnerability was actively exploited in the wild before patches were available. Assetnote responsibly withheld PoC details for 30 days to allow organizations time to patch. The research methodology demonstrates the value of patch diffing: obtaining both patched and unpatched versions, using DiffMerge for file-level analysis, decompiling .NET assemblies with ILSpy, and reverse engineering native binaries with Ghidra. The vulnerability required chaining multiple weaknesses (SSRF + session manipulation + SQL injection) to achieve pre-authentication RCE. CVE affected versions include 2023.0.0; patched in 2023.0.1. This represents a supply chain risk given MOVEit's role in file transfer operations across many critical organizations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
