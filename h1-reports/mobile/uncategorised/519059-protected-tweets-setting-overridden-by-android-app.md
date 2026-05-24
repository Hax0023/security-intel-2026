# Protected Tweets setting overridden by Android app

## Metadata
- **Source:** HackerOne
- **Report:** 519059 | https://hackerone.com/reports/519059
- **Submitted:** 2019-03-30
- **Reporter:** alexiaya
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insecure Direct Object References (IDOR), State Management Flaw, Settings Synchronization Bug, Data Integrity Issue
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Twitter Android app incorrectly overrides the 'Protect your Tweets' privacy setting when users modify unrelated Direct Message settings, causing protected tweets to become publicly visible. This occurs due to improper state synchronization between the mobile app and web platform, potentially exposing a user's previously protected content without their knowledge.

## Attack scenario
1. Attacker identifies target user with protected tweets on Twitter
2. Attacker convinces user to adjust Direct Message settings (e.g., 'Receive message requests' or 'Show read receipts') via social engineering
3. User opens Android app and navigates to Direct Messages settings tab
4. User clicks gear icon and modifies any of the mentioned DM settings
5. Android app sends update request that incorrectly resets protected tweets flag to unprotected status
6. Target user's entire tweet history becomes publicly visible without explicit consent or awareness

## Root cause
The Android app's settings synchronization logic fails to preserve the protected tweets setting when updating unrelated Direct Message preferences. The app likely sends a full settings object to the backend that either lacks the protected tweets parameter or explicitly overrides it with a cached/default value, bypassing the actual server-side protection setting.

## Attacker mindset
Low-effort privacy violation through manipulation of app behavior. Attacker leverages legitimate app functionality (DM settings) to trigger unintended side effects. Social engineering required makes this less reliable than direct exploitation, but highly effective for targeted deanonymization or exposure of sensitive tweets.

## Defensive takeaways
- Implement granular API endpoints for settings updates rather than monolithic settings objects to prevent accidental overwrites
- Use differential updates (PATCH/delta) instead of full object replacement (PUT) for settings synchronization
- Add server-side validation to preserve security-critical settings (like privacy controls) across all update operations
- Implement conflict resolution logic that prioritizes most restrictive privacy settings during sync conflicts
- Add audit logging for changes to privacy-critical settings with source tracking (web vs mobile)
- Include explicit confirmation prompts when privacy settings are modified via indirect operations
- Implement client-side state verification before submitting settings to prevent stale data overwrites
- Version settings schemas and handle backward compatibility without data loss

## Variant hunting
Test other privacy-sensitive settings (block lists, follower permissions, visibility toggles) for similar override behavior across different features
Check iOS app for identical vulnerability
Verify if other unrelated settings changes (profile updates, notification preferences) trigger the same issue
Test account sync across multiple Android devices to see if protection status diverges
Investigate whether the bug occurs with other protected account features (private replies, quote tweet settings)
Check for race conditions when rapidly toggling DM and privacy settings simultaneously

## MITRE ATT&CK
- T1190
- T1539
- T1491

## Notes
This is a state management vulnerability resulting from poor synchronization architecture between client and server. The mention that 'explicitly unsetting the protected tweets setting in the Android app' first makes the bug reproducible suggests the app maintains cached state that isn't properly invalidated. The lower social engineering barrier compared to email-change exploits still makes this a viable attack vector for targeted harassment or exposure campaigns. The bug demonstrates how secondary features (DM settings) can have unintended side effects on primary security controls.

## Full report
<details><summary>Expand</summary>

**Summary:** Protected Tweets setting overridden by Android app

**Description:** The Android app overrides the "Protect your Tweets" setting set from outside the app in some cases when changing other settings.

## Steps To Reproduce:

  1. Log in to an account with unprotected tweets on the Android app.
  1. Log in to the same account on mobile.twitter.com and turn on protected tweets.
  1. Confirm that the account's tweets are protected.
  1. In the Android app, go to the Direct Messages tab, click the gear icon and change a setting such as "Receive message requests" or "Show read receipts."
  1. The account's tweets are now unprotected.

If this does not work, you may have to first explicitly unset the protected tweets setting in the Android app before setting it elsewhere.

## Impact:

This can cause a user's tweets to unknowingly become public. It is possible this could be exploited by an attacker asking the user to change their settings but that is less likely to succeed than with the previous bug where only changing the email address was required.

## Impact

See above.

</details>

---
*Analysed by Claude on 2026-05-24*
