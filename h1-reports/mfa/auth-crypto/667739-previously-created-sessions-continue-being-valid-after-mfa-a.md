# Previously created sessions continue being valid after MFA activation

## Metadata
- **Source:** HackerOne
- **Report:** 667739 | https://hackerone.com/reports/667739
- **Submitted:** 2019-08-05
- **Reporter:** brdoors3
- **Program:** Grammarly
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Session Management, Authentication Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
When a user activates two-factor authentication (2FA) on their account, existing sessions from other devices remain valid and authenticated without requiring 2FA verification. An attacker with access to a pre-2FA session can maintain indefinite account access even after the victim enables 2FA protection.

## Attack scenario
1. Attacker compromises user's password and logs in from device A
2. Attacker maintains this authenticated session without closing the browser
3. Legitimate user discovers the compromise and enables 2FA on their account via device B
4. Attacker on device A reloads the page or makes API requests with the existing session cookie
5. Attacker's session remains valid and authenticated, bypassing the newly activated 2FA requirement
6. Attacker maintains persistent access to the account despite 2FA being enabled

## Root cause
The application does not invalidate existing sessions when 2FA is activated. Session validation logic does not check for MFA requirement status at request time; instead, it only enforces MFA during initial login. Existing session tokens remain valid even after account security settings change.

## Attacker mindset
An attacker who has already obtained valid credentials or session tokens would want to maintain access even if the account owner discovers the breach and adds additional security layers. By keeping a pre-2FA session alive, the attacker can continue unauthorized access indefinitely without needing to provide 2FA codes.

## Defensive takeaways
- Invalidate all existing sessions when security-critical settings like MFA are modified
- Implement real-time session validation that checks current account security status on each request
- Force re-authentication with updated security requirements when MFA is activated
- Provide users with visibility into active sessions and allow bulk session termination
- Implement session binding to detect anomalous access patterns post-MFA activation
- Log all security setting changes and monitor for sessions continuing after such changes
- Consider reducing session lifetime significantly and implementing absolute timeout

## Variant hunting
Check if other security settings (password reset, email change, security keys) also fail to invalidate sessions
Test if downgrading from 2FA to single-factor auth invalidates sessions properly
Verify if API tokens and OAuth tokens are similarly invalidated during 2FA activation
Check if 2FA can be bypassed entirely through pre-existing sessions on mobile apps or desktop clients
Test whether session invalidation works across different authentication protocols (SAML, OAuth)
Examine if similar issues exist with IP-based access restrictions or device whitelisting features

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (login bypass)
- T1078 - Valid Accounts (maintaining unauthorized session access)
- T1056 - Input Capture (credential compromise leading to initial session)
- T1550 - Use Alternate Authentication Material (session token reuse)

## Notes
This is a classic session management flaw where security state changes are not reflected in active session validation logic. The vulnerability has significant real-world impact because it defeats the purpose of MFA as a recovery mechanism after credential compromise. OWASP would classify this under A07:2021 – Identification and Authentication Failures. The fix should be straightforward: maintain a session invalidation timestamp on the user account that is checked on every request, and increment it whenever security settings change.

## Full report
<details><summary>Expand</summary>

Hi team,

I found one issue related to your 2FA system on https://account.grammarly.com/security

POC

1 access the same account on https://account.grammarly.com in two devices
2 on device 'A' go to https://account.grammarly.com/security > complete all steps to activate the 2FA system

Now the 2FA is activated for this account

3 back to device 'B' reload the page

The session still active

## Impact

In this scenario when 2FA is activated the other sessions of the account are not invalidated.

2FA is required to login. I believe the expected and recommended behavior here is to terminate the other sessions> request a new login> request the 2FA code> so then give the account access again

</details>

---
*Analysed by Claude on 2026-05-24*
