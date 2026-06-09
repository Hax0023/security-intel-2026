# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain through a UUID parameter that was reflected unsanitized within HTML title tags. The attacker was able to break out of the title tag and inject arbitrary JavaScript code to execute in the victim's browser.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl endpoints
2. Attacker uses waybackurls tool to discover historical URLs and finds endpoint with UUID parameter
3. Attacker observes that the UUID parameter value is reflected in the page's title tag without sanitization
4. Attacker crafts payload: test</title><script>alert(document.domain)</script> to break out of title context
5. Attacker closes the title tag and injects script tag with arbitrary JavaScript
6. Victim visits malicious link containing payload and script executes in their browser context with access to session cookies and sensitive data

## Root cause
The UUID parameter was directly reflected into the HTML title tag without proper input validation, sanitization, or output encoding, allowing tag breakout and script injection.

## Attacker mindset
Opportunistic reconnaissance-focused approach: methodically enumerate subdomains, use passive recon tools (waybackurls) to discover endpoints, test for reflection points, then craft minimal tag-breaking payloads to achieve code execution.

## Defensive takeaways
- Implement input validation and sanitization for all user-supplied parameters regardless of context
- Apply context-appropriate output encoding (HTML entity encoding for HTML context, JavaScript escaping for JS context)
- Use Content Security Policy (CSP) headers to restrict script execution and prevent inline script injection
- Avoid placing user input directly in HTML tags; use framework-provided templating engines with auto-escaping
- Conduct security testing on all subdomains and less-obvious endpoints
- Implement a Web Application Firewall (WAF) to detect and block common XSS patterns
- Regular security audits and penetration testing of parameter handling across all endpoints

## Variant hunting
['Test other query parameters on the same endpoint for similar reflection vulnerabilities', 'Check if the vulnerability exists in other title tag implementations across uu.nl subdomains', 'Investigate if the same parameter is reflected in other HTML contexts (attributes, JavaScript, etc.) for DOM-based XSS', 'Search for similar UUID/identifier parameters on other uu.nl endpoints', 'Test for Stored XSS if the UUID parameter is persisted and displayed to other users', 'Check if filters exist on certain characters and attempt filter bypass techniques']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter

## Notes
The writeup is basic and lacks technical depth. The subdomain and specific parameter names are redacted. No information provided on remediation timeline, bounty amount, or program terms. The vulnerability represents a classic reflected XSS with straightforward tag-breaking exploitation requiring minimal technical skill.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
