# Reflected XSS in UUID Parameter on uu.nl Subdomain

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a UUID parameter on a uu.nl subdomain where user input was reflected directly within HTML title tags without proper sanitization. The attacker successfully broke out of the title tag context and injected arbitrary JavaScript code that executes in the victim's browser.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl as targets
2. Attacker uses waybackurls tool to discover historical endpoints and identifies a URL pattern with vulnerable UUID parameter
3. Attacker crafts payload with UUID value: test</title><script>alert(document.domain)</script>
4. Victim receives malicious link via phishing/social engineering and visits the crafted URL
5. Browser renders the page with injected JavaScript code that executes in victim's security context
6. Attacker gains ability to steal session cookies, perform actions on behalf of user, or redirect to malicious sites

## Root cause
The application reflected the UUID parameter value directly into the HTML title tag without proper HTML entity encoding or input validation. The developers failed to escape special characters like '<' and '>', allowing tag injection attacks. No Content Security Policy (CSP) was in place to prevent inline script execution.

## Attacker mindset
Systematic reconnaissance using subdomain enumeration and historical URL discovery tools to identify attack surface. Opportunistic exploitation of common parameter names (UUID) known to be used for tracking/logging. Practical payload construction to break out of existing HTML context with minimal code.

## Defensive takeaways
- Implement HTML entity encoding for all user-controlled data reflected in HTML context (use framework-provided escaping functions)
- Apply input validation to reject or sanitize unexpected characters in UUID parameters
- Implement Content Security Policy (CSP) headers to prevent inline script execution even if XSS bypasses encoding
- Use security-focused template engines that default to auto-escaping output
- Conduct security testing on all subdomains, particularly wildcard subdomains often overlooked in assessments
- Implement Web Application Firewall (WAF) rules to detect and block common XSS payloads
- Regular security code reviews focusing on output encoding in templating code

## Variant hunting
['Test other parameters on the same endpoint for similar reflection vulnerabilities', 'Check other subdomains for identical vulnerable patterns', 'Attempt DOM-based XSS variants if JavaScript processes the UUID client-side', 'Test for stored XSS if UUID values are cached/logged and displayed elsewhere', 'Explore attribute context escaping (if parameter reflected in HTML attributes)', 'Test for JavaScript context XSS if UUID is used in script sections', 'Examine error messages and 404 pages for reflected input']

## MITRE ATT&CK
- T1190
- T1566.002
- T1059.007

## Notes
This vulnerability demonstrates 'accidental' XSS from incomplete security implementation rather than sophisticated exploitation. The writeup lacks specific subdomain disclosure (redacted as uu.nl standard practice). No mention of bounty amount or impact assessment. The payload is straightforward tag-breaking approach. Waybackurls tool proved valuable for discovering parameters not actively advertised, highlighting importance of historical data in vulnerability research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
