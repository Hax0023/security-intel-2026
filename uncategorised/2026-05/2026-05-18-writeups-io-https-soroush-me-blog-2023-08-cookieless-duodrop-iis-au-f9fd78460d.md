# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, URL-based Session Token Exposure
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET's cookieless authentication mechanism in IIS, allowing attackers to bypass authentication and escalate privileges to the application pool identity. The vulnerability stems from improper handling of session tokens embedded in URLs when cookies are disabled, combined with path traversal capabilities.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application configured with cookieless authentication enabled
2. Attacker crafts a malicious URL containing a forged or stolen session token in the URL path (format: /(sessionid)/)
3. Attacker gains unauthorized access by bypassing standard cookie-based authentication checks
4. Attacker leverages elevated application pool identity privileges to access restricted resources or execute arbitrary code
5. Attacker achieves code execution within the application pool security context
6. Attacker escalates to application pool identity with higher privileges than the web application itself

## Root cause
ASP.NET's cookieless session authentication relies on URL-embedded session tokens without proper validation of token authenticity, CSRF protection, or secure transmission. The implementation fails to verify token legitimacy and improperly trusts URL-provided identifiers, combined with insufficient access control checks in IIS request processing.

## Attacker mindset
Exploit legacy ASP.NET configurations (cookieless mode) that prioritize compatibility over security; identify applications with disabled cookies; craft authenticated requests using URL manipulation; escalate from application context to pool identity for maximum privilege.

## Defensive takeaways
- Never use cookieless authentication in production; enforce cookie-based sessions with secure flags (HttpOnly, Secure, SameSite)
- Implement CSRF tokens and validate all session identifiers cryptographically
- Apply principle of least privilege to application pool identities
- Use modern ASP.NET Core instead of legacy ASP.NET Framework
- Implement strict URL filtering and canonicalization to prevent session token injection
- Monitor for suspicious URL patterns containing encoded session data
- Regular patching of IIS and ASP.NET Framework components
- Conduct security audits of session management configurations

## Variant hunting
Search for other .NET authentication mechanisms that embed sensitive data in URLs; examine custom session handlers that replicate cookieless patterns; test URL rewriting modules in IIS for token manipulation; investigate Forms Authentication implementations with path-based token storage.

## MITRE ATT&CK
- T1190
- T1556
- T1134
- T1078
- T1021

## Notes
CVE-2023-36899 focuses on auth bypass; CVE-2023-36560 on privilege escalation. The vulnerability particularly affects legacy ASP.NET Framework applications using cookieless authentication—a deprecated practice. The attack chain demonstrates the dangers of mixing deprecated features with insufficient access controls. Researcher Soroush Dalili's analysis reveals deep IIS/ASP.NET internals knowledge.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
