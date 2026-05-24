# Missing Authorization/MFA on Windows Phone Web Application Login

## Metadata
- **Source:** HackerOne
- **Report:** 148537 | https://hackerone.com/reports/148537
- **Submitted:** 2016-06-30
- **Reporter:** ahsan
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Missing Authentication, Missing Multi-Factor Authentication, Improper Access Control, Information Disclosure, Broken Authentication
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Coinbase's web application failed to enforce email-based authorization on Windows Phone browsers, allowing unauthenticated users to directly access sensitive financial data including transaction history and account balance without completing the required authorization flow. Attackers could additionally modify critical account settings such as password and recovery options by accessing the /settings endpoint.

## Attack scenario
1. Attacker obtains a Coinbase user's credentials through phishing or credential stuffing
2. Attacker accesses Coinbase via Windows Phone browser on the target device or emulates Windows Phone user-agent
3. Login request is processed without triggering the standard email-based authorization challenge
4. Attacker gains direct access to dashboard displaying transactions, balance, and financial account details
5. Attacker navigates to /settings endpoint to modify password, delete account, or alter security configurations
6. Account compromise is completed with no legitimate user notification or authorization required

## Root cause
Insufficient server-side validation of the authorization requirement based on client user-agent or device type. The application implemented device-specific logic that exempted Windows Phone browsers from the mandatory MFA/authorization flow, likely due to incomplete testing or platform-specific handling code that bypassed security controls.

## Attacker mindset
An attacker would recognize that financial applications often implement varying security policies across platforms and might exploit device-specific logic gaps. By targeting less common platforms like Windows Phone, they could bypass authentication mechanisms while accessing sensitive banking information. The ability to then modify account settings represents a complete account takeover path.

## Defensive takeaways
- Implement authorization/MFA consistently across all client platforms and user-agents—never conditionally disable critical security controls based on device type
- Enforce server-side authorization requirements independent of client characteristics; all authentication decisions must occur server-side
- Test security flows exhaustively across all supported browsers, devices, and user-agent combinations, including legacy platforms
- Implement device fingerprinting and anomaly detection to flag logins from unusual devices regardless of platform
- Require step-up authentication for sensitive operations (password change, account deletion) on all platforms uniformly
- Audit all conditional security logic in codebase to identify similar bypasses in other features or platforms
- Log and monitor authentication bypass attempts by platform/user-agent for breach detection

## Variant hunting
Check for similar platform-specific exemptions in mobile apps (iOS, Android) or other browsers (Opera, UC Browser, etc.)
Test other uncommon user-agents or spoofed client identifiers to determine if other device types bypass MFA
Verify that password reset flows, email change, and API key generation also enforce consistent authorization across platforms
Examine whether legacy or deprecated platform support (Blackberry, Firefox OS) contains similar bypasses
Check if sensitive API endpoints bypass authorization checks when accessed from specific user-agent strings

## MITRE ATT&CK
- T1190
- T1110
- T1078
- T1556
- T1098

## Notes
This report demonstrates a critical platform-specific authentication bypass in a financial application. The vulnerability is particularly severe because Coinbase handles cryptocurrency assets where account compromise has direct financial impact. The bug appears to stem from incomplete platform coverage in security implementation rather than a fundamental architectural flaw, suggesting the authorization logic was platform-aware when it should have been universal. The report lacks information on bounty amount and whether Windows Phone traffic was intentionally deprioritized or simply overlooked during development.

## Full report
<details><summary>Expand</summary>

Hey, this is Ahsan Tahir! I've found a authorization issue in coinbase! :-)

Issue
=======
When we login to coinbase using PC (not authorized) it asks for authorization using a link, which is sent to our email and we have to authorize it by clicking on that email; but, when we login to a windows phone (using a browser), it doesn't requires any authorization, and we directly login, it shows the transactions and the total balance in our wallet, which is no doubt **Information Disclosure**; further, if we go to this URL https://www.coinbase.com/settings, we can edit our settings [change password, delete account, change other settings] etc.. so this is no doubt **Authorization/Authentication** Issue.

### Steps to Reproduce:
1. Login with Windows Phone (Lumia). 
2. It won't ask for any authorization, and it will disclose the transactions etc..
3. Go to https://www.coinbase.com/settings.
4. Now you can also *edit* the settings.

How to Fix?
----------------
When we login to windows phone using browser, it *should* ask for authorization! Like sending a mail to the email of that account or other type of authorization!

If you have any other questions or if anything needs clarification, please let me know.
Hoping for you to fix this issue ASAP!

Thanks,
- Ahsan Tahir


</details>

---
*Analysed by Claude on 2026-05-24*
