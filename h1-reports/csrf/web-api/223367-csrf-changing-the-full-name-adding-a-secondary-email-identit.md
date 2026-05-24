# CSRF - Changing the full name / adding a secondary email identity of an account via a GET request

## Metadata
- **Source:** HackerOne
- **Report:** 223367 | https://hackerone.com/reports/223367
- **Submitted:** 2017-04-24
- **Reporter:** inhibitor181
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
SUMMARY
----------
Hello, I have found a CSRF request via the activation email that will change the full name of the targeted account. This vulnerability exists if the attacker registers a new account and then gives his activation link to someone else. If the victim uses the received activation link while he is logged in his account the attacker's email will be added as a secondary email and the m

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

SUMMARY
----------
Hello, I have found a CSRF request via the activation email that will change the full name of the targeted account. This vulnerability exists if the attacker registers a new account and then gives his activation link to someone else. If the victim uses the received activation link while he is logged in his account the attacker's email will be added as a secondary email and the main full name will be changed.

POC
-------
I have attached the POC as a video where you can see all the steps.

IMPACT
------
Medium - high impact IMO. Changing the name may not be such a big deal, but adding a secondary email identity may turn into something more dangerous.

</details>

---
*Analysed by Claude on 2026-05-24*
