# XSS in my.shopify.com in  widget

## Metadata
- **Source:** HackerOne
- **Report:** 185826 | https://hackerone.com/reports/185826
- **Submitted:** 2016-11-27
- **Reporter:** xssa
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** medium
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi security team
I found XSS in the Buy Button in my.shopify.com


Step to reproduce 

1-Go to Product and create Product with these payload <img src="a" onerror="prompt(document.cookie)" />;
See (Step1)

2- Now Go to Embed on a website  and in the buy bouton page chose the third template and XSS will pop up 


Patch it 



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

Hi security team
I found XSS in the Buy Button in my.shopify.com


Step to reproduce 

1-Go to Product and create Product with these payload <img src="a" onerror="prompt(document.cookie)" />;
See (Step1)

2- Now Go to Embed on a website  and in the buy bouton page chose the third template and XSS will pop up 


Patch it 



</details>

---
*Analysed by Claude on 2026-05-24*
