# Missing rate limit for current password field (Password Change) Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 827484 | https://hackerone.com/reports/827484
- **Submitted:** 2020-03-23
- **Reporter:** full109tun
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Restriction of Authentication Attempts
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Vulnerability:
Missing Rate Limit for Current Password field (Password Change) Account Takeover

Steps to reproduce the bug:
1)Go to Profile > Password. Enter any (wrong password) In current password filed.
2)Now enter the new password and Turn the Intercept ON.
3)Capture the request & Send the request to Intruder and add a Payload Marker on the current password value.
4)Add the payload for the pa

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

Vulnerability:
Missing Rate Limit for Current Password field (Password Change) Account Takeover

Steps to reproduce the bug:
1)Go to Profile > Password. Enter any (wrong password) In current password filed.
2)Now enter the new password and Turn the Intercept ON.
3)Capture the request & Send the request to Intruder and add a Payload Marker on the current password value.
4)Add the payload for the password field having a list of more than 100 password or more for test and start attack.
BOOM!

Screen shot is attached as a proof of concept.

## Impact

There is no rate limit enabled for "Current Password" field on changing password on your website. A malicious minded user can continually tries to brute force an account password. If user forget to logout account in some public computer then attacker is able to know the correct password, and also able to change the password to new one by inputting large number of payloads.

</details>

---
*Analysed by Claude on 2026-05-24*
