# Authenticated Path Traversal to RCE in Concrete5 CMS Layout Designer

## Metadata
- **Source:** HackerOne
- **Report:** 1102067 | https://hackerone.com/reports/1102067
- **Submitted:** 2021-02-12
- **Reporter:** d3addog
- **Program:** Concrete5 CMS
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Path Traversal, Arbitrary File Inclusion, Remote Code Execution, Insecure File Upload
- **CVEs:** CVE-2021-40097
- **Category:** memory-binary

## Summary
The bFilename parameter in the block design submission endpoint is vulnerable to path traversal, allowing authenticated users with page editing rights to include arbitrary files via relative paths. By uploading a PNG file with embedded PHP code and referencing it through the vulnerable parameter, attackers can achieve remote code execution with web server privileges.

## Attack scenario
1. Attacker authenticates to Concrete5 with page editing privileges
2. Attacker uploads a malicious PNG file containing PHP code at the end (polyglot file) using any available upload function (e.g., blog comments)
3. Attacker notes the relative file path from the uploaded file's properties
4. Attacker navigates to page edit mode and adds a new layout block
5. Attacker modifies the bFilename parameter in the block design submit request using path traversal (e.g., ../../../../application/files/...) to point to the uploaded malicious PNG
6. When the page is reloaded or the layout is rendered, the PHP code in the PNG file is executed by the server

## Root cause
Insufficient input validation and sanitization of the bFilename parameter. The application fails to restrict file inclusion to legitimate design files and does not properly validate or canonicalize file paths, allowing traversal sequences to bypass directory restrictions. Additionally, the application includes user-supplied file paths in PHP include/require statements without proper access controls.

## Attacker mindset
An authenticated user with page editing permissions seeks to elevate privileges and execute arbitrary commands. The attacker exploits the trust placed in authenticated users by uploading a polyglot file that is valid as PNG but contains executable PHP. By manipulating the file path parameter through path traversal, the attacker bypasses intended upload directory restrictions and achieves code execution in the application context.

## Defensive takeaways
- Implement strict whitelist-based validation for file paths - only allow filenames without directory traversal sequences (../, .., etc.)
- Use basename() or similar functions to extract only the filename component, preventing directory traversal
- Maintain a mapping of allowed layout/design files and validate that bFilename matches approved resources
- Never directly include user-supplied file paths in include/require statements without prior validation
- Implement proper access controls - verify that the referenced file belongs to the user's allowed scope
- Use realpath() to resolve canonical paths and verify they remain within intended directories
- Disable PHP execution in upload directories via web server configuration (.htaccess or nginx config)
- Separate uploaded files from executable code directories with strict permission boundaries
- Implement file type validation beyond extension checking (verify MIME type and file signatures)
- Apply principle of least privilege - limit page editing rights to only necessary users
- Log and monitor all file inclusion operations for security auditing

## Variant hunting
Search for other endpoints accepting filename/filepath parameters in admin and user-facing interfaces
Audit all include(), require(), include_once(), require_once() calls for user-supplied input
Test other file upload functions and subsequent file retrieval/inclusion mechanisms
Examine template rendering engines for similar path traversal vulnerabilities
Review permission checks around file operations - may allow lower-privileged users to access files
Test for polyglot file bypass techniques with other image formats (JPEG, GIF, WebP)
Check for similar vulnerabilities in theme/template customization features
Investigate file manager functionality for path traversal in download/preview operations

## MITRE ATT&CK
- T1190
- T1083
- T1059.004
- T1021.004
- T1105
- T1040
- T1566.002

## Notes
Concrete5 8.5.4 confirmed affected. The vulnerability chain combines authenticated access requirement with path traversal and code inclusion. The polyglot PNG file technique is effective because PNG format validation occurs separately from PHP parsing. This is a design flaw where file inclusion logic trusts authenticated users without validating actual file paths. The report was collaborative research by multiple security researchers.

## Full report
<details><summary>Expand</summary>

** crayons **

## Description
The `bFilename` parameter in the scenario `index.php/ccm/system/dialogs/block/design/submit` is vulnerable to remote code execution via path traversal vulnerability. Authenticated attacker with rights to edit web application pages can upload malicious PNG file containing PHP code using any attachment upload functions (for example in comment section of the blog) and then use its relative path in `bFilename` parameter while editing layout design.  The file, supplied in vulnerable parameter will be included in PHP, leading to injected malicious code to run.

## Testing setup :
Concrete5 CMS version: 8.5.4
PHP Version: 7.2.24

## Steps to reproduce
1) Login to your Concrete5 account with rights to edit pages
2) Upload using any attachment upload function png file, containing php code at its end. You can use file ```png-transparent.png``` from the attachments . It is empty PNG file with the following payload at its end:

```
<?php system("uname -a");?>
```
You can get file path for example by viewing uploaded file properties:
{F1193239}
3) Navigate to page edit constructor
4) Select any element (for example Sidebar) and click "Add Layout" -> "Add Layout"
5) Click on newly added block and select "Edit layout Design" -> Save
6) Get the request from step 5 from any web proxy (for example Burp Suite) and resend it modifying `bFilename` with the system relative path to the uploaded file, for example:

```
bFilename=../../../../application/files/9316/1312/5391/png-transparent.png
```
7) Reload the page, your are editing, and see the payload fired

{F1193235}

## Credits
This bug was found as a part of Solar Security CMS Reseach, with https://hackerone.com/d0bby, https://hackerone.com/wezery0, https://hackerone.com/silvereniqma in collaboration. Can you, please, add them to this report?

## Impact

Authenticated attacker with page editing rights can run arbitrary system commands and obtain sensitive information

</details>

---
*Analysed by Claude on 2026-05-24*
