# Path Traversal Bypass in OwnCloud Android - Exported Activity Allows Arbitrary File Access

## Metadata
- **Source:** HackerOne
- **Report:** 377107 | https://hackerone.com/reports/377107
- **Submitted:** 2018-07-04
- **Reporter:** shell_c0de
- **Program:** OwnCloud Android
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Insufficient Path Validation, Exported Activity Abuse, Arbitrary File Read
- **CVEs:** None
- **Category:** web-api

## Summary
The exported activity ReceiveExternalFilesActivity in OwnCloud Android implements insufficient path validation that can be bypassed using alternative path symlinks. An attacker can exploit this to read arbitrary protected files from the application's data directory, including databases containing sensitive user information.

## Attack scenario
1. Attacker crafts a malicious Android application with required permissions
2. Malicious app constructs an Intent targeting the exported ReceiveExternalFilesActivity
3. Instead of using the blocked /data/data/ path, attacker specifies /data/user/0/ alternative path pointing to same application data
4. OwnCloud processes the request, bypassing incomplete path validation checks
5. Attacker gains access to protected files including filelist database and other sensitive application data
6. Attacker extracts account credentials, file lists, sync history, and other confidential information

## Root cause
The application implemented path validation that only checks for the /data/data/ prefix but fails to account for alternative system paths like /data/user/0/ which resolve to the same protected directories. The validation logic is incomplete and does not use canonical path resolution before verification.

## Attacker mindset
An adversary seeking to compromise user accounts would target exported activities accepting file URIs. By discovering the path validation mechanism, they recognize that alternative Linux filesystem paths could bypass the check. This requires knowledge of Android filesystem structure and URI handling.

## Defensive takeaways
- Always use canonical path resolution (File.getCanonicalPath()) before validating paths
- Implement allowlist-based validation instead of blacklist approaches
- Validate resolved paths against expected directories, not just prefixes
- Minimize exported activities; use explicit permission checks for file access
- Do not accept arbitrary file URIs from external intents without strict validation
- Consider using Content Providers with restricted access instead of direct file URIs
- Implement defense-in-depth: validate at URI receipt, path resolution, and file access layers
- Test path validation with known Android filesystem symlinks and aliases

## Variant hunting
Check for other exported activities accepting file paths or URIs
Test with /data/user_de/ paths on work profile devices
Verify validation in content providers serving files
Check for relative path traversal using ../ sequences combined with alternative paths
Test symbolic link following in path validation logic
Examine other intent filters that might process file-like URIs
Look for similar path validation patterns in other Android applications

## MITRE ATT&CK
- T1190
- T1001_003
- T1057
- T1555_003

## Notes
This is a classic example of incomplete input validation. The developers attempted to fix path traversal but only blacklisted one specific path without understanding the full scope of alternative paths that could reference the same location. The vulnerability demonstrates why canonical path resolution is essential in security-critical code. The use of StrictMode.VmPolicy bypass in the PoC suggests the attacker may face file access restrictions that were intentionally added as a secondary defense layer.

## Full report
<details><summary>Expand</summary>

Hi. I have found an issue which allows to retrieve any files from `/data/data/com.owncloud.android/*` directory. The problem is in exported activity `com.owncloud.android.ui.activity.ReceiveExternalFilesActivity` which accepts a URI to download files. I see that you've added verification path `/data/data/`
You can bypass the verification using specifying an alternative path: `/data/user/0/com.owncloud.android/` 
Malicious code:
```java
        StrictMode.VmPolicy.Builder builder = new StrictMode.VmPolicy.Builder();
        StrictMode.setVmPolicy(builder.build());
        Intent intent = new Intent("android.intent.action.SEND");
        intent.setClassName("com.owncloud.android", "com.owncloud.android.ui.activity.ReceiveExternalFilesActivity");
        intent.setType("*/*");
        intent.setFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
        intent.putExtra("android.intent.extra.STREAM", Uri.parse("file:///data/user/0/com.owncloud.android/databases/filelist"));
        startActivity(intent);
```
###How to Fix
Add an alternative path to the folder check

## Impact

This vulnerability can get a complete account, malware can access everything, including, file database and history.

</details>

---
*Analysed by Claude on 2026-05-24*
