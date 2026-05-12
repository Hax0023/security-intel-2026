# Stored XSS in Shopify Admin Product Description

## Metadata
- **Source:** HackerOne
- **Report:** 978125 | https://hackerone.com/reports/978125
- **Submitted:** 2020-09-10
- **Reporter:** jaka-tingkir
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, HTML/JavaScript Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Shopify admin product creation page where unsanitized HTML/JavaScript payloads can be injected into product description fields. The malicious script executes in the context of admin users viewing the product, potentially allowing attackers to steal session cookies and perform unauthorized administrative actions.

## Attack scenario
1. Attacker creates or edits a product in Shopify admin dashboard
2. Attacker injects XSS payload into product description using img onerror event handler or other HTML attributes
3. Payload is stored in the backend database without proper sanitization
4. Admin user or other staff members view the product details page
5. JavaScript payload executes in their browser context with admin privileges
6. Attacker exfiltrates cookies, session tokens, or performs actions like account takeover or data theft

## Root cause
The product description field uses a rich text editor (MCE - TinyMCE) that fails to properly sanitize or escape user input before storing or rendering HTML content. The application does not implement Content Security Policy or adequate output encoding for user-controlled HTML content.

## Attacker mindset
An attacker with low privileges (potentially a vendor or reseller with product editing rights) could escalate impact by stealing admin session cookies, modifying other products, or accessing sensitive business data. The stored nature means the payload persists and affects multiple users.

## Defensive takeaways
- Implement strict HTML sanitization libraries (e.g., DOMPurify, bleach) on both client and server side
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Apply allowlist-based HTML filtering - only permit safe tags and attributes
- Implement proper output encoding (HTML entity encoding) when rendering user content
- Use rich text editors with built-in XSS protection or configure them securely
- Perform server-side validation and sanitization regardless of client-side controls
- Regular security testing of user input fields, especially rich text editors
- Implement frame isolation for rich text editor content

## Variant hunting
Test all rich text editor fields across Shopify admin (product titles, descriptions, collection descriptions, page content)
Try event handler attributes (onerror, onload, onmouseover, onclick)
Test data attributes (data-mce-fragment) for bypasses
Attempt SVG-based XSS payloads in image uploads
Test with encoded payloads and polyglot techniques
Check stored XSS in customer-facing pages if product descriptions are publicly displayed
Test privilege escalation via stored XSS to admin account takeover

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1539 - Steal Web Session Cookie
- T1566 - Phishing (if chained with social engineering)
- T1083 - File and Directory Discovery (post-compromise)

## Notes
This is a classic stored XSS in an admin panel context, making it particularly dangerous due to the elevated privileges of admin users. The use of TinyMCE suggests the application attempted to provide rich text functionality but failed to configure it securely. The vulnerability affects integrity of product data and confidentiality of admin sessions. Report demonstrates lack of input validation despite using a rich text editor framework.

## Full report
<details><summary>Expand</summary>

I tried to make a product description and add the xss script in the paragraph.

## steps for reproduction
1. create a new product
2. enter xss in the product description paragraph, such as;
`<div align =" center "data-mce-fragment =" 1 "> <img src = x onerror = prompt (document.cookie)>
<h4 dir = "ltr" data-mce-fragment = "1"> <span style = "text-decoration: underline; color: # ff2a00;"> <em> <strong> (name_product) </strong></em></span> </h4>
</div> ``

## Impact

xss can be triggered

</details>

---
*Analysed by Claude on 2026-05-12*
