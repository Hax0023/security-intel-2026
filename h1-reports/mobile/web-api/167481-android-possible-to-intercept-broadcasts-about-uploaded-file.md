# Android - Unprotected Broadcast Interception of File Upload Events

## Metadata
- **Source:** HackerOne
- **Report:** 167481 | https://hackerone.com/reports/167481
- **Submitted:** 2016-09-11
- **Reporter:** bagipro
- **Program:** Nextcloud Android
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Improper Access Control, Insecure Inter-Process Communication, Information Disclosure, Broadcast Intent Interception
- **CVEs:** None
- **Category:** web-api

## Summary
The Nextcloud Android application sends unprotected broadcasts containing sensitive file upload information, account details, and file metadata using Context.sendStickyBroadcast(). Malicious applications can intercept these broadcasts by registering high-priority receivers to capture sensitive data about user uploads before legitimate receivers process them.

## Attack scenario
1. Attacker creates a malicious app with a BroadcastReceiver exported with high priority (999)
2. Attacker registers intent filters for FileUploader actions: UPLOAD_START, UPLOAD_FINISH, UPLOADS_ADDED
3. User installs malicious app alongside legitimate Nextcloud app
4. When Nextcloud user uploads files, the system delivers broadcasts to all registered receivers
5. Due to high priority, malicious receiver intercepts broadcasts first, capturing account info and file details
6. Attacker logs sensitive information about user files, accounts, and upload activities for further exploitation

## Root cause
Nextcloud Android uses global Context.sendStickyBroadcast() to communicate upload events instead of LocalBroadcastManager, which restricts broadcasts to the application process. Unprotected broadcasts are vulnerable to interception by any app with permission to receive broadcasts and ability to set high priority filters.

## Attacker mindset
An attacker seeks to passively harvest intelligence about user file operations and account information. By intercepting broadcasts with high-priority receivers, they can gain knowledge of what files users upload, when uploads occur, and associated account credentials without triggering notifications. This intelligence supports further attacks like spear-phishing or account targeting.

## Defensive takeaways
- Replace all Context.sendStickyBroadcast() calls with LocalBroadcastManager.sendBroadcast() to restrict broadcasts to application process only
- Replace all Context.registerReceiver() calls with LocalBroadcastManager.registerReceiver()
- Remove sticky broadcast patterns and use LocalBroadcastManager.removeStickyBroadcast() replacement where needed
- Never broadcast sensitive data (account information, file names, file paths) through global intents
- Use protected broadcasts with explicit intent targets or inter-app communication mechanisms that validate caller identity
- Audit all broadcast actions for sensitive information exposure
- Implement permission checks on broadcast receivers if global broadcasts are necessary
- Consider using app-internal event bus libraries instead of broadcasts for internal communication

## Variant hunting
Search for other sendBroadcast/sendStickyBroadcast calls carrying user/account identifiers
Identify broadcasts for sync operations, authentication events, or storage operations that may contain sensitive metadata
Check SyncFolderHandler and other service classes for unprotected broadcast patterns
Look for sticky broadcasts that may remain in system after app crashes, increasing exposure window
Examine other Nextcloud client apps (iOS, desktop) for similar inter-process communication vulnerabilities
Test with broadcast monitoring tools to identify all broadcasts sent by the application

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1557 - Man-in-the-Middle
- T1040 - Traffic Sniffing
- T1491 - Defacement

## Notes
This vulnerability is particularly dangerous because broadcasts remain sticky and can be intercepted even after the sending event completes. The use of high-priority intent filters is a well-documented Android security bypass technique. LocalBroadcastManager was the recommended Android framework solution at the time of filing (deprecated in favor of LiveData/Flow in modern Android development). The vulnerability affects all users of the application simultaneously without requiring app installation via Play Store filtering.

## Full report
<details><summary>Expand</summary>

Hi.
There are the moments of sending unprotected broadcasts
https://github.com/nextcloud/android/blob/master/src/com/owncloud/android/files/services/FileUploader.java#L1170
https://github.com/nextcloud/android/blob/master/src/com/owncloud/android/files/services/FileUploader.java#L1116
https://github.com/nextcloud/android/blob/master/src/com/owncloud/android/files/services/FileUploader.java#L1136
https://github.com/nextcloud/android/blob/600225c7c9684295bfdb43bcf7d078113b8b2f73/src/com/owncloud/android/services/SyncFolderHandler.java#L186
https://github.com/nextcloud/android/blob/600225c7c9684295bfdb43bcf7d078113b8b2f73/src/com/owncloud/android/services/SyncFolderHandler.java#L201
etc
A malware can simply create a receiver:
```xml
<receiver android:exported="true" android:enabled="true" android:name=".InterceptReceiver">
	<intent-filter android:priority="999">
		<action android:name="FileUploader.UPLOAD_START"/>
		<action android:name="FileUploader.UPLOAD_FINISH"/>
		<action android:name="FileUploader.UPLOADS_ADDED"/>
	</intent-filter>
</receiver>
```
(and other actions)
And receive the broadcasts **first** than your own receivers
More info about priority here
https://developer.android.com/guide/topics/manifest/intent-filter-element.html#priority

It will disclose info about account, file info, etc

The one thing you should do is to change all calls of ```Context.sendStickyBroadcast``` on ```LocalBroadcastManager.sendBroadcast``` and all calls of ```Context.registerReceiver``` on ```LocalBroadcastManager.registerReceiver```
https://developer.android.com/reference/android/support/v4/content/LocalBroadcastManager.html
instead on using ```removeStickyBroadcast(intent);```


</details>

---
*Analysed by Claude on 2026-05-24*
