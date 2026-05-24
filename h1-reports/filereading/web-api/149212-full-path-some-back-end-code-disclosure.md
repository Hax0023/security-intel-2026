# Full Path Disclosure and Backend Code Exposure via Path Traversal in Avatar Upload

## Metadata
- **Source:** HackerOne
- **Report:** 149212 | https://hackerone.com/reports/149212
- **Submitted:** 2016-07-04
- **Reporter:** strukt
- **Program:** ExpressionEngine (inferred from URL pattern /ee/admin.php)
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Path Traversal, Information Disclosure, Error-Based Information Leakage
- **CVEs:** None
- **Category:** web-api

## Summary
An admin profile settings endpoint fails to properly validate the avatar_filename parameter, allowing path traversal attempts that trigger verbose exception handling. When malicious path traversal payloads are submitted, the application discards sensitive information including full server paths and backend code snippets in error responses.

## Attack scenario
1. Attacker authenticates as an admin or identifies the admin profile endpoint
2. Attacker crafts a POST request to /ee/admin.php?/cp/members/profile/settings with multipart form data
3. Attacker modifies the avatar_filename parameter from a benign value (e.g., 'ee_paint.jpg') to a path traversal payload (e.g., '../../../../../../etc/passwd')
4. The backend processes the request without proper input sanitization and attempts file operations
5. An exception is raised during file processing due to the invalid path
6. Exception handler returns detailed error message to client, revealing full server path, file system structure, and backend code implementation details

## Root cause
Insufficient input validation on the avatar_filename parameter combined with verbose error handling that exposes system details in exception messages. The application does not sanitize or validate the filename against path traversal sequences before attempting file operations, and error responses are not sanitized before being sent to clients.

## Attacker mindset
An attacker seeking reconnaissance through information disclosure would recognize that file upload parameters often lack proper validation. By attempting directory traversal sequences, they can trigger errors that leak sensitive architectural and implementation details useful for planning further attacks. The combination of admin-level access requirement with the disclosure itself creates a pathway for privilege escalation or lateral movement insights.

## Defensive takeaways
- Implement strict whitelist validation for file-related parameters, rejecting any input containing path traversal sequences (../, ..\ etc.)
- Use basename() or equivalent functions to extract only the filename component, discarding any directory path information
- Implement generic error messages shown to users; log detailed exceptions server-side only
- Apply input validation at multiple layers: parameter validation, filename validation, and file operation validation
- Use a dedicated secure file handling library rather than manual path concatenation
- Implement file upload directories outside the webroot or with restricted execution permissions
- Conduct security testing of file upload/avatar functionality with path traversal payloads during development

## Variant hunting
Test other file upload parameters (profile_picture, attachment, document, etc.) with similar traversal payloads
Check for similar vulnerabilities in user-facing avatar/profile picture upload functionality (non-admin endpoints)
Examine other multipart form endpoints for insufficient parameter validation
Test null byte injection in avatar_filename (avatar.php%00.jpg) for bypass attempts
Attempt unicode or double encoding variations of traversal sequences
Check if the vulnerability extends to arbitrary file read or write operations beyond avatar handling
Test with different path traversal depths and encoding schemes (URL encode, HTML encode, etc.)

## MITRE ATT&CK
- T1190
- T1083
- T1526
- T1592

## Notes
Reporter explicitly notes they hadn't verified if this issue affects normal (non-admin) users at time of report submission. The vulnerability chain involves both path traversal capability and information disclosure; the path traversal alone may not achieve immediate compromise, but the information disclosure enables further attack planning. The error-based information leakage is the primary security concern since it exposes implementation details that could facilitate other attacks. This is classified as a tier-2 vulnerability - significant for reconnaissance and information gathering but requiring authenticated admin access.

## Full report
<details><summary>Expand</summary>

Hello,

Ironically enough, I just discovered a full path disclosure issue. When an admin edits their personal information, a request like the following gets sent:

```
POST /ee/admin.php?/cp/members/profile/settings&id=1 HTTP/1.1
Host: localhost
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:45.0) Gecko/20100101 Firefox/45.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: close
Content-Type: multipart/form-data; boundary=---------------------------14340353543714380361467519033
Content-Length: 1708

-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="csrf_token"

{TOKEN}
-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="url"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="location"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="bday_d"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="bday_m"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="bday_y"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="bio"


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="language"

english
-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="preferences[]"

display_avatars
-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="avatar_filename"

ee_paint.jpg
-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="upload_avatar"; filename=""
Content-Type: application/octet-stream


-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="avatar_picker"

choose
-----------------------------14340353543714380361467519033
Content-Disposition: form-data; name="link_avatar"

http://
-----------------------------14340353543714380361467519033--
```

The problem originates from the fact that, when the user attempts to change the value of the parameter "avatar_filename" to something like `../../../../../../etc/passwd`, as an attempt to include such file, an exception gets thrown, disclosing the full path and some code from the back end.

Note: I didn't check if this is the case for normal uses or not, yet, working on it.

Regards

</details>

---
*Analysed by Claude on 2026-05-24*
