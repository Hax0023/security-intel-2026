# Expire User Sessions in Admin Site does not expire user session in Shopify Application on iOS

## Metadata
- **Source:** HackerOne
- **Report:** 67220 | https://hackerone.com/reports/67220
- **Submitted:** 2015-06-10
- **Reporter:** nismo
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Session Management, Insufficient Session Invalidation, Client-Server Synchronization Flaw
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Shopify iOS mobile application fails to properly invalidate active user sessions when an administrator executes the 'Expire User Sessions' command from the admin dashboard. While the web interface confirms all users have been logged out, iOS app users remain authenticated and can continue accessing the application without re-authentication.

## Attack scenario
1. Attacker gains temporary physical access to a logged-in iOS device or compromises the device remotely
2. Store owner/administrator notices suspicious activity and executes 'Expire User Sessions' from admin site to revoke all active sessions
3. Admin receives confirmation notification that all user sessions have been terminated
4. Attacker continues using the compromised iOS app without interruption, as the session token remains valid
5. Attacker maintains unauthorized access to store data and can perform administrative actions
6. Session expiration only occurs when the app is forcibly closed and reopened, defeating the purpose of immediate session revocation

## Root cause
The iOS application does not maintain real-time synchronization with the backend session management system. The app caches session tokens locally without implementing a mechanism to receive or check for session revocation status from the server. The 'Expire User Sessions' backend operation only invalidates server-side sessions but does not proactively notify or invalidate the iOS client's cached credentials.

## Attacker mindset
An attacker with brief device access could exploit this to maintain persistent unauthorized access even after the legitimate owner attempts to revoke all sessions. This is particularly dangerous for store administrators handling sensitive business operations and customer data.

## Defensive takeaways
- Implement push notification mechanism to immediately notify clients of session revocation events
- Add server-side session validation on every API request, not just during login
- Implement session token versioning that invalidates all tokens when 'Expire User Sessions' is triggered
- Add real-time session status checking in the mobile app on app resume/focus events
- Reduce session token lifetime for mobile clients and implement refresh token rotation
- Display active session list to users with ability to revoke specific sessions remotely
- Implement certificate pinning and token binding to prevent replay attacks with stale tokens
- Add out-of-band confirmation (email/SMS) when sessions are forcibly expired

## Variant hunting
Test if other mobile platforms (Android) have the same session expiration bypass
Check if background refresh of app credentials occurs during app hibernation
Verify if switching between WiFi/cellular networks triggers session re-validation
Test if Admin user expiration only affects non-admin accounts
Examine if API endpoints properly validate session freshness vs. just token presence
Check if stored session data persists across app updates/reinstalls

## MITRE ATT&CK
- T1190
- T1555
- T1563

## Notes
This vulnerability was reported in 2015 on iOS 8.3. The issue highlights a critical gap between server-side authorization enforcement and client-side session handling in mobile applications. The asynchronous nature of mobile app updates means users may remain on vulnerable versions for extended periods. This type of vulnerability is particularly critical for financial/commerce applications handling sensitive business operations.

## Full report
<details><summary>Expand</summary>

If an owner or an administrator clicks "Expire User Sessions" in Admin Site although you get the notification that all users where logged out, but this does not actually happens for the user that is currently logged in using the Shopify Application in IOS

This was tested on the latest Shopify app held in iTunes Store, using latest build of IOS 8.3 in iphone 6 plus

Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
