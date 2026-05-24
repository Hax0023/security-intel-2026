# XSS in Myshopify Admin Site in DISCOUNTS

## Metadata
- **Source:** HackerOne
- **Report:** 71614 | https://hackerone.com/reports/71614
- **Submitted:** 2015-06-19
- **Reporter:** nismo
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
POC

1. Go to Customers and add a new search group named "><img src=x onerror=prompt(7) See creategroup.png
2. Go to Discounts and add a Discount Code based on Customer group and choose the one created above
3. Click Save

XSS in discounts occur (discountxss.png)

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

POC

1. Go to Customers and add a new search group named "><img src=x onerror=prompt(7) See creategroup.png
2. Go to Discounts and add a Discount Code based on Customer group and choose the one created above
3. Click Save

XSS in discounts occur (discountxss.png)

</details>

---
*Analysed by Claude on 2026-05-24*
