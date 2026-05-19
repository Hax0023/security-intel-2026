# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain where a UUID parameter was reflected unsanitized within HTML title tags. By injecting a payload that closes the title tag and opens a script tag, arbitrary JavaScript execution was achieved, allowing access to sensitive information like document.domain.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl and identifies www.*.uu.nl domains
2. Attacker uses waybackmachine historical URL collection to discover parameter-based endpoints
3. Attacker identifies a URL containing a 'uuid' parameter: https://www.*.uu.nl/XXXXXX/?uuid=vulnerablepoint
4. Attacker tests the uuid parameter and discovers it reflects within HTML title tags without encoding
5. Attacker crafts payload: test</title><script>alert(document.domain)</script>
6. Attacker sends malicious URL to victim; when clicked, JavaScript executes in victim's browser with same-origin privileges

## Root cause
The application fails to properly encode or sanitize user input (uuid parameter) before inserting it into HTML context, specifically within title tag attributes. No Context-Aware Output Encoding (CAOE) was implemented.

## Attacker mindset
Methodical reconnaissance through subdomain enumeration and historical URL discovery to identify attack surface, followed by systematic parameter testing to locate reflection points and identify encoding gaps in HTML context.

## Defensive takeaways
- Implement Context-Aware Output Encoding (CAOE) for all user inputs in different contexts (HTML, JavaScript, URL, CSS)
- Use Content Security Policy (CSP) headers to restrict inline script execution and prevent XSS payload execution
- Apply input validation to reject unexpected characters in UUID parameters
- Utilize security libraries and frameworks with built-in auto-escaping capabilities
- Conduct regular security audits of historical URLs and legacy endpoints that may have reduced security
- Implement a Web Application Firewall (WAF) with XSS detection rules

## Variant hunting
['Test other parameters on identified subdomains for similar reflection patterns', 'Search for other HTML contexts (attributes, event handlers) where parameters may reflect', 'Enumerate additional uu.nl subdomains for similar unsafe reflection vulnerabilities', 'Test different HTML tag injection points (div, span, input, etc.) for context-bypass techniques', 'Check for DOM-based XSS variants using JavaScript execution paths', 'Investigate related Utrecht University domains for shared vulnerable code']

## MITRE ATT&CK
- T1190
- T1598

## Notes
The writeup is brief with limited technical detail. The subdomain name was redacted. No indication of bounty amount or formal vulnerability disclosure timeline is provided. The vulnerability appears to be a straightforward reflected XSS with poor output encoding in an HTML context, suggesting potentially legacy or unreviewed code paths. The use of historical URL archives (waybackurls) demonstrates effective reconnaissance methodology.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
