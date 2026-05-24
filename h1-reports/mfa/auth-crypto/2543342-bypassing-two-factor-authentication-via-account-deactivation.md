# Bypassing Two-Factor Authentication via Account Deactivation and Password Reset

## Metadata
- **Source:** HackerOne
- **Report:** 2543342 | https://hackerone.com/reports/2543342
- **Submitted:** 2024-06-10
- **Reporter:** 011alsanosi
- **Program:** Unknown (HackerOne Report 2543342)
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Authentication Bypass, Two-Factor Authentication Bypass, Logical Flaw, Account Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A logical flaw in the account recovery process allows attackers to bypass 2FA by deactivating a target account and then resetting its password. After password reset, the compromised account can be accessed without 2FA verification, despite 2FA being enabled prior to deactivation. This effectively nullifies the second factor of authentication when an attacker has access to the victim's email.

## Attack scenario
1. Attacker gains access to victim's email account through phishing, credential stuffing, or other means
2. Attacker navigates to account settings and initiates account deactivation
3. Attacker proceeds to password reset functionality and resets the account password
4. Attacker uses new credentials to log into the previously 2FA-protected account
5. System fails to prompt for 2FA verification despite it being previously enabled
6. Attacker gains full account access and control

## Root cause
The application does not maintain 2FA enforcement state across account deactivation and recovery workflows. The password reset mechanism does not validate whether 2FA was enabled on the account prior to deactivation, and the deactivation process does not restrict password reset operations or require additional verification steps.

## Attacker mindset
An attacker with email access would recognize that account deactivation acts as a security bypass mechanism. They would leverage the logical disconnection between the deactivation workflow and 2FA state management to circumvent multi-factor authentication, which represents a common but often overlooked attack vector in account recovery scenarios.

## Defensive takeaways
- Maintain 2FA enforcement state throughout account lifecycle (including deactivated states)
- Require 2FA verification during password reset if 2FA was previously enabled
- Restrict or disable password reset functionality for deactivated accounts without explicit reactivation
- Implement additional email verification or challenge-response for sensitive operations on previously 2FA-protected accounts
- Add audit logging for deactivation and password reset events to detect suspicious patterns
- Consider rate limiting and anomaly detection on account recovery flows
- Require user confirmation or out-of-band verification before allowing password reset on deactivated accounts

## Variant hunting
Test if account suspension or lockout has similar bypass mechanisms
Check if 2FA bypass exists via account reactivation workflows
Investigate if other account recovery methods (security questions, backup codes) bypass 2FA
Test if email change/verification flows maintain 2FA enforcement
Examine if session management properly invalidates sessions during deactivation
Check for 2FA bypass during account migration or data export flows
Verify if API endpoints bypass 2FA checks that web UI enforces

## MITRE ATT&CK
- T1586 - Compromise Accounts
- T1589 - Gather Victim Identity Information
- T1606 - Forge Web Credentials
- T1110 - Brute Force
- T1548 - Abuse Elevation Control Mechanism
- T1556 - Modify Authentication Process

## Notes
This vulnerability demonstrates a critical gap in security design where different authentication workflows (deactivation, password reset, 2FA) are not properly integrated. The flaw is particularly severe because it affects users who have explicitly enabled 2FA, creating a false sense of security. The attack is also low-complexity, requiring only email access and no special tools. The vendor's recommended mitigations are sound and address the core architectural issue.

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
