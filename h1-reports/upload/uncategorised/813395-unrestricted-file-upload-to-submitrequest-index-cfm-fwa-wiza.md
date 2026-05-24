# Unrestricted File Upload in SubmitRequest/Index.cfm Wizard Form

## Metadata
- **Source:** HackerOne
- **Report:** 813395 | https://hackerone.com/reports/813395
- **Submitted:** 2020-03-09
- **Reporter:** z32
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Unrestricted File Upload, Arbitrary File Upload, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unauthenticated attacker can upload files of any type (executable, PHP, etc.) up to 5MB in size through a public request submission form. If an administrator opens the malicious file or discovers the upload path, the attacker could achieve remote code execution on the target system.

## Attack scenario
1. Attacker navigates to the public request submission form at PublicSite/index.cfm?fwa=newreq
2. Attacker fills out the request form with minimal information and email address
3. Attacker clicks the 'Upload Files' tab to access the file upload functionality
4. Attacker uploads a malicious file (executable, PHP webshell, etc.) under 5MB in size without restrictions
5. Attacker submits the request with the malicious attachment included
6. Administrator downloads and executes the file, or attacker discovers the upload directory and directly accesses the webshell for RCE

## Root cause
The file upload endpoint implements only a size restriction (5MB) without validating file types, extensions, MIME types, or content. No allowlist of safe file extensions is enforced, and uploaded files are likely stored in a web-accessible directory.

## Attacker mindset
An attacker recognizes that public-facing request/support forms are common attack vectors. By uploading malicious files disguised as legitimate documents or executable payloads, they can either social engineer administrators into running code or discover the upload path for direct webshell access. The 5MB limit is sufficient for most malicious payloads.

## Defensive takeaways
- Implement strict file type validation using allowlists (e.g., .pdf, .jpg, .png, .docx only)
- Validate file extensions, MIME types, and magic bytes to prevent bypasses
- Store uploaded files outside the web root or in a non-executable directory
- Rename uploaded files to remove original names and extensions
- Set proper file permissions (no execute) on upload directories
- Implement virus/malware scanning on uploaded files
- Require authentication for file upload functionality
- Log all upload attempts and monitor for suspicious patterns
- Consider reducing or removing file size limits for public uploads

## Variant hunting
Check for similar unrestricted uploads in other public forms (contact, feedback, ticket systems)
Test for path traversal in file upload endpoints (e.g., ../../../shell.php)
Attempt double extension bypasses (shell.php.jpg)
Test null byte injection in filenames (shell.php%00.jpg)
Try uploading .htaccess or web.config files to enable execution of otherwise safe extensions
Test for MIME type mismatch (upload PHP with image MIME type)
Look for race conditions in upload processing
Check if upload directory is directly accessible via HTTP

## MITRE ATT&CK
- T1190
- T1204.002
- T1566.002
- T1570

## Notes
This is a classic unrestricted file upload vulnerability with direct RCE potential. The attack requires low skill and involves zero authentication. The social engineering component (getting admin to download file) makes this particularly dangerous. The vulnerability was reported responsibly and files were deleted after proof-of-concept. Severity should be critical in most enterprise contexts due to RCE potential.

## Full report
<details><summary>Expand</summary>

**Summary:**
An attacker is able to upload files of any type to `███SubmitRequest/Index.cfm?fwa=wizardform` as long as they are less than 5 MB.

**Description:**
The █████ ████ Request System allows a user to submit requests to the ██████████ ███ for event support. An attacker can exploit this request form by uploading malicious files due to an unrestricted file upload feature.

## Impact
An attacker is able to upload malicious files onto the server. These files are attached to a request for support from the ██████ █████████. If a member of the ██████ ████ were to open the malicious file, the attacker could gain remote code execution on ████ information systems. Alternatively, if the attacker finds out how to browse to the file, they could obtain a web shell on the target, giving them remote code execution.

## Step-by-step Reproduction Instructions

1. Browse to `██████PublicSite/index.cfm?fwa=newreq` and click on `Create a New Request`.
██████████
2. Fill in your e-mail address and click `Submit`.
██████████
3. Fill out the fields in the form.
███
████
███
███████
4. Before submitting the request, click the `Upload Files` tab.
█████
5. This page will allow you to upload any file you wish as long as it is under 5MB in size. I tested by uploading an executable (visual studio community installer) and a php file. These files were deleted from my request after submitting this report.
███████
6. Once uploaded, you can submit your request. An attacker would need to submit this request in hopes of the █████ ████████ downloading the malicious attachment.

## Suggested Mitigation/Remediation Actions
Restrict file uploads to safe extensions such as .jpg, .png, etc. to prevent an attacker from uploading malicious files onto the server.

## Impact

An attacker is able to upload malicious files onto the server. These files are attached to a request for support from the ████ ██████████. If a member of the ████ ██████████ were to open the malicious file, the attacker could gain remote code execution on ██████ information systems. Alternatively, if the attacker finds out how to browse to the file, they could obtain a web shell on the target, giving them remote code execution.

</details>

---
*Analysed by Claude on 2026-05-24*
