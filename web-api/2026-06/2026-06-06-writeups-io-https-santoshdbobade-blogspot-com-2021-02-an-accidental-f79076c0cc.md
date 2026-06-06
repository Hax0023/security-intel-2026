# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln types:** Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered in a UUID parameter on a uu.nl subdomain where user input was insufficiently sanitized and reflected within HTML title tags. The attacker was able to break out of the title tag and inject arbitrary JavaScript code that executes in the victim's browser context.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl using subdomain enumeration techniques
2. Attacker collects historical URLs using waybackurls tool to identify interesting endpoints
3. Attacker identifies a URL parameter 'uuid' that reflects user input in the page
4. Attacker observes the uuid parameter is reflected within an HTML title tag without proper encoding
5. Attacker crafts payload closing the title tag and injecting script: test</title><script>alert(document.domain)</script>
6. Attacker shares malicious link with victim; when clicked, JavaScript executes with victim's session context

## Root cause
The application accepted user-supplied input via the 'uuid' query parameter and reflected it directly into the HTML title tag without proper encoding or sanitization, allowing attackers to break out of the tag context and inject arbitrary HTML/JavaScript.

## Attacker mindset
Systematic reconnaissance through subdomain enumeration and historical URL analysis to identify attack surface, followed by testing common reflection points and HTML tag boundary testing to achieve code execution.

## Defensive takeaways
- Implement proper output encoding based on context (HTML entity encoding for HTML context)
- Use Content Security Policy (CSP) to restrict script execution and reduce XSS impact
- Apply input validation to restrict uuid parameter to expected format (UUID format validation)
- Implement automated security scanning in CI/CD pipeline to detect XSS vulnerabilities
- Use templating engines with auto-escaping enabled by default
- Conduct regular security code reviews focusing on user input handling
- Apply defense-in-depth with multiple layers of protection rather than relying on single defense

## Variant hunting
['Check other URL parameters on same endpoint for similar reflection issues', 'Test other subdomains of uu.nl for identical vulnerable endpoints', 'Search for other instances where uuid parameters are used without encoding', 'Test DOM-based XSS variants using JavaScript manipulation of same parameter', 'Investigate whether other query parameters exhibit similar encoding failures', 'Look for stored XSS if uuid values are persisted in database and displayed elsewhere']

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
The vulnerability is relatively straightforward - basic XSS via insufficient output encoding. The writeup lacks details on: specific bounty amount, exact subdomain name (redacted), remediation timeline, and impact assessment. The discovery methodology (subdomain enumeration + waybackurls) is a practical approach for reconnaissance. UUID parameters being reflected suggests backend is simply echoing input without sanitization - a common mistake in parameter echo scenarios.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
