# Enable 2FA without verifying the email

## Metadata
- **Source:** HackerOne
- **Report:** 3016540 | https://hackerone.com/reports/3016540
- **Submitted:** 2025-02-27
- **Reporter:** samtime
- **Program:** xvideos.com
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Broken Authentication, Insufficient Email Verification, Unauthorized 2FA Enablement, Account Takeover, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
xvideos.com allows registration with unverified email addresses and permits 2FA enablement without email verification, enabling attackers to lock legitimate users out of accounts using their email addresses. An attacker can register an account with a victim's email and activate 2FA, rendering the account inaccessible even if the victim tries to recover it, resulting in permanent account lock-out.

## Attack scenario
1. Attacker identifies target victim email address for attack
2. Attacker registers new xvideos.com account using victim's email without requiring email verification
3. Attacker navigates to account security settings while email remains unverified
4. Attacker enables Two-Step Verification (2FA) using Google Authenticator
5. Victim attempts to login or recover account but cannot due to active 2FA on unverified account
6. Victim is permanently locked out; password reset insufficient due to 2FA requirement

## Root cause
The application fails to enforce email verification as a prerequisite for critical account security features (2FA enablement). The registration flow accepts unverified emails, and security settings are accessible before email confirmation, creating a gap in the authentication chain.

## Attacker mindset
An attacker would target this vulnerability to perform account hijacking or deny service to specific users. The motivation could be competitive sabotage, harassment, or systematic account lockouts. Low effort required with high impact against victims.

## Defensive takeaways
- Enforce email verification as mandatory before account activation
- Require email verification completion before accessing critical security settings
- Implement additional confirmation steps for 2FA enablement (send verification code to email)
- Add rate limiting on account registration per email address
- Implement account lockout detection and alerts when 2FA is enabled on new accounts
- Require recent email verification proof before any security setting changes
- Add admin override mechanisms and account recovery procedures for locked accounts

## Variant hunting
Check if other security-critical features (API keys, payment methods, email forwarding) can be configured without email verification
Verify if password reset tokens are sent to unverified emails, allowing attackers to lock accounts
Test if 2FA can be disabled without email verification on recovery codes
Examine if backup authentication methods can be added without email verification
Investigate if account username/email can be changed before verification

## MITRE ATT&CK
- T1190
- T1110
- T1098
- T1531
- T1556

## Notes
This vulnerability has a direct reference to a prior similar report (ID 1618021), indicating a pattern of insufficient email verification controls. The impact is amplified by the irreversible nature of 2FA activation on unverified accounts. The attack requires no authentication bypass or technical exploitation, making it particularly dangerous due to its simplicity and broad applicability.

## Full report
<details><summary>Expand</summary>

A vulnerability in xvideos.com allows an attacker to register using victim email addresses which are unverified. This can be further exploited to enable two-factor authentication (2FA), permanently locking the victim out of their own email account. This results in a denial-of-service attack against the legitimate email owner.

Steps to Reproduce:
Go to: https://www.xvideos.com/
Then, navigate to join for free and create an account using victim email address
After that, Navigate to: https://www.xvideos.com/account/security
Select "Two-step verification" and enable it using the Google Authenticator app.

 Reference

https://hackerone.com/reports/1618021

## Impact

The victim can't register an account with their email. If the victim reset the password, the password will change, but the victim can't login because of 2FA which was enabled by attacker leading to denial-of-service against the legitimate email owner.

</details>

---
*Analysed by Claude on 2026-05-24*
