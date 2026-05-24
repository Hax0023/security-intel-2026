# Arbitrary File Upload via External Avatar Link

## Metadata
- **Source:** HackerOne
- **Report:** 149268 | https://hackerone.com/reports/149268
- **Submitted:** 2016-07-05
- **Reporter:** strukt
- **Program:** ExpressionEngine (implied from context)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Arbitrary File Upload, Insufficient Input Validation, Path Traversal, Remote Code Execution (potential)
- **CVEs:** None
- **Category:** memory-binary

## Summary
An administrator can upload arbitrary files to the server by specifying external URLs in the avatar upload feature. The application fetches content from user-supplied URLs and saves them with their original extensions without proper validation, allowing upload of malicious file types including executables and archives.

## Attack scenario
1. Attacker gains or compromises administrator account credentials
2. Attacker navigates to admin panel avatar settings at /admin.php?/cp/members/profile/settings
3. Attacker selects 'Link to avatar' option and provides URL to malicious file (e.g., http://attacker.com/shell.php or shell.svg.php)
4. Application downloads content from attacker's URL without validating MIME type or file extension safety
5. File is saved to /images/avatars/ directory with original extension intact
6. Attacker accesses uploaded file and achieves arbitrary code execution if executable file type was uploaded

## Root cause
The avatar upload handler blindly fetches remote content and saves it with the source URL's file extension without: (1) validating that only image MIME types are downloaded, (2) enforcing allowed file extensions, (3) converting uploaded files to safe formats, or (4) storing uploads outside web root or with execution disabled.

## Attacker mindset
An attacker with admin access seeks to escalate privileges to server-level code execution. By abusing the avatar feature's URL handling, they bypass typical file upload restrictions by leveraging the server's own HTTP client to fetch arbitrary files. Using polyglot files (e.g., .svg with embedded scripts or .php.svg) or relying on web server misconfiguration (.svg served as PHP), they achieve RCE.

## Defensive takeaways
- Validate MIME types of downloaded content using server-side inspection, not client-supplied extensions
- Whitelist only safe image formats (JPEG, PNG, WebP) and convert all uploads to these formats
- Disable script execution in upload directories via web server configuration (.htaccess, nginx config)
- Store uploads outside webroot or in directories not directly accessible via HTTP
- Implement strict filename sanitization; rename files to remove original extensions
- Use Content-Disposition: attachment headers for uploaded files
- Validate URLs before fetching; restrict to internal URLs only or use a whitelist
- Enforce rate limiting on external URL fetches to prevent SSRF/DoS
- Log all admin file operations and audit avatar uploads regularly

## Variant hunting
Check other user-uploadable features that accept external URLs (profile banners, logos, cover photos)
Test if path traversal works in filename parameter (e.g., ../../../shell.php)
Attempt to upload files with double extensions (.php.jpg) to bypass validators
Try uploading to different extensions that may be executable (.phtml, .phar, .shtml)
Test if SVG files with JavaScript payloads execute in browser context
Check if .zip or archive uploads can be auto-extracted by the application
Verify if non-admin users can exploit similar features in profile editing
Attempt SSRF via internal IP ranges (127.0.0.1, 192.168.x.x) to access internal services
Test for XXE payloads in SVG upload handling

## MITRE ATT&CK
- T1190
- T1434
- T1566
- T1598
- T1105

## Notes
This vulnerability requires admin access but poses critical risk as it leads to server compromise. The use of SVG with embedded scripts and the mention of .zip files suggests the server may execute content within upload directories. The reporter responsibly demonstrated the issue without providing actual payload details. ExpressionEngine and similar CMS platforms should implement strict file validation pipelines for all external content ingestion.

## Full report
<details><summary>Expand</summary>

Hello,

When an administrator attempts to set an avatar from an external link, the parser just takes the source of whatever link they point it to and creates a file with the same extension and content in the uploads folder.

##Steps to reproduce:

1- Visit http://[HOST]/admin.php?/cp/members/profile/settings and scroll to the "Change avatar" section.
2- Choose "Link to avatar" and set it's value to `http://strukt.tk/test.svg`
3- After redirection, if you have a proxy, a request will be made to something like `http://[HOST]/images/avatars/test_1.svg` on your localhost. Try opening that in your browser and you should see an alert box over there.
4- You can try that with `https://ellislab.com/asset/file/ee_server_wizard.zip`, it will create a .zip file over there.

That being said, an attacker can use other file types and may be able to run arbitrary commands on the OS.

Regards

</details>

---
*Analysed by Claude on 2026-05-24*
