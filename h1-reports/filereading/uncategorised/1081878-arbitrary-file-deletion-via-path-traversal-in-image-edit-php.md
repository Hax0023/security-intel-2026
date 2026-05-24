# Arbitrary File Deletion via Path Traversal in image-edit.php

## Metadata
- **Source:** HackerOne
- **Report:** 1081878 | https://hackerone.com/reports/1081878
- **Submitted:** 2021-01-19
- **Reporter:** egix
- **Program:** ImpressCMS
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Path Traversal, Arbitrary File Deletion, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The image-edit.php script fails to sanitize the 'image_temp' parameter before using it in unlink() function calls, allowing authenticated attackers to delete arbitrary files via path traversal sequences. This vulnerability can lead to denial of service by deleting critical application files like mainfile.php.

## Attack scenario
1. Attacker authenticates to ImpressCMS with any valid user account (Webmaster or Registered User)
2. Attacker crafts a malicious URL with path traversal payload: image-edit.php?op=save&image_id=1&image_temp=../../../mainfile.php
3. The application copies the file from temp directory using the unsanitized parameter
4. Before deletion, unlink() is called on the traversal path, resolving to the actual target file location
5. Critical application files are deleted, rendering the website unusable or exposing sensitive functionality
6. Optional: Attacker deletes index.html to enable directory listing and disclose file contents

## Root cause
Insufficient input validation and sanitization of user-supplied 'image_temp' parameter. The parameter is concatenated directly into file paths without removing or validating path traversal sequences (../, ..\ etc.). The unlink() function operates on the unsanitized path.

## Attacker mindset
An authenticated attacker with basic application knowledge can exploit this to cause denial of service by removing critical files. The low barrier to entry (any authenticated user) and severe impact (application destruction) makes this an attractive attack vector for disgruntled insiders or compromised accounts.

## Defensive takeaways
- Implement strict whitelist validation on user-supplied filenames - reject any input containing path traversal sequences (.., /, \)
- Use basename() function to strip directory components from filenames before file operations
- Implement proper access controls - restrict file deletion operations to admin/privileged users only
- Store temporary files outside web root or in a restricted directory with limited permissions
- Use security-focused path functions like realpath() to canonicalize paths and verify they resolve within expected directories
- Implement file operation logging and alerting for unauthorized deletions
- Apply principle of least privilege - run web server process with minimal required permissions

## Variant hunting
Search for other file operations (unlink, rmdir, fopen, file_get_contents) using unsanitized user input parameters
Check image management functionality in other PHP applications for similar path traversal in temp file handling
Investigate other parameters in image-edit.php (image_id, op) for injection vulnerabilities
Test upload/download functionality for similar path traversal in file retrieval operations
Look for similar patterns in backup, cache, or log file cleanup routines

## MITRE ATT&CK
- T1190
- T1526
- T1565

## Notes
The vulnerability requires authentication but accepts any authenticated user, significantly lowering the attack barrier. The use of @unlink() with error suppression masks the actual impact. The copy operation before deletion provides a timing window for exploitation. The ability to delete index.html enables secondary attacks (directory listing disclosure).

## Full report
<details><summary>Expand</summary>

## Summary:
The vulnerability is located in the `/libraries/image-editor/image-edit.php` script:

```
161.		if (@copy ( ICMS_IMANAGER_FOLDER_PATH . '/temp/' . $simage_temp, $categ_path . $simage->getVar ( 'image_name' ) )) {
162.			if (@unlink ( ICMS_IMANAGER_FOLDER_PATH . '/temp/' . $simage_temp )) {
163.				$msg = _MD_AM_DBUPDATED;

[...]

190.		} else {
191.			if (copy ( ICMS_IMANAGER_FOLDER_PATH . '/temp/' . $simage_temp, $categ_path . $imgname )) {
192.				@unlink ( ICMS_IMANAGER_FOLDER_PATH . '/temp/' . $simage_temp );
193.			}
```

User input passed through the "image_temp" parameter is not properly sanitized before being used in a call to the `unlink()` function at lines 162 and 192. This can be exploited to carry out Path Traversal attacks and delete arbitrary files in the context of the web server process.

**NOTE**: before being deleted, the file will be copied into the `/uploads/imagemanager/logos/` directory. As such, by firstly deleting the `index.html` file in that directory, it might be possible to disclose the content of arbitrary files in case the web server allows for directory listing.

## ImpressCMS branch :
The vulnerability has been tested and confirmed on ImpressCMS version 1.4.2 (the latest at the time of writing).

## Steps To Reproduce:
  1. Login into the application as any user (this should work both for Webmasters and Registered Users) 
  1. Go to: `http://[impresscms]/libraries/image-editor/image-edit.php?op=save&image_id=1&image_temp=../../../mainfile.php`
  1. The `mainfile.php` script will be deleted, rendering the website unusable

## Impact

This vulnerability might allow authenticated attackers to delete arbitrary files, potentially leading to a Denial of Service (DoS) condition or destruction of users data.

</details>

---
*Analysed by Claude on 2026-05-24*
