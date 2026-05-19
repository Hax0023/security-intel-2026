# Android Security Checklist: Theft of Arbitrary Files via Implicit Intents and File Exposure

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Android ecosystem (general security research)
- **Bounty:** N/A - Security research article
- **Severity:** high
- **Vuln types:** Arbitrary File Access, Implicit Intent Interception, Path Traversal, Insecure File Permissions, Content Provider Exposure
- **Category:** uncategorised
- **Writeup:** https://blog.oversecured.com/Android-security-checklist-theft-of-arbitrary-files

## Summary
Android developers frequently make mistakes when handling file exchanges between apps through implicit intents and file storage, allowing attackers to steal sensitive data from private app directories. The vulnerability primarily stems from unsafe handling of Uri results from implicit intents and improper file permission configurations, enabling arbitrary file theft.

## Attack scenario (step by step)
1. Attacker identifies target app that uses implicit intents (e.g., ACTION_PICK, IMAGE_CAPTURE) to obtain user files
2. Attacker creates malicious app that registers handlers for the same intent actions with higher priority
3. Target app launches implicit intent expecting benign file manager or camera app
4. Malicious app intercepts the intent and responds with a crafted Uri pointing to sensitive files in target app's private directory
5. Target app processes the Uri without validation and caches/copies the sensitive file to accessible location
6. Attacker's app or other third-party app reads the exposed sensitive data from public storage

## Root cause
Developers trust implicit intent results without validating Uri sources and fail to properly restrict file access permissions. The use of external cache directories and improper Content Provider implementations expose private files to unauthorized access.

## Attacker mindset
An attacker recognizes that Android's intent system allows interception and that developers commonly cache files from intent results in accessible locations. They exploit this by creating a malicious app that responds to implicit intents with pointers to sensitive files, leveraging the target app's own file-copying functionality against itself.

## Defensive takeaways
- Validate and sanitize all Uri results from implicit intent responses; verify the source app is trusted
- Store sensitive data only in private app directories (/data/user/0/{package_name}), never in external storage
- Use explicit intents with specific package names instead of implicit intents when possible
- Implement proper file permissions and never expose private files through misconfigured ContentProviders
- Use FileProvider with restricted path permissions for file sharing between apps
- Never cache sensitive content from untrusted intent results in public directories
- Regularly audit file storage patterns and validate permission models
- Implement runtime checks to ensure files being accessed belong to expected sources

## Variant hunting
['Check for all implicit intent action handlers (ACTION_PICK, IMAGE_CAPTURE, VIDEO_CAPTURE, ACTION_GET_CONTENT)', 'Trace Uri processing in onActivityResult() for unsafe file operations', 'Hunt for external cache directory usage with user-controlled or intent-derived filenames', 'Identify ContentProvider implementations with overly broad path permissions', 'Search for file:// Uri schemes which indicate direct filesystem exposure', 'Audit apps sharing android:sharedUserId for cross-app file theft vectors', 'Review file copying operations after intent callbacks for path traversal possibilities']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1005 - Data from Local System
- T1040 - Network Sniffing
- T1120 - Peripheral Device Discovery
- T1083 - File and Directory Discovery
- T1005 - Data Staged: Local Data Staging

## Notes
This is a comprehensive security research article from Oversecured highlighting systematic vulnerabilities in Android file handling. The article covers multiple attack vectors including implicit intent interception, unsafe file caching, and improper permission models. The vulnerability class affects many popular Android apps and represents a common developer mistake pattern rather than a single CVE.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
