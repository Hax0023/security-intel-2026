# Stored XSS in Product Reviews API via Unsafe JSON Response Handling

## Metadata
- **Source:** HackerOne
- **Report:** 168458 | https://hackerone.com/reports/168458
- **Submitted:** 2016-09-14
- **Reporter:** zombiehelp54
- **Program:** Shopify
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Missing Content-Type Header, Unsafe JSON Rendering as HTML, JSONP Callback Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Product Reviews API endpoint where product data containing malicious payloads is returned without proper Content-Type headers. When the callback parameter is omitted, the response defaults to text/html rendering, allowing stored XSS payloads in product titles to execute in the browser context.

## Attack scenario
1. Attacker creates a product on a Shopify store with an XSS payload embedded in the product title (e.g., <script>alert('XSS')</script>)
2. Attacker crafts a malicious URL to the productreviews.shopifyapps.com API endpoint without the callback parameter: https://productreviews.shopifyapps.com/proxy/v4/reviews/product?product_id=<ID>&version=v4&shop=<SHOP>&_=cache
3. When victim visits the malicious URL, the API returns JSON data containing the product information with the XSS payload
4. Due to missing Content-Type header, browser interprets response as text/html instead of application/json
5. JavaScript payload in the product title executes in the victim's browser with full access to their session context
6. Attacker gains ability to steal session tokens, modify page content, or perform actions on behalf of the victim

## Root cause
The API endpoint fails to enforce proper Content-Type headers and Content Security Policy. The application incorrectly assumes that the presence of a callback parameter determines response type, creating a state where JSON data is rendered as HTML. Additionally, stored user-controlled data (product titles) is not sanitized before being included in API responses.

## Attacker mindset
An attacker would recognize that API responses lacking explicit Content-Type headers can be misinterpreted by browsers. By storing malicious payloads in product metadata and manipulating URL parameters to bypass JSONP safety mechanisms, the attacker leverages the application's trust in user-supplied product data and its inconsistent response handling.

## Defensive takeaways
- Always explicitly set Content-Type headers for all API responses (application/json for JSON, text/plain for JSONP)
- Never rely on optional URL parameters to determine security-critical response handling behaviors
- Implement input validation and output encoding for all user-supplied data, especially product metadata that will be returned in API responses
- Use Content Security Policy (CSP) headers to restrict script execution origins
- Sanitize or escape all data returned from APIs before rendering in browser context
- Implement strict JSONP callback validation (whitelist allowed characters) rather than relying on Content-Type headers alone
- Apply defense-in-depth: validate, encode, and set appropriate headers regardless of request parameters

## Variant hunting
Look for similar patterns across Shopify API endpoints: other proxy endpoints that return user-controlled data (reviews, comments, descriptions), any endpoints with optional callback parameters that affect response handling, endpoints lacking explicit Content-Type headers, and other productreviews subdomain variations (CDN endpoints, regional variations). Check for similar trust-based rendering in other Shopify app integration points.

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The vulnerability affects multiple endpoints/domains (productreviews.shopifyapps.com and productreviews.shopifycdn.com). The attack is particularly dangerous because it leverages stored data, meaning any user visiting the affected product creates a malicious URL is compromised. The missing callback parameter creates an implicit fallback to HTML rendering, suggesting poor API design. The use of cache-busting parameters (_=cache) indicates potential for parameter pollution attacks.

## Full report
<details><summary>Expand</summary>

Hi , I have found a stored XSS issue in `https://productreviews.shopifyapps.com`
#Details:
Going to `https://productreviews.shopifyapps.com/proxy/v4/reviews/product?product_id=8254331011&version=v4&shop=zh5403-attacker.myshopify.com&_=cache&callback=test` will show you the details of a product with the id `8254331011` in JSON format.
Having the `callback` parameter in the url will return `Content-Type:application/javascript` in the response headers, however, if the url does not contain that parameter, the response won't contain **Content-Type** header in the response so the browser will display the page as **text/html**. 
#PoC:
I have created a product with an XSS payload in the title and added the id in the url.
`https://productreviews.shopifyapps.com/proxy/v4/reviews/product?product_id=8254331011&version=v4&shop=zh5403-attacker.myshopify.com&_=cache&callback=test`

PS: This was originally found at `https://productreviews.shopifycdn.com/proxy/v4/reviews/product?product_id=8254331011&version=v4&shop=zh5403-attacker.myshopify.com&_=xxxxxxxx` but I found that it also works for `https://productreviews.shopifyapps.com`


</details>

---
*Analysed by Claude on 2026-05-12*
