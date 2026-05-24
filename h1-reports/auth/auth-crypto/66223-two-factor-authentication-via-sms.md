# Two-factor authentication (via SMS)

## Metadata
- **Source:** HackerOne
- **Report:** 66223 | https://hackerone.com/reports/66223
- **Submitted:** 2015-06-05
- **Reporter:** dia2diab
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** unknown
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hello Coinbase Security Team

I just found a problem in Two-factor authentication mechanism, here is the details and how to reproduce this issue:

I have two accounts with two emails on `████` i active `2FA` on the both of two emails with this phone number `██████████.

From `Chrome` i will try to login using my first email `█████` and now i recieved my code related to this email here `60209

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

Hello Coinbase Security Team

I just found a problem in Two-factor authentication mechanism, here is the details and how to reproduce this issue:

I have two accounts with two emails on `████` i active `2FA` on the both of two emails with this phone number `██████████.

From `Chrome` i will try to login using my first email `█████` and now i recieved my code related to this email here `6020930`.

From `FireFox` i will try to do the same thing using my second email `████████` and now i recieved my second code for the second email `1091566`.

Logically, the following steps must be excuted to make the two accounts be logged in:

`████████` => `6020930`
`████` => `1091566`

But the problem is when i change the two code and emails to be 
`███` => `1091566`
`███████` => `6020930`

I found myself be logged in with two accounts and there is no problem there, The exactly problem is you allow accounts that have the same number to be logged in with each other verification code if they request a login via SMS.

Thank you.
█████ 

</details>

---
*Analysed by Claude on 2026-05-24*
