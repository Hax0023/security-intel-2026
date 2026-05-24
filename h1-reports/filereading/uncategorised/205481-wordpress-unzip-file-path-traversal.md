# WordPress unzip_file Path Traversal Vulnerability

## Metadata
- **Source:** HackerOne
- **Report:** 205481 | https://hackerone.com/reports/205481
- **Submitted:** 2017-02-11
- **Reporter:** ajxchapman
- **Program:** WordPress
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Path Traversal, Arbitrary File Write, Remote Code Execution
- **CVEs:** None
- **Category:** uncategorised

## Summary
The WordPress unzip_file function is vulnerable to path traversal attacks when extracting zip files, allowing attackers to write arbitrary files outside the intended extraction directory. By crafting malicious zip entries with directory traversal sequences (../) in filenames, an attacker can place files anywhere the web server has write permissions, enabling remote code execution through PHP file placement.

## Attack scenario
1. Attacker identifies a WordPress installation or plugin that uses unzip_file with untrusted zip files
2. Attacker crafts a malicious zip file containing PHP webshell with filename like '../../../../../../var/www/html/shell.php'
3. Attacker uploads the zip file through vulnerable plugin functionality (e.g., plugin upload or gallery import)
4. WordPress unzip_file function extracts entries without validating normalized paths remain within target directory
5. Malicious PHP file is written to web root, bypassing the intended extraction directory constraint
6. Attacker accesses the PHP webshell and achieves remote code execution on the server

## Root cause
The _unzip_file_ziparchive and _unzip_file_pclzip functions do not normalize extracted file paths or validate that normalized paths remain within the specified $to target directory before extraction. Both extraction methods fail to sanitize or check directory traversal sequences in zip entry filenames.

## Attacker mindset
An attacker would target WordPress galleries, media management plugins, or any plugin allowing file uploads with automatic extraction. The path traversal technique is straightforward to exploit by crafting malicious zip files. RCE potential makes this highly valuable for compromising WordPress installations, particularly those allowing non-admin users to upload files.

## Defensive takeaways
- Always normalize file paths after extraction and validate they remain within intended target directories
- Implement whitelist-based path validation: ensure realpath(extracted_path).startswith(realpath(target_dir))
- Sanitize zip entry filenames to remove or reject directory traversal sequences (../, .., etc.)
- Use built-in PHP ZipArchive when possible, as it is not vulnerable to this specific attack
- Apply principle of least privilege: restrict write permissions for web server process
- Validate file types after extraction to prevent execution of unexpected file types
- Audit all plugins and custom code using unzip_file or similar extraction functions
- Implement security updates promptly when vendor patches are released

## Variant hunting
Search for vulnerable patterns: any use of unzip_file, ZipArchive->extractTo, or PclZip extraction without path normalization validation. Check plugins allowing file uploads with automatic zip extraction (gallery plugins, backup plugins, theme installers). Look for similar vulnerabilities in custom file extraction implementations across WordPress plugins and themes.

## MITRE ATT&CK
- T1190
- T1195
- T1567
- T1106

## Notes
This vulnerability affects both ZipArchive and PclZip extraction methods in WordPress. The report notes that native PHP ZipArchive extractTo is not vulnerable, suggesting the issue is specific to WordPress wrapper implementation. The vulnerability is particularly dangerous in multi-user WordPress installations and those with gallery plugins. Exploitation requires either admin access or vulnerable plugin functionality accepting untrusted uploads.

## Full report
<details><summary>Expand</summary>

# Summary
The Wordpress unzip_file function (https://codex.wordpress.org/Function_Reference/unzip_file) is vulnerable to path traversal when extracting zip files. Extracting untrusted zip files using this function this could lead to code execution through placing arbitrary PHP files in the DocumentRoot of the webserver.

# Analysis
The unzip_file function takes a target directory, `$to`, as an argument into which the files in the zip should be extracted. If a maliciously crafted zip file is extracted with a filename starting with the parent directory specifier (`../`) the file will be extracted into the parent of the '$to' argument target directory. Filenames can be crafted in order to place files in any directory which the webserver has write permissions, for example a zip entry with a filename of `../../../../../../../../../../tmp/poc_file` would place the file contents in the '/tmp/poc_file' directory.

This vulnerability exists both when unzip_file uses PHP's built-in ZipArchive (/wp-admin/includes/file.php:`_unzip_file_ziparchive`) and the 3rd party PclZip (/wp-admin/includes/file.php:`_unzip_file_pclzip`) extraction methods. Neither of these functions check to confirm that the normalised output path is within the `$to` target directory.

An example zip, 'zip_poc.zip' is attached. If this is extracted with the unzip_file function, for example through the "Upload Plugin" admin function or the attached 'poc.php', a file called 'poc_output' will be extracted to the operating system '/tmp' directory. The 'poc.php' attachment shows how the unzip_file function may be used in a wordpress plugin. This Proof of Concept has been tested on Wordpress 4.7.2 running on Ubuntu 14.04 LTS.

It should be noted that the built-in PHP ZipArchive extractTo method is not vulnerable to this path traversal.

Cursory analysis of a number of popular Wordpress plugins suggests that gallery plugins, such as NextGen Gallery, which allow lower privilege non-admin users to upload zips to be extracted would be particularly susceptible to this issue.

# Suggested Remediation
The `_unzip_file_ziparchive` and `_unzip_file_pclzip` functions should normalise the output paths of zip file entries ensuring that after normalisation the paths reside within the `$to` argument target directory.

</details>

---
*Analysed by Claude on 2026-05-24*
