# Android Security Checklist: Theft of Arbitrary Files via Implicit Intent Handling

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** General Android Security Research
- **Bounty:** Not specified (Educational/Research)
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Insecure Intent Handling, Path Traversal, Improper Content Provider Usage, Symlink Attack, Race Condition
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android developers frequently introduce file theft vulnerabilities by improperly handling implicit intents and caching files from untrusted content providers into predictable locations. Attackers can exploit these patterns to steal arbitrary files from an app's private directories by returning malicious URIs that point to sensitive data or by using symlinks in publicly writable directories. The vulnerability class demonstrates multiple attack vectors including improper implicit intent handling, race conditions during file operations, and insufficient validation of file paths.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the target device that registers a handler for common implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.)
2. Victim app launches an implicit intent requesting user to select a file, triggering the attacker's malicious app via the activity chooser
3. Malicious app returns a malicious Uri pointing to sensitive files in the victim app's private directory (/data/user/0/{package_name}) or crafts a path traversal URI
4. Victim app's onActivityResult() receives the malicious Uri and processes it via getContentResolver().openInputStream()
5. Victim app caches the file content to external storage or processes it, or attacker leverages symlinks in predictable cache directories to redirect writes
6. Attacker reads the stolen files from the public directory or monitors the race condition window to access sensitive data

## Root cause
The vulnerability stems from a combination of factors: (1) Implicit intents do not validate the source of returned Uris, (2) Apps blindly trust content from intent results without path validation, (3) Caching sensitive data to external directories without proper access controls, (4) Predictable file paths in public/external cache directories enable symlink attacks, (5) Race conditions between file creation and permission setting, and (6) Insufficient validation of returned URIs before accessing them with openInputStream()

## Attacker mindset
An attacker recognizes that implicit intent handling is a common Android pattern trusted by developers. By registering handlers for standard actions and returning crafted Uris, the attacker exploits the assumption that the selected app is trustworthy. The attacker focuses on races, symlinks, and path traversal to circumvent simple validations. This is an elegant attack because it leverages the app's own legitimate functionality against it.

## Defensive takeaways
- Validate all Uris returned from implicit intents - check the authority and path before processing
- Avoid storing sensitive data in external cache directories; use private app directories (/data/user/0/{package_name}) exclusively
- If external storage is necessary, use private app directories (getExternalFilesDir()) which are protected by Android's permission model
- Implement proper file permissions immediately after file creation, not before
- Use canonical file paths and verify they do not escape intended directories (check for .., symlinks, etc.)
- Consider using FileProvider with restricted paths instead of exposing arbitrary file access
- Implement race condition protections by using atomic file operations and temporary file patterns
- Request the minimum necessary permissions and validate intent sources when possible
- Store truly sensitive data (tokens, keys) only in encrypted shared preferences or encrypted files
- Use content encryption for sensitive files even in private directories as defense-in-depth

## Variant hunting
Hunt for: (1) calls to startActivityForResult() with ACTION_PICK, IMAGE_CAPTURE, VIDEO_CAPTURE, or CROP intents, (2) usage of getContentResolver().openInputStream() without Uri validation, (3) files written to getExternalCacheDir() or getExternalFilesDir() without immediate permission setting, (4) File operations without canonical path checks, (5) predictable cache file names in public directories, (6) symlinks in app cache paths, (7) usage of hardcoded paths in onActivityResult(), (8) missing or improper Uri authority validation, (9) apps with android:sharedUserId allowing cross-app file theft

## MITRE ATT&CK
- T1430
- T1533
- T1040
- T1041
- T1005
- T1083
- T1057
- T1071

## Notes
This is a systematic security checklist article from Oversecured covering multiple file theft attack vectors rather than a single vulnerability disclosure. The writeup emphasizes that implicit intent handling combined with improper file caching creates exploitable conditions in many Android apps. The vulnerability is particularly dangerous because it affects normal, expected Android functionality. Modern Android (SDK 29+) introduces some mitigations, but apps must still validate intent sources and protect sensitive files. The article serves as both an attacker's guide and a developer's security hardening manual.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
