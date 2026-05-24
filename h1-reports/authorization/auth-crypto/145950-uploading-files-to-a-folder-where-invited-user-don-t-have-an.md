# Unauthorized File Upload via Copy Feature in Nextcloud Android App

## Metadata
- **Source:** HackerOne
- **Report:** 145950 | https://hackerone.com/reports/145950
- **Submitted:** 2016-06-19
- **Reporter:** detroitsmash
- **Program:** Nextcloud
- **Bounty:** Not specified
- **Severity:** Medium
- **Vuln:** Broken Access Control, Privilege Escalation, Authorization Bypass
- **CVEs:** CVE-2016-9461
- **Category:** auth-crypto

## Summary
The Nextcloud Android app fails to properly enforce edit privilege restrictions when users attempt to copy files into shared folders. A user without edit permissions can bypass access controls by using the copy feature, allowing unauthorized file uploads to folders where they should have read-only access.

## Attack scenario
1. Attacker receives an invitation to a shared Nextcloud folder with view-only permissions (no edit privilege granted)
2. Attacker logs into the Nextcloud Android app with their invited account
3. Attacker selects a file from their own root folder or accessible directories
4. Attacker uses the copy feature to copy the selected file to the restricted shared folder
5. The Android app bypasses server-side permission checks and completes the copy operation
6. The unauthorized file now appears in the shared folder, visible to all folder members, confirming the privilege escalation

## Root cause
The Nextcloud Android app does not properly validate user permissions before executing copy operations. The client-side application fails to check if the user has EDIT privileges on the destination folder before initiating the file copy, allowing the copy request to proceed. The server either doesn't validate permissions on the copy endpoint or the validation is insufficient.

## Attacker mindset
An attacker with legitimate access to a shared folder seeks to exceed their granted permissions. Recognizing that mobile apps sometimes have weaker validation than web interfaces, they explore alternative operations (copy vs direct upload) to circumvent restrictions. The attacker understands that copy operations might be handled differently than standard uploads in the codebase.

## Defensive takeaways
- Always enforce permission checks on the server-side regardless of client-side validation, especially for file operations
- Implement consistent permission validation across all endpoints that modify data (upload, copy, move, create)
- Mobile apps should perform identical permission checks as web clients before executing privileged operations
- Validate write/edit permissions on the destination path before allowing copy, move, or similar operations
- Implement role-based access control (RBAC) consistently at the API layer, not relying on client enforcement
- Add comprehensive audit logging for file operations to detect permission bypass attempts
- Test permission boundaries across all client types (web, mobile, desktop) with the same test cases

## Variant hunting
Check if move operations have the same vulnerability as copy
Test if sharing files from restricted folders uses the same flawed logic
Verify if drag-and-drop operations in desktop client have similar issues
Investigate whether the vulnerability exists when copying directories vs individual files
Check if symbolic links or shortcuts can be created in restricted folders
Test permission bypass through collaboration/commenting features on shared folders
Examine if API-based copy requests (direct API calls) bypass the same checks as mobile app
Investigate if folder creation is similarly affected in read-only shared spaces

## MITRE ATT&CK
- T1190
- T1548
- T1078
- T1526

## Notes
This is a client-server trust issue where the mobile application assumes the server will enforce permissions but executes operations without pre-flight permission checks. The vulnerability demonstrates the importance of defense-in-depth: even if the client validates permissions, the server must independently verify all operations. The use of a feature-specific endpoint (copy) rather than standard upload allowed the vulnerability to persist if that endpoint had weaker permission validation than direct upload handlers.

## Full report
<details><summary>Expand</summary>

Hi,

Any invited user to a shared folder with no edit privilege can create files in it through copy feature of ``Nextclod`` android app.

### Steps to reproduce it

+ Create any folder and invite a user in it without any edit privilege.
+ Now login from invited user account through android app.
+ Copy any file from your ``nextcloud`` root folder to shared folder.
+ Check nextcloud web app!! Copied file will show in shared folder

Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
