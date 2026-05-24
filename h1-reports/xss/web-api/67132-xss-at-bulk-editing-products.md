# XSS at Bulk editing products

## Metadata
- **Source:** HackerOne
- **Report:** 67132 | https://hackerone.com/reports/67132
- **Submitted:** 2015-06-10
- **Reporter:** mafia
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
after following above the steps in #67125 goto  Bulk editing products:

for me the url was:
 https://img-src-x-onerror-prompt1-24.myshopify.com/admin/bulk?resource_name=Product&edit=variants.sku%2Cvariants.price%2Cvariants.compare_at_price&message=&return_to=%2Fadmin%2Fproducts&ids=1151578433

it is also vulnerable to xss
(Change the requierd fields in above url according to your shop)


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

after following above the steps in #67125 goto  Bulk editing products:

for me the url was:
 https://img-src-x-onerror-prompt1-24.myshopify.com/admin/bulk?resource_name=Product&edit=variants.sku%2Cvariants.price%2Cvariants.compare_at_price&message=&return_to=%2Fadmin%2Fproducts&ids=1151578433

it is also vulnerable to xss
(Change the requierd fields in above url according to your shop)


</details>

---
*Analysed by Claude on 2026-05-24*
