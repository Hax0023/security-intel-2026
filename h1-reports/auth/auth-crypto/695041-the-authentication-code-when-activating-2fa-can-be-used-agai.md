# The authentication code when activating 2FA can be used again to log in

## Metadata
- **Source:** HackerOne
- **Report:** 695041 | https://hackerone.com/reports/695041
- **Submitted:** 2019-09-15
- **Reporter:** shadow-m
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** low
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi team,
Summary:
======================
I noticed that when activating 2FA by sms, you can also use that 2FA activation code, to use as an authentication code when logging in.
Steps:
=========================
1, Go to: https://accounts.shopify.com/accounts/36430415/security and log in
2, Activate 2FA by sms for the account and save the code sent in your phone
3, Log out and perform login again
4,

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

Hi team,
Summary:
======================
I noticed that when activating 2FA by sms, you can also use that 2FA activation code, to use as an authentication code when logging in.
Steps:
=========================
1, Go to: https://accounts.shopify.com/accounts/36430415/security and log in
2, Activate 2FA by sms for the account and save the code sent in your phone
3, Log out and perform login again
4, After entering the password and being asked to enter the verification code, you only need to replay the code used to activate the previous 2FA.
5, Logged in successfully.

## Impact

Assuming the hacker knows the authentication code when activating the victim's 2FA, he can reuse the victim's code to replay and log in successfully without the victim knowing.

Recommend:
============
Each authentication code should only be used once.

Best regards,
john

</details>

---
*Analysed by Claude on 2026-05-24*
