# Reflected XSS in Blog Search via 'q' Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1145162 | https://hackerone.com/reports/1145162
- **Submitted:** 2021-04-02
- **Reporter:** zqgnd
- **Program:** Exchange Marketplace
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Inadequate Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the blog search functionality at /blogsearch endpoint where the 'q' query parameter is not properly sanitized or encoded before being rendered in the HTML response. An attacker can inject malicious JavaScript code through the parameter to execute arbitrary scripts in a victim's browser context.

## Attack scenario
1. Attacker crafts a malicious URL: https://exchangemarketplace.com/blogsearch?q=OnMoUsEoVeR=prompt(/hacked/)//
2. Attacker sends the URL to a victim via email, chat, or social engineering
3. Victim clicks the link while logged into exchangemarketplace.com
4. The malicious payload in the 'q' parameter is reflected in the HTML page without sanitization
5. The injected JavaScript (onmouseover event handler) executes in the victim's browser
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to phishing pages

## Root cause
The application fails to properly encode or validate user input from the 'q' parameter before outputting it into HTML context. The search parameter is likely being directly concatenated into the HTML response without applying appropriate output encoding (HTML entity encoding) or using a templating engine with auto-escaping enabled.

## Attacker mindset
An attacker would recognize that search functionality is frequently overlooked in security reviews and commonly accepts arbitrary input. The use of event handler attributes (onmouseover) demonstrates knowledge of bypassing basic filters that might block script tags. The attacker is targeting user trust in legitimate domains to deliver malicious payloads.

## Defensive takeaways
- Implement strict input validation on all query parameters, especially search inputs
- Apply proper output encoding based on context (HTML entity encoding for HTML context, JavaScript encoding for JS context)
- Use security-focused templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Apply parameterized/prepared statements and templating to prevent injection attacks
- Conduct security code review focusing on user input handling and output rendering
- Implement automated security testing (SAST/DAST) to catch XSS vulnerabilities early
- Use HTTPOnly and Secure flags on session cookies to prevent XSS-based theft
- Perform regular penetration testing on search and input features

## Variant hunting
Test other search endpoints and form inputs (e.g., product search, user search) with the same payload
Try alternative event handlers: onload, onerror, onclick, onkeypress
Attempt tag-based injection: <img src=x onerror=alert(1)>, <svg onload=alert(1)>
Test HTML comment escaping: <!-- payload -->, script comment variations
Check for filter bypasses using case variations, encoding (URL, double-URL, Unicode), and HTML entities
Examine other parameters in the blogsearch endpoint for similar vulnerabilities
Test stored XSS if blog posts or comments are indexed and reflected in search results
Check for DOM-based XSS in client-side search processing

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a straightforward reflected XSS vulnerability in a search function. The payload uses an event handler attribute to bypass basic script tag filters. The application likely reflects user input directly without encoding, which is a common vulnerability pattern in search functionality. No CSRF token validation appears to be required for this GET request. The vulnerability affects any user who can be tricked into clicking the malicious link, posing a risk to session hijacking and account compromise.

## Full report
<details><summary>Expand</summary>

There is an XSS vulnerability on https://exchangemarketplace.com/blogsearch page through the `q` parameters.
`https://exchangemarketplace.com/blogsearch?q=OnMoUsEoVeR=prompt(/hacked/)//`
{F1251282}

## Impact

XSS  at https://exchangemarketplace.com/blogsearch

</details>

---
*Analysed by Claude on 2026-05-12*
