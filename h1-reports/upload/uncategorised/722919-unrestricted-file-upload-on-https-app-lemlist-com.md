# Unrestricted File Upload on https://app.lemlist.com

## Metadata
- **Source:** HackerOne
- **Report:** 722919 | https://hackerone.com/reports/722919
- **Submitted:** 2019-10-25
- **Reporter:** ctulhu
- **Program:** Lemlist
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Unrestricted File Upload, Arbitrary File Upload, Client-Side File Type Validation Bypass, Remote Code Execution (potential)
- **CVEs:** None
- **Category:** uncategorised

## Summary
An unrestricted file upload vulnerability was discovered in the Email Signature upload feature of Lemlist's application, allowing authenticated users to upload arbitrary file types including executable files like .html. The uploaded files are accessible and executable by visiting their direct URL, potentially enabling website defacement or remote code execution.

## Attack scenario
1. Attacker authenticates to https://app.lemlist.com with valid credentials
2. Attacker navigates to Settings > Email Signature and clicks the upload option
3. Attacker uploads a malicious file with .html extension containing JavaScript payload or other executable content
4. The application accepts the upload without proper file type validation
5. Attacker retrieves the direct URL of the uploaded file from the file context menu
6. Attacker visits the URL or distributes it to victims, causing the malicious content to execute in the browser context

## Root cause
The application implements insufficient file upload validation, likely relying only on client-side extension checking or weak server-side validation that can be bypassed. The uploaded files are stored in a web-accessible directory and served with MIME types that allow browser execution rather than forcing download.

## Attacker mindset
An authenticated attacker seeks to abuse file upload functionality for malicious purposes. The attacker recognizes that file extension filters are bypassable and that web-accessible storage combined with executable MIME types creates an exploitation pathway for defacement or XSS attacks.

## Defensive takeaways
- Implement strict server-side file type validation based on file content (magic bytes) rather than extension alone
- Maintain a whitelist of allowed file types and reject all others by default
- Store uploaded files outside the web root or in a non-executable directory
- Serve uploaded files with restrictive Content-Disposition headers (force download) and appropriate Content-Type headers
- Disable script execution in upload directories via web server configuration (.htaccess, nginx rules)
- Implement file size limits and scan uploads for malware
- Apply principle of least privilege to file upload functionality (restrict to necessary users)
- Use random filenames and avoid preserving original extensions that could indicate file type
- Validate uploads after storage to ensure they match expected types

## Variant hunting
Check other upload features in Lemlist (profile pictures, attachments, templates) for similar vulnerabilities
Test uploading executable formats: .php, .jsp, .asp, .exe, .sh, .svg+xml, .phtml
Test null byte injection (.html%00.jpg) on older PHP versions
Attempt double extension uploads (.html.jpg)
Test case sensitivity bypasses (.HTML, .HtMl)
Check if Content-Type header manipulation allows bypass
Verify if uploaded files inherit folder-based execution permissions
Test compressed archive uploads (.zip, .tar) for extraction vulnerabilities
Check polyglot file uploads (valid image + embedded HTML)
Investigate if admin/premium users have different validation rules

## MITRE ATT&CK
- T1190
- T1204.001
- T1566.002

## Notes
This is a classic unrestricted file upload vulnerability with high practical impact. The presence of authentication is a control, but not sufficient given that any authenticated user can exploit it. The defacement impact mentioned suggests XSS capabilities; RCE is possible if the server executes server-side templates or scripts. The writeup lacks specific MIME type details and server response codes that would strengthen the analysis.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi! i found an Unrestricted File Upload on https://app.lemlist.com which let me upload anything.
File Extensions Such as .html and others should not be executed on the server side.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

* 1.) Login to https://app.lemlist.com
* 2.) Go to Settings >  Email Signature > Click the 3 Dots > Upload File
{F617850}
* 3.) Download {F617851} and Upload it 
* 4.) Right Click and Get the Link of the Uploaded File, Visit the Link.
{F617852}

## Impact

attacker can bypass upload restrictions and deface the page.

</details>

---
*Analysed by Claude on 2026-05-24*
