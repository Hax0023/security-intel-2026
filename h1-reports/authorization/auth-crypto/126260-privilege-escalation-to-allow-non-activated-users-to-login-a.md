# Privilege Escalation: Non-Activated Users Can Login to Uber Partner iOS App

## Metadata
- **Source:** HackerOne
- **Report:** 126260 | https://hackerone.com/reports/126260
- **Submitted:** 2016-03-27
- **Reporter:** mini
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Access Control, Client-Side Validation Bypass, Privilege Escalation, Insufficient Server-Side Validation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Non-activated Uber Partner users could bypass activation requirements by manipulating client-side requests and server responses. By intercepting login requests to change 'allowNotActivated' flag and using proxy response manipulation, attackers could successfully authenticate and access full app features intended only for activated partners.

## Attack scenario
1. Attacker downloads the Uber Partner iOS app
2. Attacker intercepts login request using Burp Suite proxy
3. Attacker modifies request payload changing 'allowNotActivated':false to 'allowNotActivated':true
4. Initial login fails as server returns 'isActivated':false in response
5. Attacker configures Burp Suite Match/Replace rule to convert 'false' to 'true' in response bodies
6. Attacker repeats login with modified request and intercepted response, successfully bypassing activation check

## Root cause
Server relied on client-side enforcement of the activation requirement and accepted modified client parameters without proper validation. Additionally, the response containing activation status was not properly validated by the client logic, allowing response manipulation to bypass authorization checks.

## Attacker mindset
An unactivated partner driver seeking unauthorized access to premium features, or a malicious actor attempting to perform fraudulent activities using an inactive account without completing proper verification procedures.

## Defensive takeaways
- Implement strict server-side validation of user activation status independent of client-sent flags
- Never trust client-side parameters for security-critical decisions; always validate on server
- Implement certificate pinning to prevent proxy interception attacks
- Use response signing/integrity verification to prevent tampering with authentication responses
- Enforce server-side session validation regardless of client-provided activation status
- Log and alert on suspicious activation state mismatches between requests and server records
- Implement rate limiting on login attempts to prevent brute force variants

## Variant hunting
Check for similar 'allow*' or 'bypass*' flags in other API endpoints that might be client-controlled
Test other user status fields (isVerified, isApproved, isPremium) for similar bypass techniques
Examine other mobile apps (Uber driver, Uber eats) for identical vulnerable patterns
Test if other HTTP methods (PUT, PATCH) accept activation status modifications
Check for similar bypass patterns in registration, onboarding, or account upgrade endpoints
Test if activation status can be modified in subsequent API calls after initial login
Examine if JWT tokens or session cookies contain modifiable activation claims

## MITRE ATT&CK
- T1190
- T1547
- T1556
- T1556.004

## Notes
This is a textbook example of broken access control stemming from client-side security enforcement. The vulnerability demonstrates two distinct issues: (1) accepting client-controlled activation flags without validation, and (2) allowing response manipulation to bypass authorization. The attack requires man-in-the-middle capabilities but is relatively simple to execute. High impact due to unauthorized access to partner platform functionality.

## Full report
<details><summary>Expand</summary>

Hi


It is possible for non activated users to login to partner app and use its full features! 

Steps:

1- download uber partner iOS app

2- intercept the login request with burp suite and change “allowNotActivated":false to "allowNotActivated":true


3- Login failed because the server responded with isActivated":false

4- Go to burp suite Match and replace from proxy options tab

5- add a match/replace rule ( Type: Response body, Match: false, Replace: true )

6- repeat login process once again and intercept the login request and change allowNotActivated”:false to allowNotActivated”:true

7- you are logged in successfully :)


</details>

---
*Analysed by Claude on 2026-05-24*
