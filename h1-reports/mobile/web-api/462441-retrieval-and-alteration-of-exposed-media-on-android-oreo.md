# Retrieval and Alteration of Exposed Media on Android Oreo via Shared Storage

## Metadata
- **Source:** HackerOne
- **Report:** 462441 | https://hackerone.com/reports/462441
- **Submitted:** 2018-12-14
- **Reporter:** doragon
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Insecure Data Storage, Inadequate Access Controls, Missing Encryption, Path Traversal/Shared Storage Misuse, Data Integrity Violation
- **CVEs:** None
- **Category:** web-api

## Summary
The Nextcloud Android app stores downloaded media in a world-readable shared folder (/sdcard/Android/media/com.nextcloud.client/nextcloud/ACCOUNT/) on Android Oreo, allowing third-party applications to read, modify, or delete user files without consent. When files are tampered with, the app automatically re-uploads the modified content to the server, compromising both confidentiality and integrity even when Nextcloud app lock is enabled.

## Attack scenario
1. Attacker installs a malicious application on the target device with READ_EXTERNAL_STORAGE and WRITE_EXTERNAL_STORAGE permissions
2. Attacker's app enumerates and accesses downloaded Nextcloud media stored in the unencrypted shared folder
3. Attacker modifies sensitive files (PDFs, images, documents) locally using the malicious app
4. User opens the Nextcloud app, which automatically detects the tampered files and syncs them back to the cloud server
5. Attacker's modified content now persists on the Nextcloud server, affecting all synced clients
6. Alternatively, attacker deletes files from shared storage, rendering them unavailable locally regardless of network connectivity

## Root cause
Nextcloud stores cached/downloaded media in Android's shared external storage directory without encryption or access control restrictions. The app does not validate file integrity before re-uploading and relies on the OS permission model which allows any app with storage permissions to access peer application data in shared directories.

## Attacker mindset
An attacker with basic app installation capability can compromise data integrity at scale by leveraging loose Android storage permissions. The automatic sync mechanism creates a feedback loop where local modifications reach the server without integrity verification, enabling supply-chain-style attacks on cloud-backed documents.

## Defensive takeaways
- Store sensitive downloaded media in app-private directories (Context.getFilesDir() or Context.getCacheDir()) rather than shared external storage
- Implement encryption for all cached files using Android Keystore and algorithms like AES-256-GCM
- Calculate and validate file hashes/signatures before re-uploading to detect tampering
- Restrict file permissions using SELinux contexts and enforce app-only access via encrypted containers
- Implement integrity checking on sync operations; quarantine and alert on unexpected file modifications
- Use content encryption at rest with per-file decryption only during display, especially for files opened in external apps
- When app-lock is enabled, extend protection to stored files with mandatory encryption
- Monitor file modification times and hashes; alert user before re-uploading altered content

## Variant hunting
Check if other sync apps (Dropbox, OneDrive, Google Drive, Syncthing) store cached files in shared storage without encryption
Test whether modified files on shared storage trigger automatic re-sync in other cloud clients without integrity validation
Investigate if other Android versions (pre-Oreo, post-Oreo) have different storage isolation behavior affecting this vulnerability
Examine whether files encrypted on-server remain encrypted in the shared cache directory
Test if app-lock mechanisms in other apps properly protect offline cached data from third-party modification
Check for similar issues in Nextcloud's iOS implementation regarding Documents directory exposure

## MITRE ATT&CK
- T1530
- T1040
- T1565.001
- T1557.001
- T1213.002

## Notes
The vulnerability is particularly severe because: (1) automatic re-upload creates persistent damage, (2) app-lock feature provides false security by not protecting stored files, (3) no integrity verification exists, and (4) third-party modifications appear legitimate to other clients. The reporter notes this could be split into separate confidentiality (disclosure) and integrity (tampering) issues. Resolution requires moving away from shared storage paradigm to encrypted app-private storage with integrity checks.

## Full report
<details><summary>Expand</summary>

Good afternoon.

Any media downloaded from the cloud server within the Android app is subject to third party modification and server re-upload without explicit  user consent.

This happens at least on Android Oreo, as data is automatically stored on shared folder /sdcard/Android/media/com.nextcloud.client/nextcloud/ACCOUNT/.

This report could be probably divided in two as one aspect is data confidentially while the other one is data integrity, which could be solved separately.

## Impact

Local media availability  is impacted if device is not web connected as third app can delete any downloaded assets

Local media confidentiality is impacted as any third app can access any downloaded assets, even if  Nextcloud lock is set up.

Local media confidentiality is impacted as any third app can alter any downloaded assets, even if  Nextcloud lock is set up. Once the user open up NC app, content get automatically reuploaded to sever.

As it seems NEW content does not get uploaded nor DELETED content get removed, it seems that Nextcloud app maintain a local sync setup and this setup could be used for metadata control to at least prevent/control data re-upload.

if Nextcloud lock is setup, it would also good to at least provide a minimal confidentiality setup so that data gets encrypted PER default and decrpyted on tmp folder only on click (which is required to open assets with PDF/other app).

</details>

---
*Analysed by Claude on 2026-05-24*
