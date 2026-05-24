# Business Logic, currency arbitrage - Possibility to pay less than the price in USD

## Metadata
- **Source:** HackerOne
- **Report:** 1677155 | https://hackerone.com/reports/1677155
- **Submitted:** 2022-08-22
- **Reporter:** xctzn
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Business Logic Errors
- **CVEs:** None
- **Category:** business-logic

## Summary
Currency fluctuate all the time. Theses days EUR / USD key pair is around 1for1. It was even 1:0.99 when I was writing this report.
Portswigger doesn't change dynamically the price and exchange rate dynamically. 

Vulnerability at the following link: https://portswigger.net/buy/pro 

When you want to buy a product choose the currency, you can noticed they are fixed and with today difference it's q

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

Currency fluctuate all the time. Theses days EUR / USD key pair is around 1for1. It was even 1:0.99 when I was writing this report.
Portswigger doesn't change dynamically the price and exchange rate dynamically. 

Vulnerability at the following link: https://portswigger.net/buy/pro 

When you want to buy a product choose the currency, you can noticed they are fixed and with today difference it's quite a big difference.

## Impact

USD price is 399$USD, while EUR price is 349$. 
Therefore someone could just change the price to Euro and pay 347 $USD (349 Euro) instead of 399$(with current rate).

PS: It scale with the price, it could lead to thousands of dollars lost for your company.

</details>

---
*Analysed by Claude on 2026-05-24*
