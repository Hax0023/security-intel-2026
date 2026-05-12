# Remote Code Execution via Unvalidated File Upload in Profile Picture Feature

## Metadata
- **Source:** HackerOne
- **Report:** 1164452 | https://hackerone.com/reports/1164452
- **Submitted:** 2021-04-13
- **Reporter:** aliyugombe
- **Program:** MTN Cameroon (careers.mtn.cm)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unrestricted File Upload, Remote Code Execution, Insufficient Input Validation, Path Traversal
- **CVEs:** None
- **Category:** memory-binary

## Summary
The careers portal allows authenticated users to upload arbitrary file types as profile pictures without validation, including executable PHP files. Uploaded files are stored in a web-accessible directory with predictable paths and are executed by the server, enabling remote code execution.

## Attack scenario
1. Attacker registers a legitimate account on careers.mtn.cm
2. Attacker navigates to profile update page and selects a file upload field
3. Instead of an image, attacker uploads a malicious PHP file containing backdoor code
4. Server stores the file in /en/user/images/users/ directory with predictable naming
5. Attacker views page source to retrieve the complete file path of uploaded PHP
6. Attacker accesses the file via direct URL, triggering PHP execution and gaining code execution

## Root cause
Complete absence of file type validation on the backend. Server accepts all file extensions without checking MIME types, file signatures, or restricting executable extensions. Uploaded files are stored in a web-accessible directory with execution permissions enabled.

## Attacker mindset
Low-skill attacker exploiting obvious security gaps. The attack is straightforward and requires minimal technical knowledge—registering an account, uploading a file, and accessing it. This suggests the attacker was conducting basic security reconnaissance or vulnerability scanning of public-facing portals.

## Defensive takeaways
- Implement strict whitelist-based file type validation using both extension checking and MIME type verification
- Validate file signatures/magic bytes to prevent disguised malicious files
- Disable script execution in upload directories via web server configuration (.htaccess for Apache: php_flag engine off)
- Store uploaded files outside the web root or in non-executable directories
- Rename uploaded files to remove original names and prevent direct execution
- Use randomized, unpredictable file paths and prevent directory traversal
- Implement Content-Disposition: attachment header to force downloads instead of inline execution
- Apply principle of least privilege to file permissions (644 or read-only)
- Scan uploaded files with antivirus/malware detection before storage
- Log and monitor file upload activities for suspicious patterns
- Conduct security code review of all file handling functions

## Variant hunting
Check other file upload endpoints (documents, resume uploads, company logos) for identical vulnerabilities
Test polyglot files (e.g., valid image files with embedded PHP/shell commands)
Attempt to upload .phtml, .php3, .php4, .php5, .phar, .pht, .phps extensions
Test .htaccess file upload to modify execution rules
Try uploading executable formats: .jsp, .jspx, .jsw, .asp, .aspx, .cgi, .pl, .py
Attempt null byte injection in filenames (file.php%00.jpg)
Test double extensions and case variation bypasses
Check if uploaded files can be accessed via alternative paths or symbolic links
Verify if other user roles (admin, recruiter) have different upload restrictions
Test authenticated vs unauthenticated upload endpoints

## MITRE ATT&CK
- T1190
- T1570
- T1059
- T1505
- T1136

## Notes
This is a textbook example of a critical file upload vulnerability. The reporter responsibly disclosed a non-harmful PoC. The vulnerability is trivial to exploit post-authentication but devastating in impact. The predictable file path disclosure in HTML source code is an additional information disclosure issue. This vulnerability likely affects many similar HR/recruitment portals with inadequate security development practices.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello 
I found a critical vunerability in one of your site, where user can upload any file type as a profile picture (including php file)


## Steps To Reproduce:
1. Visit https://careers.mtn.cm and register as a user.
2. After successful registration, login and update your data.
3. When uploading profile photo, select any file type.
 4. When its updated, view the source code of the page, you will see your file with complete path.
5. Copy the file path and paste into your browser.
6. Boom your file will be executed



## Supporting Material/References:
Here i upload non-harmful file as a poc 
```
<?php
echo "proof of concept (PoC) by aliyugombe@wearehackerone.com";
?>
```
https://careers.mtn.cm/en/user/images/users/-13-04-2021-20-15-16-payload.php

## Impact

Attacker can upload malicious file and inject to your server or deface the entire website since its possible to upload php file and gain access to direct file path.

</details>

---
*Analysed by Claude on 2026-05-12*
