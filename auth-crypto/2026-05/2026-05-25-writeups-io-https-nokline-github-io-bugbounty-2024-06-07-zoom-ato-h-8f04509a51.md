# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permissions Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Zoom Bug Bounty
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cookie XSS, Cookie Tossing, OAuth Authorization Code Theft, Browser Permission Hijacking, Content Security Policy Bypass, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two seemingly unexploitable Cookie XSS vulnerabilities into a persistent account takeover by exploiting cookie string parsing in the CSP nonce cookie (_zm_csp_script_nonce), combined with cookie tossing to bypass defenses, and OAuth dirty dancing to steal authorization codes. This allowed complete session hijacking and silent activation of webcam/microphone permissions on Zoom web.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce by exploiting server-side cookie string parsing with escaped quotes
2. Attacker crafts malicious CSP nonce payload that breaks out of attribute context and injects arbitrary JavaScript
3. Attacker uses cookie tossing technique to set multiple cookies with same name across subdomains, bypassing same-origin protections
4. XSS executes and steals OAuth authorization codes during user login via 'OAuth Dirty Dancing' attack
5. Stolen auth codes used to create persistent session tokens and hijack victim's Zoom account
6. Attacker leverages XSS to hijack browser permissions APIs, silently enabling webcam and microphone access

## Root cause
Zoom's backend performed unsafe cookie string parsing treating cookie values as quoted strings without proper escaping validation. CSP nonce values were reflected into both HTTP headers and HTML attributes without sanitization. The combination of CSP bypass, cookie tossing support, and OAuth implementation allowed chaining into account takeover.

## Attacker mindset
Researchers demonstrated persistence in finding unexploitable primitives and creatively chaining them together. They understood cookie parsing edge cases, CSP mechanics, OAuth flows, and browser security models. The 'cookie tossing' technique shows deep knowledge of HTTP semantics and subdomain relationships. They recognized that seemingly self-XSS bugs could become severe when combined with other mechanisms.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding for all cookie-derived values reflected in HTTP headers and HTML
- Avoid custom cookie parsing logic; use standard library functions that properly handle escaping
- Use cryptographically random CSP nonces on every request, never derived from user-controlled input
- Implement SameSite cookie attributes with 'Strict' mode to prevent cookie tossing across subdomains
- Apply defense-in-depth: validate OAuth state parameters, implement PKCE, and verify authorization code origin
- Sanitize and validate all inputs used in script nonce attributes
- Implement strict CSP policies that cannot be bypassed by nonce injection
- Require explicit user interaction and consent for sensitive permission requests
- Monitor for unusual authorization patterns and cookie manipulation attempts
- Consider using subresource integrity (SRI) for inline scripts

## Variant hunting
Hunt for other cookie-based XSS vulnerabilities in CSP-related cookies, JWT tokens in cookies, session identifiers, or tracking cookies that get reflected. Test cookie string parsing edge cases on other domains. Look for cookie tossing vulnerabilities in applications with multiple subdomains. Search for OAuth implementations vulnerable to authorization code interception. Identify other browser permission hijacking vectors beyond webcam/microphone.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1539: Steal Web Session Cookie
- T1187: Forced Authentication
- T1528: Steal Application Access Token
- T1040: Network Sniffing
- T1113: Screen Capture
- T1123: Audio Capture
- T1598: Phishing - Spearphishing Link

## Notes
Reported October 2, 2023; patched and verified January 1, 2024. This writeup demonstrates advanced chaining of multiple seemingly low-severity vulnerabilities into critical account takeover. The 'cookie tossing' attack vector is particularly noteworthy as a technique to amplify XSS impact across trust boundaries. The researchers' focus on CSP nonce parsing and cookie string semantics shows sophisticated understanding of web internals. The ability to hijack browser permissions silently represents a particularly severe impact for communication platforms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
