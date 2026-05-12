# Remote Code Execution in ExpressionEngine Import Channel Function via Incomplete Archive Upload

## Metadata
- **Source:** HackerOne
- **Report:** 236607 | https://hackerone.com/reports/236607
- **Submitted:** 2017-06-05
- **Reporter:** strukt
- **Program:** ExpressionEngine
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unrestricted File Upload, Remote Code Execution, Improper Input Validation, Directory Traversal/Exposure
- **CVEs:** None
- **Category:** memory-binary

## Summary
ExpressionEngine's channel import functionality allows administrators to upload ZIP archives that are extracted to a temporary cache directory. When the archive is incomplete or malformed, extracted files remain accessible and executable in the web-accessible `/system/user/cache/cset/` directory, enabling RCE through PHP file uploads. The vulnerability is compounded by directory listing being enabled on the cache folder.

## Attack scenario
1. Attacker crafts a malicious ZIP archive containing a PHP webshell (test.php) alongside intentionally omitted required import files
2. Attacker obtains or is granted administrator access to ExpressionEngine instance
3. Administrator navigates to admin.php?/cp/channels/sets and uploads the malicious ZIP file
4. Import fails due to missing required files, but extracted PHP file persists in /system/user/cache/cset/[directory]/
5. Attacker accesses the uploaded PHP shell via HTTP at /system/user/cache/cset/[directory]/test.php?cmd=whoami
6. PHP shell executes arbitrary system commands with web server privileges (cat /etc/passwd, reverse shell, etc.)

## Root cause
The application fails to validate and sanitize uploaded archive contents before extraction. When import validation fails, temporary extracted files are not cleaned up. Additionally, the cache directory is web-accessible with directory listing enabled, and PHP execution is not disabled in that directory via .htaccess or web server configuration.

## Attacker mindset
An attacker with administrator credentials (or who can socially engineer an admin) seeks persistent code execution on the target server. By exploiting the incomplete validation of import archives, they can bypass file upload restrictions and gain RCE. The directory listing exposure provides easy discovery of uploaded files.

## Defensive takeaways
- Implement strict whitelist validation of archive contents before extraction—verify all required files exist before proceeding
- Disable directory listing on cache directories via .htaccess (Options -Indexes) or web server configuration
- Disable PHP execution in cache directories via .htaccess or web server directives (php_flag engine off)
- Implement automatic cleanup of temporary extraction directories on import failure
- Store uploaded/extracted files outside the web root if possible
- Restrict file permissions on cache directories to prevent unauthorized access
- Implement file type validation beyond extension checking (MIME type, magic bytes)
- Add administrative logging and alerts for file upload activities
- Consider implementing a quarantine/scanning mechanism for uploaded archives before extraction

## Variant hunting
Other import/export functions in ExpressionEngine or similar PHP-based CMSs with archive handling
Theme/plugin upload functionality that may suffer from similar extraction/validation flaws
Backup/restore functions that extract archives to web-accessible directories
Any admin-only file upload feature that creates temporary directories without proper isolation
Check if template import, form builder imports, or other ZIP-based imports have similar issues

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1434 - External Remote Services
- T1132 - Data Obfuscation
- T1571 - Non-Standard Port

## Notes
This vulnerability requires administrator access, reducing immediate attack surface but critical for compromised admin accounts or supply chain attacks. The bug demonstrates a cascading failure: incomplete validation → incomplete cleanup → directory exposure → PHP execution. The fact that directory listing was enabled suggests multiple layers of security misconfiguration. Report lacks bounty amount and timeline information but represents a serious RCE vector in a popular CMS.

## Full report
<details><summary>Expand</summary>

Hello,

Administrators are allow to import channels by visiting http://HOST/PATH_TO_EE/admin.php?/cp/channels/sets and uploading .zip archives that contain the information about the channels to be imported. The archives are then extracted into temporary directories, which are kept in the `/system/user/cache/cset/` directory. The problem is that, if the archive doesn't have all the required files for the import to be successful, the extracted files remain in their folders and an error is thrown to the administrator stating that a file doesn't exist in the archive.

This allows an administrator to upload .php scripts to the server, which is not allowed by default in ExpressionEngine as far as I can see.

###Steps to reproduce:
1- Download the attached .zip archive and browse to http://HOST/PATH_TO_EE/admin.php?/cp/channels/sets
2- Try to upload the zip file you just downloaded as the imported channel
3- Navigate to http://HOST/PATH_TO_EE/system/user/cache/cset/, which will show a directory listing of all the temporary directories, this is a problem by itself
4- If this is your first time trying this, you should find a single directory, click the directory's name and then click the test.php file and edit the URL in the address bar by adding "?cmd=whoami" to the URL
5- Notice that the command has executed and that the information is returned in the page

Regards,

</details>

---
*Analysed by Claude on 2026-05-12*
