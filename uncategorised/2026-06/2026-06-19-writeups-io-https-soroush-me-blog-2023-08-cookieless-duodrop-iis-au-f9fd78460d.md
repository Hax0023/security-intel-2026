# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Path Traversal
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET Framework's cookieless session handling in IIS to bypass authentication and achieve privilege escalation within application pool context. The vulnerability leverages improper validation of session identifiers embedded in URLs when cookies are disabled, allowing attackers to impersonate users and escalate privileges.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application configured with cookieless sessions (sessionState cookieless='true')
2. Attacker crafts malicious URL containing forged session identifier embedded in path or query string
3. ASP.NET processes the cookieless session identifier without proper validation or cryptographic verification
4. Attacker gains access to another user's session context, bypassing authentication checks
5. Attacker escalates privileges by accessing admin session or manipulating session state variables
6. Attacker executes arbitrary actions within the application pool's security context

## Root cause
ASP.NET Framework fails to properly validate and cryptographically verify session identifiers when cookieless session mode is enabled. The framework accepts user-supplied session IDs from URL paths without sufficient integrity checking, allowing session fixation and hijacking attacks.

## Attacker mindset
An attacker recognizes that disabling cookies (common in legacy or specific scenarios) shifts session management to URL-embedded tokens. By understanding ASP.NET's weak validation logic, they craft valid-looking session identifiers to hijack admin sessions or escalate privileges without authentication.

## Defensive takeaways
- Avoid using cookieless sessions in ASP.NET; always prefer secure HTTP-only cookies with proper encryption
- If cookieless sessions are required, implement strong cryptographic signing and validation of session tokens
- Use HMAC or digital signatures to ensure session identifier integrity and prevent tampering
- Implement proper access controls and session validation at the application layer
- Upgrade to patched versions of ASP.NET Framework addressing CVE-2023-36899 and CVE-2023-36560
- Employ security headers and mechanisms to prevent session fixation attacks
- Regular security audits of session management implementation across legacy systems

## Variant hunting
['Examine other ASP.NET session handlers (e.g., StateServer, SQLServer modes) for similar validation weaknesses', 'Test custom session management implementations that parse URL-embedded identifiers', 'Investigate applications using URL rewriting or URL-based session tracking mechanisms', 'Search for legacy .NET Framework applications still using cookieless sessions in production', 'Test other web frameworks with URL-based session handling for equivalent vulnerabilities', 'Analyze multi-tier architectures where session state is shared across app pools']

## MITRE ATT&CK
- T1190
- T1548
- T1550
- T1556
- T1187
- T1021

## Notes
This vulnerability affects long-standing ASP.NET Framework deployments, particularly those configured with cookieless sessions for compatibility reasons. The dual CVE designation indicates multiple exploitation vectors. Organizations should prioritize patching and migration away from cookieless session models. The vulnerability demonstrates how legacy security configurations can introduce critical flaws in modern threat landscapes.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
