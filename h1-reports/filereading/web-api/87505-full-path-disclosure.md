# Full Path Disclosure via File Upload Error Message

## Metadata
- **Source:** HackerOne
- **Report:** 87505 | https://hackerone.com/reports/87505
- **Submitted:** 2015-09-04
- **Reporter:** ishahriyar
- **Program:** ownCloud
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Information Disclosure, Path Traversal, Error-Based Information Leakage
- **CVEs:** CVE-2016-1501
- **Category:** web-api

## Summary
A non-admin user uploading an HTML file as a profile picture triggers an error message that exposes the full server file path including internal directory structure. This information disclosure reveals sensitive system paths that could aid in further attacks against the ownCloud installation.

## Attack scenario
1. Attacker creates ownCloud account as non-admin user
2. Attacker attempts to upload an HTML file to the profile picture field
3. Server rejects upload and returns error message
4. Error message contains full path: /opt/lampp/htdocs/owncloud/data/12/files/opt/lampp/htdocs/owncloud/data/12/cache/avatar_upload
5. Attacker maps internal file structure and directory locations
6. Attacker uses this information to identify other potential attack vectors or vulnerable paths

## Root cause
Improper error handling in the file upload/avatar processing functionality. The application directly includes filesystem paths in error messages shown to users instead of sanitizing or using generic error responses. Additionally, the path itself appears malformed with duplication (data/12 appears twice), suggesting a path concatenation bug.

## Attacker mindset
An information gatherer looking for reconnaissance opportunities. The attacker probes file upload functionality with unexpected file types to trigger error messages. This passive reconnaissance technique helps map the target's internal infrastructure without requiring authentication level escalation.

## Defensive takeaways
- Implement generic error messages for users - log detailed errors server-side only
- Never expose filesystem paths in client-facing error messages
- Sanitize and validate all error output before returning to users
- Implement proper input validation to reject HTML files before processing
- Use try-catch blocks with generic user messages while logging detailed errors internally
- Implement path normalization to prevent duplicate path components in cache/upload handlers
- Add file type validation on both client and server side before attempting file operations

## Variant hunting
Search for similar path disclosure in: other file upload endpoints (document storage, gallery uploads), backup/export functions, log download features, temporary file handlers, API endpoints that process file operations, admin file management tools

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1592 Gather Victim Host Information

## Notes
The malformed path (data/12 appearing twice) suggests a path traversal or directory traversal bug in the upload handler. The cache path appears incorrectly nested within the files path. This may indicate a more serious vulnerability than simple information disclosure worth investigating further. The issue affects non-admin users, making it exploitable by low-privileged accounts.

## Full report
<details><summary>Expand</summary>

When I was trying to upload a html file as profile picture as a non admin user. then it popped up with a message containing full path . Like that
"Could not obtain lock type 1 on "/opt/lampp/htdocs/owncloud/data/12/files/opt/lampp/htdocs/owncloud/data/12/cache/avatar_upload"."

Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
