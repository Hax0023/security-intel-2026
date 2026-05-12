# Stored XSS in Image Filename on Image Upload and Display

## Metadata
- **Source:** HackerOne
- **Report:** 583710 | https://hackerone.com/reports/583710
- **Submitted:** 2019-05-17
- **Reporter:** rioncool22
- **Program:** Undisclosed Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can upload an image with XSS payload embedded in the filename, which is stored and executed when the image is viewed. The application fails to sanitize filenames on upload and properly encode them during display, allowing arbitrary JavaScript execution in the context of the victim's browser.

## Attack scenario
1. Attacker logs into their account on the vulnerable application
2. Attacker uploads an image with filename containing XSS payload: "><img src=x onerror=prompt(document.domain)>.png
3. Application accepts and stores the malicious filename without validation or sanitization
4. Attacker shares the image link or tricks another user into viewing the uploaded image
5. When victim clicks on or views the image, the stored XSS payload executes in victim's browser
6. Arbitrary JavaScript runs with victim's privileges, enabling session hijacking, credential theft, or further attacks

## Root cause
The application fails to implement input validation on file uploads and output encoding when displaying file metadata. Filenames are directly rendered in HTML context without escaping special characters, and dangerous HTML entities are not filtered during upload.

## Attacker mindset
An attacker recognizes that user-controllable data (filenames) are often overlooked in security reviews. By exploiting the trust users place in file metadata, they can achieve persistent XSS that survives across sessions and affects multiple users who view the malicious image.

## Defensive takeaways
- Implement strict filename validation: accept only alphanumeric characters, hyphens, and underscores; reject special characters and HTML entities
- Sanitize filenames on upload using allowlist-based approach and remove/replace suspicious characters
- Apply context-appropriate output encoding (HTML entity encoding) when displaying filenames in HTML context
- Use Content Security Policy (CSP) headers to mitigate XSS impact even if payload reaches browser
- Store original filenames separately from display names; generate safe system filenames independent of user input
- Implement file upload scanning and validation libraries that detect encoded/obfuscated payloads
- Perform security testing on all user-controllable data sources, not just form inputs

## Variant hunting
Check other file upload features (avatars, documents, attachments) for similar filename XSS vulnerabilities
Test image metadata fields (EXIF data, image title properties) for stored XSS
Examine how filenames are displayed in directory listings, search results, and file management interfaces
Test with double-encoded payloads and alternative XSS vectors (SVG, data URIs) in filenames
Check if filename XSS persists in exported reports, archives, or API responses
Test multipart form uploads and alternate upload mechanisms for bypass techniques

## MITRE ATT&CK
- T1190
- T1566.002
- T1204.001

## Notes
This is a classic overlooked vulnerability category - file metadata exploitation. The simplicity of the payload and reproduction steps suggests this may have been missed during development. The vulnerability has high impact due to persistent nature and affects all users viewing the image. Report lacks specific application context and bounty amount, suggesting it may be from an earlier HackerOne report with limited details captured.

## Full report
<details><summary>Expand</summary>

I want to report bug XSS in "ADD IMAGES" 

How To Produce it : 
1. Login to your Account
2. Then Add Images With XSS Payload In filename (example : "><img src=x onerror=prompt(document.domain)>.png)
3. Click on Image that you upload
4. in the name of picture XSS will fired

## Impact

https://www.owasp.org/index.php/Cross-site_Scripting_(XSS)

</details>

---
*Analysed by Claude on 2026-05-12*
