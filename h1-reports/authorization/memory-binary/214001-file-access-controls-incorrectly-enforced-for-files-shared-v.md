# QuickLink File Access Control Bypass - Prefix-Based Path Traversal

## Metadata
- **Source:** HackerOne
- **Report:** 214001 | https://hackerone.com/reports/214001
- **Submitted:** 2017-03-16
- **Reporter:** eboda
- **Program:** BrickFTP
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Insufficient Access Control, Path Traversal, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
BrickFTP's QuickLink file sharing feature fails to properly validate file paths, allowing attackers to download any file whose name starts with the shared file's name. An attacker sharing file 'foo' can access 'footer.php' and files within 'foobar/' directory by manipulating the path parameter in download requests.

## Attack scenario
1. Attacker creates or has access to a file named 'foo' and generates a QuickLink share URL
2. Attacker obtains a valid QuickLink bundle code and session token through normal sharing process
3. Attacker modifies the 'path' parameter in the download URL from 'foo' to 'footer.php' (same prefix)
4. Server incorrectly validates the path using string prefix matching instead of exact path matching
5. Attacker successfully downloads 'footer.php' and other unintended files like 'foobar/secret'
6. Attacker can exfiltrate sensitive files shared in the same directory hierarchy without explicit permission

## Root cause
The path validation logic uses prefix matching (e.g., 'starts with foo') instead of exact path matching or proper file access control lists. The server likely checks if the requested path starts with the shared file's name rather than verifying it exactly matches or is within the intended bundle contents.

## Attacker mindset
An attacker with legitimate access to generate a QuickLink for one file can probe the filesystem by manipulating path parameters, discovering and accessing unintended files. This is a low-effort, high-impact attack requiring only URL parameter modification.

## Defensive takeaways
- Use exact path matching instead of prefix/substring matching for file access validation
- Maintain an explicit whitelist of permitted files/paths within each bundle rather than deriving access from request parameters
- Validate all path components are sanitized and do not attempt directory traversal (../, absolute paths)
- Implement server-side bundle definitions that cannot be modified by client-side parameters
- Use strong cryptographic checks for path parameters beyond simple string comparison
- Add logging and alerting for unusual file access patterns (accessing files with similar names outside intended bundle)

## Variant hunting
Check if QuickLink works with file extensions - can 'foo' access 'foo.php', 'foo.txt'?
Test directory traversal: does path manipulation allow '../' or absolute path injection?
Verify if symbolic links or case sensitivity can be exploited for bypass
Check other file sharing features (not just QuickLink) for similar prefix-matching vulnerabilities
Test whether accessing files outside the original directory is possible through path manipulation
Examine if the 'x' session token validation is properly tied to the specific file path or only the bundle code

## MITRE ATT&CK
- T1190
- T1566
- T1005
- T1052

## Notes
This is a logic flaw in authorization rather than a traditional path traversal vulnerability. The attacker doesn't need to break out of a directory - they simply need files with overlapping names. The report demonstrates good security research methodology by providing reproducible steps and a live test environment. The session-specific 'x' parameter likely serves as a CSRF token but does not address the core path validation issue.

## Full report
<details><summary>Expand</summary>

Enter the support PIN from your test site (if applicable): **305056**
Enter the name of your test site (if applicable): **pwn.brickftp.com**
Enter the subdomain from your test site (if applicable): **pwn.brickftp.com**

## Summary

This is a bug in the file sharing feature QuickLink. The file access control is flawed which allows an attacker to download not just the shared file, but any file that has the same name prefix as the shared file.

## Steps to reproduce
I have created the following files and folders:

```
bar
foo
foobar/secret
footer.php  
```

Let's say I want to share `foo` with some friends, so I use the *Copy Public QuickLink* action and it will create a bundle (see https://pwn.brickftp.com/f/23a17148e ) with just that file: {F169390}.

Now when I try to download `foo` a GET request is sent to https://pwn.brickftp.com/bundles/download?code=23a17148e&path=foo&x=767de6540 . 

Notice that the `path` variable contains foo, if we change it to `bar`, it will tell us: *Invalid path for bundle*.

However, any other path starting with `foo` can be downloaded. For example https://pwn.brickftp.com/bundles/download?code=23a17148e&path=footer.php&x=767de6540

This would also allow to download any file in `foobar/`: https://pwn.brickftp.com/bundles/download?code=23a17148e&path=foo&x=767de6540

### Final Remark
Please note that the above links will most likely not work for if you click on them because the `x` parameter is session specific. But you can still download my files if you go to the QuickLink: https://pwn.brickftp.com/f/23a17148e and then simply replace the `path` variable yourself like I did above.

---
If something is unclear or you have any questions please let me know.

</details>

---
*Analysed by Claude on 2026-05-24*
