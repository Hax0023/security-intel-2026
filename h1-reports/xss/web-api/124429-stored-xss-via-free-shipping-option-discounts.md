# Stored XSS via "Free Shipping" option (Discounts)

## Metadata
- **Source:** HackerOne
- **Report:** 124429 | https://hackerone.com/reports/124429
- **Submitted:** 2016-03-19
- **Reporter:** ancst
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
POC  steps:
1) Go to the customers page and add a new search group named as "><img src=x onerror=prompt(7) (see img1.png)
2) Go to the discounts page, create a new discount code and mark the "Free Shipping" option. 
3) Open a web proxy (i.e. tamper data) and press the "save discount" button.
4) Through the web proxy (i.e. tamper data) modify the POST request and change the value of "discount%5Bapp

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

POC  steps:
1) Go to the customers page and add a new search group named as "><img src=x onerror=prompt(7) (see img1.png)
2) Go to the discounts page, create a new discount code and mark the "Free Shipping" option. 
3) Open a web proxy (i.e. tamper data) and press the "save discount" button.
4) Through the web proxy (i.e. tamper data) modify the POST request and change the value of "discount%5Bapplies_to_resource%5D" to "customer_saved_search" and the "discount%5Bapplies_to_id%5D" to "1131411463" (the id of the new search group in step 1)(see img2.png).
5) Xssed (img3.png)

    Click Save

</details>

---
*Analysed by Claude on 2026-05-24*
