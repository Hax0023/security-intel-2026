# 2FA Activation Code Reuse Allows Unauthorized Login

## Metadata
- **Source:** HackerOne
- **Report:** 695041 | https://hackerone.com/reports/695041
- **Submitted:** 2019-09-15
- **Reporter:** shadow-m
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Code Reuse, Broken Authentication, Insufficient Token Expiration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A critical authentication flaw in Shopify's 2FA activation process allows an attacker to reuse the SMS verification code sent during 2FA setup to authenticate subsequent login attempts. This enables unauthorized account access if an attacker obtains the activation code, completely bypassing the intended second factor of authentication.

## Attack scenario
1. Attacker intercepts or socially engineers the victim to reveal the SMS 2FA activation code (e.g., phishing, SIM swap, or by compromising the phone)
2. Attacker obtains the victim's email/username and password through credential stuffing or phishing
3. Attacker navigates to Shopify login page and enters the victim's credentials
4. System prompts for 2FA verification code
5. Attacker enters the previously obtained 2FA activation code instead of generating a new one
6. System incorrectly validates the reused code and grants login access without requiring a fresh verification

## Root cause
The authentication system fails to invalidate 2FA activation codes after initial use. The same code generation/validation mechanism is used for both activation and login verification without enforcing single-use token semantics or time-based expiration windows that differ between activation and login contexts.

## Attacker mindset
An attacker who has obtained a victim's 2FA activation code (through interception, social engineering, or account compromise during setup) realizes this code remains valid indefinitely for login purposes, enabling persistent unauthorized access even after the victim secures their password.

## Defensive takeaways
- Implement strict single-use-only semantics for all authentication codes with server-side state tracking
- Use separate code generation mechanisms for account setup vs. authentication flows
- Enforce short expiration windows (5-10 minutes) on all OTP/verification codes
- Invalidate activation codes immediately after successful 2FA setup completion
- Log and alert on code reuse attempts as potential security incidents
- Implement rate limiting on failed verification attempts per account
- Add cryptographic binding between codes and their intended use (activation vs. login)

## Variant hunting
Test if other setup codes (password reset, email verification) can be reused for authentication
Check if backup codes generated during 2FA setup can be reused multiple times
Verify whether codes from one account can be used on another account
Test if activation codes work after 2FA is disabled and re-enabled
Examine if SMS and authenticator app codes have the same reuse vulnerability
Check if recovery codes bypass the same verification logic

## MITRE ATT&CK
- T1110.4
- T1621
- T1556
- T1078.001

## Notes
This vulnerability is particularly dangerous because: (1) 2FA is a security control, so compromising it defeats layered defense, (2) attackers may obtain activation codes during the setup window when users are less vigilant, (3) the reusability is unlimited and time-independent, allowing exploitation weeks or months later. The fix is relatively straightforward from an implementation perspective but requires careful token lifecycle management.

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
