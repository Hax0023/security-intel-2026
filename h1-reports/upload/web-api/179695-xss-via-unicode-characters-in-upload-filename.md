# XSS via Unicode Characters in Upload Filename

## Metadata
- **Source:** HackerOne
- **Report:** 179695 | https://hackerone.com/reports/179695
- **Submitted:** 2016-11-02
- **Reporter:** kahoots
- **Program:** WordPress
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Privilege Escalation, Improper Input Validation, Character Encoding Bypass
- **CVEs:** CVE-2020-11026
- **Category:** web-api

## Summary
WordPress fails to properly sanitize Unicode characters in uploaded filenames server-side, allowing attackers to create files with names like '-1' that render as HTML and execute JavaScript. An authenticated user with upload privileges can exploit this to inject malicious scripts that execute when administrators visit the file page, potentially leading to privilege escalation through account creation.

## Attack scenario
1. Attacker with upload privileges crafts a POST request using an interceptor tool (tamperdata) to bypass client-side JavaScript validation
2. Attacker uploads a file with a Unicode character (e.g., '±myfile.png') in the filename, which server-side sanitization reduces to '-1'
3. The file is saved to disk with a numeric filename ('-1') in the WordPress uploads directory (e.g., wp-content/uploads/2016/10/-1)
4. When accessed directly, the '-1' file renders as HTML instead of an image, executing embedded JavaScript content
5. Administrator visits the crafted file URL, triggering the JavaScript payload
6. Malicious JavaScript (via hidden iframe) redirects admin to create a new privileged user account, achieving privilege escalation

## Root cause
The _wp_handle_upload() function in wp-admin/includes/file.php calls sanitize_file_name() to handle filenames, but Unicode character handling is inconsistent between client-side and server-side. Unicode characters are escaped client-side but not validated server-side, causing sanitize_file_name() to return 0 or invalid values, resulting in numeric filenames like '-1' that bypass Apache's JavaScript execution restrictions and render as HTML.

## Attacker mindset
An authenticated user exploits a trust boundary issue—WordPress sanitizes for XSS in normal filenames but fails on edge cases with Unicode. The attacker recognizes that numeric filenames bypass directory traversal protections and that direct file access renders content as HTML. By chaining this with social engineering (admin visits a page), privilege escalation becomes achievable without requiring admin credentials.

## Defensive takeaways
- Implement strict whitelist-based filename validation accepting only alphanumeric characters, hyphens, and underscores; reject or strip all other characters including Unicode
- Sanitize filenames consistently on both client and server side; never rely solely on client-side validation
- Validate that sanitized filenames are non-empty and do not result in numeric-only names; add fallback naming for edge cases
- Ensure uploaded files cannot be executed or rendered as HTML; use Content-Disposition: attachment headers and disable script execution in upload directories via .htaccess or web server config
- Implement Content Security Policy (CSP) headers to prevent inline script execution even if files render as HTML
- Regularly audit upload handling code for character encoding edge cases and test with international/special characters

## Variant hunting
Test other special characters (emoji, control characters, null bytes) in filenames to trigger similar sanitization failures
Check if other file operations (rename, copy, delete) have similar Unicode handling gaps
Investigate whether the vulnerability exists in other file upload endpoints (theme uploads, plugin uploads)
Test if double Unicode characters or mixed Unicode/ASCII combinations bypass sanitization differently
Check if the vulnerability allows directory traversal via Unicode normalization (e.g., ../ encoded as Unicode)
Verify if numeric filenames like '-1' can conflict with or overwrite existing files in edge cases

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1204.001 - User Execution: Malicious Link
- T1566.002 - Phishing: Spearphishing Link
- T1547.015 - Boot or Logon Initialization Scripts: Web Shell
- T1059.007 - Command and Scripting Interpreter: JavaScript

## Notes
Report dated pre-4.6.1 WordPress. The vulnerability chains client-side bypass (tampering with POST data) with server-side sanitization failure (Unicode handling) and Apache misconfiguration (rendering numeric files as HTML). The reporter's suggestion to validate in _wp_handle_upload() is sound but incomplete—fixing sanitize_file_name() behavior and ensuring files cannot render as HTML are equally critical. This is a good example of how edge cases in character handling can bypass security measures designed for typical inputs.

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
*Analysed by Claude on 2026-05-24*
