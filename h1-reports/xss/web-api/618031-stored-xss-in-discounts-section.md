# Stored XSS in Discounts Section via Product Comment Injection

## Metadata
- **Source:** HackerOne
- **Report:** 618031 | https://hackerone.com/reports/618031
- **Submitted:** 2019-06-18
- **Reporter:** mosuan
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Stored Cross-Site Scripting (XSS), Input Validation Bypass, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Discounts section where malicious JavaScript can be injected through product comments. An attacker can craft a malicious product name containing XSS payload that persists in the discount code comments, executing arbitrary JavaScript when accessed.

## Attack scenario
1. Attacker creates a new product with shop name containing XSS payload: '"'><img src=x onerror=alert(domain.domain)>'
2. Attacker navigates to Discounts section and creates or accesses a discount code
3. Attacker adds a comment to the discount code and selects the malicious product created in step 1
4. The XSS payload from the product name is reflected in the comment field without proper sanitization
5. When the discount page is viewed (by admin or other users), the onerror event triggers
6. Arbitrary JavaScript executes in the context of the victim's browser session with admin privileges

## Root cause
The application fails to properly sanitize and encode user-supplied input (product names) when storing them in the database. When these values are retrieved and rendered in the discount comments section, output encoding is either missing or incomplete, allowing stored XSS payloads to execute.

## Attacker mindset
An authenticated attacker with product creation privileges seeks to escalate impact by injecting persistent XSS into administrative sections. By leveraging the discount feature's comment functionality, they can execute code in admin contexts, potentially stealing session tokens or performing unauthorized actions.

## Defensive takeaways
- Implement strict input validation and sanitization on all user-supplied data, including product names and descriptions
- Apply proper output encoding based on context (HTML entity encoding for HTML context, JavaScript encoding for JS context)
- Use a robust HTML sanitization library (e.g., DOMPurify, sanitize-html) for any rich text fields
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Validate that product references in comments exist and sanitize before rendering
- Conduct security testing focused on stored XSS across all features that reference user-created objects
- Apply principle of least privilege - limit admin data visibility based on actual needs

## Variant hunting
Check other sections where products are referenced (orders, customer segments, bundle discounts)
Test XSS payloads in product description, variant names, and collection names
Investigate comment fields in other administrative features (notes, customer comments, order comments)
Test Unicode/encoding bypasses in product name fields to evade basic filters
Check if SVG upload fields exist that could contain embedded script tags
Test mutation XSS (mXSS) techniques using different tag combinations

## MITRE ATT&CK
- T1190
- T1566
- T1547
- T1059

## Notes
This is classified as self-XSS in the report title but actually demonstrates stored XSS since the payload persists and affects any user viewing that discount page. The vulnerability chain is interesting as it uses product creation as an injection vector for a different feature (discounts). The report lacks specific bounty information and response timeline details.

## Full report
<details><summary>Expand</summary>

self-xss

## Impact

1.add `Products`, shop name is '"'><img src=x onerror=alert(domain.domain)>'
2.click `Discounts->code`, https://mosuan-img-src-x.myshopify.com/admin/discounts/367541518396
3.add comments, Choose the goods just now.
4.alert

</details>

---
*Analysed by Claude on 2026-05-12*
