# Price Manipulation in Support Rider Amount via Negative Fraction Values

## Metadata
- **Source:** HackerOne
- **Report:** 927661 | https://hackerone.com/reports/927661
- **Submitted:** 2020-07-20
- **Reporter:** 0xdekster
- **Program:** Zomato
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Price Manipulation, Insufficient Input Validation, Business Logic Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
A price manipulation vulnerability exists in Zomato's checkout process where the support rider donation amount accepts negative fractional values, allowing attackers to reduce the total order amount by up to 0.99 Rupees. By intercepting and modifying the support rider parameter to a negative value during checkout, users can decrease their payment obligation before order placement.

## Attack scenario
1. Attacker adds items to their Zomato cart with a total cost (e.g., 500 Rupees)
2. During checkout, attacker selects a support rider donation amount (e.g., 25, 50, or 100 Rupees)
3. Attacker intercepts the HTTP request containing the donation amount using a proxy tool
4. Attacker modifies the support rider donation field from a positive value to '-0.99' in the request payload
5. Attacker forwards the modified request to the server
6. The final order total is reduced by 0.99 Rupees, and the discounted amount is paid and order is successfully placed

## Root cause
Server-side validation for the support rider donation amount lacks proper bounds checking and does not restrict negative values. The application accepts any numeric value without verifying that it is non-negative, allowing arithmetic manipulation of the final price.

## Attacker mindset
An economically motivated attacker could exploit this to save small amounts on every order. While individual savings are minimal (max 0.99 Rupees), repeated exploitation across multiple orders could result in significant cumulative fraud. This could be part of a larger exploitation pattern when combined with other price manipulation vectors.

## Defensive takeaways
- Implement strict server-side validation to ensure donation/support amounts are non-negative and meet minimum thresholds
- Use whitelist validation: only accept predefined donation amounts (25, 50, 100) rather than accepting arbitrary values
- Validate all price-related parameters at the backend, never trust client-side values
- Implement range checks: verify that support rider amounts fall within acceptable bounds (0 to max_allowed)
- Add logging and monitoring for suspicious price modifications or negative amount submissions
- Use fixed-point arithmetic or Decimal types for financial calculations to avoid floating-point precision issues
- Implement a price recalculation audit on the server before payment processing

## Variant hunting
Test other donation/tip fields with negative values across different payment flows
Attempt price manipulation on promotional discount codes with negative values
Test other numerical financial fields (taxes, delivery charges, platform fees) with negative manipulation
Check if the vulnerability exists in refund or credit note calculation flows
Investigate whether decimal values beyond -0.99 are accepted (e.g., -1.5, -10.00)
Test the vulnerability across different user account types (premium, regular, delivery partner)
Verify if the issue persists across different payment methods and currencies

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1589: Gather Victim Identity Information
- T1566: Phishing

## Notes
This is a straightforward but impactful business logic vulnerability. While individual impact is small (max 0.99 Rupees), it demonstrates a fundamental failure in price validation that could indicate similar issues elsewhere in the platform. The vulnerability requires no authentication bypass and is trivial to exploit. The bounty amount was not disclosed in the report. This type of vulnerability is common in e-commerce platforms and should be caught during security code review focusing on financial transaction handling.

## Full report
<details><summary>Expand</summary>

Hi Team

I have found an issue in support rider amount calculation at the time of checkout where the amount is tamperable by negative fraction of rupees which makes the total amount decreased by maximum of 1rs.

POC - 

1-Goto - zomato.com
2 - Add anything to your cart
3- At the checkout page , Add some money to Support Riders , click on any 25,50,100
4- Intercept the request of adding support rider money.
5- Change the price of Support Rider to " -0.99" in both fields of donation money.
6- Forward the request , the Cart value will change.
7- Pay by any platform, order will get placed.


Thanks

## Impact

Price Manipulation in Support Rider

</details>

---
*Analysed by Claude on 2026-05-24*
