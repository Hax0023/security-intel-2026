# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Unsafe Deserialization
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 represent a critical authentication bypass combined with privilege escalation vulnerability in ASP.NET Framework when cookieless authentication is enabled. An attacker can bypass authentication mechanisms and escalate privileges within the IIS application pool by exploiting improper session handling and state validation.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application running with cookieless authentication mode enabled
2. Attacker crafts malicious session identifier or manipulates URL-encoded session state to forge authentication tokens
3. Attacker bypasses initial authentication checks by exploiting improper validation of session credentials
4. Attacker escalates privileges by manipulating application state or session objects to assume higher privilege levels
5. Attacker gains access to sensitive resources or achieves code execution within the IIS application pool context
6. Attacker maintains persistent access through forged session credentials

## Root cause
ASP.NET Framework fails to properly validate and secure cookieless session tokens. When cookieless authentication is enabled, session identifiers are embedded in URLs or request data. The framework does not adequately verify the integrity and authenticity of these tokens, allowing attackers to forge or manipulate session state without cryptographic validation or sufficient entropy checks.

## Attacker mindset
Opportunistic attacker targeting legacy or misconfigured ASP.NET applications with cookieless authentication enabled. The attacker recognizes this as a configuration choice that weakens security and exploits the lack of cookie-based CSRF protections and token validation. The focus is on horizontal privilege escalation within the application pool.

## Defensive takeaways
- Disable cookieless authentication; use secure, HTTP-only, Secure flagged cookies instead
- Implement cryptographic validation and integrity checks for all session identifiers
- Apply principal of least privilege to application pool identities
- Use strong, unpredictable session token generation with sufficient entropy
- Implement proper authorization checks on sensitive operations beyond authentication
- Validate and sanitize all user-supplied session-related data
- Use ASP.NET Core instead of legacy ASP.NET Framework where possible
- Apply all security patches and updates for ASP.NET Framework
- Monitor and audit session-related anomalies and privilege escalation attempts

## Variant hunting
Search for other .NET applications using cookieless authentication modes; investigate URL rewriting implementations that handle session tokens; examine applications with custom session handlers that may not properly validate token integrity; look for other authentication mechanisms in IIS that might similarly fail to validate embedded credentials.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1134 - Access Token Manipulation
- T1548 - Abuse Elevation Control Mechanism
- T1550 - Use Alternate Authentication Material
- T1578 - Modify Cloud Compute Infrastructure

## Notes
This vulnerability affects ASP.NET Framework applications specifically when cookieless authentication is enabled, which is an insecure non-default configuration. The dual CVE designation (CVE-2023-36899 and CVE-2023-36560) suggests multiple related attack vectors or bypass techniques. The blog title 'DuoDrop' suggests two distinct privilege escalation/bypass mechanisms exploitable together. Organizations should audit all ASP.NET applications for cookieless authentication usage immediately.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
