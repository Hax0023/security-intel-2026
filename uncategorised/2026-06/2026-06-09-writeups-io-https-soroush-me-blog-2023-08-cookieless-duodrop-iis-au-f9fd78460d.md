# Cookieless DuoDrop: IIS Auth Bypass & App Pool Privilege Escalation in ASP.NET Framework

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Microsoft ASP.NET Framework / IIS
- **Bounty:** Not specified in provided content
- **Severity:** CRITICAL
- **Vuln types:** Authentication Bypass, Privilege Escalation, Session Management Flaw, Cookie Handling Vulnerability
- **Category:** uncategorised
- **Writeup:** https://soroush.me/blog/2023/08/cookieless-duodrop-iis-auth-bypass-app-pool-privesc-in-asp-net-framework-cve-2023-36899/

## Summary
CVE-2023-36899 and CVE-2023-36560 represent critical authentication bypass and privilege escalation vulnerabilities in ASP.NET Framework's cookieless session handling mechanism in IIS. An attacker can bypass authentication controls and escalate privileges to the application pool identity by exploiting flaws in how ASP.NET processes cookieless sessions.

## Attack scenario (step by step)
1. Attacker identifies ASP.NET application configured with cookieless sessions enabled
2. Attacker crafts malicious session identifiers or manipulates URL-based session tokens
3. Session validation logic fails to properly authenticate the crafted session
4. Attacker gains unauthorized access to authenticated user contexts
5. Attacker escalates privileges by exploiting app pool identity context
6. Full compromise of application with app pool-level permissions achieved

## Root cause
ASP.NET Framework's cookieless session handling mechanism contains improper validation of session identifiers passed via URLs or form parameters. The authentication validation logic fails to properly verify session integrity when cookies are disabled, allowing session fixation or token manipulation attacks.

## Attacker mindset
Target high-value ASP.NET applications, particularly legacy systems using cookieless sessions for compatibility. Focus on bypassing authentication layers to gain unauthorized access, then leverage app pool identity for lateral movement and privilege escalation within the server infrastructure.

## Defensive takeaways
- Disable cookieless sessions unless absolutely required; use secure cookie-based session management instead
- Implement robust session token validation and integrity checks (HMAC, cryptographic signatures)
- Apply principle of least privilege to application pool identities
- Implement defense-in-depth with additional authentication factors beyond session tokens
- Apply all ASP.NET Framework security patches (CVE-2023-36899, CVE-2023-36560)
- Use security headers and content security policies to limit attack surface
- Monitor and log session token usage patterns for anomalies

## Variant hunting
['Examine other cookieless session implementations in legacy frameworks (Classic ASP, JSP)', 'Test session token manipulation in other IIS/.NET authentication schemes', 'Investigate URL rewriting mechanisms that handle session identifiers', 'Research other privilege escalation paths via app pool identity context', 'Analyze cookieless session handling in custom session providers']

## MITRE ATT&CK
- T1190
- T1518
- T1134
- T1548
- T1556
- T1021

## Notes
This vulnerability chain (two CVEs) demonstrates the danger of legacy authentication mechanisms in widely-deployed frameworks. The 'cookieless' feature, designed for compatibility, introduces significant security risks. Organizations should prioritize patching and migration away from cookieless sessions. The vulnerability likely affects numerous enterprise applications with long deployment cycles.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
