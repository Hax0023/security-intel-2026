# Login CSRF using Google OAuth

## Metadata
- **Source:** HackerOne
- **Report:** 118737 | https://hackerone.com/reports/118737
- **Submitted:** 2016-02-25
- **Reporter:** 5hivaay
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
This bug is related to bug report [https://hackerone.com/reports/774] as this bug also allows a user to be logged in as the attacker. 

An attacker could exploit this bug as follows:

Attacker initiates Google OAuth process with thisdata
Attacker allows access to thisdata app
Attacker records and drops redirection to thisdata (in order not to consume token)
Attacker directs victim to /oauth/redire

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

This bug is related to bug report [https://hackerone.com/reports/774] as this bug also allows a user to be logged in as the attacker. 

An attacker could exploit this bug as follows:

Attacker initiates Google OAuth process with thisdata
Attacker allows access to thisdata app
Attacker records and drops redirection to thisdata (in order not to consume token)
Attacker directs victim to /oauth/redirect?state={attacker's state}&code={attacker's code}
Victim is now logged in as attacker

state parameter is solution for this but in this case state parameter is not getting validated on server side.


</details>

---
*Analysed by Claude on 2026-05-24*
