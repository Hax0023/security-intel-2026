# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Path Traversal
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 demonstrate a critical vulnerability in ASP.NET Framework's cookieless forms authentication mechanism in IIS environments. An unauthenticated attacker can bypass authentication and escalate privileges to the application pool identity by manipulating URL-based session tokens, enabling complete application compromise and lateral movement within the server.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application using cookieless forms authentication (tokens embedded in URLs instead of cookies)
2. Attacker crafts malicious URL with manipulated session token/authentication ticket in the path
3. IIS processes the request and extracts authentication context from the manipulated URL without proper validation
4. Attacker's request is authenticated as a legitimate user or elevated privilege account
5. Attacker gains access to protected resources or achieves code execution within the app pool context
6. Attacker leverages app pool identity privileges for lateral movement or system compromise

## Root cause
ASP.NET Framework's cookieless authentication implementation fails to properly validate and secure authentication tickets when embedded in URLs. The vulnerability stems from insufficient token encryption/integrity checking and improper separation of authentication context from URL path processing, allowing token manipulation and reuse across security boundaries.

## Attacker mindset
An attacker recognizes that URL-based session tokens lack the same protections as cookie-based sessions (SameSite, HttpOnly flags) and can be easily intercepted, logged, or manipulated. They understand that IIS path processing may not properly validate token integrity, allowing crafted tokens to bypass authentication checks and escalate to application pool privileges for complete system access.

## Defensive takeaways
- Migrate from cookieless authentication to cookie-based forms authentication with secure flags (HttpOnly, Secure, SameSite)
- Implement strong token encryption and HMAC validation for any URL-embedded authentication data
- Apply principle of least privilege to application pool identities
- Implement rate limiting and anomaly detection for authentication attempts
- Deploy Web Application Firewall rules to detect malformed authentication tokens
- Regularly audit and validate authentication mechanisms in legacy ASP.NET applications
- Apply all Microsoft security patches for ASP.NET Framework versions in use
- Use runtime protection tools to monitor and restrict app pool process capabilities

## Variant hunting
Search for other ASP.NET Legacy applications using cookieless authentication across organizational infrastructure. Investigate whether similar token manipulation flaws exist in custom session management implementations or third-party authentication modules. Test other Microsoft web technologies (SharePoint, Exchange) that may rely on URL-based token passing mechanisms.

## MITRE ATT&CK
- T1190
- T1556
- T1134
- T1548
- T1550
- T1021

## Notes
This vulnerability chain is particularly dangerous because it combines authentication bypass with privilege escalation. The cookieless authentication mechanism was common in legacy ASP.NET Framework applications and may still exist in production environments. Affected organizations should prioritize immediate patching and migration strategies away from URL-based session tokens.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
