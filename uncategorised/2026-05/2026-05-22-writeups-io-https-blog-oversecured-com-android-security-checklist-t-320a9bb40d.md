# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Android Ecosystem / General Security Research
- **Bounty:** Not specified - Educational/Research Article
- **Severity:** HIGH
- **Vuln types:** Arbitrary File Access, Insecure File Permissions, Implicit Intent Interception, Path Traversal, Exposure of Sensitive Data, Content Provider Misconfiguration
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android developers commonly expose private application files to theft through insecure file handling practices, particularly when processing results from implicit intents like ACTION_PICK and IMAGE_CAPTURE. Attackers can intercept implicit intents, return malicious URIs pointing to private files, or exploit improper file permissions to access sensitive data stored in the app's private directories.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the target device that declares intent filters matching common implicit actions (ACTION_PICK, ACTION_IMAGE_CAPTURE, etc.)
2. Victim app launches an implicit intent requesting user to select a file or capture an image, expecting a legitimate app to handle it
3. Malicious app intercepts the implicit intent and becomes the default handler or wins the intent resolution priority
4. Instead of returning a legitimate file URI, the malicious app returns a content:// URI pointing to a private file in the victim app's /data/user/0/{package_name} directory
5. Victim app blindly processes the returned URI using ContentResolver, copying the private file content to accessible locations or exposing it directly
6. Attacker reads the stolen private files containing sensitive data like tokens, user credentials, or personal information

## Root cause
Developers fail to validate URIs returned from implicit intent results and assume all returned content is legitimate user-selected files. Additionally, insufficient file permission validation, storing sensitive data in externally accessible cache directories, and lack of proper sandboxing between apps with shared user IDs create exploitation opportunities.

## Attacker mindset
An attacker recognizes that implicit intents are a fundamental Android mechanism with predictable behavior. By registering for common intent actions, they can become the default handler and control the URI that gets returned. The attacker exploits developer assumptions that returned URIs are safe, knowing most developers implement minimal validation. The goal is to exfiltrate high-value private data like authentication tokens or personal information that developers mistakenly believe are protected by Android's sandboxing.

## Defensive takeaways
- Validate all URIs returned from implicit intent results before processing - verify the URI authority and path are from expected sources
- Never blindly copy content from returned URIs to external cache directories without verifying the source
- Use explicit intents with known safe apps instead of implicit intents when possible
- Implement proper file permissions using MODE_PRIVATE for sensitive files and avoid storing secrets in shared external directories
- Do not store sensitive data in /storage/emulated/0 or app cache directories accessible to other apps
- Use FileProvider with proper path restrictions to securely share files with other apps
- Be cautious with apps sharing the same android:sharedUserId - treat such apps as potential adversaries
- Regularly audit file access patterns and implement runtime permission checks
- Use Android's modern Scoped Storage APIs (SDK 29+) with appropriate access restrictions

## Variant hunting
['Search for calls to startActivityForResult() with ACTION_PICK, ACTION_IMAGE_CAPTURE, ACTION_VIDEO_CAPTURE, ACTION_GET_CONTENT, or ACTION_CROP without URI validation', 'Identify ContentResolver.openInputStream() calls on unsanitized URIs from intent results', 'Find File.copy() or Files.copy() operations on URIs from implicit intent results without source verification', 'Search for file operations in onActivityResult() that process intent data without authority/scheme validation', 'Look for sensitive files stored in getExternalCacheDir() or getExternalFilesDir()', "Identify apps with android:sharedUserId declarations that may access each other's private files", 'Find implicit intent handlers that return URIs without proper content access restrictions', 'Search for hardcoded file paths or predictable URI construction in content providers', 'Look for Intent.getData() usage without null checks or URI validation', 'Identify apps storing tokens, passwords, or PII in world-readable files']

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1083
- T1566
- T1555
- T1652
- T1649

## Notes
This is an educational security research article from Oversecured that documents a systematic class of vulnerabilities rather than a single CVE. The article emphasizes that implicit intent interception combined with insufficient URI validation creates a widespread attack vector on Android. The vulnerability class affects apps across multiple categories and is difficult to detect without static/dynamic analysis tools. The research highlights the gap between Android's security model assumptions (that developers properly validate external input) and actual developer practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
