# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Unknown - Coordinated disclosure CVE-2023-36899 & CVE-2023-36560
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Vulnerability, Path Traversal
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET Framework's cookieless authentication mechanism in IIS to bypass authentication and escalate privileges to the application pool identity. The vulnerability allows unauthenticated attackers to forge session identifiers through path-based authentication tokens, leading to complete compromise of ASP.NET applications using cookieless Forms Authentication.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using cookieless Forms Authentication mode (enabled via web.config)
2. Attacker crafts a URL containing a specially formed authentication token in the path component (e.g., /(S(token))/) instead of a cookie
3. The malicious token bypasses authentication validation due to improper sanitization in the session handler
4. Attacker gains authenticated access without valid credentials and can impersonate any user
5. If application runs with elevated app pool identity, attacker executes code with those privileges
6. Attacker achieves RCE or accesses sensitive data with elevated IIS app pool permissions

## Root cause
ASP.NET Framework's cookieless authentication implementation fails to properly validate session tokens embedded in URL paths. The vulnerability exists in how IIS parses and processes the /(S(...))/ syntax for cookieless session management, allowing attackers to inject arbitrary authentication tokens without cryptographic validation or signature verification.

## Attacker mindset
Opportunistic exploitation of framework design flaws. Attacker recognizes that cookieless authentication is a legacy feature with weaker security properties than cookie-based mechanisms, and exploits the fact that session tokens in URLs are often inadequately protected against forgery and path manipulation attacks.

## Defensive takeaways
- Migrate from cookieless Forms Authentication to cookie-based authentication immediately
- Enforce HTTPS-only communication and set Secure and HttpOnly flags on authentication cookies
- Implement strict input validation and canonicalization for all URL-based authentication tokens
- Apply the Microsoft security patches CVE-2023-36899 and CVE-2023-36560 to all affected IIS/ASP.NET installations
- Audit web.config files for cookieless='true' settings and disable if not absolutely required
- Run IIS application pools with minimal required privileges (principle of least privilege)
- Implement Web Application Firewalls (WAF) to detect and block suspicious /(S(...))/ patterns in URLs
- Enable request logging and anomaly detection for authentication bypass attempts

## Variant hunting
['Test other URL path-based authentication mechanisms in legacy ASP.NET applications', 'Examine Windows Authentication impersonation combined with cookieless mode', 'Investigate similar token injection vulnerabilities in other MVC session handlers', 'Search for applications using deprecated SessionStateModule with improper token validation', 'Analyze custom authentication modules that replicate cookieless behavior', 'Test for bypass via URL encoding variations of the /(S(...))/ syntax', 'Check for similar vulnerabilities in other framework implementations (Classic ASP, ISAPI filters)']

## MITRE ATT&CK
- T1190
- T1556
- T1548
- T1021
- T1078

## Notes
This is a critical framework-level vulnerability affecting legacy ASP.NET applications. The cookieless authentication feature was designed for WAP/mobile compatibility in early 2000s but has fundamental security flaws. Organizations should prioritize migrating to ASP.NET Core with modern authentication patterns. The vulnerability demonstrates how legacy features in widely-deployed frameworks can create persistent security issues across millions of installations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
