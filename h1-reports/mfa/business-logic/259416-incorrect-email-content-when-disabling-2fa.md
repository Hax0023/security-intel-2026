# Incorrect Email Content When Disabling 2FA - False Statement About Security Key Registration

## Metadata
- **Source:** HackerOne
- **Report:** 259416 | https://hackerone.com/reports/259416
- **Submitted:** 2017-08-13
- **Reporter:** goodhackonly
- **Program:** LegalRobot
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Information Disclosure, Logic Error, Misleading Security Communication
- **CVEs:** None
- **Category:** business-logic

## Summary
When users disable 2FA authentication via authenticator app, they receive an email notification containing a false statement claiming '2-Factor Authentication is still enabled since you registered a security key' even when no security key was ever registered. This misleading communication undermines user trust and creates confusion about their actual security posture.

## Attack scenario
1. Attacker creates a new LegalRobot account and enables 2FA using the authenticator app
2. Attacker deliberately does not register any FIDO U2F security key
3. Attacker disables the 2FA authenticator app registration through account settings
4. Attacker receives notification email stating '2-Factor Authentication is still enabled since you registered a security key'
5. Attacker verifies via account settings that no security key was ever registered, confirming the false statement
6. Attacker documents the discrepancy between actual security configuration and email notification content

## Root cause
The email template for 2FA disabling events contains a conditional statement that displays a message about security key registration without properly verifying whether the user actually has a registered security key. The logic appears to assume a security key exists when generating the email, rather than checking the user's actual security configuration before populating the message.

## Attacker mindset
A conscientious security researcher identifying a logic flaw in transactional email content generation that could erode user trust through misleading security communications. This researcher is focused on improving the application's reliability and user experience rather than exploiting a vulnerability.

## Defensive takeaways
- Implement server-side validation to verify user's actual security configuration (registered authenticators, security keys) before generating transactional emails
- Create conditional email templates that only display relevant security statements based on verified user configuration
- Add comprehensive testing for all 2FA-related email notifications across different user configuration scenarios
- Implement logging and monitoring for email template rendering to catch mismatches between user state and email content
- Establish a review process for all security-related communications to prevent misleading statements
- Consider adding a visual representation of current security settings in emails to reduce confusion

## Variant hunting
Check email notifications for other 2FA events (enabling, recovery, etc.) for similar false statements
Test 2FA emails across different authentication method combinations (authenticator app + security key, authenticator app only, security key only)
Review other transactional emails that reference user security configuration
Examine backup code generation/destruction email notifications for similar logic errors
Test concurrent 2FA modifications to see if race conditions cause incorrect email generation

## MITRE ATT&CK
- T1589 - Gather Victim Identity Information
- T1598 - Phishing

## Notes
This is a low-severity logic error in security-related communication rather than a direct security vulnerability. However, it has reputational impact as it erodes user trust in the platform's security claims. The issue demonstrates the importance of validating user state before generating transactional emails, especially those related to security features. Video proof-of-concept was provided by the researcher.

## Full report
<details><summary>Expand</summary>

Hello @team,

I found that there is false statement in the 2FA disabled mails sent by the legalrobot.

what is the issue?
When user is disabling the 2fa authenticator app Registration.He will get a notification regarding the Disabling of the 2FA .the mail structure is like this:
**
2FA disabled

The 2FA Authenticator App registration was just removed from your Legal Robot (TEST) account. 2-Factor Authentication is still enabled since you registered a security key.

**


but the user haven't registered any security key.

steps to reproduce:
1.Create a new account.
2.login to your account and enable the 2FA authentication.
3.dont make any changed to the FIDO U2F Security Key .
4.disable the 2FA Authenticator App registration.
5.now you will receive mail from legalrobot updating about the 2FA disabled.
6.but still you can find the statement " 2-Factor Authentication is still enabled since you registered a security key."

This will create confusion among the users and the trust will break.

Kindly find the attached video poc for better understanding.

Thanks!



</details>

---
*Analysed by Claude on 2026-05-24*
