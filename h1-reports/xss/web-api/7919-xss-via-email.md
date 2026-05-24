# XSS via Email

## Metadata
- **Source:** HackerOne
- **Report:** 7919 | https://hackerone.com/reports/7919
- **Submitted:** 2014-04-17
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
This one was easy.

Someone needs send an email with **Subject** line : *"><img src=x onerror=alert(document.cookie);>* to the team email, mine was **kfvm@mail.respond.ly**

So once the email arrives it will execute Javascript (See attachment)

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

This one was easy.

Someone needs send an email with **Subject** line : *"><img src=x onerror=alert(document.cookie);>* to the team email, mine was **kfvm@mail.respond.ly**

So once the email arrives it will execute Javascript (See attachment)

</details>

---
*Analysed by Claude on 2026-05-24*
