# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cookie-based XSS, CSP Nonce Bypass, OAuth Authorization Code Theft, Browser Permission Hijacking, Cookie Tossing, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable cookie-based XSS vulnerabilities through cookie tossing techniques to achieve persistent account takeover on Zoom. The attack combined CSP nonce bypass, OAuth dirty dancing to steal authorization codes, and malicious manipulation of browser permissions to silently enable webcam/microphone access on web-based Zoom.

## Attack scenario (step by step)
1. Attacker identifies XSS in _zm_csp_script_nonce cookie via cookie string parsing vulnerability and CSP nonce escaping
2. Attacker uses cookie tossing technique to send multiple cookie values, bypassing same-origin restrictions and WAF protections
3. Malicious JavaScript executes in context of zoom.us, stealing CSRF tokens and session identifiers
4. Attacker leverages OAuth dirty dancing to intercept authorization codes during OAuth flow
5. JavaScript hijacks browser permission requests to silently grant microphone/webcam access without user interaction
6. Attacker gains persistent access to user account with full AV capabilities and session control

## Root cause
Inadequate cookie value validation and parsing, improper CSP nonce generation/handling, and failure to sanitize cookie data before reflective use in HTTP headers and DOM. Cookie string parsing treated quotes as delimiters without proper escaping validation.

## Attacker mindset
Persistence-focused chain attack methodology; recognized that individual XSS bugs appeared unexploitable but systematically analyzed cookie handling mechanisms to find parsing quirks. Leveraged multiple weak primitives (XSS + cookie tossing) to achieve high-impact account takeover with AV hijacking as bonus.

## Defensive takeaways
- Implement strict cookie validation and never parse cookie values as quoted strings without explicit escaping
- Regenerate CSP nonces randomly on each request and validate nonce format strictly
- Sanitize all cookie data before use in HTTP response headers or DOM attributes
- Implement SameSite=Strict cookie flags to prevent cookie tossing attacks
- Require explicit user interaction before granting sensitive permissions (microphone, camera)
- Implement OAuth state parameter validation and PKCE for authorization code protection
- Monitor for unusual permission request patterns and require re-authentication for sensitive access grants
- Apply consistent WAF rules across all subdomains and cookie handling paths

## Variant hunting
Hunt for cookie-based XSS on domains with CSP policies; test all cookie parameters for string parsing behaviors; examine subdomain cookie inheritance; search for similar nonce-based mechanisms (CSRF tokens, tracking IDs) vulnerable to escape sequence bypass; test cookie tossing feasibility across different browser implementations; look for permission prompt abuse in other WebRTC applications.

## MITRE ATT&CK
- T1190
- T1200
- T1539
- T1557
- T1621
- T1185
- T1187
- T1566

## Notes
Excellent example of creative vulnerability chaining where individual bugs (unexploitable XSS) gain critical impact through secondary techniques (cookie tossing, OAuth interception). The cookie string parsing vulnerability is a subtle server-side implementation detail often overlooked. The bonus 'WAF Frame-Up' DoS technique demonstrates how XSS can be weaponized to manipulate security infrastructure perception. Coordinated team effort was essential for discovering the attack chain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
