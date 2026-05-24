# Email Validation Bypass in Mobile App Sign-up Process

## Metadata
- **Source:** HackerOne
- **Report:** 57764 | https://hackerone.com/reports/57764
- **Submitted:** 2015-04-22
- **Reporter:** kaleemgiet
- **Program:** Unknown (HackerOne Report #57764)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Broken Authentication, Insufficient Input Validation, Business Logic Flaw, Account Takeover
- **CVEs:** None
- **Category:** uncategorised

## Summary
The mobile application fails to enforce email verification during the sign-up process, allowing attackers to bypass validation by simply clicking the back button and logging in without confirming their email address. This enables account creation without legitimate email ownership verification, facilitating account spoofing and fraudulent registrations.

## Attack scenario
1. Attacker initiates sign-up process with arbitrary email address and password on mobile app
2. Application presents email verification confirmation screen after registration
3. Attacker presses back button to navigate away from verification screen
4. Application returns user to login screen without enforcing verification completion
5. Attacker logs in using credentials from step 1, bypassing email confirmation entirely
6. Attacker gains full account access without ever receiving or confirming the verification email

## Root cause
The application lacks server-side enforcement of email verification status before granting login access. Authentication logic does not validate that the email_verified flag or equivalent has been set to true. The back button navigation allows users to exit the verification flow and return to login without completing the required verification step.

## Attacker mindset
Attackers recognize that the verification workflow is purely client-side or weakly enforced on the backend. By circumventing the UI flow, they can create accounts with unverified email addresses, enabling account farming, credential stuffing with spoofed addresses, and potential account enumeration attacks.

## Defensive takeaways
- Implement server-side enforcement: verify email_verified status before allowing login, regardless of client-side flow
- Set account state to 'unverified' and block all authentication attempts until email link is clicked
- Implement rate limiting and CAPTCHA on registration to prevent mass account creation
- Track failed verification attempts and enforce cooldown periods for repeated bypass attempts
- Log and alert on authentication attempts from unverified accounts
- Require email verification completion before granting any API access or session tokens
- Implement email confirmation token with expiration and single-use validation
- Add security headers to prevent navigation bypass and enforce strict state management

## Variant hunting
Check if other authentication flows (password reset, account recovery) have similar back-button bypasses
Test if direct API calls to /login endpoint bypass verification checks
Verify if manipulating HTTP requests (removing verification headers/parameters) allows login
Test if session tokens are issued before email verification is complete
Check if unverified accounts can access protected resources or API endpoints
Test rapid logout/login cycles to exploit race conditions in verification logic
Verify email verification state persists correctly across app restarts

## MITRE ATT&CK
- T1190
- T1578
- T1098
- T1021

## Notes
This is a critical business logic flaw that completely nullifies email verification security controls. The vulnerability suggests weak backend validation and over-reliance on client-side UI enforcement. The reporter's tone suggests frustration with response time on previous submissions. This vulnerability affects user trust, enables spam/phishing campaigns using legitimate-appearing accounts, and may violate compliance requirements (GDPR, CCPA) for account ownership verification.

## Full report
<details><summary>Expand</summary>

Hi,

According to the design When the new user sign up using mobile apps(android,ios).It will ask for the confirmation of the email.It will send a confirmation mail to mail id and a screen will also appear in the mobile app. The user needs to open the email in the device then the screen will Off and user will successfully login.

Bypass:

Here simply we can bypass this validation and can successfully login to the application without verifying the validation email which comes to the user.Using this the attacker can create so many spoofed accounts.

1.Sign for new user using email id and password
2.Next screen will appear saying please click on the validation which sent to proceed further
3.Here in the second screen click the back button now you will go to Login screen
4.Now login with the creds which you have given in the registration process
5.Now you will successfully login to the application
6.Here it is not asking for email verification email.

Pls follow above procedure to reproduce the issue.

Pls respond to remaining bugs which I had reported 

Thanks,
kaleem

</details>

---
*Analysed by Claude on 2026-05-24*
