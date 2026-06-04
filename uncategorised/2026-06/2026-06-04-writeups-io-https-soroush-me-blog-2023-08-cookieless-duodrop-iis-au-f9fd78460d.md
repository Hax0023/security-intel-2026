# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in provided content
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 expose a critical vulnerability in ASP.NET Framework's cookieless authentication mechanism within IIS, allowing attackers to bypass authentication and escalate privileges within application pool contexts. The vulnerability leverages improper handling of authentication tokens embedded in URLs when cookies are disabled, enabling session hijacking and privilege escalation to application pool identity.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application configured with cookieless authentication enabled
2. Attacker crafts malicious URL containing forged authentication token in URL path or query string
3. Application processes authentication token without proper validation against cookie-less session state
4. Attacker gains authenticated session without valid credentials
5. Attacker leverages authenticated context to access restricted resources or trigger privileged operations
6. If application pool identity has elevated privileges, attacker escalates to application pool account context

## Root cause
ASP.NET Framework's cookieless authentication implementation fails to properly validate and secure authentication tokens when cookies are disabled. Tokens are transmitted in URLs without adequate cryptographic binding to the requestor, allowing token extraction, reuse, and forgery.

## Attacker mindset
An attacker seeks to bypass authentication controls in legacy ASP.NET applications using cookieless mode, viewing this as a design weakness offering direct authentication bypass without credential theft. The attacker recognizes URL-embedded tokens as transferable and leverages them for privilege escalation within the web server context.

## Defensive takeaways
- Disable cookieless authentication; always use secure HTTP-only cookies with proper SameSite attributes
- Implement cryptographic binding of session tokens to client identifiers (IP, TLS fingerprint)
- Apply strict input validation and token format verification before processing authentication
- Enforce principle of least privilege for application pool identities
- Use modern authentication protocols (OAuth 2.0, SAML) instead of custom token schemes
- Implement rate limiting and anomaly detection for authentication attempts
- Apply security updates and migrate from legacy ASP.NET Framework to .NET Core/5+
- Conduct security code review of custom authentication handlers

## Variant hunting
Search for other ASP.NET applications with cookieless authentication enabled; examine custom authentication modules handling URL-based tokens; investigate similar session management flaws in other web frameworks using URL-embedded credentials; analyze other IIS-specific authentication bypass vectors.

## MITRE ATT&CK
- T1190
- T1110
- T1556
- T1550.003
- T1021.006
- T1548.002

## Notes
This vulnerability is particularly severe in legacy enterprise environments still using ASP.NET Framework with cookieless authentication. The combination of auth bypass (CVE-2023-36899) and privilege escalation (CVE-2023-36560) creates a complete compromise scenario. The blog post title references 'DuoDrop' suggesting potential exploitation in tandem with other techniques. Microsoft released patches for these CVEs; immediate patching is critical for affected deployments.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
