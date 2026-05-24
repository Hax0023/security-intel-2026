# Unescaped File Path in Image Library Shell Commands

## Metadata
- **Source:** HackerOne
- **Report:** 250273 | https://hackerone.com/reports/250273
- **Submitted:** 2017-07-16
- **Reporter:** freetom
- **Program:** ExpressionEngine
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Command Injection, OS Command Injection, Shell Metacharacter Injection
- **CVEs:** None
- **Category:** memory-binary

## Summary
The Image_lib.php library in ExpressionEngine uses PHP's exec() function to process images via ImageMagick and NetPBM without properly escaping file path arguments. An attacker who can control the filename of uploaded images can inject arbitrary shell commands for code execution.

## Attack scenario
1. Attacker identifies a file upload functionality that accepts image files
2. Attacker crafts a malicious filename containing shell metacharacters and commands (e.g., 'image.jpg; malicious_command #')
3. Attacker uploads the file with the malicious filename
4. Image processing is triggered (automatic or manual) calling image_process_imagemagick() or image_process_netpbm()
5. The unescaped filename is passed to exec(), causing the injected command to execute with application privileges
6. Attacker achieves arbitrary code execution on the server

## Root cause
File paths (full_src_path and full_dst_path) are concatenated directly into shell commands passed to exec() without using escapeshellarg() or equivalent escaping. This allows shell metacharacters in filenames to break out of the intended command structure.

## Attacker mindset
An attacker would recognize that user-controlled filenames become part of shell commands and attempt to break out of the intended command syntax using shell metacharacters, backticks, or command substitution syntax to execute arbitrary commands.

## Defensive takeaways
- Always use escapeshellarg() when passing user-controlled data to shell commands via exec(), system(), or passthru()
- Sanitize or restrict uploaded filenames to alphanumeric characters, hyphens, and underscores
- Use array-based command execution (proc_open with command array) instead of shell string concatenation when possible
- Validate file uploads thoroughly and maintain a whitelist of allowed characters
- Keep frameworks and libraries updated, as this was already fixed in CodeIgniter's upstream repository
- Run application with minimal required privileges to limit impact of command injection

## Variant hunting
Search for other instances of exec(), system(), passthru(), shell_exec(), or backtick operators processing file paths or user input. Check for similar patterns in image processing, document conversion, or media manipulation libraries.

## MITRE ATT&CK
- T1190
- T1059.004

## Notes
The vulnerability exists in ExpressionEngine's outdated copy of CodeIgniter's Image_lib.php. The upstream CodeIgniter repository had already implemented the fix using escapeshellarg(). This demonstrates the importance of maintaining current dependencies and monitoring upstream security patches. The vulnerability allows Remote Code Execution (RCE) if file uploads are available to authenticated or unauthenticated users.

## Full report
<details><summary>Expand</summary>

Under `./system/ee/legacy/libraries/Image_lib.php`

There are function from CodeIgniter to manipulate images. The issue is that the PHP function `exec` is used two times in two different functions: `image_process_imagemagick` and `image_process_netpbm`

In both cases the `full_src_path` and `full_dst_path` are given unescaped to the `exec` function. If an attacker can control the filename of the image to give he can inject pretty much arbitrary code. I suggest to use `escapeshellarg` on the path arguments at rows:
-590
-604
-608
-691

Furthermore, note that in CodeIgniter Github repo, the function `image_process_imagemagick` that already prevents this potential injection.
https://github.com/bcit-ci/CodeIgniter/blob/27647c9a8b5cd5a0e1fd78123316f359fe61a672/system/libraries/Image_lib.php#L892


</details>

---
*Analysed by Claude on 2026-05-24*
