# Android Security Checklist: Theft of Arbitrary Files

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Android Security Research (Oversecured Blog)
- **Bounty:** N/A - Security Research Article
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Insecure File Handling, Implicit Intent Interception, Path Traversal, Exposure of Private Files
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
The article documents common Android file theft vulnerabilities where developers improperly handle file exchanges between apps, allowing attackers to steal sensitive data from private application directories. The primary attack vector involves implicit intents where malicious apps can intercept file operations and return malicious URIs or manipulate file paths to access private data.

## Attack scenario (step by step)
1. Attacker identifies target app that uses implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.) to request files from other apps
2. Attacker creates malicious app that registers to handle the same intent actions as legitimate file managers or camera apps
3. Target app launches implicit intent to pick a file, unaware of which app will handle it
4. Attacker's malicious app intercepts the intent and returns a Uri pointing to the target app's private directory instead of public files
5. Target app processes the returned Uri without proper validation and caches content from attacker-controlled path
6. Attacker reads the cached file from public directory or exploits path traversal to access arbitrary private files

## Root cause
Developers fail to validate file origins and paths when processing results from implicit intents, trusting that returned URIs are legitimate and safe. Additionally, insufficient path validation allows traversal attacks, and improper use of public cache directories exposes sensitive data.

## Attacker mindset
An attacker recognizes that Android's implicit intent system creates a trust boundary that apps often fail to validate. By registering for standard file-related intents, an attacker can hijack file selection flows and manipulate which files the target app accesses, gaining access to private data without requiring the target app to have explicit vulnerabilities.

## Defensive takeaways
- Never trust URIs returned from implicit intent results without validation of their origin and content
- Implement strict path validation to prevent directory traversal attacks using ../ sequences
- Store sensitive data only in private app directories (/data/user/0/{package_name}), never in public storage
- Use explicit intents with specific package names instead of implicit intents where possible
- Validate file permissions and ownership before processing files from external sources
- Implement content URI permissions (android:grantUriPermissions) to limit file access scope
- Use FileProvider for secure file sharing instead of exposing raw file system paths
- Never cache sensitive data in external cache directories that are world-readable
- Implement input validation for all file paths to detect and reject suspicious URIs
- Use scoped storage (Android 10+) to further restrict file access

## Variant hunting
['Search for apps using ACTION_PICK, ACTION_GET_CONTENT, ACTION_IMAGE_CAPTURE without URI validation', 'Identify apps caching external intent results to world-readable locations', 'Look for file copy operations from intent-provided URIs without path sanitization', 'Find apps using getExternalCacheDir() or getExternalFilesDir() for sensitive data', 'Search for relative path traversal in file operations (File manipulation with ../ sequences)', 'Identify apps with exported components handling file intents without proper validation', "Look for content provider implementations that don't properly validate requested file paths", 'Find apps storing authentication tokens or credentials in public directories']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1526 - Exposure of Sensitive Information
- T1040 - Traffic Capture or Redirection
- T1578 - Modify Cloud Compute Infrastructure
- T1552 - Unsecured Credentials

## Notes
This writeup focuses on systemic Android development mistakes rather than a single CVE. It's an educational resource from Oversecured highlighting prevalent vulnerability classes in Android apps. The article emphasizes that file theft attacks commonly exploit implicit intent handling and insufficient validation of file paths. Developers should treat all files in public directories as untrusted and implement defense-in-depth with multiple validation layers.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
