# Reflected XSS in www.shopify.com/markets utm_source Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1699762 | https://hackerone.com/reports/1699762
- **Submitted:** 2022-09-14
- **Reporter:** noblesix
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the utm_source parameter of www.shopify.com/markets that allows unauthenticated attackers to execute arbitrary JavaScript in victim browsers. The vulnerability stems from insufficient output encoding of the utm_source parameter value, enabling attribute injection and event handler execution.

## Attack scenario
1. Attacker crafts a malicious URL containing XSS payload in the utm_source parameter: https://www.shopify.com/markets?utm_source=INJECTION%22%20style=%22animation-name:swoop-up%22%20onanimationstart=%22alert(document.domain)
2. Attacker distributes the crafted URL via phishing email, social media, or other communication channels to target Shopify users
3. Victim clicks the malicious link while authenticated to Shopify or in a context where Shopify cookies are available
4. Browser requests the URL and receives HTML response with unescaped utm_source parameter value reflected in page content
5. JavaScript engine parses the injected HTML/JavaScript payload and executes the onanimationstart event handler
6. Attacker gains ability to steal session cookies, perform CSRF attacks, redirect to phishing pages, or manipulate page content

## Root cause
The utm_source parameter value is reflected into the HTML response without proper contextual encoding. The application fails to escape double-quote characters and other special characters, allowing attribute injection and event handler injection within HTML element attributes.

## Attacker mindset
An attacker would target this endpoint to distribute malicious links via social engineering, crafting URLs that execute JavaScript in the context of shopify.com domain to harvest authentication tokens, conduct credential harvesting, or perform account takeover attacks against Shopify users and merchants.

## Defensive takeaways
- Implement context-aware output encoding: HTML-encode for HTML body context, HTML-attribute-encode for attribute values, JavaScript-encode for JavaScript contexts
- Use a security-focused templating engine that enforces auto-escaping by default
- Validate and sanitize all user inputs, including UTM parameters, against a whitelist of expected values
- Apply Content Security Policy (CSP) headers to restrict inline script execution and limit script sources
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Conduct regular security code reviews and static analysis to identify reflection vulnerabilities
- Use automated SAST tools to detect unescaped output in templates and code
- Implement input validation for UTM parameters to only allow alphanumeric characters and specific safe characters

## Variant hunting
Check other UTM parameters (utm_medium, utm_campaign, utm_content, utm_term) for similar XSS vulnerabilities
Test other marketing/tracking parameters that may have similar encoding issues
Examine other Shopify properties and subdomains for identical parameter handling patterns
Look for stored XSS variants if utm_source values are persisted in user accounts or analytics
Test for DOM-based XSS if utm_source is processed client-side via JavaScript
Check for second-order XSS if utm parameters are reflected in admin dashboards or reports

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability is easily exploitable and requires no authentication. The proof-of-concept uses animation event handlers to bypass potential script-tag filters. Impact is significant given Shopify's user base. The fix is straightforward - implement proper output encoding based on the HTML attribute context where the parameter is reflected.

## Full report
<details><summary>Expand</summary>

Hello, hope you are having a good day :)

## Summary:
I found a reflected XSS in `www.shopify.com/markets` using the `utm_source` parameter

Reflected XSS vulnerabilities arise when the application accepts a malicious input script from a user and then it is executed in the victim's browser. Since the XSS is reflected, the attacker has to trick the victim into executing the payload, usually using another website or by sending a specially crafted link

##### URL: `https://www.shopify.com/markets`
##### INJECTION POINT: `utm_source` parameter
##### PAYLOAD: `injection%22%20style=%22animation-name:swoop-up%22%20onanimationstart=%22alert(document.domain)`

## Steps To Reproduce:
Visit this URL:  
```
https://www.shopify.com/markets?utm_source=INJECTION%22%20style=%22animation-name:swoop-up%22%20onanimationstart=%22alert(document.domain)
```

By visiting that link you'll get an alert on your screen, that demonstrates the existence of the vulnerability.

{F1925617}

The attack is unauthenticated

## Recommended Fix
Correctly escape special characters such as `<` `>` `"` `'` based on the context where the string gets reflected.

Thank you.

## Impact

An attacker could steal user cookies, create a trusted phishing page or bypass any CSRF protection mechanism.

</details>

---
*Analysed by Claude on 2026-05-12*
