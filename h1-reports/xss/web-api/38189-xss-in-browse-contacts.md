# xss in /browse/contacts/

## Metadata
- **Source:** HackerOne
- **Report:** 38189 | https://hackerone.com/reports/38189
- **Submitted:** 2014-12-04
- **Reporter:** defmax
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
hey guys 

i just found an xss in openfolio

i just created an contact in google with  name as "><img src=x onerror=prompt(1)>  and gave an email as random 

url >> https://www.google.com/contacts/u/0/#contact/new


then i synced  openfolio with  google contacts 

then i went here >> https://openfolio.com/browse/contacts/

then i clicked on invite of  "><img src=x onerror=prompt(1)>  

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

hey guys 

i just found an xss in openfolio

i just created an contact in google with  name as "><img src=x onerror=prompt(1)>  and gave an email as random 

url >> https://www.google.com/contacts/u/0/#contact/new


then i synced  openfolio with  google contacts 

then i went here >> https://openfolio.com/browse/contacts/

then i clicked on invite of  "><img src=x onerror=prompt(1)>  , i got the xss popup ~

POC >> http://postimg.org/image/6po3vo89l/




</details>

---
*Analysed by Claude on 2026-05-24*
