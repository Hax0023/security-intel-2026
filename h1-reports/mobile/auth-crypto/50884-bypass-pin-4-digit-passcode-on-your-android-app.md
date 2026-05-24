# Android Exported Activities Bypass PIN Protection in Whisper App

## Metadata
- **Source:** HackerOne
- **Report:** 50884 | https://hackerone.com/reports/50884
- **Submitted:** 2015-03-11
- **Reporter:** adrianbelen
- **Program:** Whisper
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper Platform Usage, Exported Component Without Protection, Authentication Bypass, Insecure Inter-Process Communication
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The Whisper Android application implements a 4-digit PIN protection mechanism for sensitive features (inbox and notifications), but critical activities (WNotificationsActivity and WInboxActivity) are exported without proper permission controls. This allows any installed third-party application to directly launch these protected activities and bypass the PIN authentication entirely.

## Attack scenario
1. Attacker develops a malicious Android application and publishes it to Google Play or distributes it via side-loading
2. User installs the malicious app on their device alongside the legitimate Whisper app
3. Malicious app uses Intent-based inter-process communication to launch sh.whisper.WNotificationsActivity or sh.whisper.WInboxActivity directly
4. Whisper's exported activities are invoked without triggering PIN authentication checks
5. Attacker gains unauthorized access to user's protected inbox and notification content
6. Sensitive messages and personal information are compromised without user knowledge

## Root cause
The AndroidManifest.xml does not properly declare the exported activities with protection-level restrictions. Activities WNotificationsActivity and WInboxActivity are exported (either explicitly with android:exported='true' or implicitly by having intent-filters) without corresponding permission declarations or internal authentication state validation before displaying protected content.

## Attacker mindset
An attacker with physical access or ability to install apps would recognize that exported activities bypass application-level authentication. By directly invoking protected activities through Intent calls, they circumvent the PIN mechanism entirely, treating the authentication as merely a UI-level gate rather than a security boundary.

## Defensive takeaways
- Never export activities containing sensitive data unless absolutely necessary; use android:exported='false' by default
- Implement re-authentication checks within sensitive activities, not just at entry points, to verify user identity regardless of how the activity was invoked
- For protected activities that must be exported, declare custom permissions with appropriate protection levels and enforce them via permission checks in code
- Use internal state verification (authentication tokens, session validation) before rendering sensitive content in any activity
- Conduct thorough component analysis during security review: map all exported components and verify each has appropriate access controls
- Test authentication flows by simulating intent-based invocations from third-party apps using adb or security testing tools
- Consider implementing deep-link verification and signature-based validation for inter-app communication

## Variant hunting
Identify all exported activities in the manifest and check which handle sensitive user data
Test other exported activities for similar bypasses: WSettingsActivity, WUserActivity, WParseDeepLinkActivity may have related issues
Check if other protected operations (payment, account changes, data deletion) can be invoked through exported components
Analyze whether exported activities validate the calling application's identity or permissions
Review similar messaging/social apps for comparable PIN bypass patterns via exported components
Test if the PIN mechanism is enforced at the fragment level or only at the activity launcher level
Check for deeplink handling in WParseDeepLinkActivity that might allow external URL-based activity invocation

## MITRE ATT&CK
- T1190
- T1204
- T1406
- T1418

## Notes
This is a classic Android platform misuse vulnerability. The developer likely intended to protect the app UI with PIN authentication but failed to account for inter-process communication (IPC) attack vectors. The CWE-926 reference is appropriate (Improper Export of Android Application Components). The vulnerability demonstrates why authentication should be enforced at the data/service layer, not just the presentation layer. The impact is significant as it affects core sensitive features (inbox/notifications) designed to require authentication.

## Full report
<details><summary>Expand</summary>

i have found that this activities are exported
** Package: sh.whisper **
  sh.whisper.WMainActivity
  sh.whisper.WWhisperBrowserActivity
  sh.whisper.WRelatedActivity
  sh.whisper.WDiscoverActivity
  sh.whisper.WCategoryFeedActivity
  sh.whisper.WSettingsActivity
    Parent Activity: sh.whisper.WMainV4Activity
  sh.whisper.WShareActivity
  sh.whisper.WQuickCreateActivity
    Parent Activity: sh.whisper.WMainV4Activity
  sh.whisper.WUserActivity
  sh.whisper.WNotificationsActivity
  sh.whisper.WInboxActivity
  sh.whisper.WParseDeepLinkActivity
  sh.whisper.WAddGroupActivity

whisper android app have a 4 digits PIN that can be set by the user to protect from unauthorized access if the phone is lost(protection for user's inbox and notification) , but   **sh.whisper.WNotificationsActivity**
  and **sh.whisper.WInboxActivity** are exported ,so any android app can called these activities to bypass the **4-digit code**

watch this video on have i bypass the 4-digit code 

** references**
http://cwe.mitre.org/data/definitions/926.html


</details>

---
*Analysed by Claude on 2026-05-24*
