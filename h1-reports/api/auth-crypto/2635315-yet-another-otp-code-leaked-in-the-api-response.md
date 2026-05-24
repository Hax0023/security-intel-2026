# Yet Another OTP code Leaked in the API Response

## Metadata
- **Source:** HackerOne
- **Report:** 2635315 | https://hackerone.com/reports/2635315
- **Submitted:** 2024-08-01
- **Reporter:** tinopreter
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** critical
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
## Summary:
This is much similar to my report here(https://hackerone.com/reports/2633888) , except it affects a different domain. The application requests a phone number for authentication, then sends an OTP code to the user. But the OTP is leaked in the response which defeats the whole purpose of it's implementation.



## Steps To Reproduce:

{F3486534}

## Supporting Material/References:
https:

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
This is much similar to my report here(https://hackerone.com/reports/2633888) , except it affects a different domain. The application requests a phone number for authentication, then sends an OTP code to the user. But the OTP is leaked in the response which defeats the whole purpose of it's implementation.



## Steps To Reproduce:

{F3486534}

## Supporting Material/References:
https://hackerone.com/reports/2633888

##Recommendation
Don't return the OTP code in the API's response

## Impact

It's possible to sign up with other users accounts. It's possible to log into other users accounts as well. Another thing I noticed is that, you can sign up with any 10-digit phone number since the OTP is in the response for you to use, makes creating junk accounts easily possible.

</details>

---
*Analysed by Claude on 2026-05-24*
