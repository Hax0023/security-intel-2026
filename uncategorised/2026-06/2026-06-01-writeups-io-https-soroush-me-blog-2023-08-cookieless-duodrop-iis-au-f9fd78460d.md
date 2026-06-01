# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in excerpt
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Vulnerability, Cookieless Forms Authentication Flaw
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 constitute a critical authentication bypass vulnerability in ASP.NET Framework's cookieless authentication mode, allowing attackers to forge authentication tokens and escalate privileges within IIS application pools. The vulnerability chain enables an unauthenticated attacker to bypass authentication mechanisms and gain elevated privileges equivalent to the application pool identity.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using cookieless authentication mode in IIS
2. Attacker analyzes the token generation mechanism used in cookieless Forms Authentication
3. Attacker crafts a malicious authentication token by exploiting the flawed token validation logic
4. Attacker injects the forged token via URL or request parameter to bypass authentication checks
5. Attacker gains access to protected resources with elevated privileges matching the app pool identity
6. Attacker escalates to full application pool compromise and potential lateral movement

## Root cause
ASP.NET Framework's cookieless Forms Authentication implementation contains insufficient validation of authentication tokens, allowing token forgery when cookies are disabled. The token generation and validation logic fails to properly protect against cryptographic attacks or token manipulation.

## Attacker mindset
An attacker would seek to exploit legacy ASP.NET applications using cookieless authentication as a shortcut to bypass authentication entirely, avoiding the complexity of session hijacking and gaining direct administrative access. This appeals to attackers targeting enterprise environments with older infrastructure.

## Defensive takeaways
- Disable cookieless Forms Authentication and enforce cookie-based authentication with secure flags (HttpOnly, Secure, SameSite)
- Implement token signing and encryption with strong cryptographic algorithms and validated implementation
- Apply the latest ASP.NET Framework patches addressing CVE-2023-36899 and CVE-2023-36560 immediately
- Conduct security audits of legacy authentication mechanisms in production ASP.NET applications
- Monitor for suspicious authentication token patterns and token reuse attempts in application logs
- Implement Web Application Firewall (WAF) rules to detect token forgery attempts

## Variant hunting
Search for other ASP.NET authentication mechanisms that rely on URL-based tokens rather than secure cookies, including custom ticket validation logic, legacy session management implementations, and non-standard authentication handlers that may have similar validation weaknesses.

## MITRE ATT&CK
- T1190
- T1110
- T1078
- T1134
- T1548

## Notes
This vulnerability particularly impacts legacy ASP.NET Framework applications in enterprise environments where cookieless authentication may have been enabled for compatibility reasons. The 'DuoDrop' designation suggests this is a chained vulnerability combining multiple weaknesses. Immediate patching is critical given the severity and ease of exploitation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
