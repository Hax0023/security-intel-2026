# Missing Authorization Check on iOS Web Browser Login - Coinbase

## Metadata
- **Source:** HackerOne
- **Report:** 148538 | https://hackerone.com/reports/148538
- **Submitted:** 2016-06-30
- **Reporter:** ahsan
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Broken Authentication, Missing Authorization, Information Disclosure, Broken Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Coinbase's web application fails to enforce email-based authorization verification when users log in via iOS browser, despite enforcing this requirement on desktop browsers. Attackers with valid credentials can immediately access sensitive financial data including transaction history, account balance, and modify critical account settings without completing the required authorization step.

## Attack scenario
1. Attacker obtains valid Coinbase credentials through credential stuffing, phishing, or data breach
2. Attacker accesses Coinbase web application via iOS mobile browser (Safari, Chrome, etc.)
3. Authentication succeeds without prompting for email-based authorization verification
4. Attacker views sensitive financial information including transaction history and wallet balance
5. Attacker navigates to /settings endpoint and modifies account settings including password and account deletion
6. Attacker gains persistent access or locks legitimate user out of their account

## Root cause
Inconsistent authentication flow implementation across platforms. The server-side authorization check is likely bypassed or skipped based on User-Agent detection, where iOS browsers are incorrectly flagged as 'trusted' or 'authorized' without completing the required email verification step. Missing server-side enforcement of authorization requirements regardless of client platform.

## Attacker mindset
Credential-based account takeover focused on financial fraud. Attacker could leverage compromised credentials (from other breaches or phishing) to gain immediate access to victim's cryptocurrency and financial accounts. The iOS path represents a lower-friction attack vector compared to desktop, making it an attractive exploitation method.

## Defensive takeaways
- Implement consistent authentication and authorization policies across all client platforms and User-Agent types
- Never trust client-side indicators (User-Agent, device type) for security decisions; enforce authentication requirements server-side
- Implement mandatory multi-factor authentication (MFA) for all login attempts, especially for sensitive operations
- Use device fingerprinting and anomaly detection to identify suspicious login patterns regardless of platform
- Implement step-up authentication for sensitive operations like accessing settings or modifying account details
- Add email verification or push notification confirmation for all login attempts from new or unrecognized devices
- Conduct cross-platform security testing to identify inconsistencies in authentication flows
- Implement server-side session validation that cannot be bypassed by client-platform variations

## Variant hunting
Check for platform-specific bypasses in other endpoints (API, settings, transactions, transfers)
Test alternative mobile browsers (Firefox, Edge on iOS) for same bypass
Investigate if other User-Agent strings (Android, tablets) trigger different authentication flows
Check if authorization bypass applies to sensitive operations (fund transfers, withdrawals, 2FA disable)
Test if session tokens from iOS login work on desktop endpoints without re-authorization
Examine if the /settings endpoint has other sub-paths (password change, 2FA settings) that bypass authorization

## MITRE ATT&CK
- T1110.004 - Credential Stuffing
- T1566.002 - Phishing: Spearphishing Link
- T1021.005 - Remote Services: Cloud Services
- T1078.001 - Valid Accounts: Default Accounts
- T1539 - Steal Web Session Cookie
- T1555 - Credentials from Password Stores

## Notes
Report demonstrates critical financial security vulnerability in production system. Affects non-technical users who may not realize authorization was bypassed. The platform-specific nature suggests code path differentiation in authentication logic. High severity due to direct access to financial accounts, transactions, and account modification capabilities. Report lacks specific HackerOne bounty amount information but vulnerability type and impact warrant substantial reward consideration.

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
