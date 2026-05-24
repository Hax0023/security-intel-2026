# XSS in Draft Orders in Timeline i SHOPIFY Admin Site!

## Metadata
- **Source:** HackerOne
- **Report:** 117449 | https://hackerone.com/reports/117449
- **Submitted:** 2016-02-19
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary

1. Create an Draft with a product named "><img src=x onerror=prompt('XSSP')
2. Send the Draft to someone and complete the order.
Order is shown as Completed Drafts as order.png
3. Create a timeline and reference this Draft. As soon as you click POST you will be XSSEd (xss.png)

Thanks

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


1. Create an Draft with a product named "><img src=x onerror=prompt('XSSP')
2. Send the Draft to someone and complete the order.
Order is shown as Completed Drafts as order.png
3. Create a timeline and reference this Draft. As soon as you click POST you will be XSSEd (xss.png)

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
