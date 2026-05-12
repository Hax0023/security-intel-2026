# Reflected XSS on Akamai ARL media endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1315898 | https://hackerone.com/reports/1315898
- **Submitted:** 2021-08-22
- **Reporter:** renzi
- **Program:** Akamai
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on an Akamai ARL (Akamai Reverse Link) endpoint that fails to properly sanitize user-supplied parameters. Attackers can inject malicious JavaScript code through URL parameters that execute in the victim's browser context, potentially leading to session hijacking, credential theft, or malware distribution.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'where' parameter of the search endpoint
2. Attacker tricks victim into clicking the malicious link via phishing email or social engineering
3. Victim's browser sends HTTP request to media endpoint with XSS payload
4. Server reflects the unsanitized payload back in the HTTP response without encoding
5. Browser parses the response and executes the injected JavaScript (e.g., confirm(document.domain))
6. Attacker gains ability to steal cookies, session tokens, credentials, or perform actions on behalf of victim

## Root cause
The Akamai ARL endpoint reflects user input from the 'where' parameter directly into the HTML response without proper HTML entity encoding or output sanitization, allowing special characters and JavaScript event handlers to be injected.

## Attacker mindset
An attacker would recognize that URL-based search parameters are often reflected in results pages. By testing common XSS payloads with HTML/SVG event handlers, they discovered the application fails to encode output, enabling arbitrary JavaScript execution within the victim's authenticated session context.

## Defensive takeaways
- Implement strict input validation and whitelist allowed characters for all user inputs
- Apply context-appropriate output encoding (HTML entity encoding, URL encoding, JavaScript encoding) based on where data is reflected
- Use Content Security Policy (CSP) headers to restrict JavaScript execution sources and event handlers
- Implement a Web Application Firewall (WAF) to detect and block common XSS payloads
- Sanitize HTML output using established libraries rather than manual filtering
- Perform security code review focused on data flow from input to output
- Test all user-facing parameters for XSS vulnerabilities during SAST/DAST scanning

## Variant hunting
Search for other Akamai ARL endpoints or reverse proxy endpoints that accept search/query parameters. Test parameters like 'search', 'q', 'query', 'filter', 'keyword', 'url', 'redirect' for reflected XSS. Check for other Akamai services using similar patterns: media.*, web.*, cdn.*, and other subdomains that might not properly encode user input.

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.001
- T1204.001

## Notes
The writeup lacks critical details including the actual remediation status, bounty amount, and disclosure timeline. The vulnerability appears to be on a customer's domain proxied through Akamai rather than Akamai's own infrastructure. The PoC uses SVG onload handler which is a common XSS bypass technique. Report quality is minimal, providing only basic OWASP reference and reproduction steps.

## Full report
<details><summary>Expand</summary>

**Description:**

Hello,
I found a Reflected Cross site Scripting (XSS) Open Akamai ARL on  http://media.████, With this security flaw is possible executing JS codes...

## References
https://owasp.org/www-community/attacks/xss/
https://community.akamai.com/customers/s/article/WebPerformanceV1V2ARLChangeStartingFebruary282021?language=en_US

## Impact

The attacker can execute JS code.

## System Host(s)
media.███

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Go to http://media.██████/7/0/33/1d/www.citysearch.com/search?what=x&where=place%22%3E%3Csvg+onload=confirm(document.domain)%3E

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
