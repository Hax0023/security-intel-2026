# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permissions Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Zoom Bug Bounty
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cookie-based XSS, CSP Nonce Injection, OAuth Token Theft, Browser Permission Hijacking, WAF Bypass, Session Takeover
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained a Cookie-based XSS vulnerability in the _zm_csp_script_nonce parameter with OAuth Dirty Dancing and browser permission hijacking to achieve persistent session takeover on Zoom. The vulnerability exploited improper cookie string parsing in CSP nonce handling to inject malicious scripts, steal OAuth authorization codes, and hijack webcam/microphone permissions on web-based Zoom.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce cookie through improper cookie string parsing and CSP nonce reflection
2. Crafts malicious cookie payload with escaped quotes to bypass CSP nonce validation and inject arbitrary JavaScript code
3. Injects payload via cookie tossing technique to make victim's browser send the malicious cookie on subsequent requests
4. Malicious script executes in victim's session and steals OAuth authorization codes using 'Dirty Dancing' technique
5. Script hijacks trusted browser permissions to silently enable webcam and microphone access
6. Attacker gains persistent access to victim's Zoom account and device capabilities

## Root cause
Improper cookie string parsing in CSP nonce generation without proper escaping; server-side parsing of cookie values as quoted strings allowed escape sequence injection; lack of sanitization of cookie input before reflection in CSP headers and script attributes; insufficient validation of OAuth token handling

## Attacker mindset
Persistence-focused - recognized that individual self-XSS vulnerabilities could be weaponized through cookie tossing to affect other users; chain-thinking approach to combine multiple weak mitigations into critical impact; OAuth exploitation through token harvesting rather than session fixation

## Defensive takeaways
- Never rely on client-side cookie parsing; implement strict server-side cookie handling without quote interpretation
- Sanitize and validate all cookie values before using them in security-critical contexts like CSP directives
- Generate CSP nonces server-side and maintain strict separation between nonce generation and cookie parsing logic
- Implement additional CSRF protections for OAuth flows beyond authorization codes
- Add robust WAF rules to detect XSS patterns in cookie values and OAuth token theft attempts
- Implement Subresource Integrity (SRI) validation for critical scripts
- Use HttpOnly and Secure flags aggressively; consider SameSite=Strict for sensitive cookies
- Monitor for unusual permission grant patterns and implement permission expiration/revocation
- Implement rate limiting and anomaly detection on OAuth token endpoints

## Variant hunting
Search for similar cookie-based XSS in other cookies with special parsing semantics (auth tokens, CSRF tokens, state parameters); test CSP nonce and other security-sensitive headers for improper cookie reflection; look for cookie tossing vectors via HTTP response splitting or cache poisoning; test OAuth implementations for dirty dancing vulnerabilities in other web applications with similar architecture

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS exploitation)
- T1056 - Input Capture (webcam/microphone hijacking)
- T1528 - Steal Application Access Token (OAuth token theft)
- T1539 - Steal Web Session Cookie (session hijacking)
- T1189 - Drive-by Compromise (XSS delivery via cookie tossing)
- T1566 - Phishing (potential delivery vector for malicious cookies)
- T1110 - Brute Force (potential WAF evasion techniques)

## Notes
Reported 10/02/23, patched 01/01/24. Multi-stage exploitation chain demonstrating that seemingly unexploitable self-XSS vulnerabilities can achieve critical impact through proper chaining. Cookie string parsing behavior was unusual and required reverse engineering. The 'Cookie Tossing' technique (referenced but not fully detailed in excerpt) was crucial for cross-user exploitation. Research credited to Sudi, BrunoZero, and H4R3L.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
