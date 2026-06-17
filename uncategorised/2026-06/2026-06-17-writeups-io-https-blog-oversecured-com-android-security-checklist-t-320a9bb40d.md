# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Android Security Research (Oversecured)
- **Bounty:** Not specified - Educational/Research Article
- **Severity:** high
- **Vuln types:** Arbitrary File Access, Implicit Intent Interception, Insecure File Sharing, Content Provider Exposure, Path Traversal, Improper File Permissions
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications frequently expose sensitive files through insecure handling of implicit intents and file sharing mechanisms. Attackers can intercept implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.) or exploit apps with shared user IDs to access private application data stored in /data/user/0/{package_name} directories. This writeup demonstrates common file theft vulnerabilities and exploitation techniques in Android apps.

## Attack scenario (step by step)
1. Attacker installs a malicious app on target device that registers handlers for common implicit intents like ACTION_PICK or ACTION_IMAGE_CAPTURE
2. Victim app launches an implicit intent to request file selection or image capture without properly validating the response source
3. Malicious app intercepts the intent and returns a crafted Uri pointing to sensitive files in the victim app's private directory
4. Victim app processes the Uri and copies/caches the sensitive content to external storage or accessible location
5. Attacker's app reads the exposed sensitive data from external cache directory or shared storage
6. Alternatively, attacker can use shared android:sharedUserId to directly access another app's private files

## Root cause
Developers fail to implement proper intent source validation, assume implicit intents are only handled by trusted system apps, don't restrict file access permissions, and carelessly copy content from untrusted Uri sources to world-readable locations without sanitization.

## Attacker mindset
Exploit the Android framework's design philosophy of implicit intents and content sharing to intercept file requests. Target apps that blindly trust returned Uris without validating source legitimacy. Leverage public storage and shared user IDs as exfiltration vectors for sensitive data stored in private directories.

## Defensive takeaways
- Use explicit intents with specific component names instead of implicit intents when possible
- Validate the source and legitimacy of responses from implicit intents before processing
- Never cache sensitive data to external storage or public directories
- Implement proper file permissions - store secrets in /data/user/0/{package_name} only
- Use FileProvider with restricted path permissions for inter-app file sharing
- Avoid using android:sharedUserId unless absolutely necessary
- Sanitize and validate all file paths to prevent traversal attacks
- Use scoped storage (SDK 29+) and restrict file access to minimum required paths
- Encrypt sensitive data before any caching or sharing operation
- Implement runtime permission checks for file access

## Variant hunting
Search for apps using Intent actions: ACTION_PICK, IMAGE_CAPTURE, VIDEO_CAPTURE, ACTION_GET_CONTENT, ACTION_OPEN_DOCUMENT. Look for patterns where apps call startActivityForResult() followed by file operations on returned Uris. Examine external cache directories (getExternalCacheDir()) and public storage usage. Check for shared user IDs across multiple apps. Audit FileProvider implementations for overly permissive path definitions. Analyze content:// Uri handling without source validation.

## MITRE ATT&CK
- T1190
- T1552
- T1083
- T1005
- T1040
- T1598
- T1526

## Notes
This is an educational security research article from Oversecured highlighting systemic Android security issues. The vulnerability relies on design patterns that are extremely common in production Android apps. The article emphasizes that file theft is typically achieved by moving private files to public directories rather than direct access, highlighting the importance of strict file permission controls. Multiple exploitation vectors exist (implicit intent interception, shared user IDs, path traversal) making this a widespread class of vulnerabilities affecting many applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
