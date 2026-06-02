# Accidental XSS on uu.nl via UUID Parameter

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** uu.nl (Utrecht University)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Cross-Site Scripting (XSS), Reflected XSS, Improper Output Encoding
- **Category:** web-api
- **Writeup:** https://santoshdbobade.blogspot.com/2021/02/an-accidental-xss-onuunl.html

## Summary
A reflected XSS vulnerability was discovered on a uu.nl subdomain through a UUID parameter that reflected user input within HTML title tags without proper sanitization. The vulnerability allowed execution of arbitrary JavaScript code by breaking out of the title tag and injecting script elements.

## Attack scenario (step by step)
1. Attacker enumerates subdomains of uu.nl using subdomain enumeration techniques
2. Attacker collects historical URLs using waybackurls tool to identify interesting endpoints
3. Attacker identifies a vulnerable endpoint with a UUID parameter that reflects input in the page title
4. Attacker crafts payload: test</title><script>alert(document.domain)</script> to break out of title tag and inject malicious script
5. Attacker shares the malicious URL with victims via phishing or social engineering
6. When victim visits the URL, JavaScript executes in their browser context, allowing session hijacking or credential theft

## Root cause
Insufficient input validation and output encoding of the UUID parameter. The application reflected the UUID parameter directly into the HTML title tag without sanitizing or encoding special characters, allowing tag breakout and script injection.

## Attacker mindset
The attacker methodically enumerated attack surface, leveraged historical data to identify potential vulnerabilities, tested for common XSS patterns, and successfully exploited poor input handling in an overlooked parameter.

## Defensive takeaways
- Implement proper context-aware output encoding for all user-controlled input (HTML encode for HTML context)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize and validate all input parameters, including UUIDs
- Conduct regular security testing on all subdomains and endpoints
- Implement automated XSS detection in development pipeline
- Use HTML parsing libraries to safely construct HTML rather than string concatenation

## Variant hunting
['Test other URL parameters for similar XSS vulnerabilities', 'Check other subdomains of uu.nl for the same vulnerable endpoint', 'Attempt stored XSS if parameter values are persisted in databases', 'Test for DOM-based XSS in JavaScript handling of the UUID parameter', 'Fuzz similar UUID-type parameters across other endpoints', 'Test for filter bypass techniques (case variation, encoding variations)']

## MITRE ATT&CK
- T1190
- T1566.002
- T1598

## Notes
The researcher demonstrated good methodology by using automated tools (waybackurls) for reconnaissance and systematically testing discovered endpoints. The vulnerability was termed 'accidental' likely because it was an oversight in a specific parameter. The writeup lacks specific details about remediation timeframe and bounty amount, suggesting it may have been accepted into a Hall of Fame rather than a formal bug bounty program.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
