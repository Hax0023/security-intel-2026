# Changing email address on Twitter for Android unsets "Protect your Tweets"

## Metadata
- **Source:** HackerOne
- **Report:** 472013 | https://hackerone.com/reports/472013
- **Submitted:** 2018-12-26
- **Reporter:** alexiaya
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Improper State Management, Privacy Setting Bypass, Logic Error
- **CVEs:** None
- **Category:** uncategorised

## Summary
Verifying a new email address on a Twitter account via the Android app causes the "Protect your Tweets" (account privacy) setting to be automatically disabled, exposing previously private tweets to the public. This occurs as a side effect of the email verification workflow and persists until the user manually re-enables the privacy setting.

## Attack scenario
1. Attacker tricks user via phishing email into changing their account email address, claiming a security issue needs resolution
2. User logs into Twitter Android app and navigates to account settings to change email
3. User enters attacker-controlled or redirected email address and initiates change
4. Twitter sends verification email to new address; user clicks verification link from Android device
5. Android app processes email verification and inadvertently resets the "Protect your Tweets" setting to disabled state
6. User's previously private tweets are now publicly visible without user awareness or consent

## Root cause
The Android app's email verification workflow contains a logic error that fails to preserve the user's existing privacy settings (specifically the 'Protect your Tweets' flag) when processing email address changes. The verification handler likely resets account settings to default values or fails to merge privacy settings with the updated email configuration.

## Attacker mindset
An attacker would exploit user trust through social engineering (phishing) to trick victims into changing their email addresses. The attacker doesn't need direct account access; instead, they rely on the user's action combined with the app's buggy behavior to automatically expose sensitive information. This represents a low-effort, high-impact privacy violation.

## Defensive takeaways
- Implement comprehensive integration testing for account modification workflows that verify all user settings are preserved across state changes
- Require explicit user confirmation before modifying privacy-critical settings, even as side effects of other operations
- Audit all code paths that update account settings to ensure privacy settings are explicitly maintained and never reset unintentionally
- Add logging and monitoring for unexpected changes to privacy settings to detect when they're modified as side effects
- Consider implementing a privacy setting snapshot/restore mechanism during account modifications
- Educate users about legitimate email change processes to improve phishing awareness

## Variant hunting
Test other account modification workflows (password change, phone number change, security key addition) for unintended privacy setting changes
Check if other privacy-related settings (DM restrictions, follower visibility, location data) are affected by email verification
Verify if this behavior occurs on web platform or only Android; test iOS app for similar issues
Check if other account settings are reset during email change (notification preferences, language, accessibility settings)
Test whether account reactivation after deactivation preserves privacy settings
Investigate if email verification through different methods (resend email, change email again) triggers similar reset behavior

## MITRE ATT&CK
- T1190
- T1566
- T1199

## Notes
The vulnerability has a moderate severity because it requires either account compromise or social engineering to trigger, but the impact is significant as it results in privacy violation affecting all of a user's tweets. The bug demonstrates insufficient state management in mobile app development. No bounty amount was disclosed in the report, suggesting this may have been resolved before HackerOne's bounty program expansion or was handled through their VRT.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** Verifying email address on Twitter for Android unsets "Protect your Tweets"

**Description:** Verifying a new email address on a Twitter account in the Android app causes the "Protect your Tweets" option to be unset, resulting in the user's tweets being made publicly visible.

## Steps To Reproduce:

(Add details for how we can reproduce the issue)

  1. Log in to a Twitter account on the Android app.
  2. Make sure the app is set to handle twitter.com links.
  3. Change the email address on the account.
  4. Verify the new email address by clicking the link in the email from the same Android device.

## Impact: This can lead to a user's private tweets being exposed to the public until they realize this happened. An attacker does not need to be involved as they would need to have access to the user's account to change the email, but a user could be tricked into changing their email if an attacker sent them a phishing email telling them to do so.
## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, etc.)

## Impact

This can lead to a user's private tweets being exposed to the public until they realize this happened. An attacker does not need to be involved as they would need to have access to the user's account to change the email, but a user could be tricked into changing their email if an attacker sent them a phishing email telling them to do so.

</details>

---
*Analysed by Claude on 2026-05-24*
