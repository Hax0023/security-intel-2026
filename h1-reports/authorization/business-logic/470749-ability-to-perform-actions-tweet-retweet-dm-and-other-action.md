# Unauthenticated Account Takeover via SMS Commands - Twitter

## Metadata
- **Source:** HackerOne
- **Report:** 470749 | https://hackerone.com/reports/470749
- **Submitted:** 2018-12-21
- **Reporter:** antisocial_eng
- **Program:** Twitter/HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Authentication, Insufficient Input Validation, SMS Spoofing, Account Takeover, Privilege Escalation
- **CVEs:** None
- **Category:** business-logic

## Summary
An attacker who knows or guesses a target's phone number associated with a Twitter account can perform unauthorized actions (tweets, retweets, DMs, 2FA removal) by sending SMS commands to Twitter's short codes without authentication. The vulnerability exploits Twitter's SMS command interface which lacks proper phone number verification, allowing unauthenticated control of account functions.

## Attack scenario
1. Attacker obtains or guesses target's phone number associated with Twitter account
2. Attacker spoofs the target's phone number using SIM swapping, VOIP service, or carrier vulnerability
3. Attacker sends SMS commands to Twitter's regional short code (e.g., 40404 for US) with commands like 'TWEET [message]'
4. Twitter's SMS gateway processes the command without verifying sender identity, only validating the phone number
5. Attacker successfully posts tweets, sends DMs, or disables 2FA from the target account
6. Attacker maintains persistence by removing SMS 2FA, enabling account takeover without password knowledge

## Root cause
Twitter's SMS command interface relies solely on phone number validation without implementing proper authentication mechanisms such as: (1) rate limiting per number, (2) verification challenges before sensitive actions, (3) device fingerprinting, (4) confirmation mechanisms for high-risk operations, or (5) detection of spoofed SMS origins

## Attacker mindset
Opportunistic threat actor exploiting a gap between SMS trust assumptions and actual security. The attacker demonstrates systematic exploration of SMS functionality to find unauthenticated command execution, recognizing that SMS is treated as a trusted channel without verifying the actual device holding the SIM. Motivation ranges from mass account compromise for botnets to targeted attacks on high-profile accounts.

## Defensive takeaways
- Never treat SMS as a primary authentication factor without additional verification - implement out-of-band authentication via authenticator apps
- Require explicit user confirmation (via app notification or secondary method) before executing sensitive SMS commands
- Implement strict rate limiting on SMS-based commands tied to account identity, not just phone number
- Add device fingerprinting and behavioral analysis to detect anomalous SMS command patterns
- Maintain audit logs of all SMS-initiated actions and alert users to unusual activity
- Use SMPP/carrier-level protections to validate SMS sender identity and detect spoofing
- Disable SMS commands for 2FA management entirely; require in-app or email verification
- Implement time-window restrictions or cooldown periods between sensitive operations via SMS

## Variant hunting
Look for similar SMS command vulnerabilities in: (1) Other social media platforms with SMS features (WhatsApp, Telegram, Signal), (2) Banking/financial institutions using SMS for transaction approval, (3) Email providers with SMS recovery options, (4) Two-factor authentication systems trusting SMS without device verification, (5) IoT platforms using SMS for device control, (6) Telecom carrier services themselves that enable number spoofing without verification

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1621
- T1104
- T1078
- T1098

## Notes
Report demonstrates critical flaw in treating SMS as secure channel for account control without authentication. The scale of impact is enormous: individual targeting, bulk spam/reporting campaigns, celebrity account compromise, and removal of security controls. Twitter's SMS infrastructure appears to have been designed for convenience over security. The reporter's proof-of-concept tweet sent from friend's account provides concrete evidence. This vulnerability likely affected millions of Twitter users with SMS enabled. Modern understanding treats SMS as inherently insecure for authentication; this case shows it's equally dangerous for command execution without proper controls.

## Full report
<details><summary>Expand</summary>

**Summary:** By knowing the mobile phone number associated with a Twitter account, or by using random mobile phone numbers! It is possible to perform the following actions against a target without their knowledge or interaction. With no account takeover scenario.

It's a case of, if I know the mobile number... I can control basic functions of the account.

I can do everything that is listed here: https://help.twitter.com/en/using-twitter/sms-commands on an account, completely unauthenticated.


## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. Spoof target number, send an SMS to a special short code for the geographical location, as seen here: https://help.twitter.com/en/using-twitter/supported-mobile-carriers


## Impact: Massive. I can remove the SMS two factor of the account. I can DM people without them knowing. If I had the mobile number of Donald Trump, I could send Tweets as him... There is so much wrong here. 

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)

https://twitter.com/___Sh4rk___/status/1076204152546619392 this is a tweet I sent from my close friends account. She did not reveal her password or authenticate it at all.

## Impact

Remove 2FA

Tweet on someones behalf.

DM Someone.

Delete someones tweets

Turn off all phone SMS notifications

Follow people

Unfollow people.

Block/Report people - with a little script I could get 10000 phone numbers all reporting innocent tweets. Controlling media etc

More stuff really.

</details>

---
*Analysed by Claude on 2026-05-24*
