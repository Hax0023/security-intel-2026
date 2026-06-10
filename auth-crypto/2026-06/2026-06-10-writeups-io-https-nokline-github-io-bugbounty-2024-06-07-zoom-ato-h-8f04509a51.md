# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permissions Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cross-Site Scripting (XSS), Cookie XSS, CSP Bypass, OAuth Token Theft, Cookie Tossing, Browser Permission Hijacking, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers discovered and chained two seemingly unexploitable XSS vulnerabilities in Zoom's CSP nonce cookie through cookie string parsing flaws to achieve persistent session hijacking. By combining cookie tossing attacks, OAuth dirty dancing, and browser permission abuse, attackers could steal authorization codes and silently enable webcam/microphone access on Zoom web. The vulnerability enabled complete account takeover with silent privilege escalation through browser permission hijacking.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS in _zm_csp_script_nonce parameter via cookie string parsing vulnerability that improperly handles escaped quotes
2. Attacker crafts malicious nonce payload using quote escaping: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//" to bypass CSP restrictions and execute arbitrary JavaScript
3. XSS payload uses cookie tossing technique to set malicious cookies across multiple domains, exploiting cookie handling inconsistencies
4. Malicious JavaScript intercepts OAuth authorization code flow through 'OAuth Dirty Dancing' to steal authorization tokens
5. Script requests browser permissions (microphone/camera) while victim is in authenticated session, exploiting permission trust context
6. Attacker gains persistent access to victim account with ability to silently activate surveillance capabilities and maintain long-term session control

## Root cause
Unsafe cookie string parsing in CSP nonce handling that treats cookie values as quoted strings without proper sanitization or escaping validation. The server failed to properly escape or validate the _zm_csp_script_nonce cookie before reflecting it in CSP headers and HTML script attributes. Double-quote escaping in cookie values was processed by the parsing mechanism, allowing attackers to break out of the intended string context and inject arbitrary CSP directives and JavaScript.

## Attacker mindset
Persistence-focused thinking: Rather than seeking quick self-XSS vulnerabilities, researchers identified underrated cookie XSS vectors with 'potential energy' that seemed unexploitable in isolation. The approach demonstrates lateral thinking by recognizing that cookie parsing edge cases (quote handling) could lead to CSP bypass. The chaining methodology shows sophisticated understanding of how seemingly separate vulnerabilities (XSS + OAuth + permissions + cookies) can be combined into a complete account takeover, treating browser security features as components to manipulate rather than barriers.

## Defensive takeaways
- Implement strict input validation and output encoding for all cookie values, especially security-critical cookies like CSP nonces
- Avoid cookie string parsing that treats values as quoted strings; use explicit, non-ambiguous parsing methods
- Generate CSP nonces server-side and validate them cryptographically rather than reflecting user-controlled or cookie-influenced values
- Implement proper quote escaping at the encoding layer (HTML entity encoding, attribute encoding) separate from application parsing logic
- Apply defense-in-depth: combine CSP with additional XSS protections (X-XSS-Protection headers, subresource integrity, trusted types)
- Validate and sanitize all cookie values even if they appear to be internal/system cookies
- Implement cookie scope restrictions and SameSite attributes to limit cookie tossing attack surface
- Add monitoring for suspicious OAuth authorization code patterns and browser permission requests from authenticated sessions
- Regularly audit CSP header generation and test with fuzzing payloads including quote escaping variations
- Implement secure cookie storage with encryption and integrity checking to prevent tampering

## Variant hunting
Hunt for similar vulnerabilities in other security-critical cookies (e.g., CSRF tokens, session identifiers, security nonces). Test quote escaping and backslash handling in all cookie-based security mechanisms. Look for cookie values reflected in security headers (Content-Security-Policy, X-Frame-Options, Strict-Transport-Security). Examine other authentication flows for OAuth interception vulnerabilities. Test browser permission request contexts in authenticated vs. unauthenticated states. Search for other domains using similar cookie parsing patterns or CSP nonce reflection mechanisms. Look for CSP bypasses via other cookie-controlled parameters or header injection points.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1012 - Query Registry (cookie examination)
- T1185 - Man in the Browser
- T1056 - Input Capture (microphone/camera hijacking)
- T1539 - Steal Web Session Cookie
- T1528 - Steal Application Access Token
- T1566 - Phishing (permission prompt social engineering)
- T1218 - System Binary Proxy Execution (WAF frame-up abuse)
- T1021 - Remote Services (session hijacking for lateral movement)

## Notes
Critical finding demonstrates that 'unexploitable' self-XSS vulnerabilities require deep technical analysis to identify exploitation paths. Cookie parsing edge cases represent an overlooked attack surface. The cookie tossing + OAuth dirty dancing + permission hijacking chain illustrates sophisticated multi-vector attack composition. Researchers identified the vulnerability on 10/02/23 and Zoom fully patched by 01/01/24. The 'WAF Frame-Up' DoS technique mentioned in title is a secondary abuse vector demonstrating how XSS can be leveraged to trigger WAF false positives. The vulnerability affected nearly every page and subdomain due to widespread CSP nonce cookie usage, indicating systemic rather than isolated weakness.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
