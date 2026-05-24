# 2FA Bypass via Email Change Allows User Impersonation

## Metadata
- **Source:** HackerOne
- **Report:** 2885636 | https://hackerone.com/reports/2885636
- **Submitted:** 2024-12-06
- **Reporter:** d3do
- **Program:** Drugs.com
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Authentication Bypass, Session Management Flaw, Logic Error in 2FA, Email Verification Bypass, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An attacker can impersonate legitimate users by exploiting a logic flaw that allows email changes without terminating existing sessions or re-validating 2FA. By changing an account's email to a victim's address and leveraging the 'Trust this device' feature, an attacker gains persistent access to an account for up to 30 days without triggering OTP challenges. The vulnerability persists because the platform fails to invalidate sessions or require 2FA re-verification when email ownership changes.

## Attack scenario
1. Attacker registers an account with their own email address on drugs.com
2. Attacker completes OTP verification and selects 'Trust this device for 1 month', creating a 30-day 2FA-exempt session
3. Attacker navigates to account details and changes the email to the target victim's email address without re-validating ownership
4. The existing session remains valid and is now associated with the victim's email, allowing login without 2FA prompts
5. Attacker optionally repeats the process (change email back to their own, re-verify with 'Trust device', change to victim's email) to extend access indefinitely
6. Legitimate victim cannot register with their own email as the system reports it already exists, and the attacker maintains account access until victim resets password

## Root cause
The platform implements insufficient validation when email addresses change: (1) sessions are not invalidated after email modification, (2) 2FA trust tokens ('Trust this device') persist across email ownership changes, (3) no re-verification of email ownership is required during the change process, and (4) no logout of other sessions occurs when email is modified.

## Attacker mindset
An attacker would target this vulnerability to gain persistent, low-friction access to victim accounts without requiring continuous 2FA bypass. The 30-day trust window provides extended impersonation capability, and the ability to refresh the trust token indefinitely allows long-term account compromise. The attacker exploits the platform's assumption that email changes are legitimate modifications by the account owner.

## Defensive takeaways
- Always invalidate all active sessions when email address is changed
- Require re-verification of 2FA (OTP challenge) after any email modification before allowing further actions
- Never allow 'Trust this device' tokens or session exemptions to persist across email ownership changes
- Implement email change confirmation via the OLD email address before applying the change
- Send immediate notifications to both old and new email addresses when email changes occur, and allow reversal within a time window
- Verify that the NEW email address is actually owned by the requester before completing the change
- Implement rate limiting on email change operations
- Audit session-to-email mappings and terminate any inconsistencies automatically
- Consider requiring full 2FA re-authentication (not just OTP, but also password) for sensitive changes like email address

## Variant hunting
Test if phone number changes bypass 2FA in similar ways
Test if payment method additions bypass 2FA verification
Test if security questions/recovery options can be changed without session invalidation
Test if account recovery mechanisms allow email takeover without victim verification
Test if other 'Trust this device' features persist across account modifications
Test if two-factor authentication methods can be disabled while under 'trusted device' status
Test if account merging/linking features validate email ownership properly
Test if social login connections can be changed without re-verification

## MITRE ATT&CK
- T1190
- T1586
- T1078
- T1556
- T1098
- T1566

## Notes
This is a critical authentication bypass with high exploitability and severe impact. The vulnerability chains multiple weaknesses: insufficient session management, weak email verification, and persistent trust tokens. The fact that victims cannot even reclaim their email addresses until they discover the unauthorized account and reset the password is particularly severe. The vendor's notification approach (notifying attacker instead of terminating session) suggests a fundamental misunderstanding of security best practices. This vulnerability likely affects a significant user population and should be patched with urgency.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello team,
I have discovered a logic flaw in the authentication system that allows an attacker (User A) to impersonate a legitimate user (User B) who has not yet registered. By abusing the email change functionality and bypassing 2FA, the attacker can retain access to the account until the legitimate user resets their password.

## Steps to re-produce
1. Go to https://www.drugs.com/account/register/ and create an account using an email you own.

██████

2. Complete OTP verification and select "Trust this device for 1 month". This gives you a valid session that does not require 2FA for one month.

3. Go to https://www.drugs.com/account/details/ and change the email to the victim's email (User B)
   - Now, the attacker has a valid session associated with User B's email for one month, bypassing 2FA.

███

4. Log out and log back in to confirm that the application doesn't prompt for OTP.

### To maintain this bypass indefinitely (until the original user resets the password):
1. Change the email back to the attacker's email.

2. Re-verify the new email by completing OTP verification and selecting "Trust this device for 1 month".
3. Change the email back to the victim's email (or any other arbitrary email).

By repeating this process, the attacker can retain access without triggering 2FA.
Note that the platform only notifying the attacker to activate the account , but not Terminating the session after the email has changed successfully 

## From victim POV
1. Go to Sign Up page 
2. try to Sign up with the victim's email
3. Note that  the platform says that email's already used (while the original Owner of the email didn't  create the account) 

███████

## Impact

## Summary:

1. ** Loss of Trust:** Users will lose confidence in the platform's security if they learn attackers had  impersonated them.

2. **Impersonation Risk:** Attackers can impersonate legitimate users and interact with the platform.

3. **Email Ownership Not Protected:** The platform fails to verify the original owner of the email, allowing attackers to use it.

</details>

---
*Analysed by Claude on 2026-05-24*
