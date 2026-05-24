# Authentication Bypassing and Sensitive Information Disclosure in Email Verification Flow

## Metadata
- **Source:** HackerOne
- **Report:** 124151 | https://hackerone.com/reports/124151
- **Submitted:** 2016-03-18
- **Reporter:** vivek-p
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Broken Authentication, Sensitive Information Disclosure, Insufficient Session Expiration, Insecure Direct Object References, Use of GET for Sensitive Operations
- **CVEs:** None
- **Category:** web-api

## Summary
Zomato's email verification link in the registration flow never expires and allows users to authenticate without a password by simply clicking a link. The verification token is Base64 encoded and transmitted via GET parameters, leaking sensitive data (user ID, verification code, email) in browser history, cache, and server logs.

## Attack scenario
1. Attacker obtains or observes the victim's email verification URL from browser history, cache, or server logs on a shared/public computer
2. Attacker decodes the Base64 'fbcid' parameter to extract the user ID, 4-digit verification code, and email address
3. Attacker clicks the verification link or reconstructs it with the extracted parameters
4. Application authenticates the attacker without requiring a password, granting full account access
5. Attacker can now perform actions as the victim including accessing account details, placing orders, modifying settings
6. If victim used public computer/cyber cafe, link persists in browser history allowing discovery by subsequent users

## Root cause
Authentication mechanism relies solely on email verification token without password re-confirmation; token lacks expiration; sensitive data encoded in URL instead of transmitted securely; use of GET method for sensitive authentication operations; insufficient session validation

## Attacker mindset
Opportunistic attacker targeting users who register from shared computers. Attacker seeks account takeover with minimal effort by leveraging poor token management and password-less authentication. Focus on gaining access to user accounts to commit fraud (food ordering, payment misuse) or extract personal information.

## Defensive takeaways
- Implement strict token expiration (15-30 minutes maximum) for email verification links
- Use POST method with CSRF tokens for sensitive authentication operations instead of GET
- Generate cryptographically strong, unpredictable tokens instead of Base64-encoded user data
- Require password confirmation when completing email verification, especially for sensitive actions
- Implement token invalidation after first successful use
- Store sensitive data server-side only, never in URL parameters
- Add rate limiting and attempt logging for verification token usage
- Implement additional verification factors (CAPTCHA, IP validation) for email verification
- Clear sensitive URLs from browser history guidelines or enforce secure headers (no-cache, no-store)
- Implement session binding to prevent token reuse across different sessions/IPs

## Variant hunting
Check all password reset/account recovery flows for similar token expiration issues
Review other transactional email links (payment confirmation, address change) for token reuse vulnerabilities
Test if tokens work across different sessions/browsers/IP addresses
Examine OAuth/third-party authentication flows for similar weaknesses
Check API endpoints for similar parameter-based authentication without password
Test if multiple verification attempts with same token are allowed
Review mobile app verification flow for identical issues
Check if tokens can be brute-forced due to weak generation
Audit other GET-based authentication mechanisms across application

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1078 - Valid Accounts (using stolen/bypassed authentication)
- T1110 - Brute Force (token enumeration potential)
- T1056 - Input Capture (obtaining link from shared computer history)
- T1020 - Automated Exfiltration (via browser history/logs)

## Notes
Report demonstrates classic broken authentication vulnerability from 2016 era when email verification best practices were less standardized. The combination of non-expiring tokens, password-less authentication, and sensitive data in URLs created a critical account takeover vector. Severity amplified by attack being passively exploitable from shared computers without user interaction needed. This pattern was common in many web applications and represents fundamental authentication design flaws.

## Full report
<details><summary>Expand</summary>

The zomato.com web application is vulnerable to authentication bypassing and sensitive information disclosure.

The flaw exist in “Verify Email Address” link which is received in a mail after registration. Once the user enters Full Name, Email Address and Password during registration, he/she is either asked to enter a 4 digit code or directly verify email address by clicking the red button for successful account activation/creation.
The verify email address link doesn’t expire even after successful user registration/account activation which allows a malicious user to authenticate into the victim’s session without password. When an user clicks on verify email address link, he/she is directly authenticated without a need of password, thereby bypassing authentication. Also, the verify email address link consist of ‘fbcid’ parameter which is just Base64 encoded. It leaks sensitive data like unique user id, 4 digit code and email address of the user. All these three parameter are being passed in URL itself (GET request).The application is authenticating a user using these three parameter without a need of a password. 

The verify email address GET URL consisting of sensitive data like unique user id, 4 digit code and email address gets stored in cache, browser history, web server logs. If the victim has accessed this link or activated his account from a public computer/cyber cafe, any user with malicious intent can access and misuse this url in order to authenticate into the victim session without a need of a password. 


</details>

---
*Analysed by Claude on 2026-05-24*
