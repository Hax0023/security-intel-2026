# Account Takeover via Unverified Email Change and Improper Session Handling

## Metadata
- **Source:** HackerOne
- **Report:** 3324823 | https://hackerone.com/reports/3324823
- **Submitted:** 2025-09-03
- **Reporter:** 0xoroot
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** high
- **Vuln:** Violation of Secure Design Principles
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Hi team,

During testing on ███
, I noticed an issue with session handling after changing the account email. When I update the email to an unregistered one, the system accepts it without proper verification. If the victim later registers on the website using that email, my existing session does not expire. Instead, I am able to access the victim’s newly created account data.

I also attempted to e

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

During testing on ███
, I noticed an issue with session handling after changing the account email. When I update the email to an unregistered one, the system accepts it without proper verification. If the victim later registers on the website using that email, my existing session does not expire. Instead, I am able to access the victim’s newly created account data.

I also attempted to end the session and log in again, but the system still redirected me into the victim’s account, indicating improper session invalidation and account takeover risk.

## Steps to Reproduce
##steps_Reproduce
1.Register a new account using Google authentication.
2.Change the account email to the victim’s email address (note: the victim’s email is not yet registered).
3.The victim registers on the website using that same email.
4.Observe that the attacker’s existing session is not expired, and the attacker now has access to the victim’s account data, even though the email is associated with the victim.
5.Log out from the attacker’s account.
6.Log in again with the attacker’s credentials.
7.You will notice that you are automatically logged into the victim’s account instead of your own, confirming account takeover.

##POC
█████████

## Impact

An attacker can fully take over any user account by exploiting weak email change and session handling logic. When the attacker changes their email to an unregistered victim email, the system does not verify ownership of that email nor invalidate active sessions. If the victim later registers with that email, the attacker’s session automatically maps to the victim’s account.

## System Host(s)
████




</details>

---
*Analysed by Claude on 2026-05-24*
