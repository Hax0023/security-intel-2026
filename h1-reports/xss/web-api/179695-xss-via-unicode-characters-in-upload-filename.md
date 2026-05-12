# XSS via Unicode Characters in Upload Filename Leading to Privilege Escalation

## Metadata
- **Source:** HackerOne
- **Report:** 179695 | https://hackerone.com/reports/179695
- **Submitted:** 2016-11-02
- **Reporter:** kahoots
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored XSS, Input Validation Bypass, Privilege Escalation, Arbitrary File Upload
- **CVEs:** CVE-2020-11026
- **Category:** web-api

## Summary
WordPress fails to properly sanitize Unicode characters in uploaded filenames server-side, allowing authenticated users with upload privileges to bypass client-side validation and create files with malicious names that render as HTML/JavaScript. When an administrator visits the crafted file page, arbitrary JavaScript can execute with admin privileges, enabling account creation and privilege escalation.

## Attack scenario
1. Attacker with upload capabilities (contributor or editor role) crafts an image file containing JavaScript payload (e.g., <script>alert('XSS')</script>) and names it with a Unicode character prefix like '±myfile.png'
2. Attacker uses browser intercept tool (Tamperdata) to bypass client-side validation and submit the malicious filename to WordPress media upload endpoint
3. WordPress sanitize_file_name() function mishandles the Unicode character, returning 0 instead of a sanitized filename, resulting in file saved as '-1' (or '-2', etc.)
4. The malicious file is accessible at a URL that renders it as HTML content, triggering JavaScript execution in the browser
5. When an administrator visits this specially crafted page, the JavaScript executes with admin context, allowing creation of new admin accounts or other privileged actions
6. Attacker gains administrative access and full control of the WordPress installation

## Root cause
The sanitize_file_name() function in wp-admin/includes/file.php does not properly handle Unicode characters server-side. When a filename begins with a Unicode character, the sanitization returns 0 instead of a valid filename string. The fallback numeric naming scheme ('-1', '-2') combined with the lack of extension validation in the naming logic allows creation of executable files. Additionally, Apache and the application fail to enforce proper MIME-type handling for files with numeric names.

## Attacker mindset
An authenticated attacker with modest upload privileges recognizes that Unicode character handling differs between client and server validation layers. By intercepting the upload request and injecting Unicode characters, they can manipulate the filename sanitization logic to produce unexpected output. The attacker understands that numeric filenames bypass typical file extension-based security restrictions and that administrative users are likely to click on uploaded content, making social engineering or accidental execution probable.

## Defensive takeaways
- Implement strict server-side whitelist validation for filenames, rejecting any non-ASCII or special characters before sanitization attempts
- Ensure sanitize_file_name() returns a valid filename string; validate return values are non-empty and contain expected extensions before file operations
- Enforce MIME-type validation on uploaded files regardless of extension or filename
- Store uploaded files outside web root or configure web server to prevent execution of files in upload directories
- Implement Content-Security-Policy headers to prevent inline script execution from HTML files served from upload directories
- Validate that generated filenames conform to expected patterns; reject numeric-only filenames as suspicious
- Apply consistent validation on both client and server sides, with server-side validation being authoritative
- Conduct security review of all file handling functions, particularly around character encoding and Unicode normalization

## Variant hunting
Test UTF-8 encoded variations (e.g., multi-byte Unicode sequences, combining characters, zero-width characters) in filenames
Investigate other sanitization functions (sanitize_title, sanitize_key, etc.) for similar Unicode bypass patterns
Check if other special characters (null bytes, emoji, RTL override characters) produce similar sanitization failures
Test double-encoded Unicode sequences (%C2%B1) in form submissions vs. direct API calls
Examine if the vulnerability exists in other upload handlers (featured images, theme/plugin uploads)
Verify if numeric filenames can be crafted with other extensions (.php, .html, .phtml, etc.)
Test if directory traversal sequences combined with Unicode bypass can write files outside upload directory
Check if file permissions on generated '-1' files differ from normal uploads, allowing modification

## MITRE ATT&CK
- T1190
- T1195
- T1199
- T1547
- T1134
- T1036

## Notes
This vulnerability demonstrates a critical failure in multi-layer validation where server-side sanitization produces unexpected output (0) instead of a valid filename, and error handling defaults to a dangerous fallback value. The combination of weak filename validation + HTML rendering + administrative user interaction creates a high-impact privilege escalation chain. The reporter's analysis correctly identifies that the root cause is in _wp_handle_upload and wp_unique_filename functions. WordPress likely patched this by implementing stricter Unicode handling and return value validation in the sanitization pipeline.

## Full report
<details><summary>Expand</summary>

Wordpress has a vulnerability that could lead to javascript execution and (thus) privileged escalation via an admin visiting the wrong page via specially crafted JavaScript. Unicode characters are escaped by javascript but they are not escaped serverside. I've checked the latest version (4.6.1) at the time of writing this report and it is vulnerable.

Steps to reproduce: 

1. You will need a way to bypass javacsript in a post request. For purposes of this report I'll assume the free firefox plugin tamperdata is used.
2. You will need an installation of wordpress with the capability of uploading files.
3. Create a blank image file with a javascript alert i.e <script> alert('XSS') </script> and name the file a valid image extension such as .png
4. In wordpress, go to the file upload screen on the side bar (Media -> Add new). Activate tamperdata and click upload. Use a special Unicode character at the begining of the filename. Note that for this step all that is required is upload privileged - see https://codex.wordpress.org/Roles_and_Capabilities
5. The image page will be called "-1" visit that page. It will render as HTML.

Note that an image could be specially crafted with a 0-sized iframe and upon an administrator visiting the page could redirect via javascript to create another user account leading to privilege escalation.

Here is my explanation for the bug:

Unicode characters are not escaped server-side, but they appear to be escaped client side which can be bypassed. This can be shown by trying to upload a file with a unicode character and seeing the "Â" character before it. For example: "±myfile.png" would become "Â±myfile.png" - this was tested with tamperdata by watching the image field.

In wordpress\wp-admin\includes\file.php there is a function called "_wp_handle_upload" Ideally, this is where special characters should be escaped or dealt with. That functon calls "wp_unique_filename" which then calls "sanitize_file_name" which the return value is a number instead of a filename. 

If a file with a valid file extension is given such as "myfile.png" intended behavior is that it will save the file. If it is given twice, then it will be named myfile-1.png and so on. However, because a special character can make a return value of 0 from the unique_filename function, it will result in "-1" being the file name. If another file is uploaded it will be called "-2" if it is in the same year and month folder. For example: "wordpress\wp-content\uploads\2016\10" if there is already a "-1" file there and a month passes -1 would go in the next folder. "wordpress\wp-content\uploads\2016\11"

Apache normally prevents javascript execution from images, however a filename such as "-1" will render text which can execute javascript. 

The best mitigation would be to check for special characters in the _wp_handle_upload function.

(I'm new to writing hackerone reports, hopefully this is clear enough.)

</details>

---
*Analysed by Claude on 2026-05-12*
