# Unauthorized Cross-Store Access to Collections, Products, Pages via Link List Subject ID Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 93921 | https://hackerone.com/reports/93921
- **Submitted:** 2015-10-14
- **Reporter:** supernatural
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Direct Object References (IDOR), Missing Authorization Checks, Broken Access Control, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical authorization bypass vulnerability exists in Shopify's admin panel link list management feature, allowing attackers to access hidden collections, products, pages, and blogs from arbitrary stores by directly manipulating the subject_id parameter. The vulnerability stems from server-side failure to validate that the accessed object belongs to the authenticated user's own store, enabling unauthorized information disclosure across shop boundaries.

## Attack scenario
1. Attacker navigates to their own Shopify store's admin panel and accesses /admin/link_lists
2. Attacker creates a new link list and selects an object type (e.g., collection)
3. Attacker uses browser developer tools to inspect the HTML form and identifies the hidden input field 'link_list[links][][subject_id]'
4. Attacker modifies the subject_id value from their own store's ID to a target ID from a different store (e.g., 12345 → 67890)
5. Attacker submits the form by clicking save
6. Upon page reload, the system retrieves and displays the hidden collection/product/page metadata from the victim store, exposing sensitive information

## Root cause
The backend API endpoint processing link list creation/updates fails to enforce store ownership validation. The application trusts client-supplied subject_id values without verifying that the referenced object belongs to the authenticated user's store, allowing cross-tenant data access.

## Attacker mindset
An attacker with a Shopify store account seeks to gather competitive intelligence, discover hidden products/collections from competitors, or enumerate store structure and catalog information without authorization. The low barrier to entry (form manipulation) and high information value make this an attractive reconnaissance vector.

## Defensive takeaways
- Implement strict server-side authorization checks: verify all object IDs belong to the authenticated user's store before processing
- Use indirect object references (token-based mapping) instead of direct numeric IDs
- Enforce store_id context in all queries and mutations; cross-reference authenticated user's store against accessed resources
- Validate subject_id against store ownership in both form submission and AJAX endpoints
- Implement audit logging for cross-store access attempts to detect exploitation
- Apply principle of least privilege; restrict admin API scopes to owned store resources only
- Use database-level row-level security policies to prevent queries outside store scope

## Variant hunting
Check other admin endpoints accepting object IDs (webhooks, themes, apps, discount configuration)
Test bulk operations and imports that reference external objects
Examine API endpoints for similar missing store_id validation in product, page, and blog management
Investigate email notification settings, customer data exports, and report generation for IDOR patterns
Test Shopify's GraphQL admin API for similar cross-store access via object ID manipulation
Check file upload/asset management for store boundary issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1526 - Enumerate External Targets
- T1087 - Account Discovery
- T1538 - Cloud Service Discovery
- T1556 - Modify Authentication Process

## Notes
This report demonstrates a classic IDOR vulnerability in a multi-tenant SaaS environment. The simplicity of exploitation (client-side form manipulation) combined with high-value disclosure (hidden catalog items) makes this a critical issue. The vulnerability likely affects multiple object types sharing similar implementation patterns, suggesting systemic authorization issues across the admin panel. Shopify's response time and remediation approach would indicate their security maturity in addressing tenant isolation.

## Full report
<details><summary>Expand</summary>

Hi

I found a vulnerability in shopify that can leak other shops hidden objects include collection,product,page,blog

steps:

- go to "/admin/link_lists"
- click on "add link list"
- select one object from list for example collection
- open "Inspect Element"
- change value of element "link_list[links][][subject_id]" to any id from other shops
- click on save then when page reloaded you will see data in box 

this works for hidden collection, products, pages

Regards

</details>

---
*Analysed by Claude on 2026-05-24*
