# Bulk Discount App in myshopify.com exposes http://bulkdiscounts.shopifyapps.com vulnerable to XSS

## Metadata
- **Source:** HackerOne
- **Report:** 62861 | https://hackerone.com/reports/62861
- **Submitted:** 2015-05-18
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Installing the Bulk Discount App in *.myshopify.com (which requires  a paid basic plan) makes the bulkdiscounts.shopifyapps.com vulnerable to XSS due to non sanitized input in products and collections.

POC:

1. Enter a product name or a collection such as "><img src=x onerror=prompt(document.domain)> and save it.
2. Install the Shopify BulkDiscounts App
3. Go to Apps -> Shopify BulkDiscount

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

Installing the Bulk Discount App in *.myshopify.com (which requires  a paid basic plan) makes the bulkdiscounts.shopifyapps.com vulnerable to XSS due to non sanitized input in products and collections.

POC:

1. Enter a product name or a collection such as "><img src=x onerror=prompt(document.domain)> and save it.
2. Install the Shopify BulkDiscounts App
3. Go to Apps -> Shopify BulkDiscounts
4. Click on "Create One now" or "New Discount Set"

Due to improper sanitization XSS occurs in the shopifyapps.com domain !!

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
