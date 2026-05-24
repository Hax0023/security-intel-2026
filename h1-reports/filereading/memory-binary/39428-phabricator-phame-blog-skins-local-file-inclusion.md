# Phabricator Phame Blog Skins Local File Inclusion to RCE

## Metadata
- **Source:** HackerOne
- **Report:** 39428 | https://hackerone.com/reports/39428
- **Submitted:** 2014-12-15
- **Reporter:** nullsub
- **Program:** Phabricator
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Local File Inclusion (LFI), Path Traversal, Remote Code Execution (RCE), Arbitrary File Inclusion
- **CVEs:** None
- **Category:** memory-binary

## Summary
Phabricator's Phame blog feature allows unauthenticated users to set a custom skin parameter that is vulnerable to path traversal, enabling attackers to include arbitrary PHP files from outside the intended skins directory. An attacker with file upload capabilities can upload malicious PHP files and then include them via the skin parameter, achieving remote code execution with Phabricator's privileges.

## Attack scenario
1. Attacker gains ability to write files to the server (via another vulnerable application, SSH access, or temporary directory permissions)
2. Attacker uploads a crafted PHP file containing malicious code to a writable location (e.g., /tmp/test/header.php with phpinfo() or webshell payload)
3. Attacker navigates to /phame/blog/new/ and creates a new blog post
4. Attacker sets the skin parameter to a path traversal payload: ../../../../../../tmp/test
5. When Phabricator renders the blog, it loads the malicious PHP file from /tmp/test/header.php
6. Malicious PHP code executes with Phabricator's privileges, granting attacker access to sensitive data or full server control

## Root cause
The Phame blog skin parameter is not properly validated or sanitized before being used in file inclusion operations. The application constructs file paths by directly concatenating user input without checking if the resulting path stays within the intended skins directory. Path traversal sequences (../) are not filtered or blocked.

## Attacker mindset
An attacker would recognize that custom skin parameters are often trusted application logic. By combining path traversal with file upload capabilities (which may exist elsewhere on the server or in related services), they can achieve code execution on the backend. This is a classic privilege escalation technique: use a minor file upload vulnerability elsewhere to compromise a critical application.

## Defensive takeaways
- Implement strict input validation on all user-supplied paths, especially those used in file inclusion operations
- Use canonical path resolution (realpath() in PHP) and verify the resolved path is within the allowed directory
- Maintain a whitelist of allowed skins rather than allowing arbitrary path specification
- Sanitize and reject path traversal sequences (../, .., etc.) in user input
- Apply principle of least privilege: ensure Phabricator runs with minimal required permissions
- Implement security controls to prevent arbitrary file uploads to system directories
- Use static file inclusion where possible; avoid dynamic includes based on user input
- Employ chroot jails or containerization to limit file system access
- Regular security audits of file handling code, particularly in plugin/extension systems

## Variant hunting
Check other template/theme/plugin/skin features in Phabricator and similar applications for similar path traversal issues
Look for other parameters that accept file paths or names (custom_domain, logo paths, CSS/JS includes)
Search for similar LFI in other PHP applications with theming systems (WordPress, Drupal, etc.)
Investigate if there are restrictions on which authenticated users can create blogs or modify skins
Test whether the vulnerability can be exploited without file upload capabilities using null byte injection or log poisoning
Check if symbolic links can be used to bypass path validation checks
Look for second-order LFI where skin paths are stored in database and later processed unsafely

## MITRE ATT&CK
- T1190
- T1083
- T1059
- T1105
- T1203

## Notes
This is a high-impact vulnerability because it bridges two separate issues: file upload/write access (which might be low-severity elsewhere) and unsafe file inclusion (which becomes critical when combined). The vulnerability requires an attacker to have file write access in some form, but this is realistic in shared hosting, containers with other vulnerable apps, or systems where temporary directories are accessible. The fix is straightforward: validate that resolved paths remain within the skins directory using realpath() comparison or explicit whitelist validation. This vulnerability pattern appears in many PHP-based CMS platforms and demonstrates why all user input affecting file operations must be treated as hostile.

## Full report
<details><summary>Expand</summary>

Phabricator's Phame blog allows users to set a skin.

An attacker with the ability to upload files to the server can exploit this LFI vulnerability to gain remote code execution through Phabricator and thus, gain access to Phabricator's data. Common scenarios may include:

- A box serving Phabricator and other web application that would allow uploading files to controlled paths.
- A box where the attacker can log in through ssh as a restricted user (not having access to Phabricator's files, but having access to write in /tmp, for instance)
- etc ...

While testing, I used the following request to create a blog:

```
POST /phame/blog/new/ HTTP/1.1
Host: phabricator
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:33.0) Gecko/20100101 Firefox/33.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: http://phabricator.48bits.com/phame/blog/new/
Cookie: phsid=o36kfovszv6sqpbjheacicu2ykx25lqoh5iepeit; phusr=guest
Connection: keep-alive
Content-Type: application/x-www-form-urlencoded
Content-Length: 254

__csrf__=B%40acbxwmgk39152b45fd9eff2e&__form__=1&name=xxxx&description=bla&can_view=users&can_edit=users&can_join=users&custom_domain=&skin=%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%2e%2e%2f%74%6d%70%2f%74%65%73%74
```

That makes phabricator try to load the skin template php files from:

/var/www/phabricator/phabricator/externals/skins/../../../../../../../../../../tmp/test/

In order to exploit the vulnerability a valid skin structure must exist at the specified location, I have simply copied the oblivious skin and modified it to output a phpinfo() within the header.php script with the expected results.

Proposed fix:

Phabricator should verify that the skin's path is not outside its own root.



</details>

---
*Analysed by Claude on 2026-05-24*
