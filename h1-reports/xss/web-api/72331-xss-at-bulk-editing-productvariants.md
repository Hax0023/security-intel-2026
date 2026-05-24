# XSS at Bulk editing ProductVariants

## Metadata
- **Source:** HackerOne
- **Report:** 72331 | https://hackerone.com/reports/72331
- **Submitted:** 2015-06-24
- **Reporter:** mafia
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Steps to Reproduce:

1.Create a Product with Title and Description as ` "><img src=x onerror=prompt(133)>`
2. Now goto https://blahblah.myshopify.com/admin/products/inventory
3. Select the Product created at Step 1 and Click on Edit variants

and XSS will be triggered


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

Steps to Reproduce:

1.Create a Product with Title and Description as ` "><img src=x onerror=prompt(133)>`
2. Now goto https://blahblah.myshopify.com/admin/products/inventory
3. Select the Product created at Step 1 and Click on Edit variants

and XSS will be triggered


</details>

---
*Analysed by Claude on 2026-05-24*
