# help.shopify.com Cross Site Scripting (XSS)

## Metadata
- **Source:** HackerOne
- **Report:** 564196 | https://hackerone.com/reports/564196
- **Submitted:** 2019-05-03
- **Reporter:** 3rd4l
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Query Parameter Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered on help.shopify.com where user-supplied input in query parameters is not properly sanitized before being reflected in the page. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when the page is accessed.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in query parameter (e.g., v0sjx'-alert(1)-'uyvvr=1)
2. Attacker sends the crafted URL to victim via email, social media, or phishing campaign
3. Victim clicks on the link in Edge, Internet Explorer, or other browser
4. Victim navigates to the feedback section (clicking 'Condividi il tuo feedback')
5. The query parameter payload is reflected into the page without proper encoding/sanitization
6. JavaScript code executes in victim's browser context with their Shopify session permissions

## Root cause
Insufficient input validation and output encoding of query parameters. The application reflects user input from the query string into the HTML page without properly escaping or sanitizing the data, allowing arbitrary JavaScript execution.

## Attacker mindset
An attacker would recognize that query parameters are often trusted and reflected directly into page content. By testing simple XSS payloads with quote-breaking syntax (e.g., '-alert(1)-'), they discovered that the parameter value is inserted into JavaScript context without proper escaping, enabling arbitrary code execution.

## Defensive takeaways
- Implement strict input validation on all query parameters
- Apply proper output encoding based on context (HTML encoding, JavaScript encoding, URL encoding)
- Use a security-focused templating engine that auto-escapes by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security testing on all user input vectors, including query parameters
- Use a Web Application Firewall (WAF) to filter malicious patterns
- Conduct regular security code reviews focusing on data flow from input to output

## Variant hunting
Test other parameters on help.shopify.com, check for similar patterns in feedback/survey functionality across Shopify domains, examine other marketing resource pages for parameter injection, test different payload formats (event handlers, script tags, data URIs) to bypass any partial filtering

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The vulnerability appears to be browser-specific or context-dependent (confirmed in Edge and IE but specific trigger requires user interaction with feedback button), suggesting the payload may be injected into JavaScript context or within an attribute. The use of quote-breaking technique (single quote followed by operator) indicates JavaScript context injection rather than HTML context.

## Full report
<details><summary>Expand</summary>

Hello Security Team. 

Tested windows 10 and edge (Microsoft Edge 44.17763.1.0) , internet explorer

Test Url : https://help.shopify.com/it/partners/resources/marketing-pack-for-accountants

Payload: ?v0sjx'-alert(1)-'uyvvr=1

Proof Url: <https://help.shopify.com/it/partners/resources/marketing-pack-for-accountants?v0sjx'-alert(1)-'uyvvr=1>

Open Url: edge , internet explorer , click me "Condividi il tuo feedback. "

## Impact

https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)

</details>

---
*Analysed by Claude on 2026-05-12*
