# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Handling

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** General Android Ecosystem (Educational)
- **Bounty:** N/A - Educational Security Research
- **Severity:** High
- **Vuln types:** Arbitrary File Access, Implicit Intent Interception, Insecure File Handling, Content Provider Abuse, Path Traversal, Privilege Escalation via sharedUserId
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android applications frequently expose private files to theft through improper handling of implicit intents and insecure file operations. Attackers can intercept implicit intents like ACTION_PICK and ACTION_GET_CONTENT to return malicious URIs pointing to sensitive app data, or exploit file copying functionality to extract private files into public directories. The vulnerability affects apps storing sensitive data (tokens, user credentials) in private directories that are then inadvertently exposed through standard Android file-sharing mechanisms.

## Attack scenario (step by step)
1. Attacker creates a malicious app with intent filters matching standard actions (android.intent.action.PICK, android.intent.action.GET_CONTENT, etc.)
2. Victim app launches an implicit intent requesting file selection (e.g., for avatar upload or file attachment)
3. System presents attacker's app as a handler option; attacker's app is selected or set as default handler
4. Attacker's app intercepts the intent and returns a malicious content URI pointing to sensitive files in victim app's private directory (e.g., /data/user/0/com.victim/cache/tokens.txt)
5. Victim app blindly processes the returned URI and copies sensitive data to external storage or processes it unsafely
6. Attacker reads the exposed sensitive files from public storage or accesses them via the content URI

## Root cause
Applications fail to validate the source and content of data returned from implicit intent handlers, assuming returned URIs are benign. Additionally, insecure file copying patterns (especially to external cache directories) expose sensitive data. The security model allowing any app to handle implicit intents without verification enables intent spoofing attacks.

## Attacker mindset
Attackers recognize that implicit intents are commonly used for legitimate file operations but are inherently insecure by design. They exploit developers' assumption that returned URIs are trustworthy, then either return malicious URIs or trigger unsafe file operations. By setting their malicious app as the default handler for common intents, attackers achieve reliable exploitation.

## Defensive takeaways
- Use explicit intents with specific component names instead of implicit intents when possible
- Validate all URIs returned from intent handlers and verify the source app using permission checks
- Never store sensitive data (tokens, keys, user credentials) in external storage or external cache directories
- Use getExternalFilesDir() and getExternalCacheDir() cautiously; prefer internal private storage for sensitive data
- Implement file access controls and encrypt sensitive files at rest
- Avoid apps with the same android:sharedUserId unless absolutely necessary, and audit all apps sharing the same UID
- Use FileProvider with proper path restrictions instead of exposing raw file URIs
- Implement runtime permission checks and request minimal necessary permissions
- Sanitize and validate all file operations to prevent path traversal attacks
- Regularly scan apps with tools like Oversecured to detect file exposure vulnerabilities

## Variant hunting
['Search for startActivityForResult() calls with implicit intents (Intent.ACTION_PICK, Intent.ACTION_GET_CONTENT, etc.)', 'Identify onActivityResult() handlers that process returned URIs without validation', 'Find file copy operations from content URIs to external directories (getExternalCacheDir(), getExternalFilesDir())', 'Locate apps registering intent filters for common file-related actions without proper export restrictions', 'Detect usage of getExternalCacheDir() and getExternalFilesDir() with sensitive data', 'Search for apps with android:sharedUserId declarations and audit cross-app file access', 'Identify FileProvider configurations with overly permissive path restrictions', 'Find direct file path concatenation in URI handling without validation', 'Detect apps storing tokens, keys, or credentials in world-readable locations']

## MITRE ATT&CK
- T1190
- T1083
- T1552
- T1040
- T1657
- T1566

## Notes
This is educational research from Oversecured demonstrating systematic Android file theft vulnerabilities. The article emphasizes that implicit intent handling is a widespread attack vector on Android due to the platform's design allowing any app to intercept intents. The vulnerability class affects numerous real-world apps, particularly those handling file uploads, media selection, and user-generated content. The research demonstrates both the attack methodology and detection approaches, making it valuable for both attackers and defenders. Modern Android versions (29+) provide some scoped storage restrictions, but the fundamental issue persists for apps targeting lower API levels and in specific use cases.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
