# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Bypass, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 describe a critical authentication bypass vulnerability in ASP.NET Framework's cookieless mode that allows attackers to impersonate arbitrary users and escalate privileges to the application pool identity. The vulnerability leverages improper session token handling when cookies are disabled, enabling arbitrary user impersonation without valid credentials.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application configured with cookieless authentication enabled
2. Attacker crafts a malicious URL containing a forged session token embedded in the path or query string
3. The application accepts the malformed token without proper validation due to the authentication bypass flaw
4. Attacker gains authenticated access as an arbitrary user (e.g., administrator account)
5. Attacker leverages authenticated access to execute code within the application pool context
6. Attacker achieves privilege escalation to the IIS application pool identity, gaining system-level access

## Root cause
The ASP.NET Framework's cookieless authentication mode fails to properly validate session tokens when cookies are disabled. The application trusts user-supplied session identifiers in URL paths without cryptographic validation, allowing token forgery and arbitrary user impersonation.

## Attacker mindset
An opportunistic attacker would systematically probe ASP.NET applications for cookieless mode configuration, then craft forged session tokens to bypass authentication layers and gain privileged access. The attacker seeks to escalate from web application context to underlying system privileges.

## Defensive takeaways
- Enable cookie-based authentication instead of cookieless mode where possible
- Implement strict cryptographic validation of all session tokens regardless of transport mechanism
- Apply principle of least privilege to IIS application pool identities
- Use ASP.NET Core which has improved session security mechanisms over Framework
- Monitor for suspicious session token patterns in URLs and query strings
- Apply security patches CVE-2023-36899 and CVE-2023-36560 immediately
- Implement Web Application Firewall rules to detect token tampering patterns
- Conduct security review of all applications using cookieless authentication mode

## Variant hunting
Search for other ASP.NET session management implementations, particularly in legacy systems using URL-embedded tokens. Investigate Forms Authentication with custom session token generation. Examine any application accepting session identifiers outside standard cookie mechanisms.

## MITRE ATT&CK
- T1190
- T1078
- T1548
- T1550
- T1021

## Notes
This vulnerability is particularly dangerous in legacy ASP.NET Framework deployments. Cookieless authentication was designed for scenarios with cookie-incompatible clients but introduces significant security risks. The combination of auth bypass and privilege escalation makes this a critical finding. Microsoft released patches addressing both token validation and session handling mechanisms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
