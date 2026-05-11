# Zoom Account Takeover via Chained Cookie XSS and OAuth Dirty Dancing

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Stored XSS via Cookie Manipulation, Cookie Tossing / Cookie Poisoning, CSP Nonce Injection, OAuth Authorization Code Theft, Privilege Escalation, Insecure Browser Permission Handling
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two seemingly unexploitable cookie XSS vulnerabilities via cookie string parsing and cookie tossing techniques to achieve persistent account takeover of Zoom users. The attack leveraged CSP nonce injection to bypass security controls, steal OAuth authorization codes, and hijack browser permissions to enable webcams and microphones on web-based Zoom without user consent.

## Attack scenario (step by step)
1. Attacker identifies Cookie XSS vulnerability in _zm_csp_script_nonce cookie by exploiting improper cookie string parsing logic
2. Attacker crafts malicious cookie payload using escape sequences to bypass CSP nonce validation: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//"
3. Attacker uses cookie tossing/cache poisoning technique to persist malicious cookie across multiple user sessions
4. When victim visits zoom.us, malicious JavaScript executes in victim's browser context with full page privileges
5. Injected payload intercepts OAuth flow, steals authorization codes, and hijacks browser permission grants for camera/microphone
6. Attacker gains persistent account takeover, can impersonate user, access meetings, and enable surveillance capabilities

## Root cause
Insufficient input validation and improper escaping of cookie values when reflected into CSP headers and script nonce attributes. The backend performed quote-based cookie string parsing without sanitizing special characters, allowing escape sequence injection. Additionally, inadequate cache control headers and cookie scope restrictions enabled cookie tossing attacks across multiple requests.

## Attacker mindset
Persistence and creative thinking - recognizing that seemingly unexploitable self-XSS vulnerabilities could be chained through cookie manipulation and cache poisoning. The attacker viewed cookie XSS as underrated and investigated non-obvious attack vectors like CSP nonce injection and cookie tossing rather than direct payload execution. Focus on understanding server-side logic (cookie parsing) rather than client-side filtering.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding for all cookie values before reflecting them into HTTP headers or DOM attributes
- Use parameterized/templated approaches for CSP nonce generation rather than string concatenation with user-controlled data
- Enforce consistent Cache-Control headers (no-store, no-cache) on all authenticated endpoints to prevent cookie tossing attacks
- Implement SameSite cookie attributes (Strict/Lax) to prevent cross-site cookie injection
- Avoid cookie string parsing logic that treats cookies as quoted strings - parse cookie name and value strictly
- Implement additional CSRF protections and state validation in OAuth flows to prevent authorization code theft
- Use content security policies that prevent cookie-based nonce manipulation through stricter nonce generation and validation
- Monitor and alert on unusual CSP policy modifications or nonce mismatches
- Implement browser permission request validation with additional user confirmations for sensitive features like camera/microphone

## Variant hunting
['Search for other security-critical cookies that are reflected in HTTP headers without sanitization (_zm_csp_*, csrf tokens, session identifiers)', 'Audit all CSP implementations across subdomains for similar nonce injection vectors', 'Test cache poisoning on other endpoints with dynamic content that may have improper cache headers', 'Look for cookie string parsing logic in other frameworks and applications - this is a subtle but exploitable pattern', 'Investigate OAuth implementations for other code/token leakage through XSS vectors', 'Test browser permission hijacking on other web applications supporting camera/microphone access', 'Search for similar escape sequence handling in cookie processing across Zoom infrastructure']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1539 - Steal Web Session Cookie
- T1556 - Modify Authentication Process
- T1111 - Multi-Factor Authentication Interception
- T1187 - Forced Authentication
- T1185 - Capture Web Session Cookie
- T1566 - Phishing
- T1528 - Steal Application Access Token
- T1552 - Unsecured Credentials

## Notes
This is an exemplary bug bounty writeup demonstrating creative vulnerability chaining. The researchers moved beyond basic XSS exploitation to understand underlying server-side logic (cookie string parsing) and web caching mechanisms. The $15k bounty reflects the critical impact of full account takeover with surveillance capabilities. The writeup emphasizes that 'useless' or 'self-XSS' vulnerabilities should not be dismissed - context and chaining with other weaknesses can create critical exploits. The cookie tossing/cache poisoning component appears to be the persistence mechanism that transformed a cookie XSS into a stored vulnerability affecting multiple sessions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
