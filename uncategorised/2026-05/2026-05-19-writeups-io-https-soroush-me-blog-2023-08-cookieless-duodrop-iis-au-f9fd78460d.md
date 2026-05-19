# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Cookieless Session Hijacking, IIS Configuration Weakness
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 demonstrate how ASP.NET applications using cookieless session management can be exploited to bypass authentication and escalate privileges from guest/limited user to app pool identity. The vulnerability exploits improper session handling in IIS when cookies are disabled, allowing attackers to hijack or forge session identifiers.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application configured with cookieless sessions enabled (sessionState cookieless='true')
2. Attacker crafts a request containing a forged or hijacked session ID in the URL path (format: /(sessionid)/apppath)
3. Application accepts the session identifier without proper validation due to weak cryptographic protection
4. Attacker escalates to authenticated state by replaying or guessing valid session tokens
5. With elevated session context, attacker executes code or actions with app pool identity privileges
6. Attacker achieves arbitrary command execution or data access with application pool account permissions

## Root cause
ASP.NET's cookieless session implementation relies on URL-embedded session identifiers that lack sufficient entropy and cryptographic validation. The framework fails to properly authenticate session tokens and enforce per-request validation, allowing session fixation and privilege escalation via the application pool identity context.

## Attacker mindset
An attacker would recognize that cookieless sessions are inherently riskier and search for implementations relying on this feature. The attacker would focus on session token predictability, lack of HTTPS enforcement, and weak server-side session validation to forge valid tokens and escalate from guest to authenticated/privileged context.

## Defensive takeaways
- Avoid cookieless session management entirely; enforce secure HTTP-only cookies with SameSite flags
- Implement strong session token generation using cryptographically secure random sources with sufficient entropy
- Enforce HTTPS/TLS for all session transmission to prevent token interception
- Validate session tokens server-side on every request with proper expiration and rotation
- Run IIS application pools with minimal required privileges (principle of least privilege)
- Use Windows authentication or OAuth/modern identity protocols instead of custom session schemes
- Implement additional integrity checks (HMAC/signatures) on session data
- Monitor and alert on suspicious session activity patterns

## Variant hunting
["Search for other ASP.NET applications using sessionState cookieless='true' in web.config", 'Test legacy applications with URL-rewritten session identifiers for predictability', 'Examine other Microsoft frameworks or custom session implementations lacking HTTPS enforcement', 'Review IIS configurations running application pools with elevated privileges', 'Hunt for applications implementing custom session management bypassing .NET built-in protections', 'Test for session fixation in applications with cross-domain or relative path session handling']

## MITRE ATT&CK
- T1190
- T1133
- T1078
- T1548
- T1555
- T1056

## Notes
This vulnerability chain (CVE-2023-36899 and CVE-2023-36560) represents a significant security issue in legacy ASP.NET configurations. The 'DuoDrop' designation suggests the combination of two related auth/privilege escalation flaws. Organizations running cookieless sessions should immediately migrate to modern authentication schemes. The vulnerability highlights why cookieless sessions have been considered a security anti-pattern for over a decade.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
