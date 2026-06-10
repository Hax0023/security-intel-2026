# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Path Traversal
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET's cookieless session mechanism in IIS to bypass authentication controls and escalate privileges from a standard user to app pool identity. The vulnerability leverages improper session token handling when cookies are disabled, allowing attackers to forge or hijack session identifiers embedded in URLs.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application configured with cookieless sessions (sessionState cookieless='true')
2. Attacker crafts a malicious URL containing a forged session token or hijacks an existing session ID from legitimate traffic
3. The application processes the session token from the URL without proper validation, accepting the attacker's session
4. Attacker gains authentication as an arbitrary user or escalates to higher privilege levels
5. If the app pool runs under elevated credentials, attacker can execute commands in the context of the app pool identity
6. Attacker achieves code execution and potential lateral movement within the IIS infrastructure

## Root cause
ASP.NET's cookieless session implementation fails to properly validate and protect session tokens when they are embedded in URLs rather than stored in HTTP-only cookies. The lack of cryptographic integrity checks and proper token binding allows attackers to forge or manipulate session identifiers, bypassing authentication mechanisms designed to rely on cookie security.

## Attacker mindset
An attacker seeks to compromise ASP.NET applications by exploiting framework-level weaknesses rather than application logic flaws. By targeting the default session management mechanism, the attacker gains code execution at the app pool privilege level, enabling persistent compromise and lateral movement within enterprise IIS environments.

## Defensive takeaways
- Avoid using cookieless sessions in production; enforce HTTP-only, Secure, SameSite cookie attributes instead
- Implement strong cryptographic signing and encryption for any session tokens, including URL-embedded variants
- Apply session token binding to client IP addresses or user-agent strings to prevent token reuse
- Deploy input validation and session token format verification in authentication middleware
- Run IIS app pools with minimal required privileges (least privilege principle)
- Apply security patches CVE-2023-36899 and CVE-2023-36560 immediately to all affected ASP.NET versions
- Monitor for suspicious URL patterns containing encoded session tokens or unusual session activity
- Conduct security code reviews of session management implementations across legacy ASP.NET applications

## Variant hunting
Search for other ASP.NET session handling mechanisms that embed tokens in URLs (ViewState, CSRF tokens, custom session wrappers). Investigate applications using URL rewriting modules that may interact unsafely with session tokens. Look for cookieless session configurations across client-facing and internal ASP.NET applications. Test for similar vulnerabilities in other web frameworks that support URL-based session management.

## MITRE ATT&CK
- T1190
- T1548
- T1556
- T1539
- T1021
- T1046

## Notes
This vulnerability represents a critical flaw in ASP.NET Framework's core session management when configured for cookieless operation. The dual CVE assignment reflects both authentication bypass (CVE-2023-36899) and privilege escalation (CVE-2023-36560) impacts. Organizations should prioritize patching and configuration hardening. The blog post details sophisticated exploitation chains combining URL manipulation with IIS authentication mechanics.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
