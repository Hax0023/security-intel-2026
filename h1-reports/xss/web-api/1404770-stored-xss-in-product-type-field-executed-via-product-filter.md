# Stored XSS in Product Type Field Executed via Product Filters

## Metadata
- **Source:** HackerOne
- **Report:** 1404770 | https://hackerone.com/reports/1404770
- **Submitted:** 2021-11-18
- **Reporter:** chupa__chups
- **Program:** judge.me
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Insufficient Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the judge.me Shopify app where malicious JavaScript payloads injected into the product type field are executed when the product type filter is accessed in the app's admin interface. The vulnerability allows attackers to execute arbitrary JavaScript in the context of authenticated admin users, potentially leading to session hijacking and credential theft.

## Attack scenario
1. Attacker gains access to a Shopify store (as authorized user or via compromised credentials)
2. Attacker creates or modifies a product and injects XSS payload in the 'Product Type' field (e.g., "><img src=x onerror=prompt(document.domain)>)
3. Attacker saves the product, and the malicious payload is stored in the backend database
4. Admin user installs or accesses the judge.me app and navigates to the products filtering interface
5. Admin user clicks on the 'TYPE' filter dropdown to view available product types
6. Stored XSS payload executes in admin's browser session, allowing script execution with admin privileges

## Root cause
The judge.me application fails to properly sanitize and encode user-supplied input from the Shopify product type field before rendering it in the filter dropdown menu. The product type data is stored unsanitized and later output without HTML encoding or Content Security Policy protection.

## Attacker mindset
An insider or compromised store account could strategically inject XSS payloads into product types to target admin users. The attacker could escalate from product data tampering to complete account compromise by stealing session cookies or admin credentials when filtering products.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, including product type metadata, with whitelist-based character restrictions
- Apply HTML entity encoding/escaping to all user-generated content before rendering in HTML context
- Utilize context-aware output encoding (HTML encoding for HTML context, JavaScript encoding for JS context)
- Implement Content Security Policy (CSP) headers with strict directives to prevent inline script execution
- Sanitize data from external sources (Shopify product data) before storage and display
- Use templating engines with auto-escaping enabled by default
- Implement regular security testing and code review focused on XSS-prone areas (dropdowns, filters, search results)
- Apply the principle of least privilege to filter and dropdown functionalities

## Variant hunting
Test other product metadata fields (product title, description, tags, collections) for stored XSS
Test admin filter/search functionality across different sections of the judge.me app for similar issues
Check if other Shopify apps have similar vulnerabilities in product type or metadata handling
Test whether the payload is also reflected in product listing pages, review displays, or public-facing pages
Investigate if variant names, SKUs, or other product attributes are similarly vulnerable
Test Unicode and alternate encoding bypass techniques in the product type field

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1185 - Steal Web Session Cookie
- T1539 - Steal Web Session Cookie
- T1566 - Phishing (if used to target other admins)

## Notes
This is a critical vulnerability for SaaS applications like judge.me that integrate with e-commerce platforms. The presence of a video POC demonstrates reliable reproducibility. The vulnerability requires relatively low privilege (product creation capability) to exploit but can impact high-privilege accounts (admin users). The judge.me app processes Shopify data but fails to maintain security boundaries between data storage and rendering layers.

## Full report
<details><summary>Expand</summary>

HI @judgeme!
I found Stored XSS!)
I Install judge.me in Shopify E-Commerce. Step to reproduce:
1. Log in to our shopify dev store and install "judgeme" app.
2. Create random product in our Shopify store (make it active) and insert XSS playload  "><img src=x onerror=prompt(document.domain)> in "PRODUCT TYPE" field and SAVE


{F1518888}


3. Then go to our judgeme app https://xxx.myshopify.com/admin/apps/judgeme/products. There is a filter field TYPE . Click on it and select our playload from the list 
{F1518897}
4. And it works )))



{F1518898}

I attached video POC

## Impact

Session Hijacking, Cookie Stealing.

</details>

---
*Analysed by Claude on 2026-05-12*
