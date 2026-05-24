# Authentication Bypass and Privilege Escalation via URL Manipulation in Cloudup File Access

## Metadata
- **Source:** HackerOne
- **Report:** 13959 | https://hackerone.com/reports/13959
- **Submitted:** 2014-05-29
- **Reporter:** niks
- **Program:** Cloudup
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Authentication Bypass, Privilege Escalation, Information Disclosure, Insufficient Access Control
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Cloudup's file access control mechanism can be bypassed by removing the '/download' endpoint from a password-protected file URL, allowing unauthorized users to access restricted files and sensitive metadata. An attacker can circumvent authentication protections by simply modifying the URL structure, gaining access to files they should not be able to view and retrieving exposed EXIF data including file system information.

## Attack scenario
1. Attacker creates two accounts on Cloudup (Account X and Account Y)
2. Using Account X, attacker uploads a file and protects it with a password, then obtains the download link (e.g., /files/[ID]/download)
3. Attacker logs out and logs in with Account Y (or any other unauthorized account)
4. Attacker modifies the copied URL by removing '/download' endpoint to access /files/[ID]/
5. The modified URL bypasses password protection and access controls, serving file contents
6. Attacker exfiltrates sensitive metadata including EXIF data, file permissions, timestamps, and file system paths

## Root cause
The application implements access control checks only on the '/download' endpoint but fails to enforce equivalent authentication and authorization checks on the base file path endpoint. The directory listing or file serving logic at '/files/[ID]/' operates without proper validation of user permissions, allowing any authenticated or unauthenticated user to access protected resources.

## Attacker mindset
An attacker recognizes that security implementations often focus on specific endpoints while overlooking alternative access paths. By systematically testing URL variations, the attacker discovers that removing path components bypasses restrictions. This demonstrates the value of path manipulation and endpoint enumeration in identifying access control flaws.

## Defensive takeaways
- Implement consistent authorization checks across all endpoints and URL paths that serve the same resource
- Enforce authentication and access control at the resource level, not just at specific endpoints
- Apply the principle of least privilege - deny all access by default and explicitly grant permissions
- Validate user permissions before serving any file content, regardless of the requested endpoint
- Implement proper URL routing validation to prevent directory traversal and endpoint bypass attacks
- Review and audit all URL patterns that access the same underlying resource for consistent security controls
- Disable automatic directory listing and metadata exposure for protected resources
- Implement security testing that includes URL manipulation and alternative endpoint discovery

## Variant hunting
Test other file endpoints: /files/[ID]/preview, /files/[ID]/info, /files/[ID]/metadata without authentication
Attempt to access files via direct path traversal: /files/[ID]/../[OTHER_ID]/
Test parameter manipulation: /files/[ID]/?download=0 or ?auth=bypass
Check for similar patterns in other Cloudup features (shares, collaborations, team files)
Attempt to access parent directories: /files/ without an ID parameter
Test with incomplete URLs: /files/[ID]?partial_download=1
Check API endpoints for similar authentication bypass patterns
Test case sensitivity variations in endpoint names

## MITRE ATT&CK
- T1190
- T1548
- T1566
- T1087
- T1526

## Notes
This vulnerability demonstrates a common class of access control bypass where developers secure one endpoint but neglect to protect alternative access paths to the same resource. The exposure of EXIF data containing file system paths and permissions exacerbates the severity. The fix should involve centralizing authorization logic and ensuring all paths to a resource enforce equivalent security controls. This type of vulnerability is particularly dangerous in file-sharing platforms where confidentiality and access control are critical business requirements.

## Full report
<details><summary>Expand</summary>

This vulnerability includes privileges escalation, authentication bypass, as well as some information disclosure as well. follow the below steps for reproduction.

1. go to https://cloudup.com and make two accounts say X and Y.
2. login with the account X and upload a file(can be txt,php,anything) and set a password for this file, now right click on download and copy the link location of the file. It is something like (https://cloudup.com/files/iDQ23wk5p1O/download)
3. Now logout from account X, and login with account Y. Now load the link location of file copied in step 2. what you will get? Forbidden, right?
4. But wait a second, modify the url mentioned in step 2 like below
 https://cloudup.com/files/iDQ23wk5p1O/   (remove the download part)
5. Load the above modified url, and you will see, you can access the file contents i.e. password protected file (authentication bypass), accessed by another user who is not authorized (privilege escalation) and information disclosure like 
"exif":{"exiftool version number":"9.35","file name":"HiTmbEE-C2","directory":"/tmp/thumbs","file size":"46 kB","file modification date time":"2014:05:29 08:37:22+00:00","file access date time":"2014:05:29 08:37:22+00:00","file inode change date time":"2014:05:29 08:37:22+00:00","file permissions":"rw-rw-r--"

</details>

---
*Analysed by Claude on 2026-05-24*
