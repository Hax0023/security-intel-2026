# Plain Text File Upload via Driver Document Upload with Incorrect Extension Validation

## Metadata
- **Source:** HackerOne
- **Report:** 126374 | https://hackerone.com/reports/126374
- **Submitted:** 2016-03-27
- **Reporter:** ddworken
- **Program:** Uber
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Improper Input Validation, Unrestricted File Upload, Content-Type Mismatch, Phishing Vector
- **CVEs:** None
- **Category:** uncategorised

## Summary
Uber's driver document upload page only validates file extensions without verifying actual file content, allowing attackers to upload plain text files with image extensions (.png). When accessed via Internet Explorer, these files render as plain text, enabling phishing attacks through S3-hosted URLs.

## Attack scenario
1. Attacker creates a plain text file containing phishing content (fake login form, credential harvesting, etc.)
2. Attacker renames file with .png extension to bypass extension-based validation
3. Attacker uploads file through Uber driver registration document upload page
4. File is accepted and stored on uber-documents.s3.amazonaws.com with attacker-controllable content
5. Attacker generates S3 signed URL and distributes it to Uber users (via email, SMS, etc.)
6. Victims open URL in Internet Explorer, which renders plain text content instead of image due to matching extension/MIME type, enabling phishing attack

## Root cause
Uber implements insufficient file validation on the driver document upload endpoint. The validation only checks file extension without verifying: (1) actual file content/magic bytes, (2) MIME type matching actual file type, or (3) image validity. This contrasts with other upload forms where Uber performs proper image validation.

## Attacker mindset
Attacker identified a security control inconsistency - noticing that driver document uploads lack the same rigorous validation applied to profile picture uploads. They recognized that while JavaScript execution is blocked by IE's extension/MIME matching, plain text rendering still enables phishing. The attacker is security-conscious, reporting the vulnerability responsibly rather than exploiting it maliciously.

## Defensive takeaways
- Implement server-side file content validation using magic byte/file signature checking, not just extension validation
- Verify actual MIME type by parsing file headers, not accepting client-supplied Content-Type headers
- Apply consistent file upload validation across all upload endpoints in the application
- For document uploads, consider additional validation: validate image dimensions, re-encode images, scan for embedded content
- Implement Content-Disposition: attachment headers on S3 objects to force downloads instead of rendering
- Use X-Content-Type-Options: nosniff header to prevent MIME-type sniffing
- Consider hosting user-uploaded files on a separate domain (not same origin as main application) to limit attack surface
- Implement virus/malware scanning on uploaded files

## Variant hunting
Check other file upload endpoints (profile images, documents, media) for similar extension-only validation
Test with polyglot files (files valid as multiple types) to bypass validation
Attempt SVG uploads with script tags, validated only by extension
Test upload endpoints for XXE attacks in XML documents with image extensions
Check if other browsers (Chrome, Firefox) render content differently due to MIME type vs extension conflicts
Investigate if Content-Disposition headers are properly set on S3 objects
Test for direct file access without going through S3 signed URLs
Look for similar issues in other document submission workflows (background checks, licensing, etc.)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Identity Information: Spearphishing Link
- T1608.003 - Stage Capabilities: Install Digital Certificate

## Notes
Reporter demonstrates maturity by comparing to related vulnerability #126197 (likely JS execution via upload). The distinction between XSS protection and phishing risk shows nuanced security understanding. The vulnerability is rated Medium rather than High because: (1) phishing effectiveness depends on social engineering, (2) attack requires victim to click malicious link, (3) no direct system compromise. However, the impact on Uber drivers (financial fraud, identity theft) could be significant. The reference to IE-specific behavior is important context, though modern browsers have reduced this attack surface. Follow-up: check if Uber implemented similar fixes across all upload endpoints.

## Full report
<details><summary>Expand</summary>

Hi, 

When a new driver is registering on Uber, they have to upload a variety of files (proof of insurance, ID, etc). When these files are being uploaded, Uber.com only checks whether the files have the correct extension. This means that one can upload a plain text file with a ```.png``` extension and it will be rendered as plain text when viewed in Internet Explorer. 

At first I was attempting to get js execution with this (similar to how I did #126197), but that is not possible. When the file extension (```.png``` in our case) and the MIME type (```image/png```) match, Internet Explorer will not render it as HTML, it is only willing to render it as plain text. This still opens up a possibility of a fishing attach by doing something like this: 

```
https://uber-documents.s3.amazonaws.com/f7e83fb2-a309-4845-a038-8cb3846a0f0d.png?Signature=eQwYlK31HVRqaHN%2FdvaImVEDQuI%3D&Expires=1459110446&AWSAccessKeyId=AKIAIQSUTKT5KJFDBULQ
```

While this is not as bad as JS execution, I believe that this still qualifies as a vulnerability. In all other image upload forms (e.g. profile picture upload), Uber carefully checks that the image is valid before accepting it and hosting it. In this case, Uber fails to do so. 

Thanks,
David Dworken

</details>

---
*Analysed by Claude on 2026-05-24*
