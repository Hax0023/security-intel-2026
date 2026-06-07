# Zoom Session Takeover via Cookie XSS, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS) - Cookie-based, Cookie Tossing, OAuth Authorization Code Interception, Browser Permission Hijacking, Content Security Policy (CSP) Bypass, WAF Evasion
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained multiple vulnerabilities to achieve account takeover on Zoom: exploiting a cookie XSS in the _zm_csp_script_nonce parameter through cookie string parsing weakness, leveraging cookie tossing to inject malicious cookies, intercepting OAuth authorization codes via dirty dancing techniques, and hijacking browser permissions to silently enable webcam and microphone access. The vulnerability required sophisticated payload crafting to bypass CSP policies and affect all major Zoom subdomains.

## Attack scenario (step by step)
1. Attacker identifies that Zoom's _zm_csp_script_nonce cookie undergoes unsafe string parsing, treating the cookie value as a quoted string
2. Attacker crafts malicious cookie payload using escape sequences to break out of CSP nonce attribute: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//"
3. Using cookie tossing techniques, attacker injects malicious cookie into victim's browser via Set-Cookie headers from attacker-controlled domain
4. Victim visits zoom.us, malicious cookie is reflected in CSP headers and script nonce attributes, executing arbitrary JavaScript
5. Injected script intercepts OAuth authorization flows using 'dirty dancing' to steal authorization codes during redirect chains
6. JavaScript payload requests browser permissions and silently activates webcam/microphone on Zoom web application

## Root cause
Multiple weaknesses: (1) Unsafe cookie value parsing treating input as quoted strings without proper sanitization, (2) CSP nonce generation logic that fails to sanitize reflected cookie values, (3) Cookie domain/path inheritance allowing cookie tossing from subdomains, (4) Insufficient validation of OAuth redirect URIs enabling code interception, (5) Lack of user-prompted verification for sensitive permission grants

## Attacker mindset
Persistent vulnerability chaining specialist seeking high-impact account takeover; willing to invest time in understanding CSP mechanics, cookie handling quirks, and OAuth flows; recognizes that 'self-XSS' and cookie-based XSS are underestimated attack vectors; systematically tests unusual input handling (quoted string parsing) rather than assuming standard sanitization

## Defensive takeaways
- Implement strict input sanitization on all cookie values regardless of perceived trust level; never reflect cookie data into security-critical contexts like CSP directives without proper HTML entity encoding
- Use context-aware output encoding: HTML encode, attribute encode, and JavaScript encode based on where data is reflected
- Implement SameSite=Strict cookie attribute to prevent cookie tossing attacks from related domains
- Regenerate CSP nonces server-side on each request rather than reflecting from cookies; use cryptographically random nonces that cannot be influenced by user input
- Enforce strict OAuth redirect URI whitelisting with exact matching; validate that redirect URIs are on expected domains
- Require explicit user interaction and informed consent for sensitive permissions (camera, microphone) with clear security warnings
- Implement additional CSRF tokens for critical operations beyond cookie validation
- Regular security audits of cookie handling logic across all subdomains with consistent policies
- Monitor and alert on unusual CSP violations or permission grants from JavaScript

## Variant hunting
Hunt for similar cookie parsing vulnerabilities in other security-critical cookies (_zm_auth_token, session identifiers); test for cookie tossing on other platforms using wildcard domain cookies; search for other instances where CSP nonces or security tokens are derived from user-controllable input; look for OAuth implementations with lax redirect URI validation; test permission grant flows on other web-based communication platforms for similar hijacking

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS vulnerability exploitation)
- T1539 - Steal Web Session Cookie (session hijacking via OAuth code theft)
- T1185 - Man in the Browser (JavaScript injection to intercept OAuth flows)
- T1528 - Steal Application Access Token (OAuth authorization code interception)
- T1115 - Gather Victim Host Information (permission hijacking reconnaissance)
- T1656 - Impersonate Third-Party Vendor (OAuth dirty dancing attack)

## Notes
Vulnerability reported 10/02/2023 and fully patched by 01/01/2024; demonstrates the power of chaining multiple 'low-severity' vulnerabilities (self-XSS, cookie handling, OAuth quirks) into critical account takeover; cookie XSS is an underrated attack vector that deserves more attention in security research; the cookie string parsing behavior was non-standard and required deep understanding of the application's backend logic; authors successfully exploited nearly all Zoom subdomains due to cookie inheritance; WAF frame-up technique mentioned as bonus DoS vector where XSS can be used to generate malicious traffic appearing to originate from victim

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
