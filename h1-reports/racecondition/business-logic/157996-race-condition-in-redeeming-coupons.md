# Race Condition in Redeeming Coupons

## Metadata
- **Source:** HackerOne
- **Report:** 157996 | https://hackerone.com/reports/157996
- **Submitted:** 2016-08-09
- **Reporter:** cablej
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** business-logic

## Summary
Hello,

There exists a race condition in redeeming coupons, allowing a user to redeem the same coupon multiple times, and stacking savings added. This allows for a user to get virtually any discount.

POC:

1. Visit your account and select 'Promo Codes'.
2. Select redeem promo code, and add any promo code. For example, I found the code 'dallas20'.
3. Intercept the request using a proxy, and make t

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

Hello,

There exists a race condition in redeeming coupons, allowing a user to redeem the same coupon multiple times, and stacking savings added. This allows for a user to get virtually any discount.

POC:

1. Visit your account and select 'Promo Codes'.
2. Select redeem promo code, and add any promo code. For example, I found the code 'dallas20'.
3. Intercept the request using a proxy, and make the request multiple times, asynchronously.
4. The code will be redeemed multiple times.

For an example, see the screenshot attached.

</details>

---
*Analysed by Claude on 2026-05-24*
