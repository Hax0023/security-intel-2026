# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not disclosed
- **Severity:** High
- **Vuln types:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a uu.nl subdomain parameter that directly reflected user input within HTML title tags without proper encoding. The attacker was able to break out of the title tag context and inject arbitrary JavaScript code by crafting a payload that closes the title tag and injects a script element.

## Attack scenario (step by step)
1. Researcher enumerates subdomains of uu.nl and selects www.*.uu.nl for testing
2. Historical URLs are collected using waybackurls tool to identify interesting endpoints
3. An endpoint with a UUID parameter is discovered at https://www.*.uu.nl/XXXXXX/?uuid=vulnerablepoint
4. Input is tested and confirmed to reflect between HTML title tags without sanitization
5. Payload is crafted: test</title><script>alert(document.domain)</script>
6. Payload is injected via the uuid parameter, successfully breaking out of title context and executing JavaScript

## Root cause
The application failed to properly encode or sanitize user-supplied input (uuid parameter) before reflecting it within HTML title tags. No context-aware output encoding was implemented, allowing tag boundaries to be bypassed.

## Attacker mindset
Methodical reconnaissance approach using subdomain enumeration and historical URL analysis to identify potential vulnerable endpoints. When an interesting parameter was found, the attacker systematically tested for reflection points and crafted a simple tag-breaking payload to achieve code execution.

## Defensive takeaways
- Implement context-aware output encoding for all user inputs before reflection in HTML
- Use HTML entity encoding for data reflected in HTML context
- Employ Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and sanitize all user inputs, particularly URL parameters
- Use security-focused template engines that provide automatic escaping
- Conduct regular security testing and code reviews focusing on input/output handling
- Implement a Web Application Firewall (WAF) with XSS detection rules

## Variant hunting
['Test other URL parameters for similar reflection patterns', 'Check other subdomains (*.uu.nl) for the same vulnerability', 'Look for stored XSS variants if user input is persisted', 'Test different HTML contexts (attributes, JavaScript, CSS) for encoding bypasses', 'Examine API endpoints for JSON context XSS', 'Search for DOM-based XSS in JavaScript files handling similar parameters']

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The writeup lacks specific subdomain disclosure and exact bounty details. The vulnerability appears to be a straightforward reflected XSS with minimal complexity. The researcher used standard reconnaissance techniques (subdomain enumeration, wayback machine) to identify the target. This is a common type of XSS vulnerability resulting from missing output encoding rather than sophisticated bypass techniques.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
