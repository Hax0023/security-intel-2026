# Authenticated Path Traversal to RCE in Concrete5 CMS

## Metadata
- **Source:** HackerOne
- **Report:** 1102067 | https://hackerone.com/reports/1102067
- **Submitted:** 2021-02-12
- **Reporter:** d3addog
- **Program:** Concrete5 CMS
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Path Traversal, Local File Inclusion (LFI), Remote Code Execution (RCE), Arbitrary File Upload
- **CVEs:** CVE-2021-40097
- **Category:** memory-binary

## Summary
The bFilename parameter in Concrete5's block design submission endpoint is vulnerable to path traversal, allowing authenticated users with page editing rights to include arbitrary files. An attacker can upload a PNG file with embedded PHP code and use path traversal to include it, resulting in arbitrary code execution.

## Attack scenario
1. Attacker authenticates to Concrete5 CMS with page editing privileges
2. Attacker uploads a malicious PNG file containing PHP code via any attachment upload function (e.g., blog comments)
3. Attacker notes the relative file path from the uploaded file properties
4. Attacker navigates to page edit mode and opens the block layout design editor
5. Attacker intercepts the layout design submission request and modifies the bFilename parameter with path traversal payload (e.g., ../../../../application/files/9316/1312/5391/png-transparent.png)
6. The application includes and executes the malicious file as PHP, running arbitrary system commands

## Root cause
Insufficient input validation and sanitization of the bFilename parameter before passing it to a PHP include/require statement. The application fails to restrict file inclusion to intended directories or validate that the resolved path is within allowed boundaries.

## Attacker mindset
An authenticated attacker with page editing permissions seeks to escalate privileges by achieving code execution. By combining file upload capabilities with path traversal, they bypass file type restrictions by uploading a valid PNG file containing PHP code, then exploiting the unvalidated bFilename parameter to include and execute it.

## Defensive takeaways
- Implement strict path validation using realpath() and verify the resolved path is within a whitelist of allowed directories
- Never trust user input for file paths; use indirect reference mapping or file IDs instead
- Apply input validation to reject path traversal sequences like ../, ..\ and null bytes
- Disable PHP execution in upload directories via web server configuration (e.g., Apache .htaccess or nginx configuration)
- Use allow-lists for file extensions rather than block-lists when accepting uploads
- Separate uploaded files from web-accessible directories or serve them through a file delivery script without execution
- Implement proper access controls; validate user permissions before allowing file inclusion operations
- Use security headers like Content-Security-Policy to restrict script execution sources

## Variant hunting
Search for other file inclusion parameters in page/layout editing features. Examine all dialog submission endpoints (index.php/ccm/system/dialogs/*/submit) for similar bFilename or path-related parameters. Investigate other CMS features that allow file selection or inclusion (themes, add-ons, templates). Test upload functionality in different contexts (user avatars, document libraries) combined with inclusion points.

## MITRE ATT&CK
- T1190
- T1083
- T1105
- T1059
- T1020

## Notes
The vulnerability requires authentication and specific permissions (page editing rights), reducing immediate risk but still significant for insider threats or compromised accounts. The use of PNG file format to bypass upload filters while containing executable PHP code is a noteworthy evasion technique. Report credits Solar Security CMS Research team collaboration.

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
*Analysed by Claude on 2026-05-12*
