# MOVEit Transfer RCE (CVE-2023-34362) - Patch Diffing Analysis

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Progress MOVEit Transfer
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** SQL Injection, Remote Code Execution, Arbitrary Session Variable Setting, SSRF (Server-Side Request Forgery), Pre-authentication Code Execution
- **Category:** uncategorised
- **Writeup:** https://blog.assetnote.io/2023/06/07/moveit-transfer-patch-diff-adventure/

## Summary
Assetnote researchers reverse-engineered CVE-2023-34362, a critical pre-authentication RCE in Progress MOVEit Transfer through patch diffing analysis. The vulnerability chain involves SQL injection combined with arbitrary session variable manipulation via request headers, leading to remote code execution. The vulnerability was actively exploited in the wild at time of research.

## Attack scenario (step by step)
1. Attacker identifies unpatched MOVEit Transfer instance exposed on internet
2. Attacker crafts malicious HTTP request with specially crafted headers to set arbitrary session variables
3. Session variable manipulation allows bypassing internal-only access restrictions on machine2.aspx endpoint
4. Attacker leverages SSRF through machine2.aspx to access internal endpoints or execute commands
5. SQL injection payload executed through the session variables leads to database compromise or query manipulation
6. Remote code execution achieved through SQL injection context or subsequent exploitation steps

## Root cause
The patched version removed code that allowed arbitrary session variable setting based on HTTP header input without proper authentication or validation. This pre-authentication session manipulation combined with SSRF and SQL injection capabilities created an exploitable chain for RCE.

## Attacker mindset
Opportunistic threat actor leveraging active pre-authentication RCE in widely-deployed enterprise file transfer software. Focus on rapid exploitation before patches deployed, targeting internet-exposed instances for initial compromise and lateral movement within organizations.

## Defensive takeaways
- Implement strict input validation on all HTTP headers, especially those used for session/context setting
- Enforce authentication checks before processing any request headers that affect application state or session variables
- Segment network access - ensure internal-only endpoints cannot be accessed via SSRF from external entry points
- Parameterize all SQL queries to prevent injection attacks regardless of input source
- Monitor for suspicious header patterns and session variable manipulation attempts
- Prioritize patching of pre-authentication vulnerabilities with active exploitation
- Conduct patch diffing analysis on security updates to understand vulnerability root causes

## Variant hunting
['Search for similar header-based session variable injection in other Progress software products', 'Hunt for SSRF patterns that bypass authentication through session manipulation in web applications', 'Identify other endpoints restricted by internal-only checks that could be bypassed through session header injection', 'Review other file transfer/collaboration tools for similar pre-auth session tampering vulnerabilities', 'Check for SQL injection opportunities in database queries using unsanitized session-derived variables']

## MITRE ATT&CK
- T1190
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services
- T1190 - Pre-authentication RCE
- T1548 - Abuse Elevation Control Mechanism
- T1595 - Active Scanning

## Notes
Research conducted through patch diffing methodology: obtaining trial version for patched software, discovering unpatched version through CDN URL enumeration, performing offline activation with serial keys, using DiffMerge to identify changed files, and decompiling .NET DLLs with ILSpy for comparison. Research team withheld full POC until public disclosure available or 30 days elapsed to allow patch deployment. MOVEitISAPI.dll identified as native binary requiring Ghidra analysis. Investigation traced vulnerability through machine2.aspx endpoint access control bypass.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
