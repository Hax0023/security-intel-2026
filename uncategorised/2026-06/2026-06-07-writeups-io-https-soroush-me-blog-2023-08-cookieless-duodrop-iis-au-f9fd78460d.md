# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Unknown
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Fixation, Improper Cookie Handling
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET Framework's cookieless authentication mechanism in IIS to bypass authentication and escalate privileges to arbitrary app pool identities. The vulnerability allows attackers to craft malicious requests that manipulate session tokens embedded in URLs, circumventing cookie-based security controls and gaining unauthorized access to protected resources.

## Attack scenario (step by step)
1. Attacker identifies a vulnerable ASP.NET application running on IIS with cookieless authentication enabled
2. Attacker crafts a malicious URL containing forged session tokens embedded in the URL path using the cookieless format
3. Attacker sends the crafted request to the target application, bypassing normal cookie validation mechanisms
4. The application processes the request with elevated privileges associated with the app pool identity
5. Attacker gains access to protected resources or executes arbitrary code with app pool privileges
6. Attacker escalates privileges or pivots to compromise the entire IIS server infrastructure

## Root cause
ASP.NET Framework's cookieless authentication mode insufficiently validates session tokens when they are embedded in URLs rather than cookies. The framework fails to properly verify the integrity and origin of URL-embedded session identifiers, allowing attackers to forge valid session tokens and assume arbitrary identities, including the app pool's elevated privileges.

## Attacker mindset
An attacker targeting ASP.NET applications would recognize that cookieless authentication is often used in legacy or poorly configured systems. They would focus on understanding how ASP.NET encodes session tokens in URLs and systematically test methods to forge or manipulate these tokens, knowing that successful exploitation grants both authentication bypass and potential privilege escalation.

## Defensive takeaways
- Disable cookieless authentication; migrate to standard cookie-based session management with secure flags
- Implement cryptographic integrity checks and HMAC validation for all session tokens regardless of transport mechanism
- Apply the latest security patches for ASP.NET Framework (CVE-2023-36899 and CVE-2023-36560)
- Enforce strict input validation and URL parameter filtering on all user-supplied session data
- Use HTTPS with secure, HttpOnly, and SameSite cookie attributes to prevent session hijacking
- Implement rate limiting and anomaly detection on authentication requests
- Regularly audit IIS and ASP.NET configurations to identify and remediate cookieless authentication usage

## Variant hunting
Search for other ASP.NET session management mechanisms that embed security tokens in URLs, query strings, or custom headers. Investigate legacy authentication schemes in older .NET Framework versions, examine custom session handlers that may replicate this vulnerability, and test other IIS-integrated authentication modules for similar token validation weaknesses.

## MITRE ATT&CK
- T1190
- T1548.004
- T1550.001
- T1556.001
- T1111

## Notes
This vulnerability chain is particularly dangerous because it affects the core ASP.NET authentication pipeline and can lead to complete compromise of IIS applications. The cookieless authentication feature represents legacy security design and its continued use is a significant risk factor. Organizations should prioritize identifying and remediating affected systems immediately.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
