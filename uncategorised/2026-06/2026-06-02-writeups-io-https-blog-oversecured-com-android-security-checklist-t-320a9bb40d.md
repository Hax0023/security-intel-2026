# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Android Ecosystem (General Advisory)
- **Bounty:** N/A - Security Research/Advisory
- **Severity:** HIGH
- **Vuln types:** Arbitrary File Read/Write, Insecure File Permissions, Implicit Intent Interception, Path Traversal, Unsafe Content Provider Usage, Exported Components
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android developers frequently expose sensitive files through improper handling of implicit intents and insecure file storage practices, allowing malicious apps to read private application data. The vulnerability stems from apps accepting content URIs from unverified sources and caching them to accessible locations without proper validation or permission checks.

## Attack scenario (step by step)
1. Attacker creates a malicious app and registers itself as a handler for common implicit intents (ACTION_PICK, IMAGE_CAPTURE, etc.)
2. Victim app launches an implicit intent to request file selection or media capture without specifying a trusted handler
3. Attacker's app intercepts the intent and returns a malicious content URI pointing to the victim app's private files or a path traversal payload
4. Victim app accepts the URI without validation and processes/caches the content to external storage or world-readable locations
5. Attacker's app reads the cached sensitive data from public directories (/storage/emulated/0/Android/data/)
6. Attacker exfiltrates tokens, user data, credentials, or other sensitive information stored in private directories

## Root cause
Developers fail to validate content URIs returned from implicit intent handlers, assume implicit intent responses are from trusted sources, cache sensitive content to world-readable locations, and lack proper input validation on file paths that could enable path traversal attacks.

## Attacker mindset
An attacker exploits the Android implicit intent system as a vector to inject malicious content URIs or intercept file operations. They target common workflows like photo selection or document picking where developers implement weak validation. By registering as an intent handler with higher priority, they can hijack the response and leak sensitive application data stored in private directories.

## Defensive takeaways
- Always validate and sanitize content URIs returned from implicit intent handlers before processing
- Use explicit intents with specific package names when possible to avoid interception
- Never cache or store sensitive data in external/public storage directories
- Implement proper file permissions and use private app directories (/data/data/package_name/)
- Verify file paths for traversal sequences (../, etc.) before processing
- Use FileProvider with restricted path permissions instead of exposing content directly
- Request only minimum necessary file permissions (READ_EXTERNAL_STORAGE, WRITE_EXTERNAL_STORAGE)
- Encrypt sensitive files at rest and implement access controls
- Do not use sharedUserId unless absolutely necessary and properly validated
- Implement signature-based verification for inter-app communication

## Variant hunting
Search for: (1) startActivityForResult calls with implicit intents lacking handler specification, (2) Uri/File operations without path validation in onActivityResult, (3) getExternalCacheDir/getExternalFilesDir usage for sensitive data, (4) Missing permission checks on ContentProvider access, (5) Unvalidated file path concatenation, (6) Exported components accepting file intents, (7) Custom schemes without package verification, (8) Files created with MODE_WORLD_READABLE or MODE_WORLD_WRITEABLE (deprecated but legacy code)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1040 - Network Sniffing
- T1557 - Adversary-in-the-Middle
- T1083 - File and Directory Discovery
- T1005 - Data from Local System
- T1052 - Exfiltration Over Physical Medium
- T1548 - Abuse Elevation Control Mechanism
- T1199 - Trusted Relationship

## Notes
This is a comprehensive security advisory from Oversecured covering multiple related file theft vulnerabilities in Android. The writeup emphasizes that the root cause is not a single bug but rather a pattern of insecure development practices. The distinction between private (/data/user) and public (/storage/emulated) storage is critical. SharedUserId is a particularly dangerous feature that extends attack surface. The implicit intent attack vector is particularly effective because it's part of Android's standard API and developers often don't consider it a security boundary. Modern Android versions (SDK 29+) provide scoped storage which mitigates some but not all variants of this class of vulnerability.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
