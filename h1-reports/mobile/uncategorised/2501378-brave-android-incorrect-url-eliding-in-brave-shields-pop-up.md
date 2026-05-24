# Brave Android: Incorrect URL Eliding in Brave Shields Pop Up

## Metadata
- **Source:** HackerOne
- **Report:** 2501378 | https://hackerone.com/reports/2501378
- **Submitted:** 2024-05-11
- **Reporter:** jayateerthag
- **Program:** Brave
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** User Interface Spoofing, URL Confusion, Security Control Bypass
- **CVEs:** CVE-2024-37406
- **Category:** uncategorised

## Summary
Brave Android fails to properly elide long domain names in the Brave Shields popup UI, contrary to Chromium security guidelines. This inconsistency with the desktop version could enable URL spoofing attacks and confuse users when managing shield settings, with potential extension to Brave Rewards functionality where users donate cryptocurrency.

## Attack scenario
1. Attacker crafts a malicious URL with an extremely long subdomain designed to be visually indistinguishable from a legitimate domain when partially visible
2. User visits the attacker's URL on Brave Android browser
3. User clicks the Brave Shields icon to manage security settings for the site
4. The Brave Shields popup displays the full unelided URL, causing the legitimate-looking portion to dominate the display while the actual domain is hidden
5. User, confused by the dominant visible text, believes they are managing shields for a trusted domain and allows dangerous permissions
6. If Brave Rewards is similarly affected, user may donate BAT tokens to an attacker-controlled site believing it is legitimate

## Root cause
Android implementation of Brave Shields UI does not implement URL eliding logic that is present in the desktop (Windows) version. The codebase likely diverged between platforms, with the Android version missing calls to URL simplification/elision functions defined in Chromium security guidelines.

## Attacker mindset
An attacker would leverage this UI inconsistency to craft phishing URLs that appear legitimate in context where users make security or financial decisions. The attack is most potent when targeting Brave Rewards, where users explicitly authorize cryptocurrency transfers based on displayed URLs.

## Defensive takeaways
- Implement consistent URL eliding across all platforms (desktop, Android, iOS) using Chromium's documented URL display guidelines
- Apply URL eliding universally in any UI component displaying URLs to users, especially security controls and financial transaction interfaces
- Audit all user-facing URL displays in Brave Rewards, Shields, permission dialogs, and address bars for compliance with URL simplification standards
- Add unit tests verifying URL eliding behavior with various subdomain lengths across all platforms
- Implement automated cross-platform regression testing for URL display consistency
- Review Chromium's URL display guidelines periodically and sync implementation changes across all Brave clients

## Variant hunting
Search for similar URL display issues in: (1) Brave Rewards donation UI and BAT token transfer confirmations, (2) Permission grant dialogs across Android/iOS, (3) Site identity popup in address bar, (4) Cookie/data management UIs, (5) Extension permission scopes display, (6) Payment request UI for cryptocurrency transactions, (7) Any dialog prompting user action based on domain identity

## MITRE ATT&CK
- T1598.003 - Phishing: Spearphishing Link
- T1499.004 - Application Exhaustion Flood (visual confusion leading to incorrect user actions)
- T1539 - Steal Web Session Cookie (indirectly, via confusion leading to unsafe permission grants)

## Notes
Reporter notes potential severity impact on Brave Rewards due to financial implications but was unable to fully test in their region. This suggests the vulnerability should be escalated if Rewards UI is similarly affected. The cross-platform inconsistency (working on Windows, broken on Android/possibly iOS) indicates a platform-specific implementation gap rather than a shared vulnerability, making this a regression or incomplete port issue. Chromium reference documentation cited by reporter provides clear security guidelines that should be followed uniformly.

## Full report
<details><summary>Expand</summary>

## Summary:
Reference: https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/url_display_guidelines/url_display_guidelines.md#simplify

Urls should be elided from front when displaying anywhere in the user interface as per standard security guidelines for most browsers in order to avoid url spoofing or confusing users with actual domain name, when long domain/subdomain is used.
The desktop version(Windows) of Brave is working properly and url is elided correctly, while in android it's not. (Refer POC images for reference)


## Products affected: 

Brave for Android: 1.62.165 Chromium: M121

## Steps To Reproduce:
1. Open https://long-extended-subdomain-name-containing-many-letters-and-dashes.badssl.com/ in Brave Browser (Android)
2. Click on the Brave Icon in the URL Bar/Omnibox to enable/disable Brave Shield for the website
3. Notice that in the Brave shield UI which appears, the long subdomain is not elided from front properly in android which might lead to URL Confusion to the users.
4. Although I have reported for Brave Shields only I suspect that this might affect in places like Brave Rewards too where URL might not be properly elided. (I am currently unable to test this feature as I am located in India which does not support Uphold Wallet integration)
Incorrect URL Eliding in Brave Rewards UI might be very severe vulnerability as users might get confused when donating BAT tokens to website. [I request Brave team to test point 4 & fix if vulnerable in the same ticket]

Note: As android is affected, IOS might also be affected, Kindly check & fix the same in all Mobile OS

## Supporting Material/References:

https://chromium.googlesource.com/chromium/src/+/HEAD/docs/security/url_display_guidelines/url_display_guidelines.md#simplify

## Impact

URL confusion/spoof when user want to enable/disable Brave shields in Android

</details>

---
*Analysed by Claude on 2026-05-24*
