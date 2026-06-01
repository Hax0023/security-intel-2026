# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS) - Cookie-based, Cookie Tossing, OAuth Authorization Code Theft, Browser Permission Hijacking, Content Security Policy (CSP) Bypass, WAF Evasion
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
A chain of two seemingly unexploitable cookie XSS vulnerabilities in the _zm_csp_script_nonce parameter was exploited through cookie tossing and CSP nonce escaping to achieve persistent code execution. The attackers leveraged OAuth dirty dancing to steal authorization codes, combined with browser permission hijacking to enable webcam/microphone access without user consent, and demonstrated WAF evasion through victim framing.

## Attack scenario (step by step)
1. Attacker identifies cookie XSS in _zm_csp_script_nonce parameter via improper cookie string parsing on zoom.us and subdomains
2. Attacker crafts escaped payload to bypass cookie parsing: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//" to break out of nonce attribute and inject arbitrary JavaScript
3. Attacker uses cookie tossing technique to inject malicious cookie across Zoom's infrastructure, exploiting path/domain handling to achieve persistent execution
4. Malicious JavaScript steals OAuth authorization codes via 'dirty dancing' technique (intercepting OAuth flow parameters)
5. Injected script exploits already-granted browser permissions to silently activate webcam and microphone on Zoom web client
6. As denial of service bonus, attacker frames victim traffic through WAF to get user flagged as malicious, causing account lockout

## Root cause
Inadequate input sanitization and output encoding of cookie values in CSP nonce generation; reliance on cookie string parsing without proper escaping; insufficient cookie scope validation allowing tossing attacks; overly permissive CSP policies that permit nonce injection; browser permission persistence without explicit re-consent for sensitive devices

## Attacker mindset
Patient, methodical researcher who recognized that 'useless' self-XSS could become critical through chaining and infrastructure abuse. Focused on finding non-obvious attack primitives (cookie parsing quirks) rather than direct exploits. Understood that persistence and privilege escalation matter more than initial access complexity.

## Defensive takeaways
- Never use user-controllable input (including cookies) in CSP headers or nonce generation without strict whitelisting
- Implement robust output encoding for all contexts: HTML attributes require different escaping than HTML content or JavaScript
- Use cryptographically random, server-generated nonces instead of reflecting client input
- Validate and sanitize cookie values server-side with context-aware parsing
- Implement cookie scope isolation: use specific Path, Domain, and SameSite attributes to prevent cookie tossing
- Enforce explicit user re-consent for sensitive permissions (microphone, camera) on critical operations
- Apply strict CSP policies with frame-ancestors and object-src restrictions to limit attack surface
- Implement rate limiting and behavioral analysis on OAuth authorization endpoints
- Monitor for suspicious cookie injection patterns and CSP header anomalies
- Regular security audits of cookie handling and CSP policy generation logic

## Variant hunting
['Search for other CSP-related cookies or headers that reflect user input without encoding (e.g., x-frame-options, x-content-type-options)', 'Test all first-party cookies across Zoom subdomains for similar cookie string parsing vulnerabilities', 'Look for other OAuth endpoints vulnerable to authorization code interception', "Hunt for permission hijacking in other browsers' permission models (notifications, geolocation, payment request API)", 'Test for cookie tossing on other Zoom services and API endpoints', 'Examine other security headers that might be generated from cookies', 'Look for client-side nonce validation that could be bypassed']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token
- T1563 - Steal Web Session Cookie (via XSS)
- T1187 - Forced Authentication
- T1185 - Browser Session Hijacking
- T1115 - Cleartext Data Transmission
- T1566 - Phishing (implicit via OAuth redirect manipulation)

## Notes
Excellent example of vulnerability chaining where individual weaknesses (cookie XSS, cookie tossing, permission persistence) become critical when combined. The cookie string parsing quirk is particularly interesting as it demonstrates how non-standard server behavior can introduce unexpected attack vectors. The research team's persistence in finding unexploitable primitives and then weaponizing them through infrastructure abuse shows sophisticated exploitation mindset. The 3-month disclosure timeline (October 2023 to January 2024) indicates responsible disclosure. The $15k bounty reflects the critical nature given Zoom's security-conscious reputation and the complexity of the exploit chain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
