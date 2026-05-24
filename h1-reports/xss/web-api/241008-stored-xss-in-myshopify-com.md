# Stored XSS in *.myshopify.com

## Metadata
- **Source:** HackerOne
- **Report:** 241008 | https://hackerone.com/reports/241008
- **Submitted:** 2017-06-17
- **Reporter:** jamesclyde
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Stored
- **CVEs:** None
- **Category:** web-api

## Summary
Hello,

First of all in noticed that this is out of scope "Any issue related to the storefront area being displayed in a <iframe> element in the admin area, for example in the Theme Editor." 

This is not in the store front and this will be set in an XSS payload.

1. Go to https://(YOUR SHOP).myshopify.com/admin/themes/THEME id)/editor
2. Select header and scroll down to "annoucement text".
3. Fil

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

First of all in noticed that this is out of scope "Any issue related to the storefront area being displayed in a <iframe> element in the admin area, for example in the Theme Editor." 

This is not in the store front and this will be set in an XSS payload.

1. Go to https://(YOUR SHOP).myshopify.com/admin/themes/THEME id)/editor
2. Select header and scroll down to "annoucement text".
3. Fill there as payload: "&gt;<img src="x" onerror="alert(document.cookie)">
4. Click save and the XSS will be popped up.

I have checked it twice and it is not gonna reflect on the store front. This XSS is in the myshopify/admin section.

POC screen:
https://snag.gy/FImTKd.jpg

</details>

---
*Analysed by Claude on 2026-05-24*
