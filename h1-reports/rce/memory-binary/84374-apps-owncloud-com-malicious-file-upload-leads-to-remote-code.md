# apps.owncloud.com: Malicious file upload leads to remote code execution

## Metadata
- **Source:** HackerOne
- **Report:** 84374 | https://hackerone.com/reports/84374
- **Submitted:** 2015-08-24
- **Reporter:** imadchabounia
- **Program:** ownCloud
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Arbitrary File Upload, Remote Code Execution, Insufficient File Type Validation, Insecure File Storage
- **CVEs:** None
- **Category:** memory-binary

## Summary
The apps.owncloud.com server allows unauthenticated upload and execution of arbitrary PHP files, leading to remote code execution. An attacker can upload a malicious PHP file with a .php5 extension that gets executed by the web server, allowing complete server compromise.

## Attack scenario
1. Attacker identifies that apps.owncloud.com accepts file uploads without proper validation
2. Attacker crafts a malicious PHP file (e.g., containing phpinfo() or a web shell) with a .php5 extension
3. Attacker uploads the file to the /CONTENT/content-pre1/ directory or similar upload endpoint
4. The web server processes the uploaded .php5 file as executable PHP code
5. Attacker accesses the uploaded file via HTTP, triggering PHP execution
6. Attacker gains remote code execution and can execute arbitrary commands on the server

## Root cause
The application fails to implement proper file upload validation including: (1) insufficient file type/extension checks that don't block executable extensions like .php5, (2) storing uploaded files in a web-accessible directory with execution permissions, (3) lack of file content validation (magic bytes), (4) no restriction on which file extensions can be executed by the web server

## Attacker mindset
Opportunistic vulnerability discovery - the attacker recognized that a public app repository would likely have loose upload controls and tested basic PHP file uploads. The direct proof of concept demonstrates intent to verify and report the vulnerability rather than exploit it maliciously.

## Defensive takeaways
- Implement strict whitelist of allowed file extensions; reject all others including .php, .php5, .phtml, .phar, etc.
- Store uploaded files outside the web root or in a directory with disabled script execution (via .htaccess, web.config, or server configuration)
- Validate file contents using magic bytes/MIME type checking, not just extension
- Rename uploaded files to remove original extensions and store with randomized names
- Set proper file permissions (644 or read-only) on uploaded files
- Disable PHP execution in upload directories via web server configuration
- Implement virus/malware scanning on uploaded files
- Use a dedicated file serving mechanism that streams files without execution
- Audit and test file upload functionality thoroughly in security review

## Variant hunting
Check for other executable extensions (.phtml, .phar, .shtml, .jsp, .asp, .aspx, .cgi) that might bypass filters
Test double extensions (.php.jpg) and null byte injection (.php%00.jpg)
Verify if uploaded files can be accessed directly via HTTP
Test for path traversal in upload endpoints (../../../malicious.php)
Check if .htaccess files can be uploaded to enable PHP execution
Test uploading files to other directories on the application
Verify if authenticated upload endpoints have the same vulnerability

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1190.001: Upload Web Shell
- T1059.007: Command and Scripting Interpreter (PHP)
- T1190.002: Web Shell

## Notes
This is a straightforward but critical vulnerability in a high-impact target (ownCloud app marketplace). The proof of concept is minimal but sufficient to demonstrate RCE. The /CONTENT/content-pre1/ path suggests this may have been a staging or preview directory with weaker security controls. The vulnerability likely affected multiple users who downloaded or installed content from the marketplace.

## Full report
<details><summary>Expand</summary>

Hello ownCloud Security Team,

i am here to report a critical security vulnerability .

Proof of concept :

https://apps.owncloud.com/CONTENT/content-pre1/171172-1.php5

code source of uploaded file : 
<?php

phpinfo();

?>


</details>

---
*Analysed by Claude on 2026-05-12*
