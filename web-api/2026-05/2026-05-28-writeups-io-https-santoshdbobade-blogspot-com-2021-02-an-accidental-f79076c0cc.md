# An Accidental XSS on uu.nl

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln types:** Reflected Cross-Site Scripting (XSS)
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain where user input from a UUID parameter was reflected without proper sanitization in the HTML title tag. The researcher was able to break out of the title tag and inject arbitrary JavaScript code that executes in the context of the domain.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl using reconnaissance techniques
2. Attacker collects historical URLs using waybackmachine archive data
3. Attacker identifies a parameter endpoint vulnerable to reflection: /?uuid=vulnerablepoint
4. Attacker discovers the UUID parameter reflects directly within the HTML title tag without encoding
5. Attacker crafts payload to break out of title tag: test</title><script>alert(document.domain)</script>
6. Attacker delivers malicious URL to victim via social engineering; JavaScript executes revealing document.domain

## Root cause
Insufficient input validation and output encoding on the UUID parameter. The application failed to HTML-encode user input before reflecting it in the title tag, allowing tag breakout and script injection.

## Attacker mindset
Methodical reconnaissance approach using subdomain enumeration and historical data mining. Opportunistic discovery of reflection points followed by standard tag-breaking XSS techniques. Focus on finding low-hanging fruit in parameter handling.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable UUID formats
- Apply proper HTML entity encoding to all user input before reflection in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize all parameters regardless of expected format; never trust user input
- Conduct security code review focusing on all reflection points in templates
- Implement automated security scanning in CI/CD pipeline to catch reflection vulnerabilities
- Use templating engines with auto-escaping enabled by default
- Apply output encoding contextually (HTML, JavaScript, URL, CSS contexts require different encoding)

## Variant hunting
['Test other subdomains (*.uu.nl) for similar parameter reflection patterns', 'Search for other UUID or ID parameters across the application', 'Check if similar endpoints exist on main domain (uu.nl) vs subdomain variants', 'Test other HTML tag contexts (meta tags, data attributes, script src) for reflection', 'Probe for stored XSS variants if UUID values are persisted in user profiles or settings', 'Test different encoding bypass techniques if basic HTML encoding is present', 'Check for DOM-based XSS on client-side processing of UUID parameter']

## MITRE ATT&CK
- T1190
- T1566
- T1059

## Notes
The writeup lacks several details: specific subdomain not disclosed per responsible disclosure practices, bounty amount not mentioned, no timeline details provided, and limited technical depth on payload construction. The vulnerability appears to be a straightforward reflected XSS without additional complexity. Discovery methodology combining subdomain enumeration with historical URL collection is solid reconnaissance practice for finding older/forgotten endpoints.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
