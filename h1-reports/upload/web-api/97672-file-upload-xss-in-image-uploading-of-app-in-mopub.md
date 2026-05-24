# File Upload XSS in MoPub App Icon Upload Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 97672 | https://hackerone.com/reports/97672
- **Submitted:** 2015-11-04
- **Reporter:** indoappsec
- **Program:** MoPub
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper File Upload Validation, Cross-Site Scripting (XSS), Content-Type Manipulation, File Extension Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
MoPub's app icon upload functionality fails to properly validate uploaded files, allowing attackers to upload HTML files with XSS payloads by modifying the file extension and Content-Type header. The server serves uploaded files from images.mopub.com without sanitization, enabling arbitrary JavaScript execution in the browser context of that domain.

## Attack scenario
1. Attacker creates an HTML file containing malicious JavaScript payload (e.g., <script>alert('XSS')</script>)
2. Attacker renames the HTML file to have a .jpg extension to bypass client-side validation
3. Attacker navigates to app settings in MoPub and attempts to upload the file as an app icon
4. Attacker intercepts the HTTP request and modifies Content-Type from image/jpeg to text/html
5. Server accepts the file and stores it on images.mopub.com without proper validation
6. When the uploaded file URL is accessed, the HTML/JavaScript is executed in the user's browser within the images.mopub.com domain

## Root cause
The application implements only client-side or weak server-side validation, checking filename extension without validating actual file content. The server trusts the Content-Type header provided by the client and does not perform MIME type detection or file signature verification. Uploaded files are served with permissive Content-Type headers, allowing browsers to execute HTML/JavaScript content.

## Attacker mindset
The attacker systematically tested upload validation by attempting to bypass extension checks through double extension attacks and Content-Type header manipulation. They recognized that client-side validation alone could be circumvented and that the hosting domain (images.mopub.com) would execute uploaded HTML, making this a viable XSS vector. This demonstrates understanding of how multipart form data is processed and how browsers interpret Content-Type headers.

## Defensive takeaways
- Implement server-side file validation using magic bytes/file signatures (not just extension or Content-Type header)
- Store uploaded files outside the web root or in a location that cannot execute code (disable script execution via web server configuration)
- Serve uploaded files with Content-Disposition: attachment header to force downloads instead of inline execution
- Use a separate domain for user-uploaded content to isolate XSS attacks via Same-Origin Policy
- Re-encode/re-save images using image processing libraries to strip potential malicious content
- Implement whitelist of allowed MIME types and reject all others
- Use Content Security Policy (CSP) headers to restrict script execution
- Validate file content against expected format specifications, not just headers

## Variant hunting
Test other file upload endpoints (profile pictures, thumbnails, banners) for similar validation bypass
Attempt polyglot files (valid image + HTML/JavaScript) to bypass content inspection
Test null byte injection (filename.jpg%00.html) on older systems
Try MIME type sniffing with .jpg.html double extension
Test uploading SVG files which can contain embedded JavaScript
Check if uploaded files can be accessed via directory traversal or predictable paths
Test for XXE via SVG upload if XML parsing is involved
Verify if other user-uploaded content endpoints have similar issues

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1599

## Notes
This is a classic example of insufficient input validation combined with improper file serving. The vulnerability is straightforward to exploit and has high impact as it allows persistent XSS on a trusted domain. The attacker provided clear reproduction steps and a proof-of-concept link, making the issue immediately actionable. The vulnerability affects app developers using MoPub who may trust icons served from images.mopub.com domain, potentially compromising their users' trust.

## Full report
<details><summary>Expand</summary>

Hi Team,

I want to report a File upload XSS in your Image upload functionality of Apps in mopub. Server doesn't check whether you are uploading a jpg/jpeg files and it upload the file on image.mopub.com .

POC link : https://images.mopub.com/app_icons/126cb3308e1a464385a49c4c7aaeac56

Steps to reproduce :
1.Go to App settings and select a html file with .jpg extension.
2.Intercept the request and change the .jpg to .html and change the content type to text/html and it will upload the file.
3.Open the link of image in new file and XSS will pop up.

HTTP request :

POST /inventory/app_icon/upload/ HTTP/1.0
Host: app.mopub.com
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.9; rv:42.0) Gecko/20100101 Firefox/42.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
X-CSRFToken: YZ8hbuu1vB9p5s1ni2vPZ5kMrhMqeDo5
X-Requested-With: XMLHttpRequest
Referer: https://app.mopub.com/inventory/app/97142808ce5d4ace895480a3ffe7d631/
Content-Length: 389
Content-Type: multipart/form-data; boundary=---------------------------1714461176134095862036612614
Cookie: [Cookie values]
Connection: keep-alive
Pragma: no-cache
Cache-Control: no-cache

-----------------------------1714461176134095862036612614
Content-Disposition: form-data; name="image_upload"; filename="xssfileuploadcopy.html"
Content-Type: text/html

HTML contetn
-----------------------------1714461176134095862036612614--


Let me know if you need any other help from my side.

Best Regards !
Vijay Kumar 






</details>

---
*Analysed by Claude on 2026-05-24*
