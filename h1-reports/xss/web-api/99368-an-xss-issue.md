# an xss issue

## Metadata
- **Source:** HackerOne
- **Report:** 99368 | https://hackerone.com/reports/99368
- **Submitted:** 2015-11-12
- **Reporter:** securitythinker
- **Program:** Unknown
- **Bounty:** $100
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
i found an xss issue here :
https://www.algolia.com/explorer#?index=test&tab=ranking
i tried to put  an xss payload ("><img src=x onerror=alert(0)>)
in index > ranking> so i put the xss payload in Ranking formula then hit save ...when it is being saved the xss payload is being stored that upon Indices xss payload executed
p.s please screen shot


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

i found an xss issue here :
https://www.algolia.com/explorer#?index=test&tab=ranking
i tried to put  an xss payload ("><img src=x onerror=alert(0)>)
in index > ranking> so i put the xss payload in Ranking formula then hit save ...when it is being saved the xss payload is being stored that upon Indices xss payload executed
p.s please screen shot


</details>

---
*Analysed by Claude on 2026-05-24*
