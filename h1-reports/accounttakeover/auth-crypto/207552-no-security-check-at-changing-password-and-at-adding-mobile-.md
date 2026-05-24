# No Security check at changing password and at adding mobile number which leads to account takeover and spam

## Metadata
- **Source:** HackerOne
- **Report:** 207552 | https://hackerone.com/reports/207552
- **Submitted:** 2017-02-19
- **Reporter:** mohith_kalyan
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
#Description

I have noticed that there is no security check at changing password. If someone gets a logged in account for 5 seconds, they are extremely likely to change the password of the account with the knowledge of the victim. also, while adding a mobile number / changing a mobile number, there is no sms / call verification which leads to spamming of any user using Khan Academy as source.

Si

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

#Description

I have noticed that there is no security check at changing password. If someone gets a logged in account for 5 seconds, they are extremely likely to change the password of the account with the knowledge of the victim. also, while adding a mobile number / changing a mobile number, there is no sms / call verification which leads to spamming of any user using Khan Academy as source.

Since there is no sms verification, I could spam anyone (not necessarily khan academy user) with khan Academy notifications.


#Steps to reproduce

1. Click on the name of the profile on top right.
2. Select settings in the drop down menu.
3.  Change the password by just entering the new password, without knowing anything.
4.  Add the mobile number (if already entered, change ) of your choice, since there is no security check, they will be spammed by khan academy messages.


#Impact

Lack of security check at password change leaves a vulnerability open to attackers to change the password without knowing anything about the user.
Lack of verification of mobile while adding / changing mobile number leaves every mobile user open for spamming via Khan Academy.


#Screen shots/ References

███
F162091


</details>

---
*Analysed by Claude on 2026-05-24*
