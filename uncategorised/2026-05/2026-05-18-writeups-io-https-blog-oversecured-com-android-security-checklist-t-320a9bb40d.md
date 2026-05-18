# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** General Android Security Research
- **Bounty:** Not specified (educational/checklist article)
- **Severity:** high
- **Vuln types:** Arbitrary File Access, Implicit Intent Interception, Insecure File Permissions, Content Provider Exposure, Path Traversal, Symlink Attacks
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications commonly expose sensitive files through unsafe handling of implicit intents and improper file storage practices, allowing attackers to steal arbitrary files from private directories. The vulnerability stems from apps requesting file access via implicit intents without validating the content source, and then caching received content in publicly accessible directories. This enables a malicious application to intercept these intents and return paths to sensitive files, or exploit symlink/path traversal to access private data.

## Attack scenario (step by step)
1. Attacker analyzes target app and identifies it uses implicit intents like ACTION_PICK or IMAGE_CAPTURE to request file access
2. Attacker creates malicious app that registers intent filters for the same actions with higher priority
3. When victim app launches the implicit intent, attacker's app intercepts it instead of legitimate file manager/camera app
4. Attacker's app returns a Uri pointing to sensitive files in the target app's private directory (/data/user/0/{package_name})
5. Vulnerable app's onActivityResult() blindly processes the returned Uri and caches content to external storage or processes it insecurely
6. Attacker reads the exposed files from public storage or leverages symlinks/path traversal in the copy operation to access private data

## Root cause
Developers fail to validate the source and safety of Uris returned from implicit intent results, assume intent handlers are trustworthy, and implement insecure file operations without proper validation of paths or symlink resolution.

## Attacker mindset
An attacker seeks to steal sensitive user data, tokens, credentials, or personal information stored in private app directories. They recognize that many apps use implicit intents naively and can inject malicious responses. By registering higher-priority intent filters or exploiting symlink/path traversal in copy operations, they can exfiltrate data with minimal user interaction.

## Defensive takeaways
- Never trust implicit intent results; validate the source and type of returned Uris
- Use explicit intents with known system components when possible, or use Intent#resolveActivity() to verify intent can be handled safely
- Implement strict file path validation to prevent path traversal and symlink attacks when copying files
- Use canonical paths (File#getCanonicalPath()) and verify files exist within expected directories
- Store sensitive data only in private app directories (/data/user/0/{package_name}), never in public storage
- Implement proper file permissions (MODE_PRIVATE) and avoid world-readable/writable files
- Use content providers with permission enforcement instead of exposing raw file access
- On SDK 29+, leverage scoped storage to restrict file access
- Validate MIME types and file extensions match expected values
- Use cryptographic integrity checks on cached files to detect tampering

## Variant hunting
Search for apps using Intent.ACTION_PICK, Intent.ACTION_GET_CONTENT, android.media.action.IMAGE_CAPTURE, android.media.action.VIDEO_CAPTURE, or custom intent actions without explicit intent specification. Hunt for onActivityResult() implementations that process Uri without validation, copy operations without canonical path checks, and files written to getExternalCacheDir() or public storage. Examine apps with android:sharedUserId for cross-app file access. Look for symlink creation in world-writable directories and improper use of File constructor with untrusted paths.

## MITRE ATT&CK
- T1190
- T1552
- T1083
- T1005
- T1040
- T1566

## Notes
This is an educational security checklist article from Oversecured highlighting common Android file theft patterns. The vulnerability class affects numerous production apps due to widespread developer misunderstanding of implicit intents and Android file security models. The article emphasizes that apps exchanging files with other apps are high-risk targets. Oversecured's automated scanning can detect these patterns through static analysis of intent usage and file operations. The vulnerability requires no special permissions for the attacking app beyond standard installation, making it easily exploitable in the wild.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
