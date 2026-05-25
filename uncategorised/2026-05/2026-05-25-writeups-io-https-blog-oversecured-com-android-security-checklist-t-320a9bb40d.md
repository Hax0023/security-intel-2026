# Android Security Checklist: Theft of Arbitrary Files

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Android Developer Community / Oversecured Blog
- **Bounty:** Not specified - Educational article
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Insecure File Handling, Implicit Intent Misuse, Content Provider Abuse, Symlink/Path Traversal, Insecure File Permissions
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
This article catalogs common Android file handling vulnerabilities that allow attackers to steal arbitrary files from app private directories. Developers frequently expose sensitive data through improper handling of implicit intents, symlinks, file permissions, and insecure export of private files to public storage.

## Attack scenario (step by step)
1. Attacker identifies app using implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.) to request file operations
2. Attacker creates malicious app that responds to the implicit intent with crafted Uri pointing to private app data
3. Vulnerable app caches or processes content from untrusted Uri without validation
4. Attacker leverages symlinks or path traversal in exported directories to redirect access to private files
5. Attacker reads cached private files from public storage (/sdcard or external cache)
6. Sensitive data (tokens, user data, credentials) is exfiltrated from victim app

## Root cause
Developers trust implicit intent responses without validating Uri origin or content, fail to properly validate file paths, and store sensitive data in world-readable locations or implement inadequate access controls on exported content providers.

## Attacker mindset
Exploit trust chains between apps and standard Android APIs; abuse symmetric inter-app communication patterns; leverage symlinks and path traversal to redirect file access; focus on apps handling sensitive operations (authentication, media, user data).

## Defensive takeaways
- Never trust Uris returned from implicit intents - validate origin and content
- Store sensitive data only in private app directories (/data/user/0/{package}), never in shared storage
- Validate and sanitize all file paths to prevent symlink and directory traversal attacks
- Use Intent filters carefully and prefer explicit intents when possible
- Implement strict file permissions (mode 0600) for sensitive files
- Never export content providers unnecessarily; use exported=false by default
- Use FileProvider with restricted paths for file sharing instead of exposing raw URis
- Avoid caching untrusted content in predictable locations
- Regularly audit file access patterns and storage locations with tools like Oversecured

## Variant hunting
['Content providers with path_list patterns allowing directory traversal', 'Apps using symlinks in world-writable directories (cache, temp)', 'Implicit intent handlers in third-party keyboards, launchers, and system apps', 'File manager apps granting access to arbitrary paths via content:// schemes', 'Applications caching files from startActivityForResult without Uri validation', 'Shared user ID apps exploiting sibling app file access', 'Camera/gallery apps returning malicious Uris to vulnerable clients', 'Android backup systems exfiltrating private file contents']

## MITRE ATT&CK
- T1190
- T1083
- T1005
- T1533
- T1021
- T1552
- T1078

## Notes
Article is from Oversecured blog (May 2022) and serves as educational guidance for Android developers. Emphasizes systematic approaches to finding file theft vulnerabilities through intent interception and path manipulation. Mentions Oversecured's automated scanning capabilities as detection method. Focus on implicit intents as primary attack vector, but broader checklist covers multiple file handling anti-patterns.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
