# Broken Authentication in Mobile Verification - Unverified Phone Number Used for Password Reset

## Metadata
- **Source:** HackerOne
- **Report:** 33432 | https://hackerone.com/reports/33432
- **Submitted:** 2014-10-31
- **Reporter:** geekboy
- **Program:** Twitter
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Authentication, Account Takeover, Insufficient Input Validation, Session Management Flaw
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Twitter's mobile verification flow associates unverified phone numbers with user accounts, allowing them to be used for password reset before verification is completed. An attacker can add an arbitrary phone number during account setup and immediately use it in password reset flows, potentially leading to account takeover if they control that number.

## Attack scenario
1. Attacker logs into victim's Twitter account (or creates new account)
2. Attacker navigates to mobile verification section and enters attacker-controlled phone number
3. Twitter sends verification code to that number but attacker closes the verification dialog without completing it
4. Attacker logs out of the compromised account
5. On forgot password page, attacker enters victim's email/username
6. System offers password reset via the unverified phone number, allowing attacker to intercept the code and reset password

## Root cause
The application associates a phone number with the account during the initial verification request phase rather than only after successful verification completion. The password reset mechanism trusts incomplete verification records without checking completion status.

## Attacker mindset
Account takeover through indirect authentication bypass. Rather than brute-forcing credentials, exploit the weakest link in the multi-factor authentication chain: associating unverified contact methods with recovery mechanisms.

## Defensive takeaways
- Only associate phone numbers with accounts AFTER successful verification code validation
- Maintain explicit verification status flags and check them before allowing use in sensitive flows (password reset, security keys)
- Implement timeout windows for pending verifications
- Log and monitor password reset attempts using unverified recovery methods
- Require re-verification of recovery methods periodically or after suspicious activity
- Show users which recovery methods are verified vs pending during account recovery flows

## Variant hunting
Check email verification flows, backup code generation, two-factor authentication setup, security question associations, and any recovery mechanism that allows unverified contact methods to be used. Test if users can immediately use partially-completed multi-factor setup in account recovery scenarios.

## MITRE ATT&CK
- T1190
- T1621
- T1078

## Notes
This is a chain vulnerability: incomplete input validation + improper session state management + lack of verification status checks. The severity depends on whether attackers need account access first (lower) or can target victims directly via password reset (higher). The report demonstrates good proof-of-concept methodology by showing the actual flow that exposes the vulnerability.

## Full report
<details><summary>Expand</summary>

Hey Team
this is geekboy :)

this report is about broken authentication in mobile section .

Description : 
when user want to add any mobile number to his account , he will go mobile section and twitter will ask the user to select the country and enter the mobile number .

so when testing i entered the random mobile number and twitter says that verification code sent to the mobile number , and asking for the verification code >> http://sd.uploads.im/NsmJl.png

i cant provide the code coz i entered the random number .

now i logged out my account and came to forget password page .

the issue is here , twitter asking me to send the verification code on the mobile number which i didn't verified and  its not associated with my account .  >> http://sd.uploads.im/LRUhA.png

so without verification Twitter should not associate the mobile number with account for the password reset purpose ! 

Thanks
geekboy :) 

</details>

---
*Analysed by Claude on 2026-05-24*
