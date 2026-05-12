# Open Redirect and Reflected XSS via Tag Stripping in Root Path and GET Parameters

## Metadata
- **Source:** HackerOne
- **Report:** 196846 | https://hackerone.com/reports/196846
- **Submitted:** 2017-01-09
- **Reporter:** inhibitor181
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple Starbucks e-commerce domains (shop.starbucks.*, store.starbucks.*, teavana.com) are vulnerable to reflected XSS and open redirects through insufficient input sanitization. Payloads using the `<>` tag stripping bypass (e.g., `<>javascript:alert()` or `<>//google.com`) can be injected into the root path or GET parameters, allowing attackers to execute arbitrary JavaScript or redirect users to malicious sites.

## Attack scenario
1. Attacker discovers that angle bracket sequences like `<>` in URLs bypass tag filtering mechanisms
2. Attacker crafts malicious URL with payload `<>javascript:alert(document.cookie)` in root path or GET parameter
3. Victim clicks phishing link containing the malicious Starbucks domain URL
4. Server strips initial `<>` tags but fails to sanitize the remaining `javascript:alert()` payload
5. Browser interprets the remaining JavaScript payload and executes it in victim's session context
6. Attacker steals session cookies, redirects to phishing page, or performs account takeover

## Root cause
Improper input validation/sanitization where the application strips HTML tags but does not properly validate protocol handlers. The tag stripping logic removes `<>` but leaves the `javascript:` protocol handler intact, allowing XSS execution. The same flaw enables open redirects via `<>//external-domain.com` payloads.

## Attacker mindset
Attacker systematically tested common XSS bypass techniques, discovering that angle bracket stripping was the primary defense. By chaining tag stripping with protocol handler injection, they bypassed the intended filter. They recognized the widespread impact across multiple branded domains and multiple parameter injection points, indicating poor centralized security controls.

## Defensive takeaways
- Never rely on tag stripping alone; implement allowlist-based HTML sanitization using established libraries (e.g., DOMPurify, OWASP HTML Sanitizer)
- Validate and sanitize all user inputs including URL paths, GET parameters, and any data reflected in responses
- Use Content Security Policy (CSP) with strict `script-src 'self'` to prevent arbitrary JavaScript execution
- Implement URL validation for redirects; maintain allowlist of permitted redirect domains and reject external URLs
- Apply output encoding appropriate to context (HTML entity encoding for HTML context, URL encoding for URLs)
- Conduct security testing across all branded domains and subdomains as part of unified security program
- Use automated security scanning tools in CI/CD pipeline to catch XSS and redirect vulnerabilities early

## Variant hunting
Test other tag stripping bypasses: `<` alone, `>` alone, `<<>`, `</>`, HTML comments `<!--` with JavaScript
Test polyglot payloads combining XSS and open redirect: `<>javascript:alert(1)//google.com`
Inject payloads into other parameters: headers, cookies, POST data, HTTP method
Test protocol handlers beyond `javascript:`: `data:`, `vbscript:`, `file:`, `about:`, `blob:`
Test event handlers: `<img src=x onerror=alert(1)>`, `<svg onload=alert(1)>`
Check for double-encoding bypass: `%3C%3Ejavascript:alert(1)`
Test path traversal combinations: `/../<>javascript:alert(1)`, `//../../<>javascript:alert(1)`

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This report demonstrates a common security gap where multiple layers of input validation are missing. The vulnerability affects multiple branded properties, suggesting a shared codebase or framework vulnerability. The ease of exploitation and multiple injection vectors indicate this was likely exploited in the wild before disclosure. The bonus open redirect vectors could be chained with CSRF attacks to force legitimate users to malicious sites.

## Full report
<details><summary>Expand</summary>

Hello, during some open redirects testing, I have noticed a very strange redirect that occured when I had modified a parameter using something like `>cofee`. I have digged up further and then I have noticed that one can make a redirect by modifying GET parameters with this structure : `<>//google.com`

There seems to be a stripping of tags and after that some chained redirect, that will eventually trigger an XSS vulnerability if the payload is like : `<>javascript:alert(document.cookie);`.

__So, based on this I have noticed that all your websites except the starbucks.* are vulnerable to an XSS payload that is written directly in the root URL or almost ANY other get parameter__, thus making almost all the websites exploitable with multiple injection points (starbucks.* seems not affected)

POC EXAMPLES
-------
```
https://shop.starbucks.de/<>javascript:alert(document.cookie);
https://teavana.com/<>javascript:alert(document.cookie);
https://store.starbucks.com/<>javascript:alert(document.cookie);
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=decaffeinated&prefv1=<>javascript:alert('xss parameter');
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=<>javascript:alert('xss parameter');
```

Bonus - open redirect example :
```
https://shop.starbucks.de/coffee/coffee,de_DE,sc.html?prefn1=decaffeinated&prefv1=<>//google.com
https://teavana.com/<>//google.com
```

</details>

---
*Analysed by Claude on 2026-05-12*
