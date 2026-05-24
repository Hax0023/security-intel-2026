# Unrestricted File Upload on Contact Image

## Metadata
- **Source:** HackerOne
- **Report:** 808287 | https://hackerone.com/reports/808287
- **Submitted:** 2020-03-01
- **Reporter:** hitman_47
- **Program:** Unknown (HackerOne #808287)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Arbitrary File Upload, Insufficient Input Validation
- **CVEs:** CVE-2020-8181
- **Category:** business-logic

## Summary
The contact image upload functionality accepts and processes executable files without proper validation or restriction. An attacker can upload malicious executables disguised as image files, potentially leading to code execution or malware distribution.

## Attack scenario
1. Attacker navigates to contact creation/editing page with image upload feature
2. Attacker selects a malicious executable file (e.g., .exe, .bat, .sh) instead of image
3. File upload dialog claims to accept 'all file types' without restrictions
4. Server accepts and stores the executable file without validation
5. Attacker shares contact or waits for admin/user to access/download the file
6. Executable file is executed on victim's system, delivering payload (malware, ransomware, etc.)

## Root cause
Lack of server-side file type validation and filtering on the upload endpoint. The application relies on client-side restrictions (if any) or no restrictions at all, allowing any file type to be uploaded and stored.

## Attacker mindset
Opportunistic weaponization of feature - recognizes that user-facing upload endpoints are often overlooked security controls. Seeks to distribute malware through trusted application interface or achieve code execution through unrestricted upload.

## Defensive takeaways
- Implement server-side file type validation using magic bytes/file signatures, not just extensions
- Maintain whitelist of allowed MIME types and extensions (e.g., .jpg, .png, .gif only)
- Store uploaded files outside webroot or in directory with execution disabled
- Rename uploaded files to prevent direct execution
- Scan uploads with antivirus/malware detection engines
- Implement file size limits to prevent DoS
- Use Content-Disposition: attachment header to prevent browser execution
- Consider sandboxed preview generation for images

## Variant hunting
Profile picture/avatar uploads
Document upload features (resume, ID verification)
Attachment features in messaging/collaboration tools
Media gallery uploads
User-generated content uploads on any endpoint
Batch/bulk upload features
API file upload endpoints without UI restrictions

## MITRE ATT&CK
- T1190
- T1204.002
- T1566.001

## Notes
Reporter demonstrates basic understanding of impact but minimal technical depth (notes uploaded exe 'doesn't do anything without parameters'). This appears to be a straightforward validation bypass rather than sophisticated exploitation. The vulnerability is impactful because contact features often have lower security expectations and may be leveraged for social engineering or direct malware distribution.

## Full report
<details><summary>Expand</summary>

When uploading an image for a contact, on the file upload pop up window it shows that it can accept all files of any data type. For my testing I uploaded a sample executable, named 'SimpleCrackMe.exe' which doesn't do really do anything without passing parameters to it on a terminal when running it. The file was uploaded successfully.

## Impact

An attacker could upload a dangerous executable file like a virus, malware, etc.. If you don't think this is a vulnerability, please let me close the report myself so that I don't lose points

</details>

---
*Analysed by Claude on 2026-05-24*
