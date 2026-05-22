# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cookie XSS (CSP Nonce Injection), OAuth Authorization Code Theft, Browser Permission Hijacking, Cookie Tossing, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable Cookie XSS vulnerabilities in Zoom's _zm_csp_script_nonce cookie into a persistent attack by exploiting cookie string parsing and CSP nonce reflection. The vulnerability enabled OAuth authorization code theft, browser permission hijacking to enable webcam/microphone without user consent, and WAF evasion through frame manipulation.

## Attack scenario (step by step)
1. Attacker discovers CSP nonce cookie (_zm_csp_script_nonce) reflects unsanitized user input due to cookie string parsing
2. Attacker crafts malicious cookie payload using escape sequences to bypass CSP nonce validation: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//"
3. Attacker uses cookie tossing technique to inject malicious cookie across multiple subdomains and persist the XSS
4. Malicious JavaScript steals OAuth authorization codes during user authentication flow via 'OAuth Dirty Dancing'
5. Injected script hijacks browser permissions (notification, camera, microphone) to enable device access without explicit user consent
6. Attacker gains persistent session access and can impersonate user or enable surveillance via webcam/microphone

## Root cause
Zoom's backend performed insecure cookie value parsing treating cookie strings as quoted values, combined with insufficient sanitization of the _zm_csp_script_nonce cookie before reflection in CSP headers and script nonce attributes. The application did not validate nonce attribute escaping or prevent escape sequence injection.

## Attacker mindset
Opportunistic researcher targeting high-value program (Zoom $10M+ bounty history) through unconventional vector (Cookie XSS). Applied persistence through cookie tossing exploitation and chained seemingly 'useless' self-XSS vulnerabilities into critical account takeover by combining multiple weaknesses (CSP bypass, OAuth flow interception, permission hijacking).

## Defensive takeaways
- Implement strict input validation and output encoding for all cookie values, especially security-critical cookies like CSP nonces
- Do not parse cookie values as quoted strings; treat all cookie values as literal strings and escape appropriately
- Generate cryptographically random nonces server-side and validate them without user-controllable input
- Apply HTML entity encoding and attribute-specific escaping for all reflections, particularly in security policy directives
- Implement SameSite cookie attribute (Strict/Lax) to prevent cookie tossing attacks across subdomains
- Add robust CSP policy validation to ensure nonce mismatches are detected and logged
- Implement browser permission request interception and validation to prevent silent permission hijacking
- Apply WAF rules to detect and block XSS patterns in cookies, not just URL parameters and POST data
- Use Content Security Policy Level 3 features to restrict nonce manipulation
- Conduct security review of OAuth token handling to prevent authorization code interception

## Variant hunting
Hunt for similar cookie XSS in other security-critical cookies (CSRF tokens, session identifiers, OAuth state parameters). Test cookie parsing behavior across different server frameworks. Look for other CSP nonce or token cookies in similar web applications. Test cookie tossing on multi-subdomain applications. Search for browser permission hijacking vectors in other videoconferencing platforms. Test WAF frame-up DoS technique on other applications with WAF protections.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing (via OAuth code theft)
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token (OAuth code interception)
- T1563 - Account Manipulation
- T1564 - Hide Artifacts (silent permission enable)
- T1562 - Impair Defenses (WAF evasion)
- T1204 - User Execution
- T1185 - Browser Extensions (permission hijacking)
- T1566 - Phishing (if chain requires user click)

## Notes
Reported 10/02/23, patched 01/01/2024. This writeup demonstrates sophisticated vulnerability chaining combining multiple weak points into critical ATO. The Cookie XSS via string parsing is particularly noteworthy as it affects almost all zoom.us subdomains due to shared cookie configuration. The 'OAuth Dirty Dancing' technique for stealing authorization codes and 'WAF Frame-Up' DoS variant add significant impact beyond standard XSS. Researchers wisely focused on cookie-based XSS in heavily-audited main domain rather than looking for traditional XSS.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
