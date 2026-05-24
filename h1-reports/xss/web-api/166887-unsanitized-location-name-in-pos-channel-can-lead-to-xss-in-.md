# Unsanitized Location Name in POS Channel can lead to XSS in Orders Timeline

## Metadata
- **Source:** HackerOne
- **Report:** 166887 | https://hackerone.com/reports/166887
- **Submitted:** 2016-09-08
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi!

I would like to report XSS at Shopify Admin Interface in Orders TImeline, in line Usename processes this order at NAME

NAME is not sanitized and if this is set to <img src=x onerror=prompt(1)> XSS will happen

***POC***
Visit
https://whitehat-3.myshopify.com/admin/orders/2253786753
or
https://whitehat-3.myshopify.com/admin/orders/2253753665

XSS will trigger!

Thanks!


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

Hi!

I would like to report XSS at Shopify Admin Interface in Orders TImeline, in line Usename processes this order at NAME

NAME is not sanitized and if this is set to <img src=x onerror=prompt(1)> XSS will happen

***POC***
Visit
https://whitehat-3.myshopify.com/admin/orders/2253786753
or
https://whitehat-3.myshopify.com/admin/orders/2253753665

XSS will trigger!

Thanks!


</details>

---
*Analysed by Claude on 2026-05-24*
