# Privilege Escalation: Non-Activated Users Can Login to Uber Partner iOS App

## Metadata
- **Source:** HackerOne
- **Report:** 126260 | https://hackerone.com/reports/126260
- **Submitted:** 2016-03-27
- **Reporter:** mini
- **Program:** Uber
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Insufficient Access Control, Client-Side Validation Bypass, Privilege Escalation, Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Non-activated Uber Partner users could bypass activation requirements by manipulating client-side parameters and intercepting server responses. By modifying the 'allowNotActivated' flag to true and replacing server validation responses, attackers could gain full access to partner app features without proper account activation.

## Attack scenario
1. Attacker downloads the official Uber Partner iOS application
2. Attacker intercepts login request using Burp Suite and modifies 'allowNotActivated':false to 'allowNotActivated':true
3. Initial login fails as server validates activation status and returns 'isActivated':false
4. Attacker configures Burp Suite Match/Replace rule to replace all 'false' with 'true' in response bodies
5. Attacker repeats login attempt with modified allowNotActivated parameter
6. Server response is intercepted and modified, allowing attacker to bypass activation check and gain full authenticated access

## Root cause
Over-reliance on client-side validation without proper server-side enforcement of activation status. Server fails to independently verify user activation status beyond what the client claims, allowing response manipulation to bypass authentication checks.

## Attacker mindset
An attacker seeking unauthorized access to Uber Partner features (earnings, ride acceptance, ratings) without completing account activation process. Motivated by financial gain or account takeover scenarios where activation restrictions prevent immediate access.

## Defensive takeaways
- Never trust client-side parameters for security decisions; server must independently validate all account activation states
- Implement server-side authorization checks on every protected endpoint regardless of client-submitted activation flags
- Use certificate pinning to prevent man-in-the-middle response manipulation attacks
- Implement response signing/HMAC to detect tampering with sensitive authentication fields
- Add backend audit logging for activation state mismatches between client claims and server records
- Implement rate limiting and anomaly detection for repeated failed/suspicious authentication attempts
- Ensure activation status is verified before issuing auth tokens, not after

## Variant hunting
Check for similar 'allowed' or 'enabled' boolean flags in other client requests that control access
Test other account states (suspended, verified, premium) for similar client-side bypass patterns
Examine API endpoints for other parameters that control feature access or permissions
Review Android app version for identical vulnerability
Test other Uber products (Eats, Freight) partner apps for similar activation bypass patterns
Check if user session tokens are properly invalidated when activation requirements change

## MITRE ATT&CK
- T1190
- T1021
- T1556
- T1110

## Notes
This vulnerability demonstrates critical server-side validation failures. The attacker needed only Burp Suite and didn't require advanced techniques, indicating basic security implementation. The use of Match/Replace rules suggests server responses contained unencrypted, modifiable authentication data. This likely affected multiple user accounts and had significant business impact by allowing unauthorized partner access.

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
