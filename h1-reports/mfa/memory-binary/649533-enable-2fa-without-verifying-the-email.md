# Enable 2FA without Email Verification

## Metadata
- **Source:** HackerOne
- **Report:** 649533 | https://hackerone.com/reports/649533
- **Submitted:** 2019-07-18
- **Reporter:** rioncool22
- **Program:** Unknown (H1 Report #649533)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Broken Authentication, Insufficient Access Controls, Account Takeover
- **CVEs:** None
- **Category:** memory-binary

## Summary
An attacker can register an account using a victim's email address and enable 2FA without completing email verification, effectively locking the victim out of their own account. This allows the attacker to prevent legitimate account registration and bypass password reset attempts through the enabled 2FA.

## Attack scenario
1. Attacker registers a new account using victim's email address
2. Email verification link is sent to victim's email, but attacker proceeds without clicking it
3. Attacker logs in successfully despite unverified email status
4. Attacker navigates to account settings and enables 2FA
5. Victim attempts to register with their own email - fails due to existing account
6. Victim initiates password reset; even if successful, cannot login due to 2FA requirement

## Root cause
Insufficient validation of email verification before allowing critical account modifications like 2FA enrollment. The application does not enforce email verification as a prerequisite for enabling 2FA or allows authentication prior to verification completion.

## Attacker mindset
Account enumeration and denial of service through account lock-out. Attacker exploits the gap between account creation and email verification to permanently deny legitimate user access to their email-associated account.

## Defensive takeaways
- Enforce mandatory email verification before any account operations are permitted
- Require email verification as a prerequisite for enabling 2FA
- Implement email verification checks at login and security setting modification points
- Add alerts when 2FA is enabled from unverified accounts
- Implement account claim/recovery mechanisms for email ownership disputes
- Rate-limit account registration attempts from similar patterns

## Variant hunting
Check if other security features (password recovery options, backup codes) bypass email verification
Test if verified flag can be manually bypassed via API parameters
Verify if session token generation occurs before email verification
Look for race conditions between verification email sending and login allowance
Test adding alternative authentication methods without verification

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1496
- T1589

## Notes
Critical account takeover vector that completely denies legitimate user access. The severity is heightened because password resets become ineffective when 2FA is already enabled on a hijacked account. This demonstrates why email verification must be a gating control for sensitive operations.

## Full report
<details><summary>Expand</summary>

# Description : 
I able to add 2FA to my account without verifying my email

# Attack scenario : 
1. Attacker sign up with victim email (Email verification will be sent to victim email).
2. Attacker able to login without verifying email.
3. Attacker add 2FA.

## Impact

the victim can't register an account with victim email. If the victim reset the password, the password will change, but the victim can't login because 2FA.

</details>

---
*Analysed by Claude on 2026-05-24*
