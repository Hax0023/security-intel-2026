# Missing Authorization for iOS Browser Login at Coinbase

## Metadata
- **Source:** HackerOne
- **Report:** 148538 | https://hackerone.com/reports/148538
- **Submitted:** 2016-06-30
- **Reporter:** ahsan
- **Program:** Coinbase
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** Missing Authentication, Missing Authorization, Information Disclosure, Broken Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Coinbase's iOS web application fails to enforce the same multi-factor authorization (MFA) requirements that are present on desktop browsers, allowing attackers to gain unauthorized access to sensitive account features. An unauthenticated iOS browser login bypasses email authorization verification and grants immediate access to transaction history, account balance, and administrative settings.

## Attack scenario
1. Attacker obtains a victim's Coinbase credentials through phishing, credential stuffing, or data breach
2. Attacker accesses Coinbase on an iOS device using a mobile browser (Safari, Chrome, etc.)
3. The iOS web application skips the standard email authorization challenge that desktop browsers enforce
4. Attacker gains immediate access to the account dashboard without completing second-factor authentication
5. Attacker can view sensitive information including transaction history, account balance, and wallet details
6. Attacker navigates to coinbase.com/settings and modifies account credentials, deletes the account, or changes security settings

## Root cause
The iOS web application uses different or missing authentication logic compared to desktop browsers. The server-side authorization checks likely rely on User-Agent detection or missing session validation for mobile clients, failing to enforce consistent MFA/email verification requirements across all platforms.

## Attacker mindset
Account takeover through credential compromise becomes significantly more dangerous when follow-up authentication steps are missing. An attacker with valid credentials can immediately pivot to account destruction, fund theft, or credential modification before the legitimate owner is notified.

## Defensive takeaways
- Implement consistent, platform-agnostic authentication and authorization mechanisms regardless of User-Agent or client type
- Enforce MFA/email verification on all login attempts, not just desktop browsers
- Avoid using User-Agent or client-type detection to gate security controls; security should be uniform
- Implement server-side session validation that enforces the same authorization requirements for all authenticated endpoints
- Add device fingerprinting or behavioral analysis to detect unusual login patterns across different platforms
- Log and alert on platform-inconsistent authentication attempts
- Conduct security testing across all supported platforms (desktop, iOS, Android, web) with identical test cases
- Implement rate limiting and account lockout policies independent of platform

## Variant hunting
Test login flows on Android browsers vs iOS browsers for authorization discrepancies
Check if other sensitive endpoints (API transfers, withdrawal requests) also bypass authorization on mobile
Examine if tablet web browsers have the same authorization bypass
Test if native iOS app has different authorization requirements than web browser
Verify if changing User-Agent headers on desktop browsers can trigger the mobile bypass
Check if authorization is enforced on other Coinbase properties (Coinbase Pro, Coinbase Commerce)
Test authorization requirements on different iOS versions or browser types
Examine if the authorization bypass extends to viewing/modifying 2FA settings specifically

## MITRE ATT&CK
- T1190
- T1078
- T1110
- T1556
- T1021
- T1589

## Notes
This is a high-impact authentication bypass affecting a financial services platform. The vulnerability becomes critical when combined with credential compromise (phishing, password reuse). The researcher provided clear reproduction steps but did not mention bounty amount or fix confirmation timeline. This suggests either early-stage disclosure or the report may have been made before HackerOne integration. The inconsistent security posture across platforms is a common architectural flaw in companies with separate mobile and web teams.

## Full report
<details><summary>Expand</summary>

Hey, this is Ahsan Tahir! I've found a authorization issue in coinbase! :-)

Issue
=======
When we login to coinbase using PC (not authorized) it asks for authorization using a link, which is sent to our email and we have to authorize it by clicking on that email; but, when we login to a iOS device (using a browser), it doesn't requires any authorization, and we directly login, it shows the transactions and the total balance in our wallet, which is no doubt **Information Disclosure**; further, if we go to this URL https://www.coinbase.com/settings, we can edit our settings [change password, delete account, change other settings] etc.. so this is no doubt **Authorization/Authentication** issue.

### Steps to Reproduce:
1. Login with iOS device (browser, not app). 
2. It won't ask for any authorization, and it will disclose the transactions etc..
3. Go to https://www.coinbase.com/settings.
4. Now you can also *edit* the settings.

How to Fix?
----------------
When we login to iOS device using browser, it *should* ask for authorization! Like sending a mail to the email of that account or other type of authorization!

If you have any other questions or if anything needs clarification, please let me know.

Hoping for you to fix this issue ASAP!

Thanks,
Ahsan Tahir


</details>

---
*Analysed by Claude on 2026-05-24*
