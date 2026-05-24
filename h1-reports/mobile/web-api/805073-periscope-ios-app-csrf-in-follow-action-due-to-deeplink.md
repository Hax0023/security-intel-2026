# Periscope iOS App CSRF in Follow Action via Deeplink

## Metadata
- **Source:** HackerOne
- **Report:** 805073 | https://hackerone.com/reports/805073
- **Submitted:** 2020-02-26
- **Reporter:** mgf15
- **Program:** Periscope (Twitter/Meta)
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Cross-Site Request Forgery (CSRF), Insecure Deeplink Handling, Missing CSRF Tokens
- **CVEs:** None
- **Category:** web-api

## Summary
The Periscope iOS application fails to implement CSRF protections on the follow action when triggered via custom deeplinks (pscp://). An attacker can craft a malicious link or QR code that forces a user to follow an arbitrary account when clicked. This vulnerability exploits the app's trust in deeplink URIs without proper state validation or user confirmation.

## Attack scenario
1. Attacker identifies the unprotected deeplink handler for follow actions: pscp://user/<user-id>/follow
2. Attacker crafts a malicious deeplink or embeds it in a QR code pointing to a target profile they wish to promote
3. Attacker distributes the QR code or link via social media, messaging platforms, or embedded in web content
4. Victim clicks the link/QR code while authenticated in Periscope iOS app
5. The app processes the deeplink request without validating user intent or checking CSRF tokens
6. Victim's account automatically follows the attacker's target profile without explicit consent

## Root cause
The Periscope iOS app implements deeplink handlers that directly execute sensitive actions (follow) without: (1) CSRF token validation, (2) user confirmation dialogs, (3) state verification, or (4) SameSite cookie protections. The app trusts the deeplink scheme and assumes the user intentionally triggered the action.

## Attacker mindset
An attacker seeks to artificially inflate follower counts, manipulate social metrics, or force users to follow malicious accounts for phishing/scamming. This low-effort attack leverages widespread app usage and the naturalness of clicking links from trusted sources.

## Defensive takeaways
- Implement CSRF tokens for all state-changing operations, even in native apps
- Add user confirmation dialogs for sensitive actions triggered via deeplinks
- Validate deeplink source and implement deeplink signing/verification mechanisms
- Use short-lived, one-time tokens tied to specific deeplink operations
- Implement rate limiting on follow actions to detect automated abuse
- Add user activity logging and anomaly detection for rapid follow patterns
- Consider requiring additional authentication (biometric/PIN) for sensitive deeplinks
- Sanitize and validate all deeplink parameters before processing

## Variant hunting
Test other state-changing deeplinks (unfollow, like, comment, block, mute)
Check if deeplinks bypass authentication entirely or only work for authenticated users
Attempt to chain multiple deeplinks in sequence to trigger bulk actions
Test deeplinks with URL encoding/obfuscation to bypass link detection
Verify if deeplinks in iMessage, email, or Safari maintain session context
Examine if the vulnerability affects Android deeplinks (similar scheme: pscp://)
Test cross-app deeplink invocation from third-party apps
Check if the follow action generates notifications that might alert the user

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1021.001 - Remote Services: Remote Service Session Initiation

## Notes
This report references a prior CSRF vulnerability (report #583987) on the same platform, suggesting a pattern of inadequate CSRF protections. The deeplink mechanism is particularly dangerous because it blurs the line between in-app navigation and external attacks. Mobile app developers often overlook CSRF threats assuming native apps are inherently safer than web applications. The use of QR codes as distribution vectors is notable because users may scan codes without fully understanding the destination, making social engineering more effective.

## Full report
<details><summary>Expand</summary>

Summary

This issue is mainly in the Periscope iOS app against CSRF follow action using deeplink.

as the report  #583987 the CSRF work on iOS app 

POC 1

QR code to follow periscope profile 

`pscp://user/periscopeco/follow
`

███████

POC2 by kunal94

```
<!DOCTYPE html>
<html>
<a href="pscp://user/<any user-id>/follow">CSRF DEMO</a>
</html>
```
video
█████████

## Impact

CSRF Follow against any user in periscope iOS app

</details>

---
*Analysed by Claude on 2026-05-24*
