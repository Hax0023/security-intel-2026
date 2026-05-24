# cross site scripting in : mtn.bj

## Metadata
- **Source:** HackerOne
- **Report:** 1264834 | https://hackerone.com/reports/1264834
- **Submitted:** 2021-07-16
- **Reporter:** alimanshester
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Cross-site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Xss vulnerability in mtn.bj  in file name 

## Steps To Reproduce:


  1.Go to : 
https://www.mtn.bj/business/ressources/formulaires/plan-de-localisation-de-compte/?next=https://www.mtn.bj/business/ressources/formulaires/formulaire-de-souscription/
  2 - fill all inputs with any data 
3 - in file upload upload a file with payload file name such as : "><img src=x onerror=alert(document.

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

## Summary:
Xss vulnerability in mtn.bj  in file name 

## Steps To Reproduce:


  1.Go to : 
https://www.mtn.bj/business/ressources/formulaires/plan-de-localisation-de-compte/?next=https://www.mtn.bj/business/ressources/formulaires/formulaire-de-souscription/
  2 - fill all inputs with any data 
3 - in file upload upload a file with payload file name such as : "><img src=x onerror=alert(document.cookie);.jpg

4-the payload will executed in the page .

## Supporting Material/References:
1 - video showing poc 
2 - screen shot

## Impact

execute malicious java script in user browser

</details>

---
*Analysed by Claude on 2026-05-24*
