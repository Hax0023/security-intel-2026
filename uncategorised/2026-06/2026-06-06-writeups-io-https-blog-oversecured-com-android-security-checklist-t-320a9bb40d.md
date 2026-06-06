# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Android Ecosystem (General Security Research)
- **Bounty:** N/A - Educational/Security Research Article
- **Severity:** High
- **Vuln types:** Arbitrary File Disclosure, Insecure File Permissions, Implicit Intent Interception, Path Traversal, Insecure Data Storage
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
This writeup documents common Android developer mistakes that enable attackers to steal arbitrary files from private app directories through implicit intent interception and file exposure mechanisms. The primary attack vector exploits apps that handle implicit intents (GET_CONTENT, IMAGE_CAPTURE, etc.) and cache untrusted content into accessible storage locations without proper validation.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the target device that registers handlers for common implicit intents like android.intent.action.PICK or android.media.action.IMAGE_CAPTURE
2. Target application launches an implicit intent requesting file selection (e.g., for avatar upload)
3. Malicious app intercepts the implicit intent and becomes the default handler, responding with a crafted Uri pointing to the target app's private files
4. Target app processes the malicious Uri using getContentResolver().openInputStream() and caches content to external storage without validation
5. Attacker reads the cached private files from the public external storage directory (/storage/emulated/0 or /sdcard)
6. Sensitive data (tokens, credentials, user data) stored in app's private directory is exfiltrated to attacker's device

## Root cause
Android developers make critical assumptions about intent sources without validating Uri contents, fail to implement proper input validation when processing content from implicit intents, and store sensitive cached data in world-readable external storage directories instead of app-private storage protected by Android's security model.

## Attacker mindset
Exploit the trust model of implicit intents by registering malicious intent handlers that can intercept file selection requests. Leverage developers' common pattern of caching intent results without validation to redirect file reads to sensitive private directories. Use public storage as an exfiltration channel since most apps have READ_EXTERNAL_STORAGE permissions.

## Defensive takeaways
- Never assume implicit intent sources are trustworthy; validate all returned Uris and file content
- Avoid caching intent results in public/external storage; use only app-private directories under /data/user/0/{package_name}
- Implement strict Uri validation and check that returned Uris point to expected content (verify MIME type, file size, content hash)
- Use ContentResolver with proper permissions checking; verify the Uri's authority matches expected content providers
- Apply principle of least privilege for file permissions; never make private files world-readable
- For Android SDK 29+, properly implement scoped storage and avoid deprecated public storage patterns
- Audit all implicit intent handlers and consider using startActivityForResult() alternatives where possible
- Implement file integrity checks and sandboxing for cached content from external sources

## Variant hunting
Search for other implicit intent actions beyond the examples (CROP, EDIT, VIEW with custom schemes). Look for apps using deprecated storage APIs. Identify apps that process content:// Uris without validation. Find applications with shared android:sharedUserId that may expose each other's files. Test for path traversal in Uri processing (../ sequences). Examine apps handling file:// Uris from intents. Check for symlink-based attacks in cache directories.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548.001 - Abuse Elevation Control Mechanism: Setuid and Setgid
- T1555 - Credentials from Password Stores
- T1005 - Data from Local System
- T1011 - Exfiltration Over Other Network Medium
- T1041 - Exfiltration Over C2 Channel
- T1083 - File and Directory Discovery
- T1550 - Use Alternate Authentication Material

## Notes
This is an educational security research article from Oversecured's blog, not a specific bug bounty. The vulnerability pattern affects a broad class of Android applications handling implicit intents and file operations. The article emphasizes systematic patterns of developer mistakes rather than a single CVE. Oversecured's DAST scanner is highlighted as an automated solution for detecting these vulnerability classes. The root issue stems from the Android implicit intent system's design allowing any app to handle intents without strong identity verification.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
