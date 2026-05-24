# CSRF to Information disclosure on password reset

## Metadata
- **Source:** HackerOne
- **Report:** 2106662 | https://hackerone.com/reports/2106662
- **Submitted:** 2023-08-11
- **Reporter:** hackeriron1
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
## Summary:
Hi Team,

It's low hanging security risk but it's significant for users. where attacker able to get victim IP, Address and Browser details. 
This is disclosing users information. one click information disclosed. 

CSRF vulnerability on password reser link.
Attacker can ask for a password reset link on his own email by sending a link to the Victim, which will contain the Victim's IP add

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

## Summary:
Hi Team,

It's low hanging security risk but it's significant for users. where attacker able to get victim IP, Address and Browser details. 
This is disclosing users information. one click information disclosed. 

CSRF vulnerability on password reser link.
Attacker can ask for a password reset link on his own email by sending a link to the Victim, which will contain the Victim's IP address and browser details.


## Steps To Reproduce:
1. Go to ███████ and change email to your own email.
2. send to victim and victim will open in browser.
3. Automatically Password reset link send 

## Supporting Material/References:
POC Video you can see. 
███

## Impact

Attacker can ask for a password reset link on his own email by sending a link to the Victim, which will contain the Victim's IP address and browser details.

</details>

---
*Analysed by Claude on 2026-05-24*
