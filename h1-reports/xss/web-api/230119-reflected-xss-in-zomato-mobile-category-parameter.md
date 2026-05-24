# Reflected XSS in Zomato Mobile - category parameter

## Metadata
- **Source:** HackerOne
- **Report:** 230119 | https://hackerone.com/reports/230119
- **Submitted:** 2017-05-20
- **Reporter:** harrymg
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
Hi there. I have found a reflected XSS in Zomato.com mobile. This XSS affects mobile users of Zomato. Steps to reproduce:

1. Go to Zomato.com and change your user agent to mobile *(iPhone/Android user agent)*
2. Go to a certain restaurant/place and their photos *(e.g. site: https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=ambience)*
3. Change the value in the ```catego

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

Hi there. I have found a reflected XSS in Zomato.com mobile. This XSS affects mobile users of Zomato. Steps to reproduce:

1. Go to Zomato.com and change your user agent to mobile *(iPhone/Android user agent)*
2. Go to a certain restaurant/place and their photos *(e.g. site: https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=ambience)*
3. Change the value in the ```category``` parameter to an XSS payload: ```
"--><%2Fscript><svg%2Fonload%3D'%3Balert(document.domain)%3B'>```
4. Final URL will look like this: https://www.zomato.com/manila/artsy-cafe-diliman-quezon-city/photos?category=%22--%3E%3C%2Fscript%3E%3Csvg%2Fonload%3D%27%3Balert%28document.domain%29%3B%27%3E

XSS will execute. POC attached.

Thanks and I hope you consider and fix this

</details>

---
*Analysed by Claude on 2026-05-24*
