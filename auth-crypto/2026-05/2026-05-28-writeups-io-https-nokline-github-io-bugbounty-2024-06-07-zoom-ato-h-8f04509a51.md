# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** CRITICAL
- **Vuln types:** Cookie XSS (via CSP Nonce manipulation), Cookie Tossing, OAuth Authorization Code Theft, Browser Permission Hijacking, WAF Bypass, Stored XSS (via cookie persistence)
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable cookie-based XSS vulnerabilities into a persistent session hijacking attack by leveraging cookie tossing techniques to bypass validation. The attack chain allowed stealing OAuth authorization codes and hijacking browser permissions to silently enable webcam/microphone access on Zoom web.

## Attack scenario (step by step)
1. Attacker identifies CSP nonce cookie (_zm_csp_script_nonce) reflects user input without sanitization, but only when properly escaped through cookie string parsing
2. Attacker crafts malicious cookie payload exploiting cookie string parsing to inject JavaScript: _zm_csp_script_nonce="test\"' 'nonce-test' >alert(1)//
3. Attacker uses cookie tossing technique to set multiple cookies with same name across subdomains, causing victim browser to send crafted cookie to Zoom servers
4. Injected JavaScript executes within victim's browser context, bypassing CSP via matching nonce values reflected in 40+ scripts
5. Malicious script silently steals OAuth authorization codes or requests browser permissions (camera/microphone) using credential-included requests
6. Attacker gains persistent session access and can control victim's Zoom camera/microphone or perform account takeover via stolen auth codes

## Root cause
Insufficient input validation on CSP nonce cookie combined with unsafe cookie string parsing allowed injection of nonce attribute content. Server failed to properly sanitize cookie values before reflecting them in both CSP headers and script nonce attributes. No server-side validation prevented cookie tossing attacks across subdomains.

## Attacker mindset
Methodical cookie-focused reconnaissance on high-value target; recognized that 'unexploitable' self-XSS becomes dangerous when chained with cookie tossing and OAuth flows; understood browser permission model as attack surface; treated CSP as constraint to work around rather than accept; leveraged WAF weaknesses for denial of service amplification.

## Defensive takeaways
- Implement strict input validation and HTML entity encoding on all cookie values before reflecting in HTTP headers or HTML attributes
- Use server-side nonce generation that never reflects user input; validate nonce structure server-side before rendering
- Implement SameSite=Strict cookie attributes and validate cookie scope to prevent cookie tossing attacks
- Disable or restrict silent browser permission grants; require explicit user interaction for sensitive permissions like camera/microphone
- Implement additional CSRF/state validation for OAuth authorization code flows beyond standard PKCE
- Review CSP implementation for unintended bypass vectors; avoid reflecting any user-controllable data in security headers
- Implement rate limiting and behavioral analysis on WAF to detect distributed XSS exploitation patterns
- Conduct regular security audits specifically targeting cookie handling, CSP configuration, and OAuth implementation on all subdomains

## Variant hunting
Hunt for similar CSP nonce/header injection via cookies on: (1) other security-related cookies that generate headers (CSRF tokens, API keys), (2) subdomains with inherited cookie policies, (3) cookie-based feature flags or session identifiers reflected in HTML, (4) applications using cookie string parsing for configuration, (5) OAuth implementations with state parameter stored in cookies, (6) WAF/proxy configurations that process cookies before validation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (XSS via cookie reflection)
- T1539 - Steal Web Session Cookie (OAuth authorization code theft)
- T1528 - Steal Application Access Token (OAuth dirty dancing)
- T1056 - Phishing for Information (silent permission hijacking)
- T1559 - Inter-Process Communication (browser permission abuse)
- T1566 - Phishing (potential delivery vector for cookie tossing)
- T1204 - User Execution (permission grant with social engineering)

## Notes
This is a sophisticated multi-stage attack requiring deep understanding of cookies, CSP, OAuth, and browser security models. The 'cookie tossing' technique is underutilized in security research despite being highly effective. The research team's approach of finding self-XSS and subsequently weaponizing it demonstrates value of persistence on mature targets. Published writeup lacks detailed cookie tossing mechanics (partially redacted in provided content). Patch verification on 01/01/2024 confirms effective remediation. Total research effort involved three security researchers, indicating complexity of exploitation chain.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
