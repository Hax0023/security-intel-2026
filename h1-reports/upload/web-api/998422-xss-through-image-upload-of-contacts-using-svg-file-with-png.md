# XSS through Image Upload via SVG File with PNG Extension

## Metadata
- **Source:** HackerOne
- **Report:** 998422 | https://hackerone.com/reports/998422
- **Submitted:** 2020-10-05
- **Reporter:** hitman_47
- **Program:** Unknown (HackerOne Report #998422)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), File Type Validation Bypass, Open Redirect
- **CVEs:** CVE-2020-8280
- **Category:** web-api

## Summary
An attacker can upload a malicious SVG file with a .png extension to bypass file type validation in the contacts image upload functionality. When the image is viewed, the SVG payload executes, leading to stored XSS or open redirect attacks.

## Attack scenario
1. Attacker creates a malicious SVG file containing JavaScript code or redirect directives
2. Attacker renames the SVG file with a .png extension to bypass client-side or weak server-side validation
3. Attacker uploads the file through the contacts feature's image upload functionality
4. Server accepts the file based on extension whitelist without verifying actual file type
5. When a user views the contact's image, the browser renders the SVG and executes the embedded payload
6. XSS payload executes in the context of the application, or user is redirected to malicious site

## Root cause
Insufficient file type validation relying solely on file extension rather than MIME type verification or file content inspection. The server does not validate the actual file format before storing or serving user-uploaded images.

## Attacker mindset
Bypass security controls through simple obfuscation; exploit trust in file extension validation; target functionality that processes user-controlled files without proper sanitization.

## Defensive takeaways
- Validate file types using MIME type detection and magic bytes, not just file extensions
- Implement server-side file content verification before accepting uploads
- Store uploaded files outside webroot or in a separate domain to prevent script execution
- Sanitize SVG files or disable SVG uploads entirely in user-facing applications
- Use Content-Security-Policy headers to mitigate XSS impact
- Serve uploaded files with Content-Type: application/octet-stream to prevent browser interpretation
- Implement strict whitelist of allowed MIME types with verification

## Variant hunting
Test other image formats with dangerous file types (SVG as JPG, GIF, WEBP)
Check if double extensions bypass validation (file.svg.png)
Test null byte injection (file.svg%00.png)
Try case variation (file.SVG.png, file.sVg.png)
Attempt to upload other script-capable formats (HTML as image extension)
Check image processing library exploitation (ImageMagick delegates)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1059.007 - Command and Scripting Interpreter: JavaScript

## Notes
This is a duplicate/variant of report #89487, indicating the program had a previous similar finding that was not comprehensively patched. The vulnerability demonstrates that extension-based validation alone is insufficient for file upload security. SVG files are particularly dangerous as they natively support JavaScript execution.

## Full report
<details><summary>Expand</summary>

Hello again, this is a bypass #89487 basically use the same payload file but change the extension to PNG

## Impact

XSS or Open redirect when viewing the image of a contact

</details>

---
*Analysed by Claude on 2026-05-24*
