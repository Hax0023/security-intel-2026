# Stored XSS in Slackbot Direct Messages

## Metadata
- **Source:** HackerOne
- **Report:** 4561 | https://hackerone.com/reports/4561
- **Submitted:** 2014-03-22
- **Reporter:** prakharprasad
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-site Scripting (XSS) - Generic
- **CVEs:** None
- **Category:** web-api

## Summary
Whenever a new team is created, Slackbot uses automated profile completion by asking a few questions from the user like the first name, last name, skype account etc. But instead of providing the correct details we provide `<javascript:alert(document.cookie);>` as input then Slackbot will cause the data go inside the anchor tag `<a href=javascript:alert(document.cookie);>...</a>` so clicking on the

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

Whenever a new team is created, Slackbot uses automated profile completion by asking a few questions from the user like the first name, last name, skype account etc. But instead of providing the correct details we provide `<javascript:alert(document.cookie);>` as input then Slackbot will cause the data go inside the anchor tag `<a href=javascript:alert(document.cookie);>...</a>` so clicking on the link will trigger XSS.

Video POC: https://www.dropbox.com/s/7fmbe4jnd923pd0/Dumbbot-XSS.mov

</details>

---
*Analysed by Claude on 2026-05-24*
