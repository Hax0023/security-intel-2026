# Information Disclosure via File Upload Error Messages Revealing Server Webroot

## Metadata
- **Source:** HackerOne
- **Report:** 5073 | https://hackerone.com/reports/5073
- **Submitted:** 2014-03-29
- **Reporter:** mazen160
- **Program:** Coinbase
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Information Disclosure, Path Traversal Information Leak, Improper Error Handling
- **CVEs:** None
- **Category:** web-api

## Summary
An information disclosure vulnerability exists in Coinbase's file upload functionality at /merchant_settings that reveals the server's webroot path through error messages. When uploading files with double extensions (e.g., test.php.jpg), the server returns error responses containing the full filesystem path, allowing attackers to enumerate server directory structure.

## Attack scenario
1. Attacker navigates to https://coinbase.com/merchant_settings upload form
2. Attacker crafts a malicious filename with double extension (e.g., test.php.jpg, shell.php.png)
3. Attacker submits the file through the upload mechanism
4. Server processes the upload and returns an error message
5. Error message contains the absolute filesystem path revealing webroot location (e.g., /var/www/html, /home/user/public_html)
6. Attacker documents the webroot path for further reconnaissance and exploitation planning

## Root cause
Insufficient input validation and improper error handling in the file upload mechanism. The server fails to sanitize error messages before returning them to the user, exposing sensitive path information that should remain hidden from client-side responses.

## Attacker mindset
Reconnaissance-focused adversary using upload endpoints as reconnaissance vectors. The attacker recognized that double-extension filenames can bypass naive file type checks and leveraged resulting error messages to gain server architecture intelligence without requiring authentication escalation.

## Defensive takeaways
- Implement strict whitelist validation on file uploads (validate MIME type and extension separately)
- Sanitize all error messages before returning to clients; log full details server-side only
- Avoid exposing filesystem paths in HTTP responses or error messages
- Use generic error messages for upload failures (e.g., 'File upload failed' vs detailed path disclosure)
- Implement file type verification using magic bytes/file signatures, not just extensions
- Disable directory listing and implement proper access controls on upload directories

## Variant hunting
Test other file upload endpoints for similar path disclosure in error messages
Try triple-extension files (e.g., test.php.jpg.txt) to bypass extension filters
Test null byte injection in filenames (test.php%00.jpg) on older systems
Attempt symlink uploads if supported to map server structure
Test path traversal in filename (../../../test.php) combined with extension bypass
Check archive upload functions (ZIP, TAR) for path disclosure during extraction

## MITRE ATT&CK
- T1598 - Phishing: Reconnaissance
- T1592 - Gather Victim Host Information
- T1040 - Network Sniffing (information gathering phase)
- T1526 - Scan Web Content Discovery

## Notes
Early HackerOne report (ID 5073) from 2014. The vulnerability is relatively low-impact on its own but serves as valuable reconnaissance for attackers planning more sophisticated attacks. The use of double extensions (test.php.jpg) suggests the server may have been running older PHP versions where multiple extensions could trigger handler confusion. No explicit fix confirmation is mentioned in the provided content.

## Full report
<details><summary>Expand</summary>

Hello, 
While I was testing The upload method on https://coinbase.com/merchant_settings , I have found that if you try to upload a php file or any other file html in this shape (test.php.jpg) , an Information Disclosure will happen showing the webroot of the server. I have provide a screenshot to demonstrate the issue.

Thank you 
Mazin Ahmed
@mazen160

</details>

---
*Analysed by Claude on 2026-05-24*
