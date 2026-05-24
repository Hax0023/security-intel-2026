# Android Content Provider Exposes Password-Protected Share Password Hashes in Nextcloud Android Client

## Metadata
- **Source:** HackerOne
- **Report:** 242727 | https://hackerone.com/reports/242727
- **Submitted:** 2017-06-23
- **Reporter:** netranger
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Insecure Data Storage, Exported Content Provider, Inadequate Access Controls, Information Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The Nextcloud Android app v1.4.3 exports a content provider (com.owncloud.android.providers.FileContentProvider) that is globally accessible to any app on the device, exposing bcrypt password hashes for password-protected shared files and folders. An attacker can query this provider through a malicious app to extract share passwords and tokens for offline cracking, bypassing server-side brute force protections.

## Attack scenario
1. Attacker develops a malicious Android app that requests minimal permissions or bundles this functionality with a legitimate-seeming app
2. Victim installs the malicious app on their device that also has Nextcloud Android client installed
3. Malicious app queries the exported content provider using content://org.nextcloud/shares URI
4. App extracts bcrypt password hashes and share tokens from the provider's response
5. Attacker performs offline password cracking on the hashes using GPU acceleration or rainbow tables
6. Upon successful crack, attacker uses the recovered password and token to access protected shares on the Nextcloud server

## Root cause
The FileContentProvider was declared with exported=true in AndroidManifest.xml without implementing proper access controls or using permission-based restrictions, allowing any installed app to access sensitive authentication data that should not be available at the application level.

## Attacker mindset
An attacker recognizes that on-device data is often more accessible than server-side protections. By extracting password hashes locally, they circumvent network-based rate limiting and brute force defenses, enabling offline cracking with more computational freedom. The combination of hash + token creates a complete attack vector for unauthorized share access.

## Defensive takeaways
- Never export content providers unless absolutely necessary; use exported=false as default
- Implement permission-based access controls for any exported providers using custom permissions
- Avoid storing authentication credentials, password hashes, or tokens on-device if the server is the authoritative source
- Conduct regular security audits of AndroidManifest.xml for overly permissive component declarations
- Use Android's secure storage mechanisms (KeyStore) for sensitive data that must be stored locally
- Implement runtime permission checks in content provider query methods to verify caller identity
- Design APIs to keep sensitive data server-side; minimize what is synced to client devices
- Consider whether user file metadata (names) should be accessible to all apps on the device

## Variant hunting
Search for similar exported content providers in other cloud storage and file-sharing Android apps. Check for other Nextcloud components exporting data without restriction. Review any exported broadcast receivers or services that might leak authentication tokens or user metadata. Investigate whether other password-protected share implementations store hashes client-side.

## MITRE ATT&CK
- T1418 - Software Discovery
- T1552 - Unsecured Credentials
- T1555 - Credentials from Password Stores
- T1040 - Network Sniffing (local inter-process)
- T1110 - Brute Force (offline password cracking)
- T1555.004 - Credentials from Password Stores: Android Credential Store

## Notes
This vulnerability demonstrates the principle of 'not exporting by default' on Android. The reporter correctly notes this falls within inter-app attack scenarios which Nextcloud's threat model considers 'minimal risk', but it represents a meaningful compromise for users sharing sensitive content. The vulnerability is particularly dangerous because: (1) bcrypt hashes speed up offline cracking compared to raw passwords, (2) the share token is also exposed, providing both components needed for exploitation, and (3) legitimate apps from the app store can be repackaged to include this malicious functionality. The suggested mitigation of simply removing exported=true is straightforward but may require identifying any legitimate use cases for the provider first.

## Full report
<details><summary>Expand</summary>

## Summary
Nextcloud Android client v1.4.3 has a globally available content provider which exposes the bcrypt password hashes for password protected shared files and folders. 

