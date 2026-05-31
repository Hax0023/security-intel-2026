# Stored Cross site scripting

## Metadata
- **Source:** HackerOne
- **Report:** 145246 | https://hackerone.com/reports/145246
- **Submitted:** 2016-06-16
- **Reporter:** amirisme
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
hello zomato team,

i have found a stored xss on https://www.zomato.com/beirut/garcias-dbayeh-metn

step to reproduce
--------------------------
1- write a review by this payload : >'>"><img src=x onmouseover =prompt(document.domain)>
2-click edit
3- xss will excute :)

video : https://youtu.be/ibawEBPQs3g

best regaeds,
Amir Ezat.



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

hello zomato team,

i have found a stored xss on https://www.zomato.com/beirut/garcias-dbayeh-metn

step to reproduce
--------------------------
1- write a review by this payload : >'>"><img src=x onmouseover =prompt(document.domain)>
2-click edit
3- xss will excute :)

video : https://youtu.be/ibawEBPQs3g

best regaeds,
Amir Ezat.



</details>

---
*Analysed by Claude on 2026-05-31*
