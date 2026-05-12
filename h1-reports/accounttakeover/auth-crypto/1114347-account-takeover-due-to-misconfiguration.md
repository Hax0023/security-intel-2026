# Account Takeover via Email Verification Token Not Invalidated After Address Change

## Metadata
- **Source:** HackerOne
- **Report:** 1114347 | https://hackerone.com/reports/1114347
- **Submitted:** 2021-03-02
- **Reporter:** akashhamal0x01
- **Program:** Unknown (HackerOne Report 1114347)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Authentication, Token Management Flaw, Logic Error, Insufficient Token Invalidation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A user can change their email address during the verification process of a previous email change, but the original verification token remains active and can be exploited by an attacker who has access to the initial email. An attacker who receives the old verification link can complete the verification and take over the account even after the user has successfully verified a new email address.

## Attack scenario
1. Victim changes their email to attacker@gmail.com (accidentally or intentionally)
2. System sends verification link to attacker@gmail.com
3. Attacker gains access to attacker@gmail.com (through compromise or misconfiguration)
4. Victim realizes the mistake and changes email to victim999@gmail.com, then verifies it
5. System confirms victim999@gmail.com as the current email address
6. Attacker clicks the old verification link sent to attacker@gmail.com, successfully taking over the account

## Root cause
The application fails to invalidate previous email verification tokens when a user initiates a new email change request or successfully verifies a different email address. The token remains valid indefinitely, allowing anyone with access to the old email address to claim ownership of the account at any point in the future.

## Attacker mindset
An opportunistic attacker monitoring compromised or typo-squatted email addresses could leverage this flaw to take over accounts. The attacker would simply wait for users to make mistakes when changing email addresses and then use the valid tokens sent to these addresses to compromise accounts.

## Defensive takeaways
- Invalidate all pending email verification tokens immediately when a user initiates a new email change request
- Invalidate all pending email verification tokens when the user successfully verifies a new email address
- Implement token expiration times (15-30 minutes maximum)
- Maintain a record of which email address a token is associated with and validate that on redemption
- Send cancellation notifications when email change is initiated to warn users of potential security issues
- Require re-authentication before initiating major account changes like email address modification
- Implement rate limiting on email change requests to detect abuse patterns

## Variant hunting
Check if password reset tokens suffer from the same invalidation issue
Test if other identity-linked changes (phone number, backup email) have similar flaws
Verify if changing email address invalidates session tokens
Check if the same token can be used multiple times to re-verify the same address
Test whether tokens from different users can be mixed/swapped in verification URLs
Investigate if changing account recovery options invalidates pending verification requests

## MITRE ATT&CK
- T1586.003
- T1621
- T1110

## Notes
This is a classic token lifecycle management vulnerability. The severity is High rather than Critical because it requires either user error (mistyping email) or attacker control of a specific email address. The vulnerability demonstrates that token invalidation must occur at multiple points: (1) when a new request of the same type is initiated, (2) when the related account state significantly changes, and (3) after a maximum time-to-live expires. This type of flaw is common in applications that don't properly implement token state machines.

## Full report
<details><summary>Expand</summary>

## Summary:

HI team, i hope you are good :)

Its a very simple logical flaw that results in this

So suppose we are victim@gmail.com , now login into the website then

1. go to account settings and then change mail address to victim111@gmail.com
2. a link will be sent to victim111@gmail.com, now the user realizes that he have lost access to victim111@gmail.com due to some reasons 
3. so he will probably change mail to the another mail address for e.g victim999@gmail.com which he owns and has access to
4. but it is found that even after verifying victim999@gmail.com, the old link which was sent to victim111@gmail.com is active, so user/attacker having access to that mail can verify it and takeover acc


In a nutshell : 

It is mandatory for a web app to invalidate the tokens in time to secure its user 

In this case, suppose while changing mail address the user mistakenly typed wrong mail address, so the link will be sent to that mail address. 

So the user probably don't want the user of that mail address to verify it, so he will quickly change his mail address to one he owns and verify it

what he doesn't know is that even after verification(change of major state), the old link is still active 

the flaw :

user changes mail to attacker@gmail.com -> user realizes that he mistyped the mail -> so he again changes to mail he owns and verifies it -> old link sent to attacker@gmail.com is still active even after new mail has been verified

## Impact

An attacker can takeover acc due to misconfiguration, not invalidation of tokens at major state change, in time

</details>

---
*Analysed by Claude on 2026-05-11*
