# Password Reset Link not expiring after changing the email Leads To Account Takeover

## Metadata
- **Source:** HackerOne
- **Report:** 685007 | https://hackerone.com/reports/685007
- **Submitted:** 2019-08-30
- **Reporter:** alishah
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** medium
- **Vuln:** Improper Authentication - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
###Vulnerability:
Password Reset Link not expiring after changing the email

###Proof Of Concept:

1.Send the password reset link to your email.
2.Don`t open the password link just copy it and paste into any editor.
3.Open your account.
4.Go to your account settings.
5.Under account, you will see Account Overview.
6.Go to the Email and password Option and change the email and verify it.
7.After ch

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

###Vulnerability:
Password Reset Link not expiring after changing the email

###Proof Of Concept:

1.Send the password reset link to your email.
2.Don`t open the password link just copy it and paste into any editor.
3.Open your account.
4.Go to your account settings.
5.Under account, you will see Account Overview.
6.Go to the Email and password Option and change the email and verify it.
7.After changing the email go to your password reset link which you copied.
8.Change your password.


BooM password Changed.

#####Thanks

## Impact

The attacker can still change the password if victim thinks his/her account is compromised and decided to change his/her email.

</details>

---
*Analysed by Claude on 2026-05-24*
