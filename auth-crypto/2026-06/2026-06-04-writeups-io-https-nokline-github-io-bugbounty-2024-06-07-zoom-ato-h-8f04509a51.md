# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cookie-based XSS, OAuth Authorization Code Theft, Browser Permission Hijacking, CSP Bypass, Cookie Tossing, WAF Evasion
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable cookie-based XSS vulnerabilities into a persistent attack vector that enabled OAuth authorization code theft and browser permission hijacking on Zoom's web platform. By exploiting CSP nonce reflection in the _zm_csp_script_nonce cookie combined with cookie tossing techniques and OAuth Dirty Dancing, attackers could achieve account takeover and silently enable webcam/microphone access. The vulnerability affected nearly all Zoom subdomains and pages with CSP policies.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce parameter through cookie string parsing vulnerability where escaped quotes bypass sanitization
2. Attacker crafts malicious cookie payload that breaks out of nonce attribute and injects arbitrary JavaScript into CSP-protected scripts on zoom.us
3. Attacker uses cookie tossing technique to set malicious cookies across Zoom subdomains, achieving persistent XSS across the platform
4. Injected JavaScript intercepts OAuth authorization flow using 'OAuth Dirty Dancing' technique to steal authorization codes during legitimate user authentication
5. With stolen OAuth tokens, attacker performs account takeover and hijacks browser permissions (geolocation, camera, microphone) through XSS context
6. Attacker silently enables camera/microphone on victim's Zoom web client and performs WAF Frame-Up by triggering false positives to mask malicious activity

## Root cause
Zoom's web application implemented cookie parsing that treated cookie values as quoted strings with escape sequence support, but failed to properly sanitize the parsed values before reflecting them into CSP headers and script nonce attributes. The CSP nonce was reflected insecurely in 40+ inline scripts without proper HTML entity encoding, allowing nonce attribute escape.

## Attacker mindset
Determined vulnerability researcher demonstrating deep understanding of web security layers: identifying that individual bugs appeared 'unexploitable' but could be chained through cookie tossing, OAuth manipulation, and permission hijacking. Showed patience in reverse-engineering Zoom's cookie parsing logic through methodical payload testing and understanding that widespread CSP implementation across subdomains created massive attack surface.

## Defensive takeaways
- Implement strict HTML entity encoding on all reflected values, especially in security-critical attributes like CSP nonces and script attributes
- Avoid cookie-value string parsing that supports escape sequences; treat cookie values as literal opaque strings
- Implement SameSite cookie attributes (Strict/Lax) to prevent cookie tossing attacks across subdomains
- Use Content-Security-Policy frame-ancestors directive to prevent clickjacking during OAuth flows
- Implement CSRF tokens on all state-changing operations including OAuth authorization
- Monitor for anomalous permission grant requests and require explicit user interaction for sensitive permissions
- Implement rate limiting and behavioral analysis to detect automated permission hijacking attempts
- Regularly audit CSP policy effectiveness and ensure nonces are cryptographically random and single-use
- Consider disabling inline scripts entirely in favor of external script files to reduce XSS attack surface

## Variant hunting
['Search for other CSP-related cookies or headers that perform string parsing without sanitization', 'Identify all domains accepting user-controllable cookie values that are reflected in security headers', 'Test for cookie tossing vulnerabilities on other multi-subdomain properties (*.zoom.us, *.zoomgov.com, etc.)', 'Hunt for other OAuth implementations that may be vulnerable to authorization code interception', "Look for permission prompt handling that doesn't require explicit user gestures", 'Test for WAF bypasses using similar frame-based exploitation patterns', 'Examine other CSP implementations for nonce reflection issues in inline script tags', 'Investigate custom cookie parsing implementations for escape sequence handling bugs']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1200 - Hardcoded Keys in Source Code
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token
- T1528 - OAuth/JWT Token Theft
- T1187 - Forced Authentication
- T1080 - Taint Shared Content
- T1113 - Screen Capture
- T1113 - Video Capture
- T1123 - Audio Capture

## Notes
This was a sophisticated multi-stage attack requiring chaining of three distinct vulnerability classes. The researchers demonstrated exceptional skill in recognizing that 'unexploitable' self-XSS vulnerabilities became critical when combined with cookie tossing and OAuth manipulation. The 9+ month disclosure timeline (10/02/23 to 01/01/2024) indicates Zoom's thorough patch verification process. The use of cookie string parsing for nonce handling is highly unusual and suggests potential legacy code or overly complex cookie handling logic. The breadth of impact (40+ scripts, almost all subdomains) was amplified by the pervasive use of CSP policies across Zoom's infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
