# Reflected XSS via Referer Header in Billing Admin

## Metadata
- **Source:** HackerOne
- **Report:** 297203 | https://hackerone.com/reports/297203
- **Submitted:** 2017-12-12
- **Reporter:** inferno-
- **Program:** Semrush
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Header Injection, Improper Input Validation, Unsafe Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in Semrush's billing admin subscription page where the Referer HTTP header is echoed unsafely into the response without proper sanitization or encoding. An attacker can craft a malicious URL with JavaScript payload in the Referer header to execute arbitrary code in the victim's browser when they visit the subscription page.

## Attack scenario
1. Attacker crafts a malicious URL pointing to www.semrush.com/billing-admin/profile/subscription/?l=de with JavaScript payload in the Referer header
2. Attacker tricks a Semrush user (via phishing, social engineering, or malicious website) into clicking the crafted link or visiting the attacker's page
3. Victim's browser makes a request to the vulnerable Semrush endpoint, including the attacker's payload in the Referer header
4. Semrush server processes the request and echoes the unsanitized Referer header value into the HTML response
5. Victim's browser renders the response and executes the injected JavaScript code within the authenticated session context
6. Attacker gains ability to steal session tokens, modify page content, redirect user, or perform actions on behalf of the victim

## Root cause
The application fails to properly validate, sanitize, and HTML-encode the Referer HTTP header before reflecting it in the response. The server-side code directly concatenates or includes the header value in the HTML output without using appropriate encoding functions (e.g., HTML entity encoding).

## Attacker mindset
An attacker would identify that HTTP headers are reflected in responses and test common header injection points (Referer, User-Agent, X-Forwarded-For). They would use simple alert() payloads to confirm XSS execution, then escalate to stealing authentication tokens, account hijacking, or deploying malware to billing/admin pages where sensitive financial data is accessed.

## Defensive takeaways
- Never trust or reflect HTTP headers directly in HTML responses without sanitization
- Implement input validation to reject or sanitize unexpected characters in Referer and other headers
- Apply context-appropriate output encoding (HTML entity encoding for HTML context) to all reflected data
- Use a Content Security Policy (CSP) with strict-dynamic and nonce-based inline scripts to mitigate XSS impact
- Implement HTTPOnly and Secure flags on session cookies to prevent token theft via XSS
- Conduct regular security code reviews focusing on data flow from input (headers, query params, POST data) to output
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Perform automated and manual testing for XSS vulnerabilities across all user-controllable inputs including headers

## Variant hunting
Test other HTTP headers (User-Agent, X-Forwarded-For, X-Original-URL, Cookie) for reflection and XSS
Check different endpoints in /billing-admin path for similar vulnerabilities
Test with various language parameters (?l=en, ?l=fr) to identify if filtering differs by region
Try different XSS payloads (event handlers, img onerror, svg, iframe) to bypass any basic filters
Test stored XSS variants if headers can be persisted in user profiles or account settings
Check for DOM-based XSS if JavaScript processes Referer header client-side

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204

## Notes
This is a straightforward reflected XSS vulnerability in a sensitive area (billing/admin panel) that could lead to account compromise. The use of the Referer header makes it slightly less obvious than query parameter XSS but equally exploitable. The vulnerability demonstrates the importance of treating all user-controllable input sources (including HTTP headers) as untrusted.

## Full report
<details><summary>Expand</summary>

Host : www.semrush.com

Path : /billing-admin/profile/subscription/?l=de

Payload : c5obc'+alert(1)+'p7yd5

Steps to reproduce :

Request Header :

GET /billing-admin/profile/subscription/?l=de HTTP/1.1
Host: www.semrush.com
Accept: */*
Accept-Language: en
User-Agent: Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.1; Win64; x64; Trident/5.0)
Connection: close
Referer: http://www.google.com/search?hl=en&q=c5obc'+alert(1)+'p7yd5

Overview :

The payload c5obc'+alert(1)+'p7yd5 was submitted in the Referer HTTP header. Payload is copied from a request and echoed into the application's immediate response in an unsafe way.

## Impact

Reflected cross-site scripting vulnerabilities arise when data is copied from a request and echoed into the application's immediate response in an unsafe way. An attacker can use the vulnerability to construct a request that, if issued by another application user, will cause JavaScript code supplied by the attacker to execute within the user's browser in the context of that user's session with the application.

</details>

---
*Analysed by Claude on 2026-05-12*
