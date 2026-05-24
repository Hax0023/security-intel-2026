# Lengthy manual entry of 2FA secret (52-bit vs 16-bit code length)

## Metadata
- **Source:** HackerOne
- **Report:** 259415 | https://hackerone.com/reports/259415
- **Submitted:** 2017-08-13
- **Reporter:** goodhackonly
- **Program:** Legal Robot
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** User Experience Issue, Design Flaw, Usability Problem
- **CVEs:** None
- **Category:** business-logic

## Summary
The application requires users to manually enter a 52-bit code for 2FA authentication via Google Authenticator, which creates excessive friction and potential error rates compared to industry standard 16-bit codes. This usability issue may discourage users from adopting the 2FA feature, reducing overall security posture.

## Attack scenario
1. User attempts to enable 2FA on their account
2. System presents a 52-bit secret code for manual entry into Google Authenticator
3. User struggles with the lengthy code entry due to time constraints and high error probability
4. User either abandons 2FA setup or makes transcription errors requiring multiple retry attempts
5. Frustrated user disables or avoids using 2FA feature entirely
6. Account security is compromised as 2FA adoption drops across user base

## Root cause
Implementation decision to use 52-bit codes instead of the industry-standard 16-digit (approximately 53-bit equivalent but commonly expressed as 16 decimal digits) codes used in TOTP-based 2FA systems like Google Authenticator

## Attacker mindset
An attacker benefits from low 2FA adoption rates and user frustration, as it increases likelihood of accounts protected only by weak passwords. The lengthy code requirement naturally encourages users to skip 2FA entirely.

## Defensive takeaways
- Always prioritize usability when implementing security features to ensure adoption
- Follow industry standards for 2FA code length (typically 6-8 digit TOTP codes or 16-character base32 secrets)
- Conduct user testing and usability research before deploying security features
- Balance security requirements with practical user experience constraints
- Survey competitor implementations to understand user expectations and standards
- Consider that poor UX on security features reduces overall security by discouraging adoption

## Variant hunting
Check if other authentication methods have similarly poor UX that discourages usage
Review password reset flow for similar excessive complexity issues
Examine backup code generation and storage for usability problems
Analyze enrollment flow to identify other friction points in security feature adoption
Test if QR code scanning alternative is available to bypass manual entry

## MITRE ATT&CK


## Notes
This is a usability/UX issue rather than a traditional security vulnerability. The reporter demonstrates good security awareness by understanding that security features must be usable to be effective. The 52-bit reference appears to be the base32-encoded secret, while 16-digit refers to standard TOTP codes. The issue highlights the principle that security controls must balance protection with adoption - a feature users actively avoid provides zero protection.

## Full report
<details><summary>Expand</summary>

Hello @team,

I would like to report on some issue where users are going to face while 2FA authentication.We can see that users need to enter 52 bit code manually for 2FA authentication,which is taking a lot of time and it will be difficult for the user to enter the total 52 bits in the google authenticator app without mistakes.


why is this an issue?
we all know that our clients wont have that much  patience to enter such a lengthy code every time they want 2FA authentication .I've surveyed on other sites(paypa.com,stripe.com) who added the feature 2FA for their clients and Ive observed that users are requested to enter the 16 digit code manually so that it wont effect the time and probability for making mistakes in the google Authenticator. However attackers cannot bypass the  code or brute force because Legal robot took  necessary steps for this type of protection by implementing the web socket messages.

what is the best possible fix?
The best possible fix is to reduce the 52bit  "enter code manually code" to 16 bit.

why legal robot need this change?
--> 2FA authentication feature was newly added.If users using this feature  find this feature as a lot of time wastage they wont use this feature. As a result the impact might bring bad reputation to the entire legalrobot.

From my survey I have another image where other applications are providing 16 bit enter code manually code,which will be much easier for the users to enter in the google authenticator app.

Thanks!



</details>

---
*Analysed by Claude on 2026-05-24*
