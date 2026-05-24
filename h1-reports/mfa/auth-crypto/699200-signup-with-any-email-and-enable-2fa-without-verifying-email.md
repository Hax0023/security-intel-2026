# Account Takeover via Email Signup Without Verification and 2FA Enablement

## Metadata
- **Source:** HackerOne
- **Report:** 699200 | https://hackerone.com/reports/699200
- **Submitted:** 2019-09-21
- **Reporter:** rioncool22
- **Program:** Omise
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Authentication, Email Verification Bypass, Account Takeover (ATO), Two-Factor Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can register an account using any email address without email verification and immediately enable two-factor authentication. This allows the attacker to claim ownership of an email address and permanently lock out the legitimate email owner from registering and accessing the account, even if they attempt password recovery.

## Attack scenario
1. Attacker identifies target victim's email address
2. Attacker creates new account on dashboard.omise.co using victim's email without completing email verification
3. Attacker navigates to Two-Factor Authentication settings
4. Attacker enables 2FA on the unverified account (linking authenticator/phone)
5. Legitimate victim attempts to register with their own email and is denied due to email already in use
6. Victim initiates password reset to regain access, but cannot login as 2FA is already active on attacker's session

## Root cause
The application enforces email verification and 2FA setup sequentially rather than as prerequisites. The registration flow allows users to fully configure 2FA before email ownership is validated, and the system does not invalidate or restrict access until email verification is complete.

## Attacker mindset
An attacker seeks to perform account enumeration and hijacking by claiming high-value email addresses before legitimate owners. By enabling 2FA immediately, they create a persistent barrier preventing the legitimate owner from password recovery and account takeover, effectively creating a denial-of-service condition.

## Defensive takeaways
- Require email verification before granting access to security-sensitive features like 2FA enrollment
- Implement email verification as a mandatory prerequisite during signup, blocking further action until validated
- Send verification confirmation emails immediately upon signup and monitor for abuse patterns (multiple signups from same IP)
- Require re-verification of email changes or 2FA modifications with a confirmation token
- Implement account lockout detection: flag accounts where 2FA is active but email is unverified
- During password reset, require email verification step before allowing authentication bypass
- Add post-reset email confirmation requirement even if 2FA is present

## Variant hunting
Check if password reset works without email verification when 2FA is enabled
Test whether backup codes can be generated before email verification
Verify if email change is possible without confirming original email
Attempt to register, enable 2FA, then modify email address without re-verification
Test if disabling 2FA requires email confirmation
Check if API endpoints bypass email verification checks that UI enforces
Test race conditions: simultaneously submit email verification and 2FA enable requests

## MITRE ATT&CK
- T1190
- T1078.001
- T1098.001
- T1556.005

## Notes
This is a critical authentication bypass that enables account takeover and denial of service to legitimate users. The vulnerability is straightforward to exploit and has immediate impact on availability and confidentiality. The 2FA mechanism, intended as a security control, becomes a weapon in the attacker's hands by being enabled before email validation. This suggests inadequate security architecture where access controls are applied too late in the workflow.

## Full report
<details><summary>Expand</summary>

##Description :
When i signup, i can enable 2FA without verification my email.

##Attack Scenario : 
1. The Attacker signup with the victim email.
2. Go to `Two factor authetication` and enable 2FA

## Impact

when the victim want to register in this [site](https://dashboard.omise.co/),  they can't, because they email claims by attacker.
and if the victim reset the password to get back the email, he can, but he can't login because need 2FA code.

</details>

---
*Analysed by Claude on 2026-05-24*
