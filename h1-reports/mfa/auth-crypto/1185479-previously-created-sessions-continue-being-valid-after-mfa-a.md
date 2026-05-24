# Previously created sessions continue being valid after MFA activation

## Metadata
- **Source:** HackerOne
- **Report:** 1185479 | https://hackerone.com/reports/1185479
- **Submitted:** 2021-05-06
- **Reporter:** benjamin-mauss
- **Program:** cs.money
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Session Management, Broken Authentication, Insufficient Session Invalidation, MFA Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
After activating MFA/2FA on an account, previously authenticated sessions on other devices remain valid and active without requiring re-authentication with the newly enabled MFA. An attacker with an active session before MFA activation can continue accessing the account indefinitely without providing MFA credentials.

## Attack scenario
1. Attacker gains access to target's account (via credential compromise, phishing, etc.) and establishes a session on a device
2. Target user discovers the compromise and activates MFA/2FA as a security measure
3. Attacker's pre-MFA session remains active on their device
4. Attacker reloads the page or makes subsequent requests with the existing session cookie
5. Application continues to honor the old session without requiring MFA verification
6. Attacker maintains unauthorized account access despite MFA activation

## Root cause
The application fails to invalidate existing sessions when MFA is activated. Session tokens created before MFA enablement are not revoked, allowing them to bypass the newly enforced MFA requirement. The authentication validation logic does not check MFA status against session creation timestamp or does not force re-authentication after MFA changes.

## Attacker mindset
An attacker who has compromised credentials and established a session would perform reconnaissance to detect security changes (like MFA activation). Recognizing that MFA was enabled, the attacker would verify if their existing session persists rather than being terminated. This represents a low-effort, high-impact attack as no additional compromises are needed once initial access is obtained.

## Defensive takeaways
- Implement mandatory session invalidation whenever MFA/2FA is activated or modified
- Force all existing sessions to terminate and require complete re-authentication with MFA after MFA settings change
- Add session metadata tracking (MFA status at session creation time) to enforce consistency checks
- Implement session revocation lists or timestamps to invalidate sessions created before security policy changes
- Log all authentication state changes and cross-reference against active sessions
- Require MFA challenge on sensitive account modifications, not just at login
- Implement server-side session termination rather than relying solely on client-side token expiration
- Consider implementing 'session freshness' checks where MFA-protected accounts require re-verification of active sessions periodically

## Variant hunting
Check if other authentication mechanisms (password reset, email change, security questions) also fail to invalidate sessions
Test if enabling/disabling 2FA multiple times creates inconsistent session states
Verify if security keys or hardware tokens have the same issue
Check if removing MFA also fails to terminate sessions, allowing potential downgrade attacks
Test if account lockout or suspicious activity detection properly terminates sessions
Examine if OAuth token refreshes bypass MFA requirements on session refresh
Test cross-device session synchronization after any account security change

## MITRE ATT&CK
- T1190
- T1539
- T1556
- T1098

## Notes
This is a duplicate/related issue (#667739), indicating the vulnerability persisted after a previous report. Session management flaws are particularly critical in authentication contexts as they represent a complete bypass of newly activated security controls. The vulnerability is especially dangerous because users activate MFA specifically to prevent unauthorized access, yet the old sessions render MFA ineffective.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi, team.
This is the same issue of #667739. Please take a look.

I found one issue related to your 2FA system on https://cs.money/security/

## Steps To Reproduce:

1. access the same account on https://cs.money/ in two devices
1. on device 'A' go to https://cs.money/security/ > complete all steps to activate the 2FA system
1. Now the 2FA is activated for this account
1. back to device 'B' reload the page
1. The session still active

## Impact

In this scenario when 2FA is activated the other sessions of the account are not invalidated.
2FA is required to login. I believe the expected and recommended behavior here is to terminate the other sessions> request a new login> request the 2FA code> so then give the account access again

</details>

---
*Analysed by Claude on 2026-05-24*
