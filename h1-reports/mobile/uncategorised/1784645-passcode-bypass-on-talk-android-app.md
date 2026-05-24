# Passcode bypass on Talk Android app via notification click

## Metadata
- **Source:** HackerOne
- **Report:** 1784645 | https://hackerone.com/reports/1784645
- **Submitted:** 2022-11-26
- **Reporter:** ctulhu
- **Program:** Nextcloud
- **Bounty:** not specified
- **Severity:** medium
- **Vuln:** authentication bypass, access control weakness, insecure direct object reference
- **CVEs:** CVE-2023-22473
- **Category:** uncategorised

## Summary
The Nextcloud Talk Android app (v15.0.2 RC1) allows attackers to bypass passcode protection by clicking on incoming message notifications. An attacker with physical access to an unlocked device can directly access the app without entering the required passcode, leading to unauthorized access to files and conversations.

## Attack scenario
1. Attacker obtains physical access to a victim's Android device that has Nextcloud Talk installed with passcode protection enabled
2. Attacker waits for or causes an incoming message notification to appear on the device's lock screen or notification bar
3. Attacker clicks on the message notification to open the Talk app
4. The app opens directly to the conversation without prompting for the passcode
5. Attacker gains full access to the Talk app, including message history and conversations
6. Attacker can then navigate to Nextcloud files and other sensitive data accessible through the app

## Root cause
The notification handler in the Talk Android app does not enforce passcode authentication when launching the app from a notification intent. The authentication check is likely bypassed or not triggered when the app is opened through the notification deep link rather than through normal app launch.

## Attacker mindset
An opportunistic attacker with brief physical access (e.g., unattended device, lost phone) seeks quick unauthorized access to communications and files. The notification-based bypass provides an easy alternative to brute-forcing or other time-consuming attack methods.

## Defensive takeaways
- Always enforce authentication checks on all app entry points, including notifications and deep links
- Re-authenticate users when accessing sensitive features, regardless of how the app was launched
- Implement notification content filtering to avoid leaking sensitive information in notifications
- Consider disabling direct app access via notifications when passcode protection is enabled
- Implement session timeout and re-authentication requirements for sensitive operations
- Add security tests to verify passcode enforcement across all app navigation paths

## Variant hunting
Test other notifications (alerts, reminders, system messages) for similar bypasses
Check if deep linking to other features (settings, file browser, calendar events) bypasses authentication
Test if sharing links or other intent-based shortcuts bypass passcode protection
Verify if back/navigation gestures from notifications can access protected areas
Check other Nextcloud mobile apps for similar notification-based authentication bypasses
Test if biometric authentication can be bypassed through the same notification vector

## MITRE ATT&CK
- T1190
- T1556
- T1021

## Notes
This is a local attack requiring physical device access, limiting real-world impact but still significant for devices that may be temporarily unattended. The fix likely requires modifying the notification intent handler to trigger passcode verification before processing the deep link. The vulnerability suggests incomplete security architecture where different code paths have inconsistent authentication enforcement.

## Full report
<details><summary>Expand</summary>

## Summary:
It is possible to bypass the passcode protection in nextcloud android talk by clicking the notification of a message.

Talk App Android version: ```15.0.2 RC1```

## Steps To Reproduce:

1. Create two users
1. Using User A login it to the web interface while User B on Talk App Android
1. Using User B setup the passcode protection in settings
1. Using User A send a message to User B
1. Wait for the notification and click it

## Supporting Material/References:

█████

## Impact

To exploit this the attacker needs to have a physical access to the  target's device which makes it severity to medium. 
Due to the bypass of passcode an attacker is able to access the user's nextcloud files and view conversations.

████████

</details>

---
*Analysed by Claude on 2026-05-24*
