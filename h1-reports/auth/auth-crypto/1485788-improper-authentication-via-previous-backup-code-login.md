# Improper Authentication via previous backup code login

## Metadata
- **Source:** HackerOne
- **Report:** 1485788 | https://hackerone.com/reports/1485788
- **Submitted:** 2022-02-19
- **Reporter:** fuzzsqlb0f
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
HI Basecamp,

I would like to report Improper Authentication in basecamp. Attacker is able to login at victim account once victim update his password.


attacker knows with victims email `█████████` password `uhn)(*123HH`
victim updates his password          `uhn)(*123HHjcc`

Step To Reproduce

==Attacker==

- Step1 attacker know victim password and logs in

- Step2 attacker enables 2fa in victims

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

HI Basecamp,

I would like to report Improper Authentication in basecamp. Attacker is able to login at victim account once victim update his password.


attacker knows with victims email `█████████` password `uhn)(*123HH`
victim updates his password          `uhn)(*123HHjcc`

Step To Reproduce

==Attacker==

- Step1 attacker know victim password and logs in

- Step2 attacker enables 2fa in victims account.

- Step3 attacker logs out and login back in victim account, 2fa will be prompter, attacker gaves 2fa backup code and send request to repeater and captures the response.
██████

- Step4 attacker now removes 2fa from victim account and logout.


==Victim==

- Step5 victim logs in and `changes password.` from `uhn)(*123HH`to  `uhn)(*123HHjcc`

==Attacker==

- Step6 attacker logins in `victim account` with ==previous known password== and changes ==Step6 response with  Step3 response.==

- Attacker logged in victims account even he dose not know new password of victim.



Video POC attached for your reference.
████


Thanks,
@fuzzsqlb0f

## Impact

Improper Authentication.

</details>

---
*Analysed by Claude on 2026-05-24*
