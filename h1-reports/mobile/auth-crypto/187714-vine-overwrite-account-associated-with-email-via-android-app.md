# Vine - Account Takeover via Email Case Sensitivity Bypass on Android

## Metadata
- **Source:** HackerOne
- **Report:** 187714 | https://hackerone.com/reports/187714
- **Submitted:** 2016-12-02
- **Reporter:** mishre
- **Program:** Vine
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Account Takeover, Authentication Bypass, Email Validation Flaw, Case Sensitivity Handling Error
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Vine Android application fails to properly normalize email addresses during account creation and authentication, allowing attackers to create multiple accounts with the same email using different letter cases. This vulnerability enables denial of service to legitimate users and unauthorized access by overwriting the password associated with an email address.

## Attack scenario
1. Attacker identifies target user's email address (e.g., victim@gmail.com)
2. Attacker creates legitimate first account using victim@gmail.com with attacker-controlled password
3. Attacker creates second account using Victim@gmail.com (with capital V) and a different attacker-controlled password
4. System accepts both registrations, linking the second account to the same email but overwriting authentication credentials
5. Legitimate user attempts to login with original password and email, but fails due to password override
6. Attacker successfully logs in with the email and second password, effectively taking over the account

## Root cause
The backend authentication system treats email addresses as case-sensitive during account creation and password storage, while the login mechanism likely performs case-insensitive email lookup. This mismatch allows multiple accounts to be created for the same email address with different cases, and the last registration overwrites the password hash associated with that email in the database.

## Attacker mindset
An attacker would recognize this as a low-effort attack requiring only knowledge of a target's email address. The attacker gains account control without brute force or phishing, making it an attractive vector for mass account hijacking or competitive sabotage.

## Defensive takeaways
- Implement strict email normalization on both client and server side - convert all emails to lowercase before any database operations
- Add unique constraints on normalized email addresses at the database level to prevent duplicate accounts
- Validate email format and case-sensitivity consistently across registration, login, and password reset flows
- Implement email verification requirements before account activation to detect unauthorized registrations
- Add anomaly detection for multiple account creation attempts with email variants
- Log authentication failures and suspicious account creation patterns for security monitoring
- Implement rate limiting on account creation from single IP addresses
- Require user confirmation via email before allowing password changes or account overwrites

## Variant hunting
Check if similar case-sensitivity issues exist in username handling
Test password reset flow with email variants - does it reset the correct account?
Verify if account recovery/account linking features have the same vulnerability
Test API endpoints directly (bypass Android app) for email normalization bypass
Check if email+tag formats (victim+tag@gmail.com) are normalized consistently
Investigate if international domain names (IDN) have similar normalization issues
Test if the web version of Vine has the same vulnerability
Check if two-factor authentication setup is vulnerable to this email variant attack

## MITRE ATT&CK
- T1190
- T1078
- T1098
- T1021

## Notes
The reporter correctly notes this is technically not a full account takeover in the traditional sense - the legitimate user's original account becomes inaccessible, but the attacker gains a new account. However, the practical impact is identical to account takeover from the victim's perspective. The vulnerability likely exists due to lack of input validation/normalization - a common flaw when developers overlook email case-sensitivity standards (RFC 5321 states the local part is case-sensitive but most systems treat it as case-insensitive for UX).

## Full report
<details><summary>Expand</summary>

Hi,

It's possible to deny any user from logging in to his account by overwriting the password associated with his email. This is not an account takeover because while we do override the password associated with that specific mail we just login to a "new" account and not the user's original one.

Steps to reproduce:
===
1) Create first account via Vine for android with the mail firstaccountmail@gmail.com with the password Bla123
2) You can now see that you can login to the account created above.
3) Go and create another account - this time with a different password and with the mail Firstaccountmail@gmail.com - notice the CAPS (you can put the caps everywhere on the mail).
4) Finish the creation process - and see that it succeeds
5) Now go back and try to login with firstaccountmail@gmail.com and the password Bla123 and see that you can't. However, it's possible to login with firstaccountmail@gmail.com and the second password you have created - but you"ll login to the second created account.

</details>

---
*Analysed by Claude on 2026-05-24*
