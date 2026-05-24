# Team object in GraphQL disclosed total number of whitelisted hackers

## Metadata
- **Source:** HackerOne
- **Report:** 342978 | https://hackerone.com/reports/342978
- **Submitted:** 2018-04-25
- **Reporter:** haxta4ok00
- **Program:** Unknown
- **Bounty:** $2,500
- **Severity:** medium
- **Vuln:** Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
**Summary:**
Hi team. Whitelisted_hackers i think your setup - `Two-factor authentication and IP whitelisting are available to further restrict access to accounts.`
**Description:**
Again, because of the link error, I can see the number, but I can't see these links. Analogue #310946
### Steps To Reproduce

1. {"query": "query {team(handle:\\\"security\\\"){id,name,handle,whitelisted_hackers{total_

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
Hi team. Whitelisted_hackers i think your setup - `Two-factor authentication and IP whitelisting are available to further restrict access to accounts.`
**Description:**
Again, because of the link error, I can see the number, but I can't see these links. Analogue #310946
### Steps To Reproduce

1. {"query": "query {team(handle:\\\"security\\\"){id,name,handle,whitelisted_hackers{total_count}}}"}

Result:

`{"data":{"team":{"id":"Z2lkOi8vaGFja2Vyb25lL1RlYW0vMTM=","name":"HackerOne","handle":"security",
"whitelisted_hackers":{"total_count":30}}}}`

* whitelisted_hackers":{"total_count":30} - You have 30 members for 2FA and white IP

Sorry i bad speak english
I hope you understand me
Thank you,haxta4ok00

PS. I'm glad you accept reports in other languages, but I'm used to this format

## Impact

Disclosure count "whitelisted_hackers"

</details>

---
*Analysed by Claude on 2026-05-24*
