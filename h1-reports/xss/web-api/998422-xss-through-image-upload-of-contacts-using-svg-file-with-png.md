# XSS through image upload of contacts using SVG file with PNG extension

## Metadata
- **Source:** HackerOne
- **Report:** 998422 | https://hackerone.com/reports/998422
- **Submitted:** 2020-10-05
- **Reporter:** hitman_47
- **Program:** HackerOne (specific program not specified in writeup)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), File Upload Validation Bypass, MIME Type Mismatch
- **CVEs:** CVE-2020-8280
- **Category:** web-api

## Summary
An attacker can bypass file upload restrictions by uploading an SVG file containing malicious JavaScript with a .png extension, resulting in stored XSS when the image is viewed in the contacts section. This vulnerability is a bypass of a previous fix (report #89487) that only validated file extensions without proper MIME type verification.

## Attack scenario
1. Attacker creates an SVG file containing malicious JavaScript payload (e.g., <script> tags or onload event handlers)
2. Attacker renames or uploads the SVG file with a .png extension to bypass extension-based validation
3. Attacker uploads the malicious file as a contact image through the contacts feature
4. Server accepts the file based on extension whitelist without verifying actual file content/MIME type
5. When another user views the contact with the malicious image, the browser interprets the SVG and executes the embedded JavaScript
6. Attacker achieves stored XSS, potentially stealing session cookies, credentials, or performing actions on behalf of the victim

## Root cause
The application validates uploaded files based solely on file extension (.png) without performing proper MIME type verification or content inspection. SVG files are XML-based and can contain executable scripts, but are treated as safe image files when the extension is spoofed.

## Attacker mindset
The attacker demonstrates iterative vulnerability research by building on a previous disclosure. Rather than finding a completely new vulnerability, they identified that the patch for report #89487 was incomplete, only addressing one aspect (extension) while leaving the core vulnerability (MIME type bypass) intact.

## Defensive takeaways
- Implement server-side file type validation based on MIME type headers, not just file extensions
- Use file magic number/signature verification to confirm actual file content matches declared type
- Configure SVG files as a prohibited upload type for user profile images, or serve them with Content-Type: image/svg+xml; sandbox restrictions
- Parse and validate image files on the server using dedicated image processing libraries that reject malformed or suspicious content
- Implement Content-Security-Policy headers to prevent inline script execution
- Use randomized filenames and store uploads outside web root to prevent direct execution
- Perform comprehensive regression testing when patching file upload vulnerabilities

## Variant hunting
Test other image extensions (.jpg, .gif, .webp) with SVG content containing scripts
Attempt uploading SVG with double extensions (.png.svg, .svg.png)
Try SVG files with null byte injection (.svg%00.png)
Test uploading SVG as favicon or other image types in different application features
Attempt polyglot files (valid image + valid SVG with scripts)
Test other XML-based formats (XML, PDF) with embedded scripts and mismatched extensions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.002 - Phishing for Information: Spearphishing Link
- T1204.001 - User Execution: Malicious Link

## Notes
This is a classic example of an incomplete security patch. The original fix likely added extension whitelisting but failed to implement proper MIME type or content validation. SVG files are particularly dangerous in upload scenarios as they're legitimate image files but can contain executable code. The writeup is minimal but clearly communicates a functional bypass of a previous patch.

## Full report
<details><summary>Expand</summary>

Hello again, this is a bypass #89487 basically use the same payload file but change the extension to PNG

## Impact

XSS or Open redirect when viewing the image of a contact

</details>

---
*Analysed by Claude on 2026-05-12*
