# The csrf token remains same after user logs in

## Metadata
- **Source:** HackerOne
- **Report:** 49974 | https://hackerone.com/reports/49974
- **Submitted:** 2015-03-04
- **Reporter:** tmfelwu
- **Program:** Unknown
- **Bounty:** $50
- **Severity:** unknown
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** web-api

## Summary
As the CSRF token doesn't change after login. Any other user that uses the same workstation is vulnerable. A safer way would be to use dynamic CSRF token or just change the token after login, so attacker doesnt get hold of this. 

Details of the attacks scenario in a shared workstation environment

1. The attacker simply copies the authenticity token. This token is the only protection against 

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

As the CSRF token doesn't change after login. Any other user that uses the same workstation is vulnerable. A safer way would be to use dynamic CSRF token or just change the token after login, so attacker doesnt get hold of this. 

Details of the attacks scenario in a shared workstation environment

1. The attacker simply copies the authenticity token. This token is the only protection against the CSRF attack.

2. Any other user that uses the workstation after that is vulnerable to CSRF. The attacker simply needs to craft a link with the required GET or POST method as he already have the CSRF token and send it to the victim via email, chat etc.

3. The attacker can trick the victim in doing anything he wants without the user being aware of it.

In the most basic sense the attacker has an authenticity token of another user which he shouldn't have had in the first place.

</details>

---
*Analysed by Claude on 2026-05-24*
