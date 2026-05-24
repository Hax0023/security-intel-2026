# No rate limit in stats api token endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 412526 | https://hackerone.com/reports/412526
- **Submitted:** 2018-09-21
- **Reporter:** exploit0tango
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Restriction of Authentication Attempts
- **CVEs:** None
- **Category:** auth-crypto

## Summary
##Brute force on statsapi endpoint to view stats of an user##


## Steps To Reproduce:

  1.  Stats api token can be generated at https://chaturbate.com/statsapi/authtoken/
https://chaturbate.com/statsapi/?username=hackeronetestchat&token=**vulnerable**

 I've used my profile and and my token to check brute force

The  correct token returned with 200 ok status

## Impact

An attacker could view th

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

##Brute force on statsapi endpoint to view stats of an user##


## Steps To Reproduce:

  1.  Stats api token can be generated at https://chaturbate.com/statsapi/authtoken/
https://chaturbate.com/statsapi/?username=hackeronetestchat&token=**vulnerable**

 I've used my profile and and my token to check brute force

The  correct token returned with 200 ok status

## Impact

An attacker could view the stats of an user

</details>

---
*Analysed by Claude on 2026-05-24*
