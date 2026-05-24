# XSS through SVG image upload in contacts

## Metadata
- **Source:** HackerOne
- **Report:** 894876 | https://hackerone.com/reports/894876
- **Submitted:** 2020-06-09
- **Reporter:** hitman_47
- **Program:** Unknown
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Insufficient File Type Validation, SVG Script Injection
- **CVEs:** CVE-2020-8281
- **Category:** web-api

## Summary
An attacker can upload a malicious SVG file as a contact image that executes JavaScript when the image is opened in a new tab. This bypasses a previous XSS fix and allows arbitrary code execution in the victim's browser context.

## Attack scenario
1. Attacker crafts a malicious SVG file containing embedded JavaScript code
2. Attacker uploads the SVG file to the application as a contact profile image
3. Attacker shares the contact or victim accesses the contact information
4. Victim right-clicks on the contact image and selects 'Open image in new tab'
5. Browser renders the SVG file with embedded scripts enabled
6. JavaScript executes in the victim's browser, allowing session hijacking, credential theft, or malware distribution

## Root cause
The application failed to properly sanitize SVG files during upload validation. SVG files can contain embedded JavaScript that executes when rendered by a browser, even with image file extension restrictions. The previous fix likely only addressed direct script injection in HTML contexts but did not account for SVG-specific attack vectors.

## Attacker mindset
The attacker identified that a prior XSS mitigation was incomplete and focused on alternative file format vectors. They recognized that SVG files are treated as images by the application but can contain executable scripts, creating a bypass opportunity. The choice to use 'Open image in new tab' demonstrates awareness of browser rendering contexts.

## Defensive takeaways
- Implement strict SVG sanitization using libraries that remove script tags and event handlers
- Use Content Security Policy (CSP) headers to restrict script execution on user-uploaded content
- Serve uploaded files from a separate domain or with X-Content-Type-Options: nosniff header
- Validate file contents (magic bytes) not just extensions
- Disable JavaScript execution in uploaded SVG files by converting to raster or using sandboxed rendering
- Implement allowlist-based file type validation with strict MIME type checking
- Test all file upload vectors including SVG, XML, and other text-based image formats

## Variant hunting
Other text-based image formats: XML, PDF with embedded scripts, animated GIF with JavaScript
Upload bypass techniques: double extension (file.svg.jpg), null byte injection (file.svg%00.jpg)
Alternative XSS payloads in SVG: event handlers (onload, onerror), animate tags with script content
Other file upload fields: favicon, banner, logo, thumbnail uploads
Related vulnerabilities: SSRF through SVG parsing, XXE through SVG content

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002

## Notes
This is explicitly marked as a bypass of report #808287, indicating the organization had previously attempted to fix a similar vulnerability but the fix was incomplete. SVG files represent a critical blind spot in file upload security as they are often whitelisted as 'safe' image formats while retaining script execution capabilities. The attack surface expanded by browser features like 'Open image in new tab' which may apply different rendering rules than embedded image tags.

## Full report
<details><summary>Expand</summary>

This is a bypass of report #808287

Upload the attached file for the image of a contact, right click "Open image in new tab" and you will see the xss.

## Impact

The person viewing the image of a contact can be victim of XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