## Description
Android apps can use a content provider to handle storage and retrieval of data. Content providers that are exported allow any app on the same device to access their content. The Nextcloud Android app has an exported content provider called com.owncloud.android.providers.FileContentProvider (authority content://org.nextcloud) which holds sensitive information, including the share identifiers (aka tokens) and bcrypt password hashes for the user's password protected shares. An attacker can, through a malicious app on the device, query the provider and extract the share password hashes for offline cracking. This effectively bypasses any brute force share password protections implemented by the Nextcloud server and speeds up the cracking process, increasing the chances of share password recovery. Combined with the share identifier/token, if an attacker successfully cracks a password, he/she has enough information to access the protected share.

## Reproduction

Install the Nextcloud Android app on a device and sign in. Ensure some files are shared via password-protected links so you'll have some data to view. :)

From here there are 2 ways to reproduce the issue:

Method 1:
Connect an Android device with USB debugging enabled to a computer with the Android Studio or development tools installed. Run the following commands on a command prompt (Windows) or terminal (Linux):
- adb devices //start adb if not already running
- adb shell //get a shell on the target device
- content query --uri content://org.nextcloud/shares //use Android's 'content' program to query the vulnerable provider

The provider returns data including 1) the password hashes of shares protected with a password (the value of the 'shate_with' field) and 2) the token identifier used to access the share on the Nextcloud server (value of the 'token' field). 

Method 2:
The following app (among others), Content Provider Helper, allows you to query content providers on the device: https://play.google.com/store/apps/details?id=com.jensdriller.contentproviderhelper

Install and open it, tap the settings button in the upper right, tap 'Add Content Provider', add 'org.nextcloud/shares' (content:// is already prefilled), then tap 'Add'. Tap 'Query' and view the returned data. Since this 3rd party app can view the provider's data, it helps illustrate the fact that any app on the device can also access the provider and it's data.
 
Other queries return additional information, including file and folder names:
content://org.nextcloud/file
content://org.nextcloud/dir/[dir ID]

## Screenshots

- 1_settings - navigate to add provider in the Content Provider Helper app
- 2_add_provider - adding the vulnerable provider in the helper app
- 3_ready_to_query - provider added, tap Query here
- 4_results - results from the provider. The start of the hashes are visible in the far right column. Only shares that have been password-protected have a hash entry.
- 5_token - view showing the share identifier/token
- 6_cli - retrieving the same information via an adb shell with the 'content' command
- 7_files - results from querying content://org.nextcloud/file. Filenames are leaked which may or may not be considered sensitive information.

## Impact/Notes
This vulnerability allows a malicious app to extract the password protect hashes and send them to an attacker, who can attempt to crack them offline instead of brute-forcing the Nextcloud server. This speeds up the cracking process and increases the chance of password recovery, though password recovery is not guaranteed.

The vulnerability also allows a malicious app to retrieve the names of the user's Nextcloud files synced with the app. File names may or may not be considered sensitive information, not sure if this is noteworthy or not.

The Nextcloud threat model (https://nextcloud.com/security/threat-model/) mentions attacks involving other Android apps as 'minimal risk'. I understand if this vulnerability is considered an acceptable risk but thought it best to let you decide that.

Testing was primarily done on a Motorola Moto G running Android 6.0.1, Nextcloud Android app v1.4.3.

## Possible Mitigation
I do not see a valid reason to export the vulnerable content provider and make it accessible to any app on the device. One mitigation solution, therefore, is to mark the content provider as not exported by removing 'exported=true' from the com.owncloud.android.providers.FileContentProvider <provider> declaration in the AndroidManifest.xml file. This would prevent other apps from accessing the provider.

If there is a valid reason to export the provider, do share hashes need to be kept on the device? The Nextcloud server seems to be the one comparing the provided share password with the hash if someone attempts to access it. Not storing the hash in the content provider is another possible fix.

If this vulnerability is considered an acceptable risk, then no action is needed. :)

</details>

---
*Analysed by Claude on 2026-05-24*
