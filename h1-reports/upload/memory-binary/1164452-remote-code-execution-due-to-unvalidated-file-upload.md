# Remote Code Execution via Unvalidated File Upload in User Profile Picture

## Metadata
- **Source:** HackerOne
- **Report:** 1164452 | https://hackerone.com/reports/1164452
- **Submitted:** 2021-04-13
- **Reporter:** aliyugombe
- **Program:** MTN (careers.mtn.cm)
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Unrestricted File Upload, Remote Code Execution (RCE), Insufficient Input Validation, Path Traversal (implicit)
- **CVEs:** None
- **Category:** memory-binary

## Summary
The careers.mtn.cm application allows authenticated users to upload arbitrary file types as profile pictures without proper validation, including executable PHP files. The uploaded files are stored in a web-accessible directory with predictable paths and execute when accessed via HTTP, enabling remote code execution on the server.

## Attack scenario
1. Attacker registers a new account on careers.mtn.cm and completes authentication
2. Attacker navigates to profile/settings page and locates the profile picture upload functionality
3. Attacker crafts a malicious PHP file containing arbitrary code (web shell, reverse shell, etc.) and submits it as a profile picture
4. Application processes upload without validating file type/extension and stores file in web-accessible directory with predictable naming scheme
5. Attacker retrieves file path from HTML source code (visible in page source)
6. Attacker accesses PHP file via HTTP request to trigger code execution with web server privileges

## Root cause
The application lacks proper file type validation on upload, relying on user-controlled input without verifying MIME types, file extensions, or content. Additionally, uploaded files are stored in a web-accessible directory without disabling script execution, and paths are predictable/disclosed in source code.

## Attacker mindset
An attacker with basic web exploitation knowledge can identify this as a low-hanging fruit vulnerability. The predictable file paths and direct code execution make this trivial to exploit. The attacker may be motivated by financial gain, data theft, website defacement, or establishing persistent access for further attacks.

## Defensive takeaways
- Implement strict whitelist-based file type validation using both MIME type checking and file extension verification
- Store uploaded files outside the web root or in a directory with script execution disabled (configure web server to prevent .php/.exe execution)
- Rename uploaded files to remove user-controlled components and use randomized, non-predictable names
- Set appropriate file permissions (644 or similar) to prevent execution
- Implement proper access controls requiring authentication to retrieve uploaded files
- Validate file content (magic bytes) in addition to extension/MIME type
- Use dedicated file serving mechanisms (download script) rather than direct HTTP access
- Implement antivirus/malware scanning on uploaded files
- Log all file upload attempts with user context for audit trails
- Use Content-Security-Policy headers to prevent script execution from user-uploaded content

## Variant hunting
Check other upload functionality (documents, avatars, attachments) for similar validation gaps
Test for double extension bypasses (.php.jpg, .php.png)
Test for null byte injection (.php%00.jpg)
Test for case sensitivity bypasses (.pHP, .PhP)
Examine other user-facing endpoints for file upload features
Check if other file types (SVG, HTML, HTACCESS) can be exploited similarly
Review if ZIP/archive uploads are processed and extracted
Test if uploaded files are accessible to unauthenticated users

## MITRE ATT&CK
- T1190
- T1190
- T1567.002
- T1106

## Notes
This is a classic, well-known vulnerability pattern (CWE-434: Unrestricted Upload of File with Dangerous Type). The write-up demonstrates a real-world impact scenario. The predictable file path disclosure in HTML source is a secondary issue compounding the primary vulnerability. This vulnerability likely affects other profiles/users, making it exploitable post-compromise for lateral movement or privilege escalation. The public disclosure of the working POC path indicates the vulnerability was confirmed and exploitable at time of report.

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
*Analysed by Claude on 2026-05-24*
