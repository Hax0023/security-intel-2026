# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS) - Cookie-based, Cookie Tossing / Cookie Jar Overflow, OAuth Authorization Code Theft, Browser Permission Hijacking, Content Security Policy (CSP) Bypass, WAF Evasion
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two seemingly unexploitable cookie-based XSS vulnerabilities through cookie tossing and CSP nonce escaping to achieve persistent session takeover on Zoom. The vulnerability enabled theft of OAuth authorization codes via 'OAuth Dirty Dancing', hijacking of browser permissions to activate webcams/microphones, and WAF evasion through frame injection attacks.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce parameter via cookie string parsing vulnerability in CSP header generation
2. Attacker crafts malicious cookie payload using quote escaping to bypass Zoom's cookie parsing: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)// "
3. Attacker uses cookie tossing technique to inject malicious cookie across Zoom subdomains, bypassing same-site cookie restrictions
4. Injected XSS payload executes in victim's browser context with Zoom's privileges, allowing access to OAuth tokens and authorization flows
5. Attacker steals OAuth authorization codes and injects permission prompts to hijack webcam/microphone access without user awareness
6. Attacker leverages XSS to frame requests through victim's browser, causing WAF to flag victim as malicious source (DoS component)

## Root cause
Zoom's CSP nonce cookie value underwent cookie string parsing without proper sanitization, combined with CSP header generation that reflected cookie values insecurely. The nonce was reflected in both CSP headers and script attributes without proper HTML entity encoding. Additionally, insufficient cookie scope isolation allowed cookie tossing across subdomains.

## Attacker mindset
Persistence-focused attacker seeking to convert low-impact self-XSS into multi-stage exploitation chain. Demonstrated sophisticated understanding of cookie handling mechanisms, CSP mechanics, OAuth flows, and browser security models. Took advantage of Zoom's trust in CSP nonces and subdomain cookie sharing to achieve complete account compromise.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding for all values reflected in CSP headers and script attributes, regardless of cookie origin
- Avoid reflective use of user-controlled data in security-critical headers like Content-Security-Policy
- Use cryptographically random, server-generated nonces instead of client-controllable values in CSP policies
- Implement SameSite cookie attributes (Strict/Lax) to prevent cookie tossing attacks across subdomains
- Apply defense-in-depth: validate nonce integrity server-side before accepting CSP-protected content
- Monitor and alert on unusual cookie modifications or CSP header anomalies
- Implement Subresource Integrity (SRI) checks on inline scripts to prevent nonce-based bypasses
- Apply strict HTTP-only and Secure flags to sensitive cookies
- Implement additional OAuth CSRF protections (state parameter validation, PKCE for web flows)
- Review WAF rules to prevent exploitation via framing and ensure consistent security enforcement

## Variant hunting
Search for similar cookie string parsing vulnerabilities in other security-critical cookies containing nonces, tokens, or identifiers. Examine other CSP implementations that reflect cookie values. Look for instances where quote-escaping mechanisms are applied to cookie values before reflection in HTML/headers. Test for cookie tossing vulnerabilities on any multi-subdomain applications with shared cookie spaces. Audit OAuth implementations for authorization code leakage through XSS contexts.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token
- T1056.004 - Webcam Capture
- T1111 - Multi-Factor Authentication Interception
- T1566.002 - Phishing via Malicious Link
- T1204.001 - User Execution: Malicious Link
- T1547.014 - Browser Extensions

## Notes
This vulnerability demonstrates the critical importance of treating cookie-based self-XSS as exploitable in modern web applications, particularly when combined with architectural weaknesses like cookie tossing. The multi-stage exploit chain (Cookie XSS → Cookie Tossing → OAuth token theft → Permission Hijacking) showcases how seemingly minor vulnerabilities can compound into critical impact. The 'WAF Frame-Up' technique represents a novel DoS vector. Reported October 2, 2023; patched and verified January 1, 2024. Three-person team effort highlights value of collaborative security research. The vulnerability affected not just zoom.us but nearly all Zoom subdomains due to clone architecture.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
