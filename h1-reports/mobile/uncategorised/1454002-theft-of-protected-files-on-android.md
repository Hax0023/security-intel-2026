# Theft of Protected Files on Android via Exported Activity Intent Filter

## Metadata
- **Source:** HackerOne
- **Report:** 1454002 | https://hackerone.com/reports/1454002
- **Submitted:** 2022-01-19
- **Reporter:** n00b-cyborg
- **Program:** OwnCloud Android App
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper Input Validation, Insecure Inter-Process Communication, Path Traversal, Arbitrary File Access
- **CVEs:** None
- **Category:** uncategorised

## Summary
An exported Android activity (ReceiveExternalFilesActivity) in OwnCloud Android app v2.19 accepts SEND_MULTIPLE intent with file URIs without proper validation, allowing third-party apps to upload arbitrary files from the application's protected directory (/data/data/com.owncloud.android/). This enables theft of sensitive data including databases, cache, and user history files.

## Attack scenario
1. Attacker develops a malicious Android application that requests no special permissions
2. Attacker crafts an Intent with action android.intent.action.SEND_MULTIPLE targeting the exported ReceiveExternalFilesActivity
3. Attacker specifies file URIs pointing to protected OwnCloud directories, such as file:///data/data/com.owncloud.android/databases/filelist
4. Attacker invokes startActivity() to trigger the vulnerable activity within OwnCloud's context
5. OwnCloud processes the files without validation and uploads them to the configured server
6. Attacker retrieves the uploaded database files containing sensitive user data, credentials, or file history

## Root cause
The SEND_MULTIPLE intent filter in ReceiveExternalFilesActivity lacks input validation to restrict file access to protected application directories. While similar protection exists for the SEND intent filter, it was not implemented for SEND_MULTIPLE, creating an inconsistent security posture.

## Attacker mindset
An attacker seeks to bypass Android's sandbox isolation and access sensitive application data without user interaction or special permissions. The discovery that similar functionality (SEND vs SEND_MULTIPLE) has inconsistent security controls suggests a code review oversight, making this an attractive target for data exfiltration.

## Defensive takeaways
- Validate all file URIs received via intent extras to ensure they do not point to protected application directories
- Apply consistent security controls across all intent filters handling file operations (SEND, SEND_MULTIPLE, etc.)
- Implement a whitelist of allowed file paths or directories rather than relying on blacklist approaches
- Use FileProvider with proper permissions instead of accepting raw file:// URIs from untrusted sources
- Regularly audit exported components and their intent filters for security inconsistencies
- Consider making file-handling activities non-exported or requiring signature-level permissions
- Test both single and batch file operations with identical security controls

## Variant hunting
Search for other exported activities in OwnCloud and similar applications handling ACTION_SEND, ACTION_SEND_MULTIPLE, ACTION_VIEW, or custom file-handling intents. Check for path traversal via intent extras in activities accepting file URIs. Examine FileProvider implementations for overly permissive path configurations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552.001 - Unsecured Credentials
- T1005 - Data from Local System
- T1040 - Network Sniffing
- T1020 - Automated Exfiltration

## Notes
The vulnerability demonstrates a classic case of inconsistent security implementation across similar code paths. The PoC successfully bypasses Android's built-in file access protections by leveraging the application's own IPC mechanism. The fix is straightforward (copy existing SEND protections to SEND_MULTIPLE), suggesting this was an implementation oversight rather than a design flaw.

## Full report
<details><summary>Expand</summary>

There is an issue that allows to retrieve any files from protected directory of application - ```/data/data/com.owncloud.android/*```.
The issue is caused by exported activity ```com.owncloud.android.ui.activity.ReceiveExternalFilesActivity``` with intent filter ```android.intent.action.SEND_MULTIPLE``` that accepts URI of files for upload. Any 3rd-party application could start this activity and upload on server any files such as database file from protected directory in context of owncloud application.

Tested on latest stable version of app - 2.19.
Version of android - 11.

Java PoC:
```Java
StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
StrictMode.setVmPolicy(builder.build());
Intent intent = new Intent("android.intent.action.SEND_MULTIPLE");
intent.setClassName("com.owncloud.android", "com.owncloud.android.ui.activity.ReceiveExternalFilesActivity");
intent.setType("*/*");
intent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
ArrayList mStreamsToUpload = new ArrayList<>();
mStreamsToUpload.add(Uri.parse("file:///data/data/com.owncloud.android/databases/filelist"));
intent.putExtra("android.intent.extra.STREAM", mStreamsToUpload);
startActivity(intent);
```

**Mitigation:**
There is valid protection for preventing reading files from directory ```/data/data/com.owncloud.android/*``` in similar intent-filter ```android.intent.action.SEND```. Copy this protection for ```android.intent.action.SEND_MULTIPLE```.

## Impact

Potential attacker could steal files from protected directory of application for example files of databases, cache and history of files.

</details>

---
*Analysed by Claude on 2026-05-24*
