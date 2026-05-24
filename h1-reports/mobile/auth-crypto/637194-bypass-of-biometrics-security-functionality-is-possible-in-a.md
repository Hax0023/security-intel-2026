# Biometric Authentication Bypass via Deeplink in Shopify Android App

## Metadata
- **Source:** HackerOne
- **Report:** 637194 | https://hackerone.com/reports/637194
- **Submitted:** 2019-07-07
- **Reporter:** tiago-danin
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authentication Bypass, Insufficient Access Control, Insecure Deeplink Handling
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Shopify Android application allows biometric authentication (fingerprint) for securing user access, but this security control can be bypassed by triggering a deeplink activity (DeepLinkActivity) while the app is already running. An attacker can use ADB commands or craft intents to bypass authentication and gain unauthorized access to protected features like the admin products section.

## Attack scenario
1. Attacker gains physical access to an unlocked Android device with Shopify app installed and already running in the background
2. Attacker executes ADB command or uses another app to trigger the DeepLinkActivity with a crafted URI (e.g., 'https://www.shopify.com/admin/products')
3. The deeplink activity is launched without checking if the user has passed biometric authentication
4. User is navigated to protected admin sections (products, orders, etc.) without fingerprint verification
5. Attacker gains unauthorized access to sensitive merchant data and administrative functions
6. Attacker can perform unauthorized actions like viewing/modifying products, orders, or customer data

## Root cause
The DeepLinkActivity does not validate whether the user has completed biometric authentication before processing deeplinks. The authentication check is likely only performed during initial app launch or login flow, but deeplinks bypass this gate when the app process is already running. The activity fails to enforce authentication state verification for sensitive operations.

## Attacker mindset
An attacker with physical access to an unlocked device (or via remote ADB in some configurations) exploits the assumption that only the legitimate user would trigger intents within their own app. By circumventing the biometric gate through deeplink exploitation, they gain uncontrolled access to sensitive admin features without triggering security prompts.

## Defensive takeaways
- Always validate authentication state before processing deeplinks or intents, regardless of app lifecycle state
- Implement authentication checks as a gate before navigating to protected activities or fragments
- Use explicit intent filters and verify caller identity for sensitive deeplinks
- Implement re-authentication prompts for sensitive operations (admin functions, data access)
- Store authentication state securely and invalidate it appropriately on app suspend/resume
- Require biometric re-verification when accessing sensitive features even if the app is already running
- Implement activity stack management to prevent bypassing the login flow via deeplinks

## Variant hunting
Check other activities accessible via deeplinks for similar authentication bypass vulnerabilities
Test if the vulnerability persists after app backgrounding and resuming
Verify if other authentication mechanisms (OAuth, session tokens) are similarly bypassable
Check if export deeplinks in third-party apps can trigger the same bypass
Test if the vulnerability affects other Shopify apps or similar e-commerce applications
Examine if background service intents can be used to achieve the same bypass
Test notification click handlers and their authentication state requirements

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1556 - Modify Authentication Process
- T1111 - Multi-Factor Authentication Interception
- T1528 - Steal Application Access Token

## Notes
This is a mobile-specific vulnerability leveraging Android's intent system. The fact that the app must be already open/running suggests the authentication state is not properly maintained or checked at the activity level. This is a relatively easy vulnerability to exploit with physical access and demonstrates a common mobile security anti-pattern of checking authentication only at entry points rather than before sensitive operations.

## Full report
<details><summary>Expand</summary>

# Summary
Shopify Android App has an option to sign in to the app using fingerprint. But if the application was open and someone triggers a "deeplink", authentication is no longer required.

## Step to Reproduce
{F523700}
Link: [Shopify Help Center - Topics - Products](https://help.shopify.com/en/manual/products)

NOTE¹: The application must be **open** when triggered `com.shopify.mobile.lib.app.DeepLinkActivity`.
NOTE²: It is also possible via ADB and Java (Android App):
`adb shell am start -n com.shopify.mobile/com.shopify.mobile.lib.app.DeepLinkActivity -d 'https://www.shopify.com/admin/products'`
```java
Intent intent = new Intent();
intent.setClassName("com.shopify.mobile", "com.shopify.mobile.lib.app.DeepLinkActivity");
intent.setData(Uri.parse("https://www.shopify.com/admin/products")); 
startActivity(intent);
```

My environment information:
{F523698} {F523699}

## Impact

Unauthorized access to use the application.

</details>

---
*Analysed by Claude on 2026-05-24*
