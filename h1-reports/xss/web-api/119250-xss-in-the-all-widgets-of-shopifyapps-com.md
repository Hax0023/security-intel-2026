# xss in the all widgets of shopifyapps.com

## Metadata
- **Source:** HackerOne
- **Report:** 119250 | https://hackerone.com/reports/119250
- **Submitted:** 2016-02-28
- **Reporter:** sergeym
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
i found xss in all widgets.shopifyapps.com/* (google dork:site:widgets.shopifyapps.com)
the parameter "padding" is vulnerable,xss payload - }%0a{}*{x:expression(alert(1))}%0a{

xss does work in inetrnet explorer browsers( for ie10,ie11 in compatibility mode) , for ie5,ie6,ie7

for ie8,ie9 javascript is disabled, the content of page to have a strings:
<!--[if IE 8]><html class="ie ie8 no-js" lang="

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

i found xss in all widgets.shopifyapps.com/* (google dork:site:widgets.shopifyapps.com)
the parameter "padding" is vulnerable,xss payload - }%0a{}*{x:expression(alert(1))}%0a{

xss does work in inetrnet explorer browsers( for ie10,ie11 in compatibility mode) , for ie5,ie6,ie7

for ie8,ie9 javascript is disabled, the content of page to have a strings:
<!--[if IE 8]><html class="ie ie8 no-js" lang="en"> <![endif]-->
<!--[if IE 9 ]><html class="ie ie9 no-js"> <![endif]-->
<!--[if gt IE 9 ]><html class="ie gt-ie9 no-js"> <![endif]-->
 

how to reproduce:

1. to use ineternet explorer browser 10, for example
2. go to the page: 

https://widgets.shopifyapps.com/products/a-luv-u-pet-pink-geordie-card?shop=the-mag-shop.myshopify.com&style=artgallery&image-size=medium&border-color=%23af4fcc&padding=}%0a{}*{x:expression(alert(1))}%0a{&button-text=Buy+Now+in+The+Mag+shop&destination=product

3.  to use compatibility mode in ie10 (to use ie7 mode by default)
4. to see alert box with 1





</details>

---
*Analysed by Claude on 2026-05-24*
