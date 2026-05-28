# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Handling

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Android Developer Security
- **Bounty:** N/A - Security Research Article
- **Severity:** HIGH
- **Vuln types:** Arbitrary File Access, Intent Interception, Path Traversal, Insecure File Sharing, Data Exfiltration
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications commonly mishandle file operations when responding to implicit intents, allowing attackers to trick apps into copying sensitive files from private directories to publicly accessible locations. Developers frequently cache content from intent results without proper validation, enabling malicious apps to intercept implicit intents and return URIs pointing to arbitrary files on the device.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the target device that registers handlers for common implicit intent actions (ACTION_PICK, IMAGE_CAPTURE, VIDEO_CAPTURE, etc.)
2. Victim's vulnerable app launches an implicit intent to select a file/photo, allowing any registered app to handle the request
3. Malicious app intercepts the intent and returns a content URI pointing to a sensitive file in the victim app's private directory (/data/user/0/{package_name})
4. Victim app blindly processes the returned URI without validation and copies its content to external cache or public storage
5. Attacker's app reads the copied file from public storage, extracting tokens, user data, credentials, or other sensitive information
6. Attacker gains unauthorized access to victim app's sensitive data or can impersonate the user

## Root cause
Developers fail to validate content URIs returned from implicit intent handlers and unsafely copy content to publicly accessible locations without verifying the source legitimacy. The implicit intent mechanism allows any installed app to handle requests, creating an attack surface when combined with unsafe file caching practices.

## Attacker mindset
An attacker recognizes that Android's implicit intent system is designed for app interoperability but exploits this trust model by registering malicious intent handlers that return arbitrary file paths. The attacker understands that most developers blindly trust intent results and cache them to external storage, making it trivial to exfiltrate sensitive data without requiring explicit file access permissions.

## Defensive takeaways
- Never trust URIs returned from implicit intent handlers without validation of the source/authority
- Store sensitive data only in private app directories (/data/user/0/{package_name}), never in external storage or public directories
- Implement strict URI validation and whitelist expected content providers before processing results
- Use explicit intents when possible instead of implicit intents to avoid interception
- Never cache untrusted content in world-readable locations; use internal app storage with restricted permissions
- Implement signature verification for content providers if exchanging data between trusted apps
- For file sharing, use FileProvider with restrictive path exposure instead of file:// URIs
- Validate file paths for traversal attacks and ensure they don't escape intended directories
- Use Android's Scoped Storage (SDK 30+) to restrict file access and prevent arbitrary file operations

## Variant hunting
Hunt for: (1) startActivityForResult() calls with implicit intents followed by onActivityResult() processing URIs - examine if returned content is cached to external storage without validation; (2) ContentResolver.openInputStream() on user-controlled URIs without source verification; (3) File copy operations in onActivityResult() that use returned URIs directly; (4) Apps with READ_EXTERNAL_STORAGE or MANAGE_EXTERNAL_STORAGE permissions that handle file intents; (5) Custom URI schemes that might be intercepted; (6) SharedUserId implementations that allow inter-app file access; (7) World-readable cache directories or SharedPreferences; (8) File operations in WebView callbacks that accept external input

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (social engineering to install malicious app)
- T1005 - Data from Local System
- T1041 - Exfiltration Over C2 Channel
- T1020 - Automated Exfiltration
- T1083 - File and Directory Discovery
- T1552 - Unsecured Credentials
- T1550 - Use Alternate Authentication Material

## Notes
This is a comprehensive security research article from Oversecured documenting systematic file theft vulnerabilities in Android apps. The vulnerability chain relies on two factors: (1) the implicit intent interception capability inherent to Android's design, and (2) developer negligence in validating and safely handling returned URIs. The article emphasizes that private file theft typically occurs when apps help attackers copy files to public storage, rather than attackers directly accessing private directories. The code example shows a realistic vulnerable pattern where processPickedUri() caches external content without validating its origin. Organizations should use Oversecured's DAST scanning or equivalent security analysis to identify these patterns during development.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
