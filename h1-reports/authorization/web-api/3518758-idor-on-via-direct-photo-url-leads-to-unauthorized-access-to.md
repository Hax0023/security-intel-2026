# IDOR on Photo Access via Direct URL - Unauthorized Access to Deleted and Other Users' Photos

## Metadata
- **Source:** HackerOne
- **Report:** 3518758 | https://hackerone.com/reports/3518758
- **Submitted:** 2026-01-21
- **Reporter:** shiva2550
- **Program:** Nextcloud or similar file-sharing/photo management platform
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insecure Direct Object Reference (IDOR), Broken Access Control, Insufficient Authorization Validation
- **CVEs:** None
- **Category:** web-api

## Summary
An IDOR vulnerability allows authenticated users to access photos belonging to other users via direct URL manipulation, including photos that have been deleted. The application fails to validate user authorization when accessing photos through the DAV (WebDAV) photos endpoint, enabling unauthorized photo enumeration and retrieval.

## Attack scenario
1. Attacker creates an account and identifies the direct photo URL pattern: /remote.php/dav/photos/[user_email]/albums/[album_name]/[photo_id]
2. Attacker obtains or enumerates valid user email addresses and photo IDs through reconnaissance
3. Attacker constructs URLs targeting other users' photos by substituting different email addresses and photo IDs
4. Attacker accesses the crafted URLs and successfully retrieves photos belonging to other users without authorization
5. Attacker can also access deleted photos if they know the original URL, as the file may not be properly purged from storage
6. Attacker can systematically enumerate and harvest photos from multiple users by iterating through email addresses and photo ID sequences

## Root cause
The WebDAV/DAV photo endpoint lacks proper authorization checks before serving photo resources. The application does not verify that the authenticated user owns or has permission to access the requested photo. The authorization validation likely only checks if a user is authenticated (not anonymous) but does not enforce ownership or explicit permission grants.

## Attacker mindset
An attacker would recognize that direct object references without proper authorization are a common vulnerability pattern. They would systematically probe the URL structure, test access across accounts, and recognize that deleted files may persist on disk. The attacker seeks to harvest sensitive photos, violate user privacy, or identify patterns in photo storage for further exploitation.

## Defensive takeaways
- Implement explicit authorization checks for every resource access request, verifying user ownership or permission grants before serving content
- Use opaque, non-sequential identifiers for photos (UUIDs) instead of sequential photo IDs to prevent enumeration
- Enforce principle of least privilege - default deny access unless explicitly granted
- Properly delete/purge photo data from storage when users delete photos, including all backups and caches
- Implement role-based access control (RBAC) with granular permission models for album and photo sharing
- Log and audit all photo access attempts, especially cross-user access
- Validate user context and session permissions at the WebDAV protocol level, not just HTTP layer
- Use secure hashing or encryption to obscure actual storage paths in URLs

## Variant hunting
Look for similar patterns in other endpoints handling user-owned resources: documents, videos, files, personal data. Test GET/HEAD/OPTIONS requests on other DAV endpoints. Check if authorization bypass exists in other file operations (move, copy, share). Test direct database ID access in other features. Verify if deleted content is truly removed or recoverable.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (authorization bypass)
- T1526 - Enumerate external targets (photo/user enumeration)
- T1040 - Network sniffing (intercepting photo URLs)
- T1530 - Data from cloud storage (unauthorized cloud data access)

## Notes
The vulnerability is particularly severe because: (1) deleted photos remain accessible, indicating incomplete deletion logic; (2) the email-based URL structure aids user enumeration; (3) sequential photo IDs enable systematic enumeration; (4) the WebDAV protocol may be less commonly tested than HTTP endpoints. The report suggests this is likely a file-sharing/collaboration platform (possibly Nextcloud Photos app) where privacy is critical. This represents a complete breakdown of object-level authorization in a security-sensitive feature.

## Full report
<details><summary>Expand</summary>

## Summary:
An Insecure Direct Object Reference (IDOR) vulnerability exists in the application that allows unauthorized access to photos belonging to other users. The application does not properly validate whether the logged-in user is authorized to access a photo when accessing it via direct URL. This allows any authenticated user to view photos from other users' albums, including photos that have been deleted.

## Steps To Reproduce:

**Account A:**

1. Create an album
2. Upload a photo
3. Note the direct image URL: `https://████████/remote.php/dav/photos/███████/albums/srk./10700342-1.jpeg`
4. Delete that photo
5. Save the URL for future reference

**Account B:**

1. Copy the old image URL from Account A: `https://████/remote.php/dav/photos/████████/albums/srk./10700342-1.jpeg`
2. Paste it in the browser
3. The image loads successfully, even though Account B is a different user and the photo was deleted

## Supporting Material/References:

* Vulnerable URL pattern: `https://████████/remote.php/dav/photos/[user_email]/albums/[album_name]/[photo_id]`
* The photo was accessible despite being deleted and belonging to another account

</details>

---
*Analysed by Claude on 2026-05-24*
