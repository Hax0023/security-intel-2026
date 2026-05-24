# Bypassing Two-Factor Authentication via Account Deactivation and Password Reset

## Metadata
- **Source:** HackerOne
- **Report:** 2543342 | https://hackerone.com/reports/2543342
- **Submitted:** 2024-06-10
- **Reporter:** 011alsanosi
- **Program:** Unknown
- **Bounty:** Not disclosed
- **Severity:** none
- **Vuln:** Improper Access Control - Generic
- **CVEs:** None
- **Category:** auth-crypto

## Summary
**Summary:**

The vulnerability arises from a logical flaw in the account recovery and 2FA enforcement processes. Specifically, after deactivating an account, users can reset their password and log in without being prompted for 2FA. The 2FA mechanism, which is designed to provide an additional layer of security, is effectively bypassed.

### Steps To Reproduce

1. Go to settings enable 2fa and cli

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

**Summary:**

The vulnerability arises from a logical flaw in the account recovery and 2FA enforcement processes. Specifically, after deactivating an account, users can reset their password and log in without being prompted for 2FA. The 2FA mechanism, which is designed to provide an additional layer of security, is effectively bypassed.

### Steps To Reproduce

1. Go to settings enable 2fa and click on Deactivation
2. After Deactivation your account go to reset password and reset your password 
3. After change your password you can notice access account without 2fa

*poc*
███
### Recommendations

Disable Password Resets for Deactivated Accounts: Ensure that deactivated accounts cannot reset their passwords without reactivating.
	•	Enforce 2FA During Password Reset: Require 2FA verification as part of the password reset process.

## Impact

Attackers with access to a user’s email can deactivate the account and reset the password, gaining full access without passing 2FA.

</details>

---
*Analysed by Claude on 2026-05-24*
