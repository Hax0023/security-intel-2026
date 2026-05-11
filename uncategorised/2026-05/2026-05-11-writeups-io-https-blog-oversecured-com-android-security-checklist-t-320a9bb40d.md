# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Access Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Oversecured (Security Research/Educational)
- **Bounty:** Not applicable - Security research/checklist article
- **Severity:** high
- **Vuln types:** Insecure File Handling, Implicit Intent Interception, Path Traversal, Arbitrary File Read, Insecure Content Provider, Symlink Following, World-Readable File Permissions
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications frequently expose sensitive files through insecure file handling practices when exchanging files with other apps via implicit intents and content providers. Attackers can intercept implicit intents, exploit symlinks, or abuse file permissions to steal private application data stored in internal directories. The article documents common developer mistakes and exploitation techniques that allow arbitrary file theft from app private storage.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the same Android device as the target application
2. Target app launches an implicit intent (e.g., ACTION_PICK) to request a file from the user, expecting a legitimate file manager or camera app to handle it
3. Attacker's malicious app intercepts the implicit intent by registering for the same action and returns a crafted content URI pointing to the target app's private files
4. Target app receives the malicious URI and processes it, copying content from the attacker-controlled path into its cache or temporary storage
5. Attacker leverages symlinks, path traversal, or predictable file paths to redirect file operations to sensitive private data (tokens, user data, credentials)
6. Attacker reads the stolen files from public directories or via the compromised content provider

## Root cause
Developers fail to properly validate and sanitize URIs received from implicit intent results, do not implement proper file access controls, and do not verify the legitimacy of responding applications. Additionally, improper handling of symlinks, world-readable file permissions, and insecure content provider implementations allow arbitrary file access.

## Attacker mindset
An attacker seeks to compromise user data and sensitive information stored in private app directories. By understanding Android's implicit intent mechanism and file-sharing patterns, the attacker can intercept legitimate requests and redirect them to sensitive files. The attacker exploits developer assumptions that only legitimate apps will respond to intents, and leverages common coding patterns where apps blindly copy content from received URIs without validation.

## Defensive takeaways
- Validate and sanitize all URIs received from implicit intent results before processing them
- Use explicit intents and intent filters with specific package names when communicating with known apps rather than implicit intents
- Implement strict file access controls - never store sensitive data in world-readable locations or with permissive file permissions
- Avoid following symlinks when accessing files; validate that file paths resolve to expected locations
- Use FileProvider with restricted path permissions instead of exposing raw file system access through content providers
- Implement content provider access controls and verify requestor identity before sharing sensitive data
- Store sensitive data only in app private directories (/data/user/0/{package_name}) with restrictive permissions
- Do not copy user-selected content from implicit intents to predictable or public file paths without validation
- Use Android's built-in scoped storage (API 29+) to restrict file access to app-specific directories
- Implement runtime permission checks and request only necessary permissions

## Variant hunting
Search for: (1) Apps using ACTION_PICK, ACTION_GET_CONTENT, ACTION_IMAGE_CAPTURE without URI validation; (2) Custom content providers without proper access controls; (3) Files stored with MODE_WORLD_READABLE or MODE_WORLD_WRITEABLE flags; (4) Symbolic link following in file operations; (5) Implicit intent handlers that respond without package verification; (6) Cache directories using predictable or user-controlled paths; (7) Apps sharing user IDs (android:sharedUserId) without proper isolation; (8) External storage writes to shared directories

## MITRE ATT&CK
- T1005 - Gather Data from Local System
- T1040 - Network Sniffing (Intent Interception)
- T1057 - Process Discovery
- T1083 - File and Directory Discovery
- T1087 - Account Discovery
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1039 - Data from Local System

## Notes
This is a comprehensive security checklist article from Oversecured documenting common Android file theft vulnerabilities. The article uses code examples to illustrate vulnerable patterns and emphasizes that implicit intents are a primary attack vector. The vulnerability class affects widespread Android development practices and requires developer education and architectural changes to mitigate effectively.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
