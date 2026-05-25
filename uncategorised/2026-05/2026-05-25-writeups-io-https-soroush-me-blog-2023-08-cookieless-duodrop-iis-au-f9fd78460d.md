# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Fixation, Path Traversal
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 exploit ASP.NET's cookieless authentication feature in IIS, allowing attackers to bypass authentication mechanisms and escalate privileges to the application pool identity. The vulnerability leverages improper handling of session identifiers embedded in URLs when cookieless mode is enabled, enabling session hijacking and impersonation of authenticated users.

## Attack scenario (step by step)
1. Attacker identifies an ASP.NET application using cookieless authentication mode (session IDs embedded in URLs)
2. Attacker crafts a malicious URL containing a forged or stolen session identifier using the DuoDrop technique
3. Application accepts the embedded session ID without proper validation of its origin or authenticity
4. Attacker gains access to user session context and bypasses authentication checks
5. By leveraging the app pool identity context, attacker escalates privileges to execute code with elevated permissions
6. Attacker achieves remote code execution or data exfiltration with application pool credentials

## Root cause
ASP.NET Framework's cookieless authentication mode fails to properly validate and protect session identifiers when embedded in URLs. The implementation does not adequately verify session binding to the original request context, allowing session fixation attacks. Additionally, the app pool identity is not properly isolated, enabling privilege escalation from session hijacking.

## Attacker mindset
Target legacy or misconfigured ASP.NET applications that rely on cookieless sessions for compatibility. Exploit the inherent weakness that URL-embedded identifiers are easier to intercept and manipulate than HTTP-only cookies. Recognize that app pool privilege levels provide a powerful escalation path once authentication is bypassed.

## Defensive takeaways
- Disable cookieless authentication mode unless absolutely necessary; use secure cookie-based sessions instead
- Implement strict session binding validation including request origin, user agent, and IP address verification
- Apply cryptographic signatures or HMAC to session identifiers to prevent tampering
- Use HttpOnly and Secure flags on all authentication cookies
- Implement proper app pool identity isolation and principle of least privilege
- Apply all Microsoft security patches for ASP.NET Framework immediately
- Monitor for suspicious URL patterns containing session identifiers
- Use security scanners to detect cookieless authentication configurations
- Implement Web Application Firewalls (WAF) rules to detect session fixation attempts

## Variant hunting
['Test other URL parameter-based authentication mechanisms in ASP.NET', 'Check for similar vulnerabilities in other web frameworks using URL-embedded session tokens', 'Investigate older ASP.NET Core versions for comparable session validation bypass', 'Search for applications using custom cookieless implementations with similar flaws', 'Test for privilege escalation vectors in other IIS application pool configurations', 'Examine Windows authentication bypass possibilities in mixed-mode IIS setups']

## MITRE ATT&CK
- T1190
- T1078
- T1550
- T1134
- T1548
- T1021

## Notes
This vulnerability represents a critical authentication bypass affecting legacy ASP.NET applications. The combination of CVE-2023-36899 (auth bypass) and CVE-2023-36560 (privesc) creates a complete attack chain. Organizations should prioritize patching and migration away from cookieless authentication modes. The research demonstrates how framework-level design choices can create systemic security weaknesses across all applications using that framework.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
