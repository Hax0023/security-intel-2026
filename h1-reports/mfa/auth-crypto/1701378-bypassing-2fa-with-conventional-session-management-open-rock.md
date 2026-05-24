# 2FA Bypass via Email Verification Link in Rocket.Chat

## Metadata
- **Source:** HackerOne
- **Report:** 1701378 | https://hackerone.com/reports/1701378
- **Submitted:** 2022-09-15
- **Reporter:** hackeriron1
- **Program:** open.rocket.chat
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Authentication Bypass, Two-Factor Authentication Bypass, Session Management Flaw, Insecure Direct Object References
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Rocket.Chat allows attackers to bypass two-factor authentication by leveraging the email verification link sent during email change requests. When users verify their new email address via the confirmation link, the system logs them in directly without requiring the 2FA code, completely circumventing the security mechanism. This vulnerability exists because the email confirmation flow lacks proper 2FA enforcement at the authentication checkpoint.

## Attack scenario
1. Attacker obtains target user's email address through reconnaissance or social engineering
2. Attacker registers an account on the Rocket.Chat instance and enables 2FA on their own account to understand the workflow
3. Attacker initiates a password reset or account recovery targeting the victim's email address
4. Victim receives email verification link and clicks it (attacker monitors for or intercepts this)
5. System authenticates user based on email link without requiring 2FA credential
6. Attacker gains full session access to victim's account, completely bypassing 2FA

## Root cause
The email verification endpoint implements a separate authentication path that does not enforce or validate 2FA requirements before establishing a user session. The developers implemented email confirmation as a privileged action but failed to chain it with the existing 2FA security controls, creating a parallel authentication mechanism that bypasses the 2FA gate.

## Attacker mindset
Attackers recognize that multi-factor authentication is often implemented as a conditional check after initial password verification, but frequently email-based confirmation flows are treated as alternative trusted channels that skip downstream security checks. This is a common architectural flaw where developers trust email possession as sufficient proof of identity without considering account takeover scenarios where attackers have email access.

## Defensive takeaways
- Always enforce 2FA checks at session establishment regardless of authentication method used (password, email link, social login, etc.)
- Implement a unified authentication state machine where all pathways converge at a single 2FA enforcement point before session creation
- Email verification links should only verify email ownership; they should not automatically establish authenticated sessions
- Use time-limited, single-use tokens for email verification that require additional authentication before account access
- Log and alert on email change requests and verification completions as these are account takeover indicators
- Implement anomaly detection for logins via email verification when 2FA is enabled
- Require re-authentication or 2FA code entry when changing critical account attributes like email address

## Variant hunting
Search for similar bypasses in: password reset flows, email confirmation links, social login integrations, account recovery mechanisms, phone number verification paths, and any alternative authentication channels that may skip the 2FA enforcement point. Check if OAuth integrations or API token generation bypass 2FA. Examine whether email-based passwordless login (if available) also bypasses 2FA. Test session upgrade mechanisms that may not properly enforce MFA.

## MITRE ATT&CK
- T1190
- T1078
- T1556
- T1110
- T1621

## Notes
This vulnerability is particularly impactful because it requires no sophisticated attack - simply valid email access to the target account. The reporter correctly identified this as a conventional session management flaw similar to Instagram's password reset bypass. The vulnerability assumes attacker has access to victim's email, making it effective against accounts where email is not properly secured. The fix should involve re-validation of 2FA status before any session establishment, not just during initial login.

## Full report
<details><summary>Expand</summary>

**Summary:**
Hii Team,

I have found a vulnerability in open.rocket.chat and I able to bypass 2FA by Email confirmation link.
In this case, attackers use the email confirmation link because, often, 2FA is not implemented on the system’s login page after a email confirmation.

## Releases Affected:

https://open.rocket.chat

## Steps To Reproduce:

Attack scenario :
1). Sign up with email.
2). add 2FA.
3). Go to account change email  (Email verification will be sent to victim email).
4). Attacker able to login with email verification link without 2FA code.

## Supporting Material/References:
same vulnerability was in Instagram but via password reset.
https://infosecwriteups.com/how-i-couldve-bypassed-the-2fa-security-of-instagram-once-again-43c05cc9b755

## Suggested mitigation
Do not direct login after email confirmed. 

##POC Video
███

I hope you will understand 
If you need more info, I will provide you.

## Impact

Using this method, attackers can bypass the two-factor authentication in open.rocket.chat where the architecture of the site or platform makes it possible.

</details>

---
*Analysed by Claude on 2026-05-24*
