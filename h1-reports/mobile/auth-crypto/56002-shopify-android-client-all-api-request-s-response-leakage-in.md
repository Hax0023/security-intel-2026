# Shopify Android Client Unprotected Broadcast Receiver Leaks Sensitive API Response Data

## Metadata
- **Source:** HackerOne
- **Report:** 56002 | https://hackerone.com/reports/56002
- **Submitted:** 2015-04-12
- **Reporter:** sukhoi
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Insecure Broadcast Receiver, Information Disclosure, Lack of Access Control, Authentication Token Leakage, Credential Exposure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Shopify Android client broadcasts API response data including access tokens and session cookies using an unprotected implicit broadcast with action 'com.shopify.service.requestComplete'. Any third-party app can register a broadcast receiver without permissions to intercept and extract sensitive authentication credentials, enabling account takeover. The vulnerability requires no special permissions, root access, or user awareness.

## Attack scenario
1. Attacker develops a malicious Android app and registers a broadcast receiver for 'com.shopify.service.requestComplete' action without requiring any permissions
2. Victim installs both the Shopify app and the attacker's malicious app on their Android device
3. Victim launches Shopify app and authenticates with their credentials
4. NetworkService in Shopify broadcasts API responses containing access_token and admin_cookie via unprotected implicit broadcast
5. Attacker's broadcast receiver silently captures the broadcast containing sensitive authentication data
6. Attacker exfiltrates captured credentials (access_token, cookies, session data) to remote server and gains full account control

## Root cause
Shopify Android client uses implicit broadcasts to communicate API response information between components without implementing signature-level permission protection or using LocalBroadcastManager. The broadcast action 'com.shopify.service.requestComplete' is publicly accessible, allowing any third-party app to register a receiver and intercept sensitive data including authentication tokens and cookies.

## Attacker mindset
Opportunistic but determined - targeting mass credential theft through passive interception. The attacker recognizes that Shopify users likely have valuable accounts and administrative access. By packaging the exploit in an innocuous app, they can silently harvest credentials at scale without triggering user suspicion or requiring elevated privileges.

## Defensive takeaways
- Never broadcast sensitive data like authentication tokens, session cookies, or API credentials via implicit broadcasts
- Use LocalBroadcastManager or other restricted scope broadcast mechanisms for inter-component communication within the same app
- Implement signature-level permission protection for any inter-app broadcast requiring protection
- Avoid broadcasting PII, tokens, or sensitive response data; use secure inter-process communication (IPC) alternatives like bound services with permission checks
- Conduct regular security audits of all broadcast receivers and implicit intents in the application
- Implement certificate pinning to add additional defense-in-depth for API communications
- Sanitize and minimize data included in broadcasts; exclude credentials entirely
- Test for broadcast interception vulnerabilities during security code review and penetration testing

## Variant hunting
Check for other implicit broadcasts in Shopify app or other shopping/payment apps broadcasting authentication data
Search for unprotected broadcasts containing 'token', 'cookie', 'auth', 'credential', 'session', 'password' in action names or intent filters
Audit apps that handle financial transactions, banking, or e-commerce for similar broadcast-based credential leakage patterns
Reverse engineer popular retail/marketplace Android apps to identify unprotected response broadcasts
Monitor Android app stores for malicious apps registering receivers for known shopping app broadcasts
Test for cleartext broadcast leakage in apps using Firebase Cloud Messaging or other real-time notification systems
Examine other applications using implicit service-to-component communication for credential exposure

## MITRE ATT&CK
- T1190
- T1439
- T1417
- T1432
- T1040
- T1056
- T1557
- T1111

## Notes
Critical vulnerability affecting all Shopify Android app users. POC was provided and tested on Android 4.4.4 (Nexus 5). The vulnerability is trivial to exploit - requires only basic Android development knowledge and no elevated permissions. This represents a complete account takeover vector for any Shopify user. Timeline and resolution status not provided in writeup. The use of implicit broadcasts for sensitive data is a fundamental Android security anti-pattern, suggesting possible broader architectural issues in Shopify's mobile application design.

## Full report
<details><summary>Expand</summary>

Shopify android client all API request's response leakage, including access_token, cookie, response header, response body content and much other information. An attacker can extract cookie and access_token of Shopify android client without any permission needed and user awareness.

#Bug impact:

A malicious android app can extract cookie and access_token and other user sensitive information in Shopify android client, and thus taking control of user's account.

Bug demostration (see two screenshots with stolen cookie in http headers printed in logcat and access_token).

#Bug explaination:

The shopify client use implicit broadcast to communicate intra-app to pass network request's response infromation, with action "com.shopify.service.requestComplete". However this broadcast is not protected by permission, thus any android client can register a broadcast receiver and monitor response information, extracting sensitive account credentials.

The broadcast is send at com/shopify/service/netcomm/NetworkService, recvd at multiple points. including com/shopify/service/BaseRequestDelegate$RequestCompletionBroadcastReceiver$1.

#Steps to reproduce:

- Install the poc apk and shopify client, poc apk registered a receiver and monitor in background
- Open shopify and login, the poc apk will now receives user's admin_cookie and access_token silently, print them in logcat as demonstrated in screenshots. Of course the attacker can send it to remote control center and fully take control of user's account.
- As user operates the attacker can receives other response information.
- logcat command:  adb logcat -s SHOPIFYHACK:V

#Fix recommendations:

Use signature level permission to protect the broadcast, or use a LocalBroadcastManager

POC apk attached, tested on Nexus 5 4.4.4. No special permission or root required. No user interactions and awareness.


</details>

---
*Analysed by Claude on 2026-05-24*
