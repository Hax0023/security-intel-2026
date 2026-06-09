# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** Critical
- **Vuln types:** Cookie XSS, Cookie Tossing, OAuth Token Theft, Browser Permission Hijacking, CSP Bypass, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained multiple vulnerabilities to achieve persistent account takeover on Zoom's web platform. By exploiting a cookie-based XSS in the CSP nonce parameter combined with cookie tossing techniques, they could steal OAuth authorization codes and hijack browser permissions to enable microphone/webcam without user consent.

## Attack scenario (step by step)
1. Attacker crafts malicious cookie containing escaped payload targeting _zm_csp_script_nonce parameter
2. Cookie tossing technique forces victim's browser to reflect attacker's nonce value in CSP headers and script tags
3. XSS payload executes in victim's browser, bypassing CSP restrictions through nonce manipulation
4. Malicious script steals OAuth authorization codes during login flow or session refresh
5. Attacker exchanges stolen authorization code for session tokens and refresh tokens
6. Session hijacked and browser permissions (microphone/camera) are remotely enabled via stored XSS payload

## Root cause
Improper cookie string parsing in CSP nonce generation allowed unescaped quotes to break out of intended context. Zoom's server-side code parsed cookie values using quoted-string semantics without proper validation, reflecting user-controlled cookie data into CSP headers and DOM attributes without sanitization.

## Attacker mindset
Persistent, methodical vulnerability researcher who recognized that seemingly 'unexploitable' self-XSS vulnerabilities could become weaponized through chaining with cookie handling logic. Demonstrated deep understanding of browser security models (CSP, OAuth flows, permissions API) and willingness to invest significant effort in understanding edge cases in cookie parsing behavior.

## Defensive takeaways
- Never trust cookie values without explicit validation and sanitization, even if they appear to be internal/system cookies
- Implement strict CSP nonce generation that cryptographically generates nonces server-side without reflecting cookie data
- Avoid cookie string parsing semantics; treat all cookie values as opaque strings and escape appropriately for context
- Implement additional CSRF/state tokens on OAuth flows to prevent authorization code theft
- Monitor and validate browser permission changes, require explicit user interaction for sensitive permissions
- Test CSP effectiveness by attempting to escape nonce attributes and inject additional directives
- Implement SameSite cookie attributes to mitigate cookie tossing attacks
- Apply consistent sanitization across all subdomains and cloned domains

## Variant hunting
['Search for other system cookies used in security contexts (CSP, security headers, OAuth state)', 'Test cookie parsing behavior across different backend frameworks and web servers', 'Look for reflected cookie values in any response header or DOM attribute', 'Examine OAuth implementations for authorization code validation and state parameter verification', 'Test browser permission requests for lack of user interaction validation', 'Identify other cookies used in template rendering that might be parsed or escaped inconsistently', 'Hunt for WAF configuration allowing requests with malformed cookies to reach origin server']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS in Zoom web app)
- T1539 - Steal Web Session Cookie (Cookie-based session hijacking)
- T1528 - Steal Application Access Token (OAuth authorization code theft)
- T1005 - Data from Local System (Browser permission hijacking for microphone/camera)
- T1566 - Phishing (cookie tossing via compromised link/network)
- T1083 - File and Directory Discovery (identifying vulnerable cookie parameters)
- T1199 - Trusted Relationship (exploiting trust in Zoom subdomains)

## Notes
This writeup represents sophisticated vulnerability chaining requiring expertise in multiple domains: cookie handling, CSP mechanics, OAuth security, and browser security APIs. The 'cookie tossing' technique exploits HTTP/2 multiplexing to force victims to use attacker-controlled cookies. The research demonstrates that 'unexploitable' self-XSS can become critical when combined with infrastructure-level vulnerabilities. Zoom's 3-month remediation timeline (Oct 2023 - Jan 2024) reflects the complexity of fixing underlying cookie parsing logic across distributed infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
