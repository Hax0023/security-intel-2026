# Private program activity timeline information disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 116029 | https://hackerone.com/reports/116029
- **Submitted:** 2016-02-12
- **Reporter:** charfe
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
HI,

There are some company which are hosting as external
https://hackerone.com/directory?query=type%3Aexternal&sort=name%3Aascending&page=1

but some one was hosting private BB on HackerOne which are not visible unless they invite you. However, you can check if any company is hosting private BB on HackerOne or not if you can guess the username they use.

Poc
https://hackerone.com/<redacted> : its

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

HI,

There are some company which are hosting as external
https://hackerone.com/directory?query=type%3Aexternal&sort=name%3Aascending&page=1

but some one was hosting private BB on HackerOne which are not visible unless they invite you. However, you can check if any company is hosting private BB on HackerOne or not if you can guess the username they use.

Poc
https://hackerone.com/<redacted> : its external bb but the have a private bb

now let's discloure there activites :
https://hackerone.com/<redacted>/activities.json

and you can use it to check if they are private bb or not 
Generally most company chooses the same name as their company name like yahoo.

Cheers,
@tws_charfeddine


</details>

---
*Analysed by Claude on 2026-05-24*
