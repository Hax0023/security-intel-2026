# Upload profile photo from URL - Client-Side Validation Bypass

## Metadata
- **Source:** HackerOne
- **Report:** 713 | https://hackerone.com/reports/713
- **Submitted:** 2014-01-14
- **Reporter:** zurke
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** medium
- **Vuln:** Client-Side Validation Bypass, Improper Input Validation, SSRF (Potential), Arbitrary File Upload
- **CVEs:** CVE-2017-0889
- **Category:** web-api

## Summary
The application relies solely on client-side validation to restrict profile photo uploads to file selection only. An attacker can modify the HTML form element from type='file' to type='url' using browser developer tools to bypass this restriction and upload images from arbitrary URLs. This enables potential SSRF attacks, malicious image hosting, or unauthorized resource access.

## Attack scenario
1. Attacker opens user profile photo upload page in a web browser
2. Attacker opens browser's Developer Tools (F12) and inspects the upload form element
3. Attacker changes the input element attribute from 'type="file"' to 'type="url"'
4. Attacker enters a malicious or external image URL in the now-visible text field
5. Attacker clicks 'Update Profile' or presses Enter to submit the form
6. Server processes the URL without proper validation and downloads/stores the image from that URL

## Root cause
Server-side validation is absent or insufficient. The application trusts client-side HTML validation (input type restriction) without implementing backend checks to ensure only file uploads are accepted. The server likely processes any URL provided without validating its origin or checking file submission method.

## Attacker mindset
An attacker recognizes that web forms often have client-side restrictions that are trivial to bypass. By modifying form attributes in the DOM, they can interact with the application in unintended ways. This could be used for SSRF attacks against internal services, embedding malicious content, or accessing restricted resources that the server can reach but users cannot.

## Defensive takeaways
- Never rely on client-side validation alone; always validate on the server
- Explicitly check that file uploads are submitted via multipart/form-data POST requests with actual file content
- Reject direct URL-based image processing or implement strict URL validation (whitelist domains, validate scheme)
- Implement SSRF protections: block requests to private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Validate file content-type and magic bytes server-side, not just extension
- Use separate endpoints for file upload vs. URL-based image fetching with different security controls
- Log and monitor suspicious upload attempts from unexpected URLs

## Variant hunting
Check for similar input type bypass in other file upload fields (documents, avatars, banners)
Test if URL-based uploads accept file:// protocol for local file access
Verify if SSRF filtering is implemented for URL uploads (attempt internal IPs, cloud metadata endpoints)
Check for XXE vulnerabilities if SVG or XML image formats are supported
Test if the server fetches URLs from user-controlled sources in other features (webhooks, notifications, exports)
Examine if Content-Disposition headers are properly set to prevent script execution
Look for timing-based SSRF detection via slow/unresponsive internal services

## MITRE ATT&CK
- T1190
- T1566.002
- T1021.001
- T1040

## Notes
This is a classic example of client-side validation bypass combined with potential SSRF. The vulnerability is relatively straightforward but demonstrates the importance of defense-in-depth. The reporter's humility about English skills is noted, but the bug report is clear enough. This vulnerability likely existed in production due to developer assumptions that users cannot or will not modify HTML form elements.

## Full report
<details><summary>Expand</summary>

Using this vulnerability users can upload images from any image URL. 
Just change upload type using inspect element  (from "type=file" to "type=url") , paste URL in text field and hit enter or click on "Update Profile". Your profile photo will be changed to photo from URL.

P.S  Im sorry for my bad english.


</details>

---
*Analysed by Claude on 2026-05-24*
