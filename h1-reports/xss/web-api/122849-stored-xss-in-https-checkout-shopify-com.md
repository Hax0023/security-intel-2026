# Stored XSS in https://checkout.shopify.com/

## Metadata
- **Source:** HackerOne
- **Report:** 122849 | https://hackerone.com/reports/122849
- **Submitted:** 2016-03-13
- **Reporter:** niyaax
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
**STEPS TO REPRODUCE**

1. Go to http://hardware.shopify.com/products/custom-gift-card?variant=976094353 and Design your own gift card.
2. Change file type to url on the upload field.
3. Add the payload `javascript:alert(document.domain);//https://cdn.shopify.com/s/files/1/0224/0965/uploads/1fc1042c960abdb2f35c0950900a7b2c.svg`
4. Then add the item to the cart and go to checkout.
5. On the checkou

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

**STEPS TO REPRODUCE**

1. Go to http://hardware.shopify.com/products/custom-gift-card?variant=976094353 and Design your own gift card.
2. Change file type to url on the upload field.
3. Add the payload `javascript:alert(document.domain);//https://cdn.shopify.com/s/files/1/0224/0965/uploads/1fc1042c960abdb2f35c0950900a7b2c.svg`
4. Then add the item to the cart and go to checkout.
5. On the checkout page click the Artwork File and the XSS will trigger.



</details>

---
*Analysed by Claude on 2026-05-24*
