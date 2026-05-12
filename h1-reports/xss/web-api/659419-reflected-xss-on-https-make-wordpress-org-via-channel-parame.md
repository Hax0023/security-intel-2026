# Reflected XSS on make.wordpress.org via 'channel' parameter

## Metadata
- **Source:** HackerOne
- **Report:** 659419 | https://hackerone.com/reports/659419
- **Submitted:** 2019-07-25
- **Reporter:** gnux
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the chat logs endpoint of make.wordpress.org where the 'channel' parameter is not properly sanitized or encoded before being rendered in the HTML response. An attacker can inject arbitrary JavaScript code via a malicious URL that executes in the victim's browser within the context of the make.wordpress.org domain.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'channel' parameter with proper URL encoding (e.g., %22 for quote, %3E for >)
2. Attacker distributes the URL via phishing email, social engineering, or posting on forums targeting WordPress developers
3. Victim clicks the link while logged into make.wordpress.org
4. Browser requests the page with the malicious channel parameter
5. Server reflects the unsanitized parameter into HTML response without encoding
6. Victim's browser executes the injected JavaScript in the context of make.wordpress.org, allowing session hijacking or credential theft

## Root cause
The application fails to properly HTML-encode or validate the 'channel' parameter before outputting it in the HTTP response. The parameter value is directly concatenated into HTML without escaping special characters like quotes and angle brackets.

## Attacker mindset
An attacker recognizes that user-controlled input (channel parameter) is being reflected in the response without proper sanitization. They craft a payload using HTML/JavaScript that breaks out of any existing context and injects arbitrary code, leveraging the fact that make.wordpress.org developers trust content from their own domain.

## Defensive takeaways
- Implement consistent HTML entity encoding/escaping for all user-controlled output using context-aware encoding functions
- Use a templating engine with auto-escaping enabled by default
- Apply input validation to whitelist acceptable channel values rather than relying solely on output encoding
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Conduct code review of all endpoints that reflect user input back to responses
- Use security scanning tools in CI/CD pipeline to detect reflected XSS patterns
- Implement HTTPOnly and Secure flags on cookies to limit impact of XSS

## Variant hunting
Search for other parameters on make.wordpress.org endpoints that reflect user input (e.g., date, search, filter, query, keyword, tag, category). Check related WordPress.org subdomains (develop.wordpress.org, core.wordpress.org) for similar reflection patterns. Look for any client-side template injection in JavaScript frameworks used on the site.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The vulnerability is straightforward reflected XSS with no apparent CSRF protection bypass needed. The attacker crafted a proof-of-concept using img tag with onerror event handler. The report lacks specific bounce amount but indicates valid security concern for WordPress development infrastructure. Reproduction requires only accessing a specially crafted URL, making it easily exploitable.

## Full report
<details><summary>Expand</summary>

Hi there,
I just found a reflected XSS on make.wordpress.org domain.

steps to reproduce : 
1. visit this link :
https://make.wordpress.org/chat/logs?channel=16%22%3E%3Cimg%20src=x%20onerror=alert(document.domain)%3E&date=2019-07-21&no_bots=1
2. xss pop up will occurs

POC:
see:wp reflected xss.png

Note: it works on the latest version of firefox

## Impact

some of xss impact like stealing cookies, session hijacking, etc ..

</details>

---
*Analysed by Claude on 2026-05-12*
