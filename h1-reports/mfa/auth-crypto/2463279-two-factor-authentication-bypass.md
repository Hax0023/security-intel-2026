# Two Factor Authentication Bypass via Account Deactivation and Password Reset

## Metadata
- **Source:** HackerOne
- **Report:** 2463279 | https://hackerone.com/reports/2463279
- **Submitted:** 2024-04-15
- **Reporter:** pranshux0x_
- **Program:** HackerOne
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Authentication Bypass, Two Factor Authentication Bypass, Account Takeover, Improper State Management
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker with access to a victim's email address can bypass two-factor authentication by exploiting a flaw in HackerOne's account deactivation logic. When a deactivated account's password is reset and the account is reactivated, the 2FA protection is completely removed, allowing unauthorized access.

## Attack scenario
1. Attacker obtains victim's email address through phishing, data breach, or social engineering
2. Attacker initiates password reset on HackerOne using the victim's email address
3. Attacker sets a new password for the victim account via the email reset link
4. Attacker logs into the account with the new password
5. System fails to restore or verify 2FA status during account reactivation
6. Attacker gains full account access without providing any 2FA code

## Root cause
The application does not properly restore or maintain two-factor authentication settings when an account transitions from deactivated to reactivated state. The password reset mechanism does not validate or re-enable MFA, creating a security gap that allows bypassing the second authentication factor entirely.

## Attacker mindset
An attacker would recognize that account deactivation creates a state management weakness. They would test whether security controls like 2FA persist through account lifecycle transitions, particularly during password resets. The attacker exploits the assumption that 2FA would remain active and instead discovers it's removed during reactivation.

## Defensive takeaways
- Implement mandatory 2FA re-verification when accounts are reactivated or password resets occur
- Maintain 2FA settings independently from account active/inactive state
- Require users to explicitly confirm 2FA recovery codes or reconfigure MFA after account deactivation/reactivation
- Add security alerts and verification steps during password reset flows when 2FA is enabled
- Audit all account state transitions to ensure security controls remain enforced
- Implement rate limiting and additional verification on password reset endpoints
- Log and monitor account deactivation/reactivation patterns for suspicious activity

## Variant hunting
Test if 2FA bypass occurs with other account suspension/freeze mechanisms
Verify if disabling then re-enabling 2FA manually triggers the same vulnerability
Check if session invalidation occurs properly during account reactivation
Test password reset flows for other applications that support 2FA to identify similar patterns
Investigate if other security settings (IP whitelisting, device trust) persist through deactivation
Probe for race conditions between deactivation and password reset operations

## MITRE ATT&CK
- T1078.001
- T1199
- T1556
- T1621

## Notes
This vulnerability requires prior email compromise, making it a compound attack requiring initial access. The high severity rating is justified due to complete 2FA bypass on a security-focused platform. The vulnerability reflects improper handling of security control state across account lifecycle events. The writeup lacks specific timeline, patch details, and bounty amount information.

## Full report
<details><summary>Expand</summary>

**Summary:**

Two factor authentication bypass means. We have access to victim email and password. But we don't have access to 2fa code. So somehow we have to bypass 2fa code requirement.
so what I do here.
I had access to victim email that is used in his hackerone account. 
Victim also deactivate his account
I find out that when  user deactivate his account. Then reset his password and login again ,  2fa removed. 

**Description:**

### Steps To Reproduce

#### As a victim
- Login to your hackerone account
- Turn on your two factor authentication. 
- Deactivate your account

#### As an attacker
- You have access to victim email
- Forgot victim password on hackerone, because you have access to victim email you can do this easily.
- Now login with new password on hackerone , you will see 2fa removed completely.

## Impact

Impact is quite high two factor authentication bypass.

</details>

---
*Analysed by Claude on 2026-05-24*
