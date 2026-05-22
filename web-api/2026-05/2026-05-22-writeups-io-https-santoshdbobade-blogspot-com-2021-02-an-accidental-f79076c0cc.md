# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain where user-supplied UUID parameter input was reflected directly into the HTML title tag without proper sanitization. The attacker was able to break out of the title tag context and execute arbitrary JavaScript code by injecting a closing title tag followed by a script tag.

## Attack scenario (step by step)
1. Researcher enumerates subdomains of uu.nl using reconnaissance techniques
2. Historical URLs are collected using waybackurls tool to identify endpoint patterns
3. An interesting URL pattern is identified containing a uuid parameter: https://www.*.uu.nl/XXXXXX/?uuid=vulnerablepoint
4. Input is tested to determine where it reflects in the response (identified in title tag)
5. Payload is crafted to break out of title tag context: test</title><script>alert(document.domain)</script>
6. Payload is injected via uuid parameter, achieving arbitrary JavaScript execution in victim's browser

## Root cause
Insufficient input validation and output encoding on user-supplied uuid parameter. The application reflected the parameter value directly into an HTML title tag without proper escaping or sanitization, allowing tag breakout attacks.

## Attacker mindset
Systematic reconnaissance approach combining subdomain enumeration with historical URL analysis to identify endpoints. Methodical testing to understand reflection points before crafting context-aware payload to escape tag boundaries.

## Defensive takeaways
- Implement strict output encoding/escaping for all user input based on context (HTML entity encoding for title tags)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Apply input validation whitelisting for UUID parameters to reject unexpected characters
- Implement automatic HTML sanitization libraries that understand tag contexts
- Conduct security code review focusing on data flow from URL parameters to HTML output
- Use parameterized templating engines that enforce proper escaping by default
- Implement security testing in CI/CD pipeline for common XSS patterns

## Variant hunting
['Test other UUID/ID parameters across the same subdomain for similar reflection vulnerabilities', 'Enumerate other uu.nl subdomains for comparable parameter injection points', 'Test different tag contexts (script, iframe, img onerror, etc.) for bypass opportunities', 'Check if DOM-based XSS variants exist in JavaScript processing of URL parameters', 'Investigate if similar vulnerable patterns exist in other query parameters on the same endpoint']

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
The writeup lacks specific subdomain details (redacted) and does not mention bounty amount or remediation timeline. Attack is straightforward tag-breaking XSS in a relatively common reflection context. The simplicity suggests weak or absent input validation practices at the application level. No mention of WAF bypass or encoding evasion indicates direct reflection without preprocessing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
