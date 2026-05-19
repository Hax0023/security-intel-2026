# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permissions Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cookie-based XSS, CSP Bypass, OAuth Authorization Code Theft, Browser Permission Hijacking, Cookie Tossing, WAF Evasion
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable XSS vulnerabilities in Zoom's CSP nonce cookie to achieve persistent session takeover. The attack combined cookie string parsing exploitation, OAuth dirty dancing techniques, and browser permission hijacking to steal authorization codes and silently enable webcams/microphones on web-based Zoom.

## Attack scenario (step by step)
1. Attacker discovers XSS in _zm_csp_script_nonce cookie due to improper cookie string parsing (escaped quotes bypass sanitization)
2. Attacker bypasses CSP by crafting payload that exploits quote escaping to inject malicious nonce values matching those in script tags
3. Attacker uses cookie tossing technique to set malicious cookies across Zoom subdomains, achieving persistent XSS
4. XSS payload steals OAuth authorization codes via 'dirty dancing' - intercepting redirect flows and capturing codes before token exchange
5. Attacker hijacks trusted browser permissions (camera/microphone) through compromised session context
6. Attacker achieves persistent session takeover with ability to monitor user communications and optionally trigger WAF evasion for DoS

## Root cause
Zoom's cookie parsing logic treated cookie values as quoted strings with escape sequence support, but failed to properly sanitize the nonce value before reflecting it in both CSP headers and script nonce attributes. The combination of CSP nonce reflection and lack of proper output encoding enabled XSS injection. Additionally, cookie tossing across subdomains was not adequately mitigated.

## Attacker mindset
Patient reconnaissance focusing on underrated vulnerability classes (cookie XSS) on high-value targets. Persistence in bypassing security controls through understanding of underlying parsing mechanisms. Creativity in chaining multiple weak vulnerabilities into a critical attack chain. Understanding of web standards (CSP, OAuth flows, browser permissions) to create sophisticated multi-stage exploitation.

## Defensive takeaways
- Implement proper output encoding for all cookie values, especially security-sensitive cookies like CSP nonces
- Avoid cookie string parsing with escape sequences; use simpler, safer parsing approaches
- Validate CSP nonce values match expected format and sanitize all reflections in HTML attributes
- Implement SameSite cookie attribute to prevent cookie tossing across subdomains
- Use constant-time comparison for security-critical values like nonces
- Audit OAuth implementations for authorization code interception vulnerabilities
- Implement additional protections for sensitive browser permissions (permission prompts, user notifications)
- Implement robust WAF rules that cannot be easily bypassed via XSS payloads
- Conduct regular security audits of parsing logic and escape handling
- Use CSP strict policies to prevent inline script execution even with valid nonces

## Variant hunting
Look for similar cookie parsing issues in other security-sensitive cookies (CSRF tokens, session identifiers, authentication nonces). Search for CSP nonce reflection vulnerabilities on other major platforms. Investigate OAuth implementations for authorization code theft via XSS interception. Test browser permission hijacking on other services with web-based permission systems. Examine WAF implementations for frame-based injection bypasses.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS vulnerability)
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token (OAuth authorization code theft)
- T1563 - Impersonate User (session hijacking)
- T1564 - Hide Artifacts (persistent XSS via cookies)
- T1566 - Phishing (potentially via malicious links setting cookies)
- T1187 - Forced Authentication (OAuth flow interception)

## Notes
This is an exceptional example of chaining multiple seemingly unexploitable vulnerabilities into a critical attack. The vulnerability demonstrates the importance of understanding underlying parsing mechanisms and browser behaviors. The cookie XSS alone was self-XSS (unexploitable in isolation), but cookie tossing made it cross-domain exploitable. The OAuth dirty dancing component shows sophisticated understanding of OAuth flows. Reported October 2, 2023; patched January 1, 2024. Research team: Sudi, BrunoZero, H4R3L.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
