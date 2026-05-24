# Authentication Session Not Terminated on Mobile After Password Change

## Metadata
- **Source:** HackerOne
- **Report:** 55530 | https://hackerone.com/reports/55530
- **Submitted:** 2015-04-09
- **Reporter:** lccunha
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Session Management, Authentication Bypass, Insufficient Session Invalidation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
When a user changes their password on the desktop web version of Shopify and selects the option to log out of mobile devices, the session on the Shopify Mobile Android app is not properly terminated. This allows an attacker with access to a device to maintain authenticated access despite the password change and explicit logout request.

## Attack scenario
1. Attacker gains temporary access to a user's Android device with Shopify Mobile installed and authenticated
2. User changes their password on desktop Shopify web application
3. User explicitly selects 'Also log out of your store on Shopify Mobile and/or Shopify POS' option during password change
4. Attacker retains the Android device and discovers the mobile session remains valid
5. Attacker can continue performing authenticated actions (viewing orders, modifying store settings, etc.) despite password change
6. Legitimate user believes they have secured their account by changing password and terminating mobile sessions

## Root cause
The password change handler on the server does not properly invalidate or notify the mobile application client to terminate its session token/authentication credentials. The mobile app likely caches authentication tokens without respecting server-side session invalidation signals, or the server fails to send proper termination commands to the device.

## Attacker mindset
An opportunistic attacker who gained temporary device access could exploit this to maintain persistent unauthorized access. A sophisticated attacker could use this in conjunction with social engineering or physical theft to maintain control of a compromised merchant account.

## Defensive takeaways
- Implement server-side session tracking for all authentication tokens across all platforms (web, mobile, POS)
- When password changes occur, actively revoke all existing session tokens regardless of platform
- Ensure mobile clients validate session status with server regularly and respect explicit logout/termination commands
- Send push notifications or in-app alerts to mobile devices when sessions are being terminated due to password change
- Implement token expiration mechanisms separate from session management
- Test password change workflows across all supported platforms and clients
- Add audit logging for session termination attempts and failures

## Variant hunting
Check if logout from POS also fails when option is selected
Test if iOS mobile version has the same vulnerability
Verify if other security-sensitive actions (email change, API key revocation) properly terminate sessions
Check if enabling two-factor authentication has similar issues
Test session termination when initiating from mobile app itself
Verify if compromised account recovery flows terminate all sessions

## MITRE ATT&CK
- T1190
- T1098
- T1133
- T1550

## Notes
This is a critical session management vulnerability in a multi-platform authentication system. The vulnerability is particularly dangerous for e-commerce platforms like Shopify where merchant accounts have significant financial and operational impact. The fact that the user explicitly requested session termination and it failed indicates both a UX failure and security failure. Report lacks specifics on timeline, reproduction consistency, and whether web sessions were properly terminated (focus only on mobile).

## Full report
<details><summary>Expand</summary>

1 access shopify.com > login
2 access your profile > change password 

Insert a new password and select the 'Also log out of your store on Shopify Mobile and / or Shopify POS' field.

In my test session was not closed in mobile version for Android.

Please check it.

</details>

---
*Analysed by Claude on 2026-05-24*
