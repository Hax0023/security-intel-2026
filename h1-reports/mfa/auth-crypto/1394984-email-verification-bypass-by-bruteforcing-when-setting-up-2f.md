# Email Verification Bypass via Brute Force During 2FA Setup

## Metadata
- **Source:** HackerOne
- **Report:** 1394984 | https://hackerone.com/reports/1394984
- **Submitted:** 2021-11-09
- **Reporter:** cyberworlcload
- **Program:** Evernote
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Brute Force Attack, Insufficient Input Validation, Weak Cryptography, Lack of Rate Limiting, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A 6-digit email verification code used during 2FA setup can be brute forced without rate limiting, allowing attackers to complete 2FA enrollment on accounts they don't own. An attacker can register with a victim's email address, enable 2FA via brute force, and permanently lock the victim out of account recovery.

## Attack scenario
1. Attacker registers an Evernote account using victim's email address (e.g., victim@gmail.com)
2. Attacker initiates 2FA setup process, triggering a 6-digit confirmation code sent to the email
3. Attacker intercepts the verification request and sends it to Burp Suite Intruder
4. Attacker performs brute force attack on the confirmationCode parameter, testing all 1,000,000 possible 6-digit combinations (000000-999999)
5. Attacker identifies correct code by observing response with significantly different length (~373 bytes vs others)
6. Attacker verifies email and binds their phone to the account, completing 2FA setup
7. Victim later attempts password reset or login, but cannot access account due to 2FA codes being sent to attacker's device, resulting in permanent account lockout

## Root cause
The application implements a 6-digit numeric verification code without adequate brute force protections. Missing or ineffective mitigations include: no rate limiting on verification attempts, no exponential backoff, no account lockout after failed attempts, predictable code generation, and no CAPTCHA or other challenge mechanisms.

## Attacker mindset
Attacker leverages weak secret entropy (6 digits = 1 million possibilities) combined with lack of API rate limiting to automate account compromise at scale. The attack targets high-value accounts by pre-emptively blocking victim access before they claim the account, effectively performing denial-of-service paired with account takeover.

## Defensive takeaways
- Implement strict rate limiting on email verification endpoints (max 3-5 attempts per 15 minutes per email/IP)
- Add exponential backoff or progressive delays after each failed attempt
- Lock account or require CAPTCHA after 5-10 failed verification attempts
- Increase verification code length to minimum 8-12 characters or use time-based OTP (TOTP)
- Implement account lockout notifications; alert user of 2FA setup attempts via secondary channel
- Require email verification before allowing 2FA setup on newly registered accounts
- Add server-side validation to prevent registering accounts with email addresses already in system
- Log and monitor unusual verification patterns (multiple rapid attempts from same IP/device)
- Consider requiring user confirmation email before 2FA activation becomes effective

## Variant hunting
Test other account recovery mechanisms (security questions, backup codes) for similar brute force vulnerabilities
Check if password reset codes are similarly vulnerable to brute force attacks
Test SMS-based 2FA for brute forceable OTP codes
Examine backup code generation for weak entropy
Test account registration email confirmation codes for same vulnerability
Check if rate limiting bypasses exist via IP rotation or header manipulation
Test if same brute force can be applied to other API endpoints with token/code validation

## MITRE ATT&CK
- T1110.001 - Brute Force: Password Guessing
- T1110.004 - Brute Force: Credential Stuffing
- T1190 - Exploit Public-Facing Application
- T1078.001 - Valid Accounts: Default Accounts
- T1556 - Modify Authentication Process
- T1556.006 - Modify Authentication Process: Multi-Factor Authentication

## Notes
This is a pre-account takeover scenario where the attacker doesn't gain access to legitimate victim credentials but blocks the victim from ever claiming their account. The vulnerability is critical because it combines weak secret generation (6 digits), absence of rate limiting, and account lockout mechanisms. The impact extends beyond single account compromise to potential widespread abuse targeting multiple email addresses. Report demonstrates effective vulnerability communication with reproducible steps and clear impact assessment.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello team, I hope you are fine and doing well

when a user set ups his 2 Factor Authentication in his account  and verify his email ,i was able to bruteforce the email verification process . 

The confirmationCode is used for authentication of user's email and it can be brute forced. The code is only 6 digits long ,so it will not take much time to crack . (https://cloudnine.com/wp-content/uploads/2020/02/CrackPassword2.png)

After the victim's email confirmation code gets verified , the user can then set up his personal phone to victim's email and the victim will never be able to sign inside his account as he does not get the otp received in the attakers phone.(due to 2 fa)

## Steps To Reproduce:

  1. Request a confirmationCode in your email , enter any code
  2. Send this request to burpsuite intruder , and bruteforce the confirmationCode with any number of requests
  3. Out of all the response , one response will have a length around 373 (only response whose length is lesser than others), thus proving that was the correct confirmation code.

*Attackers Scenario*:

Attacker creates a account using victim's email ABC@gmail.com , Now attacker setups the 2FA  using brute force . Victim wants to join evernote , so he resets his password but he is unable to join since he does not have the 2FA codes . Thus he user is permanently unable to access evernote . It is a pre account takeover .

## Impact

The victim who wants to log inside or use forget password to recover his/her account in evernote will be locked out forever. Attacker did a pre account takeover.

</details>

---
*Analysed by Claude on 2026-05-24*
