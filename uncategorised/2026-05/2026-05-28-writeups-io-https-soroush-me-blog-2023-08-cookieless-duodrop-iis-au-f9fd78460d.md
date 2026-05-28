# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** CVE-2023-36899, CVE-2023-36560
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
A critical vulnerability in ASP.NET Framework's cookieless session handling allows attackers to bypass authentication and escalate privileges within IIS application pools. By exploiting improper session token validation in cookieless mode, attackers can forge valid session identifiers and impersonate authenticated users or escalate to app pool identity.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application using cookieless session mode (common in older deployments)
2. Attacker intercepts or observes session token embedded in URL path (e.g., (S(token))/page.aspx)
3. Attacker analyzes session token generation algorithm or crafts malicious token without proper validation
4. Attacker injects crafted token in URL to bypass authentication checks
5. Application grants access with escalated privileges matching the forged session identity
6. Attacker gains unauthorized access or executes code with app pool privileges

## Root cause
ASP.NET Framework fails to properly validate and cryptographically protect session tokens when operating in cookieless mode. The framework embeds session identifiers directly in URLs without sufficient entropy or HMAC validation, allowing token forgery and session hijacking.

## Attacker mindset
Target legacy ASP.NET applications still using cookieless sessions for compatibility. Focus on applications with weak entropy in token generation or missing integrity checks. Exploit the assumption that URL-embedded tokens are inherently protected by HTTPS, when they are not cryptographically bound to the user.

## Defensive takeaways
- Migrate from cookieless session mode to cookie-based sessions with Secure and HttpOnly flags
- Enforce cryptographic HMAC validation on all session tokens regardless of storage method
- Use strong, unpredictable session token generation (minimum 128 bits entropy)
- Implement session token binding to client identity (IP, user-agent, certificate pinning)
- Apply output encoding when embedding session data in URLs to prevent injection
- Disable cookieless sessions in ASP.NET configuration and audit legacy deployments
- Implement rate limiting and anomaly detection for session validation failures

## Variant hunting
Search for other session handling implementations in older frameworks (ASP classic, custom session managers). Investigate URL rewriting mechanisms in proxy layers or load balancers that might preserve or modify session tokens. Examine cookieless mode configurations across shared hosting environments.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts
- T1550 - Use Alternate Authentication Material
- T1548 - Abuse Elevation Control Mechanism
- T1647 - Exfiltration Over C2 Channel

## Notes
DuoDrop refers to the ability to drop into app pool context. Affects primarily ASP.NET Framework 4.x and earlier versions. Modern ASP.NET Core uses secure cookie handling by default. URL-embedded sessions are visible in browser history, referrer logs, and proxy logs—increasing exposure surface.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
