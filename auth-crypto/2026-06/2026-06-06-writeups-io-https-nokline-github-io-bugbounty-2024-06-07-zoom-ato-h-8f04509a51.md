# Zoom Session Takeover via Cookie Tossing, OAuth Dirty Dancing, and Browser Permission Hijacking

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Zoom Bug Bounty Program
- **Bounty:** $15,000
- **Severity:** critical
- **Vuln types:** Cross-Site Scripting (XSS), Cookie Tossing, OAuth Authorization Code Theft, Browser Permission Hijacking, Content Security Policy (CSP) Bypass, WAF Bypass
- **Category:** auth-crypto
- **Writeup:** https://nokline.github.io/bugbounty/2024/06/07/Zoom-ATO.html

## Summary
Researchers chained two unexploitable cookie XSS vulnerabilities through cookie tossing techniques to achieve persistent XSS, enabling theft of OAuth authorization codes and hijacking of browser permissions to silently activate webcams and microphones on Zoom web. The vulnerability leveraged CSP nonce parsing flaws and cookie string parsing behavior to bypass security controls across zoom.us and subdomains.

## Attack scenario (step by step)
1. Attacker identifies XSS in _zm_csp_script_nonce cookie by exploiting improper cookie string parsing that treats quoted values as literal strings
2. Attacker crafts malicious cookie payload using escaped quotes to break out of CSP nonce context and inject arbitrary JavaScript across ~40 reflected script tags
3. Attacker uses cookie tossing technique to set malicious cookies on victim's browser by injecting Set-Cookie headers via XSS payload
4. Persistent XSS payload executes on subsequent page loads, stealing OAuth authorization codes through 'OAuth Dirty Dancing' technique
5. Attacker hijacks browser permissions by executing JavaScript that triggers permission prompts or exploits existing permission grants to access webcam/microphone
6. Attacker establishes session takeover by using stolen OAuth tokens and can perform actions as victim including recording video/audio without consent

## Root cause
Unsafe cookie string parsing that treats cookie values containing quotes as quoted strings with escape sequence support, combined with lack of proper HTML escaping when reflecting cookie values into CSP headers and script nonce attributes. CSP nonce mismatch between header declaration and actual script tags enabled bypass of the security policy.

## Attacker mindset
Patient, methodical vulnerability chaining approach. Researchers recognized that individual XSS vectors were unexploitable but demonstrated creativity in finding an exploitation path through cookie tossing. This represents sophisticated thinking about browser security mechanisms and their interactions rather than exploiting obvious flaws.

## Defensive takeaways
- Never reflect cookie values directly into security-critical contexts like CSP headers without proper HTML entity encoding
- Implement strict cookie parsing that does not interpret escape sequences or quoted strings in cookie values
- Use constant, server-validated nonces for CSP that are not derived from user-controlled input
- Apply defense-in-depth by validating CSP nonce values match between headers and DOM before allowing script execution
- Implement SameSite cookie attribute to restrict cookie tossing attacks and prevent cross-site cookie injection
- Monitor for suspicious cookie manipulation patterns in WAF/security tools
- Regularly audit all cookie handling code for unsafe parsing or reflection patterns
- Implement strict Content Security Policy with proper nonce validation to prevent JavaScript injection

## Variant hunting
Hunt for similar cookie XSS in other security-critical cookies (CSRF tokens, session markers, nonce values). Test for cookie string parsing behavior on other major platforms. Examine CSP nonce generation logic for user-controlled inputs. Look for other cases where cookies are reflected into HTML attributes without proper escaping. Test for cookie tossing opportunities on applications with loose cookie validation.

## MITRE ATT&CK
- T1190
- T1539
- T1528
- T1187
- T1566
- T1598
- T1021

## Notes
Reported October 2, 2023 and fully patched by January 1, 2024. This represents sophisticated vulnerability research combining multiple attack vectors (XSS, cookie manipulation, OAuth attacks, permission hijacking). The writeup demonstrates how 'unexploitable' self-XSS vulnerabilities can become critical through creative chaining techniques. The cookie string parsing behavior was non-standard and required careful analysis to understand and exploit.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
