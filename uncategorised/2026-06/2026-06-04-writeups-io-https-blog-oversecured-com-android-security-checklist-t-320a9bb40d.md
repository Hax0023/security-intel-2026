# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Android Applications (General Security Guidance)
- **Bounty:** N/A - Educational/Advisory Article
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Implicit Intent Interception, Path Traversal, Insecure File Permissions, Content Provider Exposure, Symlink Attack
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
This security checklist identifies common Android file theft vulnerabilities where developers expose private files to unauthorized access through implicit intents and insecure file operations. Attackers can intercept implicit intents, exploit path traversal, or leverage symlinks to steal sensitive data from an app's private directories by copying files to public storage or manipulating content resolution.

## Attack scenario (step by step)
1. Attacker installs malicious app on target device with ability to handle implicit intents (e.g., ACTION_PICK, ACTION_GET_CONTENT)
2. Vulnerable app launches implicit intent to request file selection from user
3. Malicious app intercepts intent and responds with crafted Uri pointing to sensitive file in victim app's private directory
4. Vulnerable app receives Uri and copies content to external cache directory without validation
5. Attacker's app or any third-party app reads the copied file from public storage
6. Sensitive data (tokens, user data, credentials) is exfiltrated

## Root cause
Developers trust content returned from implicit intent responses without proper validation, fail to validate Uri schemes and paths, copy sensitive files to world-readable locations, and don't implement proper file access controls or use secure alternatives like FileProvider with restricted permissions.

## Attacker mindset
An attacker seeks to intercept standard Android intents to redirect file access to private directories, exploiting the assumption that implicit intent responders return legitimate user-selected files. The attacker leverages the file caching mechanism and public storage accessibility to exfiltrate sensitive application data.

## Defensive takeaways
- Never trust Uri returned from implicit intent responses - validate scheme, authority, and path
- Use explicit intents when possible instead of implicit intents
- Implement FileProvider with restricted permissions (not world-readable) for file sharing
- Store sensitive files only in private app directories (/data/user/0/{package_name})
- Avoid caching sensitive content in external storage or external cache directories
- Validate and sanitize all file paths to prevent path traversal attacks
- Use content:// Uri scheme instead of file:// scheme
- Check Uri authority against expected values before processing
- Never follow symlinks when accessing files
- Use Scoped Storage (Android 11+) and enforce access restrictions
- Implement proper file permission checks and use SELinux policies

## Variant hunting
Hunt for: (1) startActivityForResult calls with implicit intents combined with onActivityResult file operations; (2) External cache directory usage with copy operations; (3) File:// Uri handling in content resolution; (4) Implicit intent handlers for standard actions (PICK, GET_CONTENT, IMAGE_CAPTURE); (5) FileProvider definitions with grant_uri_permission children lacking proper path restrictions; (6) Symlink creation in world-writable directories; (7) SharedUserId declarations enabling cross-app file access; (8) World-readable file permissions via FileProvider or intent extras

## MITRE ATT&CK
- T1005
- T1040
- T1041
- T1071
- T1566

## Notes
This is an educational/advisory article from Oversecured rather than a traditional bug bounty report. It provides systematic guidance on file theft vulnerabilities in Android apps. The vulnerability chain relies on combining implicit intent interception with insecure file handling patterns common in Android development. The article emphasizes that private file theft typically requires two steps: (1) copying private files to public locations, and (2) reading them from public storage. Multiple attack vectors exist including implicit intent interception, content provider misconfiguration, path traversal, and symlink exploitation. Oversecured's DAST capabilities are highlighted as capable of detecting these vulnerability patterns automatically.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
