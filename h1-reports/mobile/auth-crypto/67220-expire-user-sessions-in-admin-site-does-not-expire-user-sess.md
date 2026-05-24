# Expire User Sessions in Admin Site does not expire user session in Shopify Application on iOS

## Metadata
- **Source:** HackerOne
- **Report:** 67220 | https://hackerone.com/reports/67220
- **Submitted:** 2015-06-10
- **Reporter:** nismo
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Session Management, Improper Session Invalidation, Cross-Platform Session Handling
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The iOS Shopify application fails to invalidate user sessions when an administrator clicks 'Expire User Sessions' in the admin site, despite showing a notification that all users have been logged out. This creates a security gap where a user remains authenticated on the mobile app even after session termination is initiated server-side.

## Attack scenario
1. Administrator or owner initiates 'Expire User Sessions' from the admin site interface
2. Server processes the session expiration command and displays success notification to administrator
3. User with iOS Shopify app receives no logout signal and remains authenticated in the mobile application
4. Attacker or unauthorized party gains access to the unlogged-out iOS device
5. Attacker can access the authenticated user's account and perform actions within Shopify
6. Administrator believes all sessions are terminated but a gap in cross-platform session management persists

## Root cause
The iOS Shopify application does not properly subscribe to or listen for server-side session invalidation events. The mobile app likely maintains a local session/authentication token that is not being cleared when the backend session expiration command is issued, causing a disconnect between server-side and client-side session states.

## Attacker mindset
An attacker who gains access to an unlocked iOS device running Shopify app can exploit the delayed session invalidation to maintain unauthorized access to the account even after the legitimate user or administrator attempts to terminate all sessions. This is particularly valuable for persistent access in shared device scenarios.

## Defensive takeaways
- Implement real-time session invalidation notifications from backend to all client applications (iOS, Android, web)
- Add periodic session validation checks where mobile apps verify their authentication token with the server
- Utilize push notifications or WebSocket connections to immediately notify iOS app when sessions are revoked
- Clear local authentication tokens and force re-authentication when receiving invalidation signals
- Log all session termination events and track confirmation from all client platforms
- Test session expiration across all supported platforms before releasing updates
- Implement automatic re-validation of sessions at critical operations (viewing sensitive data, making transactions)

## Variant hunting
Check if Android Shopify application has the same session invalidation issue
Test if other admin actions that should affect user sessions (password changes, permission revocation) fail on iOS
Verify if web-based sessions are properly invalidated while mobile sessions persist
Test expiration behavior on iPad vs iPhone
Check if background app refresh or cached credentials allow session persistence after logout
Test if reinstalling the app properly clears persistent authentication tokens

## MITRE ATT&CK
- T1598 - Phishing: Preparation
- T1539 - Steal Web Session Cookie
- T1556 - Modify Authentication Process
- T1021 - Remote Services

## Notes
This report was submitted to HackerOne (ID: 67220) and demonstrates a critical gap in session management across platform boundaries. The vulnerability affects user account security as the primary logout mechanism fails on iOS. The issue is particularly concerning because the UI misleads administrators into believing sessions have been terminated when they actually haven't, creating false sense of security. Testing was conducted on iOS 8.3 and the latest Shopify app from iTunes Store at time of report.

## Full report
<details><summary>Expand</summary>

If an owner or an administrator clicks "Expire User Sessions" in Admin Site although you get the notification that all users where logged out, but this does not actually happens for the user that is currently logged in using the Shopify Application in IOS

This was tested on the latest Shopify app held in iTunes Store, using latest build of IOS 8.3 in iphone 6 plus

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
