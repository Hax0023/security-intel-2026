# Arbitrary Local-File Read from Admin - Restore From Backup due to Symlinks

## Metadata
- **Source:** HackerOne
- **Report:** 213558 | https://hackerone.com/reports/213558
- **Submitted:** 2017-03-15
- **Reporter:** ziot
- **Program:** Discourse
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Arbitrary File Read, Symlink Following, Path Traversal, Insecure Deserialization/Archive Extraction
- **CVEs:** None
- **Category:** web-api

## Summary
Discourse's backup restore feature fails to validate symlinks within tar archives, allowing authenticated admin users to read arbitrary files accessible to the application process. By crafting a malicious backup tar containing symlinks to sensitive files like /etc/passwd, an attacker can extract and access those files through the web interface.

## Attack scenario
1. Attacker obtains or creates a valid Discourse backup tar file
2. Attacker extracts the tar and adds a symlink pointing to a sensitive file (e.g., /etc/passwd) within the uploads directory structure
3. Attacker re-packages the modified contents into a tar.gz file
4. Attacker uploads the crafted tar to the Discourse backup restore feature as an authenticated admin
5. Attacker triggers the restore process which extracts the tar without validating symlink contents
6. Attacker accesses the symlinked file via the web interface (e.g., viewing it as an image upload)

## Root cause
The backup restoration process extracts tar archives without sanitizing or validating symlinks. The application does not check whether extracted files are symlinks pointing outside the intended directory or to sensitive system files before making them accessible.

## Attacker mindset
An insider threat or compromised admin account seeking to exfiltrate sensitive data. The attacker recognizes that backup/restore functionality often has lower security scrutiny and that symlinks are a reliable way to bypass directory restrictions during archive extraction.

## Defensive takeaways
- Validate and reject symlinks during tar extraction; use archive libraries with symlink detection/prevention flags
- Implement strict path validation post-extraction to ensure all files remain within expected directories
- Restrict backup restore functionality to users with elevated privileges and audit all restore operations
- Use chroot/jail or containerization for backup processing to limit symlink traversal impact
- Sanitize tar archives before processing by stripping or flattening symlinks
- Implement file type validation before serving restored uploads to prevent serving system files as resources
- Consider running backup operations with minimal file system permissions

## Variant hunting
Check other backup/export/import features for symlink validation gaps
Test plugin installation/update mechanisms for similar symlink extraction issues
Audit theme upload and installation for symlink handling
Review any tar.gz extraction across the codebase for symlink sanitization
Test compressed archive formats (zip, 7z) for similar path traversal vectors

## MITRE ATT&CK
- T1190
- T1566.001
- T1040
- T1005
- T1552.001

## Notes
This vulnerability requires admin authentication, limiting its scope but showing the importance of securing admin-only features. The symlink-in-tar technique is a well-known archive extraction anti-pattern. Discourse likely patched this by validating/rejecting symlinks during tar extraction.

## Full report
<details><summary>Expand</summary>

As an Admin user on Discourse there is a feature to create, upload, and restore backups. Generating a backup creates a tar file consisting of the database as a SQL file and uploaded files from /public/upload/*. Having the ability to upload these tar files and restore from them, you can add any file that you wish. 

Manually modifying the tar archive and adding a symlink, you are able to read any arbitrary file that the user has permission to including files outside of the Discourse application directory.

## Steps

1. Load http://try.discourse.org
2. Login as an Admin user.
3. Go to the Backups page:
 * http://try.discourse.org/admin/backups/
4. Create a new backup including files.
5. Extract the backup files to a folder on your server.
6. Create a symlink to `/etc/passwd` In the /uploads/ folder of the backup, e.g. `/uploads/default/original/1X/[file].jpg`.
 * example: `ln -s /etc/passwd /home/symlink/files/uploads/default/original/1X/7ad2e8f5fe02890f20503044b604e29e6f3718fd.png`
7. Create a .tar.gz from the extracted files.
8. Upload the newly crafted tar to the server.
9. Enable `Restore from Backups` in settings if it's not enabled.
10. Restore from the backup that uploaded.
11. Go to the uploaded file in your browser after it uploads, e.g.
 * http://try.discourse.org/uploads/default/original/1X/[file].jpg
12. ---> You were able to read file contents of `/etc/passwd` due to the symlink being extracted from the tar.



</details>

---
*Analysed by Claude on 2026-05-24*
