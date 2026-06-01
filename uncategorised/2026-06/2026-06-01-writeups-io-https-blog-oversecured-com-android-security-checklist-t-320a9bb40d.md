# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Handling

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** General Android Security Research
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Insecure File Handling, Implicit Intent Interception, Path Traversal, Privilege Escalation via sharedUserId
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Developers commonly make mistakes when handling file exchanges between Android apps through implicit intents and file operations, allowing attackers to steal sensitive files from private application directories. The vulnerability typically involves apps caching content from implicit intent results without proper validation, enabling malicious apps to intercept the intent, return crafted URIs with path traversal sequences, or manipulate file operations to access private data.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the same device as the vulnerable target app
2. Target app launches an implicit intent (e.g., ACTION_PICK) to let user select a file
3. Malicious app registers itself as a handler for that implicit intent action
4. When user selects content through malicious app, attacker returns a crafted URI pointing to target app's private directory (e.g., using path traversal like ../../../data/user/0/com.target.app/files/sensitive.txt)
5. Target app receives the URI and processes it using ContentResolver without validating the path
6. Target app copies the arbitrary file to its external cache directory or other accessible location
7. Attacker reads the stolen file from the public storage location

## Root cause
Insufficient validation of URIs returned from implicit intents, improper file path handling, and unsafe caching of content to external/public directories without sanitization. Apps trust that implicit intent results are safe without verifying the returned URI points to legitimate user-selected content.

## Attacker mindset
An attacker with app installation capability seeks to exfiltrate sensitive data (tokens, credentials, user data) from target applications. They exploit the Android inter-app communication mechanism by posing as a legitimate content provider, leveraging developer assumptions that implicit intent results are trustworthy.

## Defensive takeaways
- Always validate and sanitize URIs returned from implicit intents before processing
- Avoid caching content from implicit intents to external/public directories
- Use content providers with proper permission checks and URI validation
- Implement strict path validation to prevent traversal attacks (reject ../ sequences)
- Store sensitive data only in private app directories (/data/user/0/{package_name})
- Use explicit intents instead of implicit intents when possible
- Be cautious with sharedUserId - understand that apps sharing the same ID can access each other's private files
- Implement Content URI permission validation using FLAG_GRANT_READ_URI_PERMISSION granularly
- Never trust file paths from external sources without comprehensive validation
- Use automated scanning tools to detect file theft vulnerabilities during development

## Variant hunting
Search for similar patterns in other Android apps: (1) implicit intent handlers that return URIs without validation, (2) file copy operations using untrusted URI sources to accessible directories, (3) apps using sharedUserId without understanding inter-app access implications, (4) content providers with overly permissive URI matching patterns, (5) use of getExternalCacheDir() or /sdcard paths for sensitive data caching

## MITRE ATT&CK
- T1190
- T1552
- T1005
- T1087

## Notes
This is a systematic security checklist article from Oversecured documenting common file theft patterns in Android apps rather than a single CVE. The vulnerability class is widespread and affects many apps. The article emphasizes developer education and use of automated scanning for detection. The code example shows a typical vulnerable pattern where implicit intent results are processed without URI validation before caching to external storage.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
