# Unauthenticated Arbitrary File Upload on upload.php

## Metadata
- **Source:** HackerOne
- **Report:** 698789 | https://hackerone.com/reports/698789
- **Submitted:** 2019-09-20
- **Reporter:** sp1d3rs
- **Program:** Undisclosed (Redacted)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Upload, Missing Authentication, Insufficient Input Validation, Path Traversal (potential)
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated arbitrary file upload vulnerability exists on the upload.php endpoint, allowing attackers to upload files without authentication or validation. Uploaded files are stored in a web-accessible directory (/delete.me), enabling potential stored XSS, malicious content hosting, and remote code execution.

## Attack scenario
1. Attacker navigates to https://[target]/upload.php without requiring authentication
2. Attacker crafts and uploads a malicious file (webshell, XSS payload, or executable)
3. Server accepts the file and stores it in the publicly accessible /delete.me directory
4. Attacker accesses uploaded file via https://[target]/delete.me/[filename]
5. If file is executed (PHP/JSP/ASP), attacker gains remote code execution on the server
6. If file contains XSS payload, stored XSS vulnerability affects other users accessing the file

## Root cause
Missing authentication checks on the upload endpoint combined with insufficient file validation, lack of file type restrictions, and storage of uploaded files in a web-accessible directory with executable permissions

## Attacker mindset
Reconnaissance of publicly exposed upload endpoints, testing for authentication bypass, uploading webshells or polyglot files to establish persistence and execute arbitrary commands on the target server

## Defensive takeaways
- Implement strict authentication and authorization checks on all file upload endpoints
- Validate file types using whitelist approach (check MIME type and magic bytes, not just extension)
- Store uploaded files outside the web root or in non-executable directories
- Implement file size limits and rate limiting on upload endpoints
- Sanitize and randomize uploaded filenames to prevent direct access and traversal
- Disable script execution in upload directories (configure web server to not execute scripts)
- Implement virus/malware scanning on uploaded files
- Log all upload attempts and monitor for suspicious patterns
- Use Content-Disposition: attachment headers when serving uploaded files

## Variant hunting
Search for other upload endpoints (upload.php, upload.asp, upload.jsp, /api/upload, /file/upload)
Test multipart form-data uploads with double extensions (shell.php.jpg)
Attempt null byte injection (shell.php%00.jpg) if running PHP <5.3
Test path traversal in filename parameter (../../../shell.php)
Check for zip slip vulnerabilities in file extraction functions
Test for TOCTOU races during file validation and storage
Verify if other file formats can be executed (htaccess, web.config, phtml, shtml)
Check if symbolic links or hardlinks can be exploited

## MITRE ATT&CK
- T1190
- T1190
- T1505
- T1505.003
- T1078
- T1078.001

## Notes
The report demonstrates basic proof-of-concept with minimal detail. The vulnerability is critical due to lack of authentication, validation, and secure file storage practices. The /delete.me path suggests potential directory enumeration or intentionally exposed directory. Real-world impact depends on server configuration and what file types are executable. The redacted nature of the report limits full severity assessment but the vulnerability chain is clear.

## Full report
<details><summary>Expand</summary>

##Description
I was able to identify unsafe upload endpoint on the https://█████/upload.php

##POC
1) Go to the https://█████████/upload.php
2) Upload some test file.
You will see success message:
████
3) Visit `https://███/delete.me` and you will see your uploaded file there
I uploaded example test file with string `test file`
█████████

## Impact

Arbitrary file upload, may lead to the Stored XSS, hosting attacker's content and code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
