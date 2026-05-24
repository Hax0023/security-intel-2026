# Arbitrary File Upload in Logo & Login Image Theming Setting

## Metadata
- **Source:** HackerOne
- **Report:** 155690 | https://hackerone.com/reports/155690
- **Submitted:** 2016-07-31
- **Reporter:** bastianwelfrid
- **Program:** Nextcloud
- **Bounty:** Not eligible for bounty (requires admin access)
- **Severity:** high
- **Vuln:** Arbitrary File Upload, Insufficient File Type Validation, Client-Side Code Execution
- **CVEs:** None
- **Category:** web-api

## Summary
The logo and login image theming settings in Nextcloud lack proper file type validation, allowing authenticated administrators to upload arbitrary files including HTML that will execute client-side. While PHP files are not executed server-side, HTML files are processed and executed by browsers, creating an XSS vector for admin-level users.

## Attack scenario
1. Attacker gains administrative access to Nextcloud instance through compromise, social engineering, or credential theft
2. Attacker navigates to the theming settings for Logo & Login Image configuration
3. Attacker uploads a malicious HTML file disguised as an image or with an image extension
4. Server accepts the file without proper validation and stores it in /data/themedinstancelogo or /data/themedbackgroundlogo
5. When users access the login page or interface, the HTML file is served and executed in their browsers
6. Malicious JavaScript payload within the HTML executes, potentially stealing session tokens or performing actions on behalf of users

## Root cause
Insufficient server-side file type validation on uploaded theming files. The application relies on file extension or MIME type checking without verifying actual file content or preventing execution of executable formats (HTML, SVG) that browsers will interpret.

## Attacker mindset
An admin-level attacker seeking to maintain persistence, harvest user credentials, or perform lateral attacks. The attacker recognizes that logo/login images are loaded for every user, making this an effective distribution point for client-side malicious code.

## Defensive takeaways
- Implement strict whitelist-based file type validation using magic bytes/file signatures, not just extensions or MIME types
- Re-encode uploaded images to strip any embedded code or metadata using image processing libraries
- Serve uploaded theme files with appropriate Content-Type headers and Content-Disposition: attachment to prevent browser interpretation
- Implement CSP (Content Security Policy) headers to restrict script execution and resource loading
- Validate file dimensions and properties to ensure they match legitimate image files
- Sanitize SVG files separately as they can contain malicious scripts
- Apply principle of least privilege to admin functions; restrict file upload capabilities where possible
- Monitor and alert on unusual file uploads in theming directories

## Variant hunting
Check other file upload functionality in theming/branding features (favicons, splash screens, backgrounds)
Test SVG file uploads which can contain embedded JavaScript
Test polyglot files (valid image + executable code combined)
Check if other admin upload features have similar validation bypasses
Test upload to other theme-related directories or configuration files
Verify if uploaded files can be accessed directly via web path without proper restrictions

## MITRE ATT&CK
- T1190
- T1434
- T1602

## Notes
Report classifies as low-severity/out-of-scope because it requires pre-existing admin access. However, it represents a significant privilege escalation concern in compromised admin accounts. The reporter correctly notes PHP files are not executed server-side (good defense), but HTML/SVG execution remains a valid XSS concern. The vulnerability chain (gain admin access → upload malicious HTML → XSS all users) is realistic and dangerous.

## Full report
<details><summary>Expand</summary>

Hi team

First I think this vulnerability doesn't fall at your bug bounty program but this is a bad design that should fix right now cause if an attacker get admin access he still can upload a malicious file in client server side.

I saw that Logo & Log in image allow to upload other files type example *.html and it'll execute in client server.
Other case,I created an html code and saved it as image file,server still executed it as html file.
The Logo & Log in image will upload it into ../data/themedinstancelogo & ../data/themedbackgroundlogo

Good news,I tried to upload an php file but server executed that file as text.

PoC:
Upload an html file through logo upload and Log in image and you will see that file will execute.

http://example.com/nextcloud/data/themedinstancelogo
http://example.com/nextcloud/data/themedbackgroundlogo

Regards,


</details>

---
*Analysed by Claude on 2026-05-24*
