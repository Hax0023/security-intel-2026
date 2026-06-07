# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Input Validation Failure
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a UUID parameter on a uu.nl subdomain where user input was reflected directly within HTML title tags without proper sanitization. The attacker successfully injected a script tag by breaking out of the title element context and executing arbitrary JavaScript in the victim's browser.

## Attack scenario (step by step)
1. Researcher enumerated subdomains of uu.nl and identified www.*.uu.nl as a testing target
2. Using waybackurls tool, collected historical URLs and identified an endpoint with a uuid parameter: https://www.*.uu.nl/XXXXXX/?uuid=vulnerable
3. Tested the uuid parameter and observed user input was reflected within HTML title tags without encoding
4. Crafted payload to break out of title tag context: test</title><script>alert(document.domain)</script>
5. Injected payload through uuid parameter, successfully closing title tag and opening script tag
6. Script executed in browser context, demonstrating arbitrary JavaScript execution capability

## Root cause
Insufficient input validation and output encoding. The application failed to HTML-encode or sanitize user-supplied UUID parameter before reflecting it within HTML title tags, allowing tag injection and script execution.

## Attacker mindset
Methodical reconnaissance using passive enumeration (waybackurls) to identify attack surface, systematic parameter testing to locate reflection points, and payload crafting to escape existing HTML context and execute arbitrary code.

## Defensive takeaways
- Implement strict output encoding based on context (HTML entity encoding for HTML content)
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Apply input validation whitelisting for UUID parameters (validate format before processing)
- Implement automated scanning for reflected XSS vulnerabilities in CI/CD pipeline
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Conduct regular security code reviews focusing on user input reflection points

## Variant hunting
Search for similar UUID or ID parameters across all uu.nl subdomains that reflect user input in HTML contexts (title, meta, div attributes). Test other parameter names (id, token, reference, code) with tag-breaking payloads. Look for other reflection points in HTTP headers and different HTML contexts.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The vulnerability was described as 'accidental' suggesting the application developer did not intentionally create a security flaw but rather failed to implement proper output encoding. The specific subdomain and endpoint were redacted from the writeup. No information provided regarding patch timeline, bounty amount, or whether it was submitted to a formal bug bounty program. The simplicity of the exploitation technique suggests this may have been overlooked during security testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
