# Android Security Checklist: Theft of Arbitrary Files

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** General Android Security Research
- **Bounty:** Not specified (Educational/Research)
- **Severity:** HIGH
- **Vuln types:** Arbitrary File Read, Content Provider Exposure, Implicit Intent Interception, Insecure File Handling, Path Traversal, Unauthorized File Access
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications commonly expose private files through insecure handling of implicit intents and file sharing mechanisms. Attackers can intercept implicit intents like ACTION_PICK, ACTION_GET_CONTENT, and custom actions to provide malicious URIs or intercept content providers, allowing theft of sensitive data from private app directories (/data/user/0/{package_name}).

## Attack scenario (step by step)
1. Attacker installs malicious app on same Android device as target app
2. Target app launches implicit intent (e.g., ACTION_PICK) to request file selection from user
3. Malicious app registers same intent filter and intercepts the implicit intent
4. Malicious app responds with URI pointing to sensitive private file or uses content provider to expose internal files
5. Target app receives the malicious URI and caches/processes the content
6. Attacker reads sensitive data from target app's private directories or processes exposed content

## Root cause
Developers use implicit intents without verifying the source or safety of returned URIs, blindly trusting content from any responding app. Inadequate validation of file paths and improper use of content providers expose private file system locations. File copying operations using untrusted URIs can access arbitrary locations through path traversal or symlink attacks.

## Attacker mindset
An attacker looks for apps that use implicit intents to interact with file managers, media apps, or capture actions. They create a malicious app that responds to these intents and provides crafted URIs or content providers that leak sensitive data. The attacker exploits the trust relationship implicit intents create—the target app assumes the returned URI is legitimate and safe.

## Defensive takeaways
- Never use implicit intents for sensitive file operations; prefer explicit intents with known safe apps
- Validate and sanitize all URIs received from implicit intent results before processing
- Implement strict file path validation to prevent directory traversal attacks
- Use scoped storage (SDK 30+) and enforce stricter file access policies
- Store sensitive data only in private app directories (/data/user/0/{package_name}), never in external storage
- Implement Content Provider security by validating query paths and using permission-based access control
- Use FileProvider for sharing files with specific permissions rather than exposing broad file access
- Monitor and restrict apps with shared userId to prevent cross-app file theft
- Implement runtime checks to verify responding app identity when using implicit intents
- Regularly audit file handling code and test with malicious apps during security testing

## Variant hunting
['Search for startActivityForResult with implicit intents (ACTION_PICK, ACTION_GET_CONTENT, IMAGE_CAPTURE, VIDEO_CAPTURE, ACTION_CROP)', 'Find onActivityResult implementations that process received URIs without validation', 'Identify custom implicit intent actions that may lack proper security controls', 'Search for Content Provider implementations with overly broad path permissions', 'Look for file operations using external cache directories or public storage without proper restrictions', 'Find instances of symlink following in file operations', 'Identify apps sharing userId (android:sharedUserId) that handle sensitive files', 'Search for hardcoded file paths or predictable cache file locations', 'Look for copy/read operations on URIs without MIME type validation']

## MITRE ATT&CK
- T1190
- T1040
- T1020
- T1087
- T1526
- T1005

## Notes
This is an educational security checklist article by Oversecured describing common Android file theft vulnerabilities. The article emphasizes the distinction between private (/data/user/0/{package_name}) and public (/storage/emulated/0) file storage and how implicit intents create trust boundaries that attackers exploit. The vulnerability class affects millions of Android apps and represents a systemic issue in Android development practices. The article serves as both a vulnerability guide and a catalog of weaknesses developers should avoid when building Android applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
