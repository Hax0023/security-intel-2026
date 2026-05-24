# XSS in https://app.mavenlink.com/workspaces/

## Metadata
- **Source:** HackerOne
- **Report:** 63537 | https://hackerone.com/reports/63537
- **Submitted:** 2015-05-23
- **Reporter:** enderun07
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
My name of mavelink account causes cross site scripting vulnerability

my name="><img src=x onerror=prompt(31);>

go to  https://app.mavenlink.com/workspaces/8591867/gantt

and click "save snapshot" button  than save it

When You save it you will get javascrip alert from "Can be viewed by ">" area beucae my mavelink name ("><img src=x onerror=prompt(31);>)


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

My name of mavelink account causes cross site scripting vulnerability

my name="><img src=x onerror=prompt(31);>

go to  https://app.mavenlink.com/workspaces/8591867/gantt

and click "save snapshot" button  than save it

When You save it you will get javascrip alert from "Can be viewed by ">" area beucae my mavelink name ("><img src=x onerror=prompt(31);>)


</details>

---
*Analysed by Claude on 2026-05-24*
