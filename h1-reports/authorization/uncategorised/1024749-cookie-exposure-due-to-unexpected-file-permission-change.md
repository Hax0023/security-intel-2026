# Cookie Jar File Permission Exposure in libcurl

## Metadata
- **Source:** HackerOne
- **Report:** 1024749 | https://hackerone.com/reports/1024749
- **Submitted:** 2020-11-02
- **Reporter:** nyymi
- **Program:** curl/libcurl
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Insecure File Permissions, Information Disclosure, Unintended Permission Change
- **CVEs:** None
- **Category:** uncategorised

## Summary
libcurl versions 7.72.0 and later unexpectedly modify file permissions on existing CURLOPT_COOKIEJAR files, making them world and group-readable regardless of their original restrictive permissions. This exposes sensitive cookies to unauthorized local users who could previously not access them.

## Attack scenario
1. An application creates a secure cookie jar file with restrictive permissions (0600)
2. The application upgrades libcurl to version 7.72.0 or later
3. The application uses curl to fetch content with cookie handling enabled
4. libcurl modifies the existing cookie jar file permissions to 0644 (world-readable)
5. An unprivileged local attacker on the system reads the newly-exposed cookie jar file
6. The attacker extracts authentication tokens and session cookies to hijack the application's sessions

## Root cause
A change introduced in commit b834890a3fa3f525cd8ef4e99554cdb4558d7e1b altered the file creation/writing logic for cookie jar files. The new code creates files with default umask permissions (typically 0644) without preserving the original file's existing permissions when the file already exists.

## Attacker mindset
A local attacker with non-root access seeks to steal session credentials from other users' applications. By exploiting the automatic permission change behavior, they can read previously inaccessible cookie files containing authentication tokens for web services, banking, or cloud platforms.

## Defensive takeaways
- Never silently change permissions on existing files; preserve original ownership and permissions for backward compatibility
- When writing to existing files, explicitly document and preserve their security attributes
- Implement permission-aware file handling that respects pre-existing file security contexts
- Add security warnings or errors if file permissions are more permissive than expected
- Use restrictive default permissions (0600) when creating new credential/sensitive data files
- Audit all file I/O operations for unintended permission modifications in security-sensitive code
- Test permission handling across file creation, updates, and overwrites in security test suites

## Variant hunting
Search for similar permission-modification bugs in other tools that handle credentials or sensitive data files (.ssh, .gnupg, .aws, password managers). Look for file write operations that don't explicitly preserve existing file permissions using fchmod/chmod or equivalent. Check for issues where umask changes affect existing file security contexts.

## MITRE ATT&CK
- T1552.001
- T1555
- T1187

## Notes
This is a regression bug (introduced by a prior fix) rather than a new vulnerability. The impact is significant in multi-user systems where local privilege escalation or lateral movement could be achieved through cookie theft. The bug affects any application using libcurl's cookie jar functionality with pre-existing restrictive permissions.

## Full report
<details><summary>Expand</summary>

## Summary:
libcurl since 7.72.0 changes file specified in CURLOPT_COOKIEJAR to group and world readable, regardless of prior file permissions of an already existing file (assuming typical default umask of 022). This is unexpected as typically file permissions of an already existing file  are not changed. Indeed, libcurl prior to this version keeps the original file permissions, as expected. 

## Steps To Reproduce:
1. install -m 600 /dev/null cookie.jar
2. ls -l cookie.jar
3. curl -s -c cookie.jar https://www.google.com -o /dev/null
4. ls -l cookie.jar

## Supporting Material/References:
* This bug was introduced as a side effect of https://github.com/curl/curl/commit/b834890a3fa3f525cd8ef4e99554cdb4558d7e1b

## Impact

Leak of confidential information stored in the CURLOPT_COOKIEJAR (libcurl) or -c / --cookie-jar (curl command line tool) file.

</details>

---
*Analysed by Claude on 2026-05-24*
