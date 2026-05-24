# Stored XSS in Draft Orders Timeline - Shopify Admin

## Metadata
- **Source:** HackerOne
- **Report:** 117449 | https://hackerone.com/reports/117449
- **Submitted:** 2016-02-19
- **Reporter:** nismo
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability existed in Shopify's admin draft orders timeline feature where malicious JavaScript could be injected via product names in draft orders. When a timeline entry referenced a completed draft order containing a payload in the product name, the XSS would execute in the admin's browser upon viewing the timeline.

## Attack scenario
1. Attacker creates a draft order in Shopify admin with a product name containing XSS payload: "><img src=x onerror=prompt('XSS')
2. Attacker sends the draft order to a recipient (customer or collaborator) and the order is completed
3. Attacker creates a timeline entry that references the completed draft order containing the malicious product name
4. When the timeline is loaded or a POST request is made, the payload is rendered without proper encoding
5. JavaScript executes in the context of the admin user's browser session
6. Attacker can steal session tokens, perform unauthorized actions, or compromise admin account

## Root cause
The application failed to properly sanitize and encode product names from draft orders when rendering them in the timeline feature. The product name data was stored with the XSS payload intact and later rendered as HTML without escaping special characters or validating/sanitizing the content.

## Attacker mindset
An attacker would recognize that user-supplied data (product names) in draft orders flows into the timeline display without proper sanitization. By crafting a simple IMG tag with onerror handler, they bypass basic filters and achieve arbitrary code execution in an admin context, potentially escalating to full account compromise.

## Defensive takeaways
- Always encode output based on context (HTML-encode for HTML context, JavaScript-encode for JS context)
- Implement input validation to reject or sanitize dangerous characters in product names and user-submitted fields
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Apply allowlist-based validation for product names, restricting to expected character sets
- Sanitize user input server-side before storage, not just during display
- Implement automated XSS testing in CI/CD pipeline, especially for user-generated content flows
- Use templating engines with auto-escaping enabled by default
- Regular security audits of data flows involving user input and admin surfaces

## Variant hunting
Test other product-related fields (description, SKU, variant names) for similar XSS
Check if other timeline features or order-related displays have the same issue
Test draft order notes and custom fields for XSS vulnerabilities
Investigate if customer-facing order pages have similar encoding issues
Check if the vulnerability persists across different order states (pending, completed, cancelled)
Test SVG-based payloads and other obfuscated XSS vectors in product names
Verify if the issue affects draft order exports or PDF generation

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1005

## Notes
This is a classic stored XSS vulnerability in a high-privilege context (admin panel). The simplicity of the payload (><img src=x onerror=...) suggests basic or no input validation was in place. The fact that it triggers on POST action indicates the XSS may execute during form submission or AJAX handling. This report demonstrates why sanitization must occur at storage time, not just display time.

## Full report
<details><summary>Expand</summary>


1. Create an Draft with a product named "><img src=x onerror=prompt('XSSP')
2. Send the Draft to someone and complete the order.
Order is shown as Completed Drafts as order.png
3. Create a timeline and reference this Draft. As soon as you click POST you will be XSSEd (xss.png)

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
