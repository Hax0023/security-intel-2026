# Session Persistence After 2FA Enablement Allows Unauthorized Password Changes

## Metadata
- **Source:** HackerOne
- **Report:** 2234736 | https://hackerone.com/reports/2234736
- **Submitted:** 2023-11-01
- **Reporter:** 0xchoudhary
- **Program:** Side Effects Software (sidefx.com)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Session Management, Broken Authentication, Two-Factor Authentication Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
When a user enables 2FA on their account, existing authenticated sessions are not terminated, allowing an attacker with access to another session to modify the account password without providing 2FA credentials. This defeats the security purpose of 2FA by allowing unauthorized account modifications through stale sessions.

## Attack scenario
1. Attacker gains access to one active session of a target account (via theft, phishing, or shared device)
2. Target user enables 2FA on their account in a different browser/session
3. Server processes 2FA activation but fails to invalidate other existing sessions
4. Attacker's old session remains valid and authenticated
5. Attacker navigates to profile/settings and initiates password change request
6. Password change succeeds without 2FA verification, completely compromising the account and locking out the legitimate user

## Root cause
The application does not implement session invalidation logic when critical security features like 2FA are enabled. The 2FA enablement endpoint likely only updates user settings without executing a server-side session termination for all existing sessions except the one making the change.

## Attacker mindset
An attacker with one compromised session can leverage the victim's own security-conscious behavior (enabling 2FA) to escalate the attack by changing passwords before 2FA takes full effect, essentially using the security feature against the user.

## Defensive takeaways
- Implement mandatory session invalidation for all existing sessions when 2FA is enabled
- Require full re-authentication (including new 2FA code) before allowing sensitive operations like password changes after 2FA activation
- Maintain a 'session generation counter' or timestamp that invalidates all sessions issued before 2FA enablement
- Add explicit logout confirmation prompts when users enable 2FA, warning them about automatic session termination
- Log and monitor suspicious password changes that occur shortly after 2FA enablement without proper 2FA verification
- Implement stricter authentication requirements for account modification operations

## Variant hunting
Check if other security-critical settings (email change, API keys, recovery codes) have the same session persistence issue
Test if disabling 2FA properly invalidates sessions or has the inverse vulnerability
Verify if account recovery flows re-validate sessions appropriately
Check if adding trusted devices/locations implements proper session termination
Test if password reset emails properly invalidate all sessions

## MITRE ATT&CK
- T1190
- T1078
- T1021
- T1556
- T1098

## Notes
This vulnerability combines broken authentication with improper session management, creating a critical flaw in the 2FA implementation. The severity is elevated because it allows an attacker with lateral access to completely hijack an account, and the legitimate user's security-conscious action (enabling 2FA) directly enables the attack. This is a fundamental design flaw rather than an implementation oversight.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi team,
I found one issue related to your 2FA system on https://sidefx.com
## Steps To Reproduce:
Login to the Same account in 2 different browser
Now on 1st browser go to https://sidefx.com/profile and complete the all steps of 2fa and Enable it | 2FA activated
Now go to another session or 2nd browser and reload the page.
The account doesn't logout session is still alive.
and now change the password on 2nd browser (which doesn't have 2fa enabled) 
BOOM!

## Impact

In this scenario when 2FA is activated the other sessions of the account are not invalidated.
2FA is required to login. I believe the expected and recommended behavior here is to terminate the other sessions> request a new login> request the 2FA code> so then give the account access again

</details>

---
*Analysed by Claude on 2026-05-24*
