# Arbitrary File Access in Nextcloud Android App via Path Traversal Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 1408692 | https://hackerone.com/reports/1408692
- **Submitted:** 2021-11-23
- **Reporter:** luchua
- **Program:** Nextcloud
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Insufficient Input Validation, Privilege Escalation, Information Disclosure
- **CVEs:** CVE-2022-39210
- **Category:** uncategorised

## Summary
The Nextcloud Android app's file upload functionality contains an incomplete path validation check that only blocks '/data/data/' but not the equivalent '/data/user/0/' directory, allowing attackers to upload and leak arbitrary sensitive files including app preferences and private data. An attacker can create a malicious app that returns crafted file URIs pointing to Nextcloud's protected application directories, which are then uploaded to shared public folders when the user selects the file through the upload interface.

## Attack scenario
1. Attacker creates a malicious Android app containing an Activity that returns a file URI pointing to /data/user/0/com.nextcloud.client/shared_prefs/ (private preferences containing credentials and configuration)
2. Victim installs both Nextcloud Android client and the attacker's malicious app
3. Victim creates a shared/public folder in Nextcloud and navigates to it
4. Victim initiates file upload via '+' menu and selects 'upload content from other apps'
5. Victim selects the attacker's app from the chooser, which returns the malicious URI to Nextcloud's upload handler
6. FileUploader.java only checks startsWith('/data/data/') which passes for '/data/user/0/', allowing the private file to be uploaded and exposed in the public shared folder

## Root cause
The security patch in FileUploader.java uses an incomplete blocklist approach with startsWith('/data/data/'), failing to account for the functionally equivalent '/data/user/0/' symlink/path alias on Android. The check should either use canonical paths or implement allowlisting of safe directories (cache/temp only).

## Attacker mindset
An attacker with app installation capability exploits Android's file URI handling and Nextcloud's overly permissive upload mechanism to exfiltrate sensitive application data. The attacker leverages Android's intent system to inject malicious file paths that bypass weak string-based validation, targeting credentials and configuration stored in shared preferences.

## Defensive takeaways
- Use canonical file paths (File.getCanonicalPath()) to resolve symlinks and aliases before validation, preventing bypass via alternative paths
- Implement positive allowlisting rather than blocklisting - only permit uploads from app-safe directories like cache/ and temp/
- Validate that resolved paths do not contain application package names or /data/ prefixes for any context
- Restrict file picker results through Android's DocumentsProvider APIs with proper permission constraints
- Implement runtime checks using Context.getFilesDir() and Context.getCacheDir() as the only allowed upload sources
- Add security audit logging for attempted uploads from restricted paths

## Variant hunting
Test other Android data path aliases: /data/user_de/, /data/misc_de/, /mnt/user/0/, /storage/emulated/0/Android/data/
Check if symlink resolution is bypassed using encoded URIs or double encoding
Verify if the check applies to all upload methods (direct URI, content provider, file picker)
Test with other app package names to exfiltrate data from different applications
Examine if similar path validation exists in file selection dialogs or content provider handlers

## MITRE ATT&CK
- T1190
- T1003
- T1552
- T1583

## Notes
This is a bypass of CVE-like previous fix (report #1142918). The vulnerability demonstrates how Android's symlink system and path normalization can defeat naive string-based security checks. The attack requires victim interaction but achieves complete data exfiltration of private app data including potential credentials. The fix should prioritize canonical path resolution and allowlisting safe directories.

## Full report
<details><summary>Expand</summary>

## Summary:
The Android client of nextcloud (com.nextcloud.client) allows arbitrary file including protected/private files to be leaked through the file upload functionality.

## Steps To Reproduce:
A report [1142918 ](https://hackerone.com/reports/1142918) has been submitted for the vulnerability of leaking arbitrary protected files. NextCloud added [a fix](https://github.com/nextcloud/android/pull/8433/commits/97d6f2954c879f3bfebcd241993147bced5fd50b) on May 18, 2021, which added a check to the class src/main/java/com/owncloud/android/files/services/FileUploader.java:
```
        if (file.getStoragePath().startsWith("/data/data/")) {
            Log_OC.d(TAG, "Upload from sensitive path is not allowed");
            return;
        }
```

The fix checks whether a file to be uploaded has a path starting with "/data/data". However, the check is not sufficient. We can easily bypass this check using the path "/data/user/0/" e.g. "/data/user/0/com.nextcloud.client/".  A program to exploit this vulnerability can be:
```
public class EvilActivity extends AppCompatActivity {
    private static final String LOG_TAG = EvilActivity.class.getName();

    final static String PRIVATE_URI = "file:///data/user/0/com.nextcloud.client/shared_prefs/com.nextcloud.client_preferences.xml";

    @Override
    protected void onCreate(@Nullable Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_main);

        Log.d("heen", "EvilActivity started!");
        setResult(-1, new Intent().setData(Uri.parse(PRIVATE_URI)));
        finish();
    }
}
```

A working POC is as follows:
### 1. install and login nextcloud android client e.g. through the provider https://us.cloudamo.com
### 2. create a directory and set it 'shareable'
### 3.install the POC app with the program above
### 4. Navigate to the shareable directory in the step2, click '+', then choose "upload content from other apps"
### 5. Select "poc" then protected file will be uploaded to the shared folder, which is publicly shared and leaked.

## Supporting Material/References:
A sample screenshot with protected files uploaded and their content is:
{F1523976}
{F1523979}

  * [attachment / reference]
See attachments above

## Impact

Arbitrary sensitive file of the nextcloud android client can be leaked. To address this issue, disallow any file whose path has the package name but isn't in the temp or cache folder of nextcloud. 

Please investigate. Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
