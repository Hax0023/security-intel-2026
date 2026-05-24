# Shop App - OAuth Authorization Code Interception via Deep Link Hijacking

## Metadata
- **Source:** HackerOne
- **Report:** 1700734 | https://hackerone.com/reports/1700734
- **Submitted:** 2022-09-14
- **Reporter:** kun_19
- **Program:** Shop App (HackerOne #1700734)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln:** Improper URL Scheme Registration, Missing PKCE Implementation, OAuth Authorization Code Interception, Deep Link Hijacking, Insufficient OAuth Security
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Shop App implements OAuth flow for Microsoft Outlook integration using unprotected deep links with the custom URL scheme 'shopapp://'. A malicious application can register the same URL scheme and intercept the authorization code without PKCE protection, allowing attackers to exchange the code for valid session tokens to read victim emails or link Outlook accounts to attacker accounts.

## Attack scenario
1. Attacker develops a malicious Android app that registers the same 'shopapp://' URL scheme
2. Attacker distributes malicious app through unofficial channels or installs it on target device before legitimate Shop App (on iOS due to first-come-first-served principle)
3. Victim opens legitimate Shop App and initiates OAuth flow to connect Microsoft Outlook account
4. After user grants permissions to Microsoft, the authorization code is sent via deep link to 'shopapp://'
5. Operating system routes the deep link to malicious app (either Android user selection or iOS first-installed priority), intercepting the authorization code
6. Attacker exchanges intercepted authorization code for valid Microsoft session token or links victim's Outlook to attacker's Shop account

## Root cause
Shop App fails to implement PKCE (Proof Key for Code Exchange) flow for OAuth authentication and relies on unprotected deep links with non-unique URL schemes that can be hijacked by malicious applications with identical scheme registration.

## Attacker mindset
An attacker seeks to gain unauthorized access to victim email accounts and order tracking information. By understanding mobile deep linking vulnerabilities and OAuth weaknesses, they can craft a simple app that registers an identical URL scheme, positioning themselves to intercept authentication credentials with minimal user interaction or detection, especially on iOS where no user prompt occurs.

## Defensive takeaways
- Always implement PKCE flow for mobile OAuth implementations to prevent authorization code exchange even if intercepted
- Use platform-specific secure authentication mechanisms (iOS ASWebAuthenticationSession, Android Custom Tabs) instead of custom deep links for OAuth callbacks
- Implement URL scheme validation and use unique, unpredictable redirect URIs that cannot be easily guessed or collided with
- Consider using app-to-app authentication frameworks with cryptographic verification rather than URL schemes
- Validate authorization code origin and implement state parameter validation in OAuth flow
- Use app signing certificates and implement certificate pinning to verify legitimate app identity
- Document OAuth security best practices in developer guidelines and enforce PKCE requirement for all integrations
- Implement runtime permission checks and warn users about URL scheme hijacking risks in authentication flows

## Variant hunting
Search for other mobile apps using custom URL schemes for OAuth without PKCE implementation
Identify applications integrating with Google, Facebook, or other OAuth providers via unprotected deep links
Review apps requesting EMAIL or account access permissions combined with custom URL scheme registration
Analyze apps using generic or predictable URL schemes (e.g., 'app://', 'oauth://', 'auth://')
Test OAuth flows in apps that lack state parameter validation or authorization code expiration

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1528 - Steal Application Access Token
- T1598 - Phishing
- T1187 - Forced Authentication
- T1040 - Traffic Interception and Inspection
- T1557 - On-Path Interception

## Notes
This vulnerability demonstrates the critical importance of PKCE in mobile OAuth flows. Unlike web applications with centralized redirect URI registration, mobile platforms lack inherent URL scheme security, making PKCE essential. iOS users face elevated risk due to first-come-first-served principle applying without user notification. The vulnerability allows complete account takeover and email access, representing a severe authentication bypass. Reference: Auth0 PKCE documentation confirms this is industry best practice for mobile applications.

## Full report
<details><summary>Expand</summary>

## Summary:

### Deep linking 
Mobile apps have a unique vulnerability that is non-existent in the web: deep linking. Deep linking is a way of sending data directly to a native application from an outside source. A deep link looks like app:// where app is your app scheme and anything following the // could be used internally to handle the request.
Deep links are NOT secure and you should never send any sensitive information in them. The reason deep links are not secure is because there is no centralized method of registering URL schemes. As an application developer, you can use almost any url scheme you choose by configuring it in Xcode for iOS or adding an intent on Android. There is nothing stopping a rogue application from hijacking your deep link by also registering to the same scheme and then obtaining access to the data your link contains.

### Shop app - Microsoft Outlook Oauth flow and the vulnerability
The **Shop App** allows users to connect to their Microsoft Outlook  account to import orders from the emails (via OAuth flow). Therefore, the custom url scheme `shopapp://` is used for transmitting the authorization code at the end of the Oauth flow to the Shop App, which finally can be used to exchange the the authorization code with a valid session token from Microsoft.

Another (malicious) app is also able to claim the **same url scheme** and can intercept the authorization code! When the operating system has two or more applications to choose from when opening a link, Android will show the user a modal and ask them to choose which application to use to open the link. On iOS however, the operating system will make the choice for you, so the user will be blissfully unaware. Apple has made steps to address this issue in later iOS versions (iOS 11) where they instituted a first-come-first-served principle. Thus, if the malicious app is installed **BEFORE** the official Shop App, the malicious app "wins" and will receive the authorization code.

Normally, a special Oauth flow for mobile apps (**Authorization Code Flow with Proof Key for Code Exchange (PKCE)**) is used to prevent this ! It prevents an attacker, if the authorization code was intercepted, to exchange the authorization code with a valid session token (see here for more information https://auth0.com/docs/flows/authorization-code-flow-with-proof-key-for-code-exchange-pkce). 
This specific Oauth flow (PKCE) is not implemented by the Shop App for connecting a Microsoft Outlook account.

Thus, it is vulnerable to such kind of attacks. I created a malicious Android app which is able to intercept the authorization code (see PoC).

## Steps To Reproduce:

  1. Install the attached malicious Android App (F1926639) on your device.
  2. Install the official/legit Shop App from the Google Play Store.
  3. Open the legit Shop App, create an account and start connecting to your Microsoft Outlook account:  
{F1926639}
  4. Just log in to your Microsoft account and grant the Shop App the  permissions to access/read your emails: 
{F1926645}
  5. After the login, a modal is shown which asks the user which app should handle the authentication. Choose "Shop PRO" (the malicious App):  
{F1926673}
  6. The malicious App successfully intercepted the authorization code, which can now be exchanged to get a valid session token to read the victim's emails:  
{F1926677}

**NOTE**: Keep in mind that under iOS the *first-come-first-served principle* applies. If the malicious App is installed **BEFORE** the official Shop App, the malicious app "wins" and will receive the authorization code.

## Impact

An attacker is able to intercept an authorization code and exchanges it for a valid session token from Microsoft to gain read access to the victim's emails.

Or the attacker uses the intercepted authorization code to link the Outlook account to his own Shop account via the endpoint https://server.shop.app/graphql (operation name: `LinkOutlookAccount`). Thus, all orders can now be tracked by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
