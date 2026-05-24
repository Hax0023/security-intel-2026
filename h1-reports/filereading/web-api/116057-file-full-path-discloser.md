# Directory Traversal via Unfiltered User Input in php-encryption Autoloader

## Metadata
- **Source:** HackerOne
- **Report:** 116057 | https://hackerone.com/reports/116057
- **Submitted:** 2016-02-12
- **Reporter:** acc_122
- **Program:** Paragon IE (php-encryption)
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Directory Traversal, Path Traversal, Arbitrary File Disclosure
- **CVEs:** None
- **Category:** web-api

## Summary
The php-encryption library's autoload.php file fails to sanitize user-controlled input used for directory browsing, allowing attackers to traverse the file system and disclose arbitrary files. An attacker can exploit this vulnerability by manipulating input parameters to navigate parent directories and access sensitive files outside the intended scope.

## Attack scenario
1. Attacker identifies the autoload.php endpoint or inclusion point accepting user input for file sourcing
2. Attacker crafts malicious input containing path traversal sequences (e.g., '../../../etc/passwd')
3. The unsanitized input is passed directly to file operations without validation or filtering
4. The application processes the traversal sequence and fetches the requested file from an unintended directory
5. The file contents are returned to the attacker, disclosing sensitive information
6. Attacker can escalate this to remote code execution by accessing and modifying executable files or configuration files

## Root cause
Insufficient input validation and lack of path canonicalization in autoload.php. User-controlled input used for file inclusion/sourcing is not validated against directory traversal patterns or restricted to a whitelist of allowed paths.

## Attacker mindset
Reconnaissance and information gathering focused on discovering sensitive files, configuration details, and source code. Secondary goal is escalation to RCE by leveraging file disclosure to modify or include malicious code.

## Defensive takeaways
- Implement strict input validation on all user-supplied input used in file operations
- Use whitelist-based path validation rather than blacklist pattern matching
- Canonicalize file paths and ensure they resolve within expected directories using realpath()
- Avoid using user input directly in include/require statements; use indirect mapping (array-based lookup)
- Implement proper access controls and least privilege for file system operations
- Use security headers and disable directory listing where applicable
- Regular security code review of autoloading mechanisms and dynamic file inclusion

## Variant hunting
Check other PHP applications for similar vulnerabilities in custom autoloaders
Search for unvalidated input in __autoload() and spl_autoload_register() handlers
Investigate dynamic module loading in other languages (Python __import__, Node.js require)
Review any file inclusion mechanisms accepting user-controlled path components
Audit symlink following behavior in autoloaders that may enable additional traversal attacks

## MITRE ATT&CK
- T1190
- T1083
- T1005

## Notes
The report quality is poor with minimal technical detail and broken English. However, the core vulnerability concept is valid. The actual impact depends on the specific implementation context - whether autoload.php is exposed to user input directly or through a wrapper. Path traversal in autoloaders is particularly dangerous as it can lead to arbitrary code execution in a PHP context.

## Full report
<details><summary>Expand</summary>

Hi,
Paragonie security team i found one directory browsing vulnerability in php-encryption-master where the user input will not been filtered from any security layer.
let me show you.
there is a autoload.php page in the php-encryption-master. where the input src will b used to browse the directory so this input will not been tested and fetch the file from directory and return to user.
this attack will highly affect your product and may invite for other attack to.

so i hope you will protch it as soon as possible.

thank you,
security researcher,
lucky sen

</details>

---
*Analysed by Claude on 2026-05-24*
