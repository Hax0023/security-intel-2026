# Ability to Disable Shopify Owner Login for 24 Hours via 2FA Phone Number Enumeration and Rate Limit Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1406495 | https://hackerone.com/reports/1406495
- **Submitted:** 2021-11-21
- **Reporter:** saurabhsankhwar3
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Rate Limit Bypass, Account Enumeration, Denial of Service (Account Lockout), Insecure 2FA Implementation, Insufficient Input Validation, Privilege Escalation (via 2FA manipulation)
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can intercept and modify 2FA setup requests to associate a victim's phone number with their own account, then repeatedly request OTP codes to trigger rate limiting, preventing the legitimate victim from logging in for 24 hours. This zero-click attack exploits insufficient validation during 2FA enrollment and inadequate rate limiting on code generation.

## Attack scenario
1. Attacker creates a new Shopify account with a disposable email
2. Attacker initiates 2FA setup via mobile phone and captures the request in Burp Suite
3. Attacker intercepts the request and modifies the phone number field to the victim's phone number (obtained through enumeration or social engineering)
4. Attacker forwards the modified request, successfully enrolling victim's phone number to attacker's account
5. Attacker repeatedly clicks 'RESEND CODE' button to trigger OTP generation, exhausting rate limits on the server
6. When victim attempts to login and is prompted for 2FA code, the server is rate-limited and cannot send OTP, effectively locking out the victim for 24 hours

## Root cause
Multiple security flaws in combination: (1) Insufficient validation that phone number ownership is confirmed before 2FA enrollment, (2) No rate limiting or inadequate rate limiting on OTP code generation/resend requests, (3) Shared rate limit pool between attacker and victim rather than per-user limits, (4) No verification that requesting party owns the phone number being enrolled

## Attacker mindset
Opportunistic malicious actor seeking to disable competitor accounts, harass targets, or cause account unavailability without sophisticated tools or authentication. The zero-click nature appealed to widespread exploitation potential.

## Defensive takeaways
- Implement strict rate limiting on 2FA code generation and resend requests (e.g., max 3 attempts per 15 minutes per phone number)
- Require phone number ownership verification (confirmation code sent to phone) before allowing enrollment in 2FA
- Validate that the user requesting 2FA enrollment is modifying their own account, not another user's
- Use per-user and per-phone-number rate limiting rather than global limits
- Implement progressive delays and temporary account lockouts after repeated failed 2FA attempts
- Monitor for suspicious patterns (multiple 2FA setup changes, rapid resend requests from different accounts)
- Add CSRF tokens to 2FA setup forms to prevent request interception attacks
- Implement account recovery mechanisms that don't depend solely on the compromised 2FA method

## Variant hunting
Similar rate limit bypass on password reset OTP flows
Phone number enumeration across Shopify user base
2FA bypass via SIM swapping combined with rate limit exhaustion
Email-based 2FA using identical attack vector (modify email, spam resend)
Authentication state confusion allowing modification of other user's 2FA settings
Race condition in 2FA enrollment confirmation workflow

## MITRE ATT&CK
- T1078 - Valid Accounts (account lockout of victim)
- T1190 - Exploit Public-Facing Application (2FA logic exploitation)
- T1110 - Brute Force (OTP/rate limit attack)
- T1589 - Gather Victim Identity Information (phone number enumeration)
- T1499 - Endpoint Denial of Service (account availability impact)

## Notes
Report quality is poor with significant redactions and vague explanations, making full technical assessment difficult. Video evidence is redacted. The core vulnerability chain (request modification + rate limit bypass) is sound but the report lacks clarity on whether the phone number was enumerated or obtained through other means. The 24-hour lockout duration suggests aggressive rate limiting triggers. No response or remediation timeline from Shopify provided in report excerpt.

## Full report
<details><summary>Expand</summary>

Hello Team,

I Found a Bug in which Hacker Have Ability to Disable the Login Attempt of any Shopify Owner With (Zero_Click)

Summary:
----------


Proof of Concept;
-------------------

Credentials:
-------------
Victim = ███████.com (████████)

Hacker = █████████.com 

Victim Sceanrio:
-----------------
Step 1 : Victim Login to his Account (████.com)

Step 2 : For Better Security of his Account ---------> Victim Activate the 2 Factor Authentcation ( Via Mobile Phone Number)

Step 3 : 2 FA Activated Successfully -----------> Victim Logout

Attacker Scanario: (Incognito Tab)
------------------
Step 1 : Hacker Make a New Account  in shopify (███████.com)

Step 2 : Hacker Go to Manage Account -------> Choose to Activate 2 FA 

Step 3 : Hacker Enter his Mobile Number (█████████) --------> Capture the Request in Burpsuite

Step 4 : Hacker Change the Mobile Number (████) to (███████) --------> Forward the Request

Step 5 : Hacker Logout -------> Login again

Step 6 : Now Hacker Tap Multiple times in "RESEND CODE " --------> untill Server Reflect Stop
████████

Step 7 : Now Hacker Stop Finally


Victim Sceanrio: (Again)
------------------------

Step 1 : Victim Want to Login to his Shopify Account

Step 2 : Victim Enter Email and Password --------> Server Redirect to 2 FA page

Step 3 : Here Victim See So many OTP Code But Recent Code Still Not Arrive --------> Victim Click Resend But Server Block the Attempt

As a Result Victim not Allowed to Login to his Account

Zero_Click Vulnerbaility that Will Impact many Shopify Users Who Use Mobile Number as a method of 2 FA Verification


POC Video:
-----------
████


Please Let me Know if You have any doubt

Thank You

Regards~
saurabhsankhwar3

## Impact

1. In Real World Attacker Perform a BruteForce Attack on 2 FA page (infinite Time) --------> So that Server Not able to send correct OTP to Real Victim

2. There is Improper Security While Setting 2 FA via Mobile Phone

3. Hacker try to Disable Login Attempt of any Shopify owner just By Knowing Which Mobile Number He/She used For Enabling 2 FA in his Account

4 . Violation of Security Design Priciple

</details>

---
*Analysed by Claude on 2026-05-24*
