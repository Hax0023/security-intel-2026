# Stored xss

## Metadata
- **Source:** HackerOne
- **Report:** 156373 | https://hackerone.com/reports/156373
- **Submitted:** 2016-08-03
- **Reporter:** rishi62
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Hi,i have found an stored xss which is reflected at https://www.algolia.com/explorer#?index=getstarted_actors&tab=explorer

Steps to produce:
1) Go to https://www.algolia.com/explorer#?index=getstarted_actors&tab=explorer and add "><img src=x onerror=alert(document.cookie);> as an attribute and keep it at top as in screenshot1

2) Go to  https://www.algolia.com/explorer#?index=getstarted_actors&ta

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

Hi,i have found an stored xss which is reflected at https://www.algolia.com/explorer#?index=getstarted_actors&tab=explorer

Steps to produce:
1) Go to https://www.algolia.com/explorer#?index=getstarted_actors&tab=explorer and add "><img src=x onerror=alert(document.cookie);> as an attribute and keep it at top as in screenshot1

2) Go to  https://www.algolia.com/explorer#?index=getstarted_actors&tab=ranking and take the cursor on the ranking info(the trophy icon),and you will see a pop up alert of xss. (Screenshot2)
 I have tested it on Chrome and firefox its works on both.


P.S: I dont know why but my ip got banned when i was uploading the script to test could you unban me?


</details>

---
*Analysed by Claude on 2026-05-24*
