# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS) - Cookie-based, OAuth Authorization Code Theft, Browser Permission Hijacking, Cookie Tossing, Content Security Policy (CSP) Bypass, Insecure Cookie Parsing
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two low-impact XSS vulnerabilities in Zoom's CSP nonce cookie handling to achieve persistent session takeover and user account compromise. By exploiting cookie tossing techniques combined with OAuth dirty dancing, attackers could steal authorization codes and hijack browser permissions to enable webcams and microphones without user consent on Zoom web.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce parameter via insecure cookie string parsing that reflects unescaped double quotes into script nonce attributes
2. Attacker crafts malicious cookie payload using quoted string escape sequences to bypass CSP nonce validation and inject arbitrary JavaScript across 40+ scripts on zoom.us and subdomains
3. Attacker performs cookie tossing attack to set malicious persistent cookies, causing XSS to fire on subsequent victim visits to any Zoom subdomain
4. Injected JavaScript performs OAuth dirty dancing to intercept and steal authorization codes during legitimate OAuth flows
5. Attacker uses stolen authorization codes to hijack victim's Zoom session and obtain authentication tokens
6. Malicious script requests elevated browser permissions and silently enables webcam/microphone capture, with attacker-controlled WebRTC permissions hijacking

## Root cause
Insecure cookie value parsing treating cookie contents as quoted strings without proper sanitization, combined with reflection of cookie values into CSP headers and script nonce attributes without HTML entity encoding. CSP nonce mismatch logic failed to prevent injection of additional nonce directives.

## Attacker mindset
Persistent, patient researcher who recognized that seemingly unexploitable self-XSS vulnerabilities could be weaponized through cookie manipulation and chaining techniques. Focused on identifying 'potential energy' in widespread but individually low-impact issues, then systematically chaining them with OAuth attacks and permission hijacking for maximum impact.

## Defensive takeaways
- Implement strict input validation on all cookie values regardless of source, treating cookies as untrusted input
- Use HTML entity encoding when reflecting any cookie values into HTML context, especially security-critical attributes like CSP nonces
- Validate that CSP nonce values match expected format and prevent injection of additional directives through cookie manipulation
- Implement SameSite cookie flags (Strict) to prevent cookie tossing attacks and unauthorized cross-site cookie setting
- Apply additional validation layer for OAuth flows to detect and prevent authorization code interception patterns
- Require explicit user consent for sensitive permissions (microphone, camera) with visible UI indicators, not just browser prompts
- Monitor for abnormal permission requests and WebRTC permission changes that deviate from user behavior patterns
- Implement Content Security Policy with script-src restrictions that cannot be bypassed via nonce manipulation
- Use HTTPOnly and Secure flags on authentication cookies to limit XSS impact
- Regularly audit CSP implementation for bypass techniques and nonce generation logic

## Variant hunting
Hunt for similar cookie parsing vulnerabilities in other security-critical cookies (_zm_csrf, session tokens, etc.). Search for other CSP-related cookies on Zoom subdomains. Test for cookie tossing on different domains and paths. Look for other OAuth implementations vulnerable to dirty dancing attacks. Check for browser permission hijacking in other web video conferencing platforms.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1185 - Stealing Browser Cookies via XSS
- T1528 - Steal Application Access Token (OAuth)
- T1563 - Account Hijacking via Stolen Credentials
- T1539 - Steal Web Session Cookie
- T1657 - Browser Extensions for Privilege Escalation
- T1040 - Network Sniffing (WebRTC/OAuth interception context)

## Notes
Reported 10/02/2023, patched and verified 01/01/2024. This writeup exemplifies sophisticated vulnerability chaining where multiple individually unexploitable issues (cookie XSS, CSP nonce bypass) combine with social engineering-adjacent attacks (permission hijacking) to achieve account takeover. The cookie string parsing behavior is an unusual implementation choice suggesting custom cookie handling code. Zoom's widespread use of identical code across subdomains amplified vulnerability scope significantly.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
