# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Handling

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** General Android Security Research / Oversecured
- **Bounty:** Not specified (educational/research article)
- **Severity:** high
- **Vuln types:** Arbitrary File Access, Insecure File Handling, Implicit Intent Interception, Path Traversal, Privilege Escalation via Content Providers
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android developers frequently expose sensitive files stored in private app directories through improper handling of implicit intents and file operations. Attackers can intercept implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.) or exploit file copying mechanisms to access and exfiltrate arbitrary private files from vulnerable applications.

## Attack scenario (step by step)
1. Attacker installs a malicious app on the same Android device as the target vulnerable app
2. Attacker registers intent filters for common actions like ACTION_PICK or IMAGE_CAPTURE to intercept implicit intents
3. Victim's app calls startActivityForResult() with an implicit intent seeking file selection or media capture
4. Malicious app intercepts the intent and returns a specially crafted content URI pointing to sensitive files in the victim app's private directory
5. Victim app processes the returned URI and caches/copies the sensitive file content
6. Attacker reads the exposed sensitive data from public directories or monitors file system changes to extract private information

## Root cause
Developers fail to validate returned content URIs from implicit intent responses, assume returned content is user-selected rather than attacker-controlled, and improperly handle file copying without proper permission/path validation. The trust boundary between apps is weak when implicit intents are used without proper result validation.

## Attacker mindset
Exploit the Android inter-process communication model and implicit intent mechanism to make vulnerable apps inadvertently expose their private files. Focus on high-value targets storing tokens, credentials, and user data. Leverage the fact that users install multiple apps and don't realize the security implications.

## Defensive takeaways
- Always validate content URIs returned from implicit intent responses before processing
- Use explicit intents whenever possible, or enforce strict intent filters with specific package names
- Implement URI scheme validation and reject unexpected content providers
- Store sensitive data in app's private directory (/data/user/0/{package_name}) with appropriate encryption
- Avoid copying files from untrusted sources to public/external storage without validation
- Use FileProvider for safely sharing files between apps with restricted access
- Implement sandboxing and capability-based security models for file access
- Apply the principle of least privilege for file permissions and intent handling
- Regularly scan code for implicit intent usage and validate all returned data

## Variant hunting
Look for: (1) All startActivityForResult() calls with implicit intents and validation gaps in onActivityResult(); (2) File copy operations from external sources into private storage without path canonicalization; (3) Content URI processing without scheme/authority validation; (4) Shared user IDs allowing cross-app file access; (5) World-readable file permissions on sensitive data; (6) Use of deprecated file access APIs (Environment.getExternalStorageDirectory()); (7) Implicit intent broadcasts of sensitive data; (8) Custom content providers with overly permissive path matching

## MITRE ATT&CK
- T1190
- T1526
- T1552
- T1083
- T1566
- T1204

## Notes
This is an educational security checklist article from Oversecured demonstrating common Android file theft vulnerabilities. The article emphasizes the difference between private (/data/user/0/) and public (/sdcard/) storage, with focus on how implicit intents create a critical attack surface. The Android security model's reliance on application package boundaries and the ability to intercept implicit intents without explicit recipient specification makes this a systemic vulnerability class affecting numerous applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
