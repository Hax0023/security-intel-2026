# Cross Site Scripting (Stored) 

## Metadata
- **Source:** HackerOne
- **Report:** 20221 | https://hackerone.com/reports/20221
- **Submitted:** 2014-07-16
- **Reporter:** charan-eis
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Occurred in the URL : https://store.ellislab.com/billing
After adding a product to the cart proceed to add the billing and card information and in the card fields give your card details respectively and in the fields 
1. First name
2. Last name
3. Street Address
4. Apt/Suite/#
5. City. 

Give the following payload : "><img src=x onerror=prompt(0);> and click on Place Order and there it goe

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

Occurred in the URL : https://store.ellislab.com/billing
After adding a product to the cart proceed to add the billing and card information and in the card fields give your card details respectively and in the fields 
1. First name
2. Last name
3. Street Address
4. Apt/Suite/#
5. City. 

Give the following payload : "><img src=x onerror=prompt(0);> and click on Place Order and there it goes 5 stored XSS will appear

</details>

---
*Analysed by Claude on 2026-05-24*
