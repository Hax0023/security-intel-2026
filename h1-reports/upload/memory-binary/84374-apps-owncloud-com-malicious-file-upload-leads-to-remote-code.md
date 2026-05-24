# apps.owncloud.com: Malicious file upload leads to remote code execution

## Metadata
- **Source:** HackerOne
- **Report:** 84374 | https://hackerone.com/reports/84374
- **Submitted:** 2015-08-24
- **Reporter:** imadchabounia
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** Unrestricted File Upload, Remote Code Execution, Insufficient File Type Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
A critical vulnerability in apps.owncloud.com allowed attackers to upload malicious PHP files with arbitrary extensions (e.g., .php5) that would be executed by the web server, leading to remote code execution. The application failed to properly validate file types and extensions before storing uploaded content in a web-accessible directory.

## Attack scenario
1. Attacker identifies the file upload functionality on apps.owncloud.com
2. Attacker crafts a malicious PHP file containing arbitrary code (e.g., phpinfo() or reverse shell payload)
3. Attacker uploads the file using an alternative extension (.php5) to bypass basic extension filters
4. The uploaded file is stored in a web-accessible directory without proper validation
5. Attacker accesses the uploaded file via direct HTTP request (e.g., /CONTENT/content-pre1/171172-1.php5)
6. The web server executes the PHP code, granting the attacker code execution capabilities on the server

## Root cause
Insufficient input validation on file uploads combined with inadequate file type restrictions. The application likely relied on blacklisting specific extensions (e.g., .php) rather than whitelisting safe extensions, and failed to prevent execution of files stored in web-accessible directories.

## Attacker mindset
An attacker would recognize that file upload endpoints are common attack vectors. They would test multiple file extensions (.php, .php5, .phtml, .phar) to bypass simplistic filters and locate the upload directory to verify successful code execution through direct HTTP access.

## Defensive takeaways
- Implement strict whitelist-based file type validation using MIME type checking and magic bytes verification, not just extension checking
- Store uploaded files outside the web root or in a directory with disabled script execution via web server configuration (.htaccess, web.config, nginx directives)
- Rename uploaded files with random names and remove or obfuscate original extensions
- Disable script execution for uploaded file directories using web server configuration (e.g., php_flag engine off)
- Implement proper access controls to restrict who can upload files
- Use Content-Disposition headers to force downloads instead of execution
- Implement virus scanning and content analysis for uploaded files
- Log and monitor file upload activities for suspicious patterns

## Variant hunting
Test alternative PHP extensions (.php3, .php4, .php5, .php7, .phtml, .phar, .inc, .phps)
Test double extensions (.php.jpg, .jpg.php)
Test null byte injection (.php%00.jpg)
Test case variation (.PHP, .PhP, .pHp)
Test .htaccess upload to enable script execution in specific directories
Test image file upload with PHP code embedded in metadata or polyglot files
Test other scripting languages (JSP, ASPX, CGI) if applicable to the platform

## MITRE ATT&CK
- T1190
- T1434
- T1505
- T1083

## Notes
This is a straightforward and high-impact vulnerability. The PoC demonstrates direct code execution through a simple phpinfo() call. The vulnerability exemplifies why file upload functionality requires defense-in-depth approaches combining multiple validation layers. The use of alternative extensions (.php5) to bypass basic filters is a common technique that highlights the ineffectiveness of simple blacklist approaches.

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
*Analysed by Claude on 2026-05-24*
