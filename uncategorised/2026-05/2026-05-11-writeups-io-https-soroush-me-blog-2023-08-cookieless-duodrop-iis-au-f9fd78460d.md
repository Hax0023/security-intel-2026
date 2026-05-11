# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Cookie Handling Vulnerability, URL-based Token Injection
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit a vulnerability in ASP.NET Framework's cookieless authentication mechanism, allowing attackers to bypass authentication and escalate privileges within IIS application pools. The vulnerability stems from improper validation of authentication tokens transmitted via URL query parameters instead of cookies.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application configured with cookieless authentication enabled (URL-based tokens)
2. Attacker crafts a malicious URL containing a forged or manipulated authentication token in the query string
3. The authentication token is injected into the DuoDrop (dual-drop/chained authentication) mechanism without proper validation
4. ASP.NET Framework accepts the invalid token due to insufficient cryptographic verification of URL-transmitted credentials
5. Attacker gains unauthorized access to protected resources and elevated privileges within the app pool context
6. Attacker can execute arbitrary code or access sensitive data with the privileges of the IIS application pool identity

## Root cause
ASP.NET Framework's cookieless authentication mode fails to properly validate and verify authentication tokens when they are transmitted via URL parameters. The vulnerability exists in how tokens are parsed, decrypted, and authenticated when the standard cookie mechanism is bypassed, allowing attackers to forge or inject invalid tokens that are still accepted.

## Attacker mindset
An attacker targeting ASP.NET environments would recognize that cookieless authentication is a legitimate but less commonly audited feature. They would focus on token manipulation and cryptographic weaknesses in the URL-based token handling, seeking to bypass authentication entirely or escalate to higher privileges within the application pool, which could lead to lateral movement or system compromise.

## Defensive takeaways
- Disable cookieless authentication unless absolutely necessary; use standard cookie-based authentication with secure flags (HttpOnly, Secure, SameSite)
- Implement robust token validation including proper MAC (Message Authentication Code) verification for all authentication tokens
- Apply security patches CVE-2023-36899 and CVE-2023-36560 immediately across all affected ASP.NET Framework versions
- Enforce the principle of least privilege for IIS application pool identities to minimize damage from privilege escalation
- Monitor and log authentication attempts, particularly those using URL-based tokens or containing unusual query parameters
- Implement Web Application Firewalls (WAF) rules to detect and block suspicious URL parameter patterns used in authentication bypasses

## Variant hunting
['Search for other authentication bypass vulnerabilities in ASP.NET Form Authentication, Windows Authentication integrated modes', 'Investigate similar token validation flaws in other URL-parameter-based authentication mechanisms (e.g., custom session tokens)', 'Examine IIS extensions and modules that may implement alternative authentication schemes with similar validation weaknesses', 'Test for privilege escalation vectors in other IIS-hosted applications using cookieless authentication', 'Review OAuth/OpenID implementations in ASP.NET that may transmit tokens in URLs instead of secure headers']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1548 - Abuse Elevation Control Mechanism
- T1550 - Use Alternate Authentication Material
- T1110 - Brute Force
- T1021 - Remote Services

## Notes
This vulnerability is particularly dangerous in shared hosting environments and multi-tenant IIS setups. The 'DuoDrop' naming suggests a chaining of two authentication mechanisms that creates an exploitable gap. Organizations should audit their ASP.NET configurations to identify which applications use cookieless authentication and prioritize patching. The vulnerability demonstrates that moving away from standard security patterns (like cookies) for authentication can introduce subtle but critical validation flaws.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
