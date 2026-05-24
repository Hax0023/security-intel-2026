# Arbitrary Filename Control in Logo/Favicon Upload via Key Parameter Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1781751 | https://hackerone.com/reports/1781751
- **Submitted:** 2022-11-22
- **Reporter:** ctulhu
- **Program:** HackerOne (specific program not disclosed in writeup)
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** Arbitrary File Upload, Path Traversal, Information Disclosure, Insufficient Input Validation
- **CVEs:** CVE-2023-28833
- **Category:** uncategorised

## Summary
An attacker can control the filename when uploading logo or favicon files by modifying the 'key' parameter in the upload request. Combined with path disclosure in error messages, this enables arbitrary file placement within the web application directory and reveals sensitive path information for further exploitation.

## Attack scenario
1. Attacker navigates to the admin theming settings page at /settings/admin/theming
2. Attacker initiates a logo or favicon file upload through the legitimate interface
3. Attacker intercepts the HTTP request using a proxy tool (e.g., Burp Suite)
4. Attacker modifies the 'key' parameter to specify a malicious filename or path (e.g., traversal sequences like '../' or executable extensions)
5. Attacker forwards the modified request, causing the file to be uploaded with the attacker-controlled filename
6. Attacker leverages the disclosed file path from error messages to locate and potentially execute or reference the uploaded file in subsequent attacks

## Root cause
The application does not properly validate or sanitize the 'key' parameter used as the filename during file uploads. The backend trusts the user-supplied key without implementing whitelist validation, filename restrictions, or path traversal prevention. Error messages also leak the full file path, compounding the vulnerability.

## Attacker mindset
An attacker would exploit this to achieve persistent code execution, overwrite critical files, or create web-accessible payloads. The combination of filename control and path disclosure makes this a valuable stepping stone for privilege escalation or remote code execution by uploading malicious files to predictable locations.

## Defensive takeaways
- Implement strict filename validation using a whitelist of allowed characters (alphanumeric, dash, underscore only)
- Generate server-side random filenames and map them to original filenames in a database rather than using user input
- Enforce file extension restrictions and validate MIME types server-side
- Implement path traversal prevention by rejecting any key containing './', '../', or path separators
- Avoid disclosing full filesystem paths in error messages; use generic error responses
- Store uploaded files outside the web root or in a non-executable directory
- Apply proper access controls to the theming admin page (authentication/authorization verification)
- Sanitize and reject null bytes and special characters in filenames

## Variant hunting
Check other file upload endpoints (profile pictures, documents, attachments) for similar key/filename control issues
Test if path traversal sequences can upload files to parent directories or outside intended upload folder
Attempt to upload files with executable extensions (.php, .jsp, .asp, .exe) to see if execution is possible
Test if path disclosure occurs in other error conditions (validation errors, permission denied, etc.)
Check if the 'key' parameter is used in other contexts that could be exploited (e.g., file deletion, access control)
Test if symlink or special file uploads are possible to bypass restrictions
Examine other admin settings pages for similar pattern vulnerabilities

## MITRE ATT&CK
- T1190
- T1083
- T1567
- T1105
- T1552

## Notes
This vulnerability is relatively straightforward to exploit and has clear impact when combined with path disclosure. The fix is simple (server-side filename generation), making this a common finding in web applications. The lack of input validation on what should be a server-controlled value suggests broader input validation weaknesses in the codebase. Severity could escalate to 'High' if the uploaded files can be executed or if they overwrite critical application files.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello,

When uploading a logo or favicon the filename can be controlled by attacker since the ```key``` can be modified which serves as the  filename.


{F2044799}

{F2044800}

{F2044798}

Due to an error the path is also disclosed

{F2044802}

## Steps To Reproduce:
[add details for how we can reproduce the issue]

1. go to ```http://localhost/settings/admin/theming```
2. upload  a logo or favicon
3. intercept the request using burp
4. modify the key

## Impact

The attacker can upload any files directly in the webapp and path disclosure. Combining both information can be useful in later attacks.

</details>

---
*Analysed by Claude on 2026-05-24*
