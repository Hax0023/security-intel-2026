# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in provided content
- **Severity:** critical
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Information Disclosure
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 describe critical authentication bypass and privilege escalation vulnerabilities in ASP.NET Framework's cookieless session handling mechanism on IIS. An attacker can bypass authentication controls and escalate privileges within the application pool context by manipulating session identifiers in URL paths.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application using cookieless session mode configuration
2. Attacker crafts malicious URL containing forged or stolen session identifier in the path (e.g., /(SessionID))
3. Application processes the session ID without proper validation due to DuoDrop vulnerability
4. Attacker gains access to authenticated user's session or escalates to higher privilege level
5. Attacker exploits app pool context to execute code with elevated privileges
6. Attacker achieves remote code execution or lateral movement within the system

## Root cause
ASP.NET Framework's cookieless session handling mechanism fails to properly validate and sanitize session identifiers extracted from URL paths. The vulnerability exists in how the framework processes the special (SessionID) syntax used when cookies are disabled, allowing attackers to inject or manipulate session tokens without cryptographic verification.

## Attacker mindset
An attacker would recognize that cookieless sessions represent an alternative authentication vector often overlooked in security testing. By targeting this mechanism, they bypass traditional cookie-based protections and leverage framework-level session processing flaws to achieve authentication bypass and privilege escalation without requiring valid user credentials.

## Defensive takeaways
- Always enable cookie-based sessions instead of cookieless mode when possible
- Implement strict server-side session validation and cryptographic integrity checks
- Apply principle of least privilege to application pool identities
- Monitor and log unusual session identifier patterns in URLs
- Patch ASP.NET Framework to latest versions addressing CVE-2023-36899 and CVE-2023-36560
- Conduct security review of all custom session handling code
- Implement rate limiting and anomaly detection for session hijacking attempts
- Use Web Application Firewalls to detect malformed session identifiers

## Variant hunting
['Test other ASP.NET session management mechanisms for similar path-based injection', 'Examine URL rewriting modules for session ID manipulation vulnerabilities', 'Analyze custom authentication handlers that process URL parameters', "Search for similar vulnerabilities in other framework's cookieless implementations", 'Test interaction between cookieless sessions and URL-based anti-CSRF tokens', 'Investigate privilege escalation paths in other IIS app pool contexts']

## MITRE ATT&CK
- T1190
- T1548
- T1556
- T1110
- T1133
- T1134

## Notes
This vulnerability represents a critical gap in ASP.NET Framework security that affects organizations relying on cookieless session mode. The 'DuoDrop' nomenclature suggests multiple related bypass chains. The vulnerability chain enables both horizontal (session hijacking) and vertical (privilege escalation) attacks. This is particularly dangerous in legacy ASP.NET Framework applications where cookieless mode may have been enabled for compatibility reasons.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
