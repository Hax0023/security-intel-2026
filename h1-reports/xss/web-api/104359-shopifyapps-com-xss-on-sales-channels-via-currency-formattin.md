# shopifyapps.com XSS on sales channels via currency formatting

## Metadata
- **Source:** HackerOne
- **Report:** 104359 | https://hackerone.com/reports/104359
- **Submitted:** 2015-12-09
- **Reporter:** reactors08
- **Program:** Unknown
- **Bounty:** $1,000
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
pinterest, twitter, buy button and facebook sales channels vulnerable to xss via currency formatting.

steps to reproduce:
- remove pinterest, twitter, buy button and facebook sales channels at *.myshopify.com/admin/channels
- go to *.myshopify.com/admin/settings/general
- change currency formating as shown at the `currency_formatting.jpg`(check attachment)
- add pinterest, twitter, buy button and

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

pinterest, twitter, buy button and facebook sales channels vulnerable to xss via currency formatting.

steps to reproduce:
- remove pinterest, twitter, buy button and facebook sales channels at *.myshopify.com/admin/channels
- go to *.myshopify.com/admin/settings/general
- change currency formating as shown at the `currency_formatting.jpg`(check attachment)
- add pinterest, twitter, buy button and facebook sales channels at *.myshopify.com/admin/channels
- check pinterest, twitter and buy button tabs
- create collection and add a product to it (skip this step if you already have collection with product)
- go to facebook tab --> shop  ( `*.myshopify.com/admin/apps/shopify-facebook/collections` )

</details>

---
*Analysed by Claude on 2026-05-24*
