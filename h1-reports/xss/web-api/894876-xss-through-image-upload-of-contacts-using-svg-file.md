# XSS through image upload of contacts using SVG file

## Metadata
- **Source:** HackerOne
- **Report:** 894876 | https://hackerone.com/reports/894876
- **Submitted:** 2020-06-09
- **Reporter:** hitman_47
- **Program:** HackerOne (implicit from URL structure)
- **Bounty:** Not specified in provided content
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Improper File Upload Validation, Insufficient MIME Type Checking
- **CVEs:** CVE-2020-8281
- **Category:** web-api

## Summary
An attacker can upload a malicious SVG file as a contact image that executes arbitrary JavaScript when the image is opened in a new tab. This vulnerability bypasses a previous patch (report #808287) by exploiting inadequate SVG file validation during the upload process.

## Attack scenario
1. Attacker creates a malicious SVG file containing embedded JavaScript code (e.g., alert() or credential theft payload)
2. Attacker uploads the SVG file through the contact image upload functionality
3. The application accepts the SVG file without proper sanitization or content validation
4. Victim views the attacker's contact in the application
5. Victim right-clicks the contact image and selects 'Open image in new tab'
6. Browser renders the SVG file and executes the embedded JavaScript in victim's context

## Root cause
The application fails to properly validate and sanitize SVG file uploads. SVG files are XML-based and can contain executable scripts. The previous patch (report #808287) did not comprehensively address SVG handling, allowing malicious SVG files to bypass validation by checking only file extensions or basic MIME types without inspecting the file content.

## Attacker mindset
The attacker identifies that a previous XSS vulnerability was patched and systematically tests alternative file formats (SVG) that could contain executable code. They recognize that SVG files are often treated as images but can execute scripts, and that opening images in new tabs may bypass certain protections implemented in the main application context.

## Defensive takeaways
- Implement strict server-side file validation that inspects actual file content, not just extensions or MIME types
- For image uploads, re-encode images server-side (convert to standardized formats like JPEG/PNG) to strip any potentially malicious content
- Disable script execution in uploaded SVG files by removing or sanitizing script tags and event handlers
- Serve uploaded files with Content-Disposition: attachment headers to prevent rendering in browser tab
- Implement a whitelist of allowed image formats and reject SVG unless absolutely necessary
- Use Content-Security-Policy headers to restrict script execution on uploaded content
- Implement comprehensive regression testing for bypass attempts against previously patched vulnerabilities

## Variant hunting
Test other XML-based image formats (SVGZ, XML-based TIFF variants)
Attempt data URI schemes embedded in image metadata
Test JavaScript execution through CSS within image files
Check if other file upload endpoints have similar SVG bypass issues
Test SVG files with obfuscated or nested script tags to evade simple filters
Verify if the vulnerability persists when opening images through different methods (preview, direct link, etc.)

## MITRE ATT&CK
- T1190
- T1071
- T1566

## Notes
This report explicitly references a previous vulnerability bypass (report #808287), indicating the attacker performed regression testing on a patched vulnerability. The use of SVG files is a known technique to bypass image upload restrictions since SVG is technically a vector format but is XML-based and supports embedded scripts. The severity is amplified by the contact functionality context, which may involve trusted relationships where users are more likely to interact with images.

## Full report
<details><summary>Expand</summary>

This is a bypass of report #808287

Upload the attached file for the image of a contact, right click "Open image in new tab" and you will see the xss.

## Impact

The person viewing the image of a contact can be victim of XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
