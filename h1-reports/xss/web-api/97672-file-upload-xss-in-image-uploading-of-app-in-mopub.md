# File Upload XSS in MoPub App Icon Upload

## Metadata
- **Source:** HackerOne
- **Report:** 97672 | https://hackerone.com/reports/97672
- **Submitted:** 2015-11-04
- **Reporter:** indoappsec
- **Program:** MoPub
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Improper File Upload Validation, Cross-Site Scripting (XSS), Content-Type Validation Bypass, File Extension Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
MoPub's app icon upload functionality fails to properly validate uploaded files, allowing attackers to bypass file type restrictions by uploading HTML files with spoofed extensions and content-types. The uploaded files are then served from images.mopub.com without proper content-type headers, enabling reflected XSS attacks when the file is accessed.

## Attack scenario
1. Attacker navigates to App settings in MoPub dashboard and initiates app icon upload
2. Attacker selects an HTML file containing malicious JavaScript payload and names it with .jpg extension
3. Attacker intercepts the upload request and modifies the Content-Type header to text/html while keeping .html filename
4. Server accepts and stores the HTML file on images.mopub.com without proper validation
5. Attacker shares the direct link to uploaded HTML file (https://images.mopub.com/app_icons/...) with victims
6. When victims access the link, browser executes embedded JavaScript in the HTML file due to missing Content-Type restrictions

## Root cause
Server-side validation relies solely on file extension and client-supplied Content-Type header without performing actual file content inspection (magic bytes verification). The server does not enforce strict Content-Type headers when serving files from images.mopub.com, allowing HTML execution.

## Attacker mindset
Attacker identified that the upload endpoint performs insufficient file validation and can be bypassed through simple request modification. Recognition that served files lack proper MIME-type enforcement makes this a valuable XSS vector for credential theft, session hijacking, or malware distribution via a trusted domain.

## Defensive takeaways
- Implement server-side file validation using magic byte/file signature verification, not just extension checking
- Enforce strict Content-Type headers (Content-Type: image/jpeg) when serving uploaded files regardless of stored filename
- Validate file content against expected image format (JPEG, PNG) using libraries like ImageMagick or similar
- Store uploaded files outside web root or in a directory not directly servable by the web server
- Implement X-Content-Type-Options: nosniff header to prevent MIME-type sniffing attacks
- Use separate domain (not trusted origin) for user-uploaded content or sandbox uploaded files
- Whitelist allowed MIME types both on client and server, rejecting anything else
- Consider converting/re-encoding uploaded images server-side to strip potential malicious content

## Variant hunting
Test other file upload endpoints (user avatars, documents, attachments) for similar validation bypass
Attempt to upload polyglot files (valid JPEG with embedded HTML/JS) to bypass format checks
Try alternative extensions (.jpe, .jpeg, .jpg.html, .jpg%00.html) to evade validation regex
Test SVG uploads with embedded JavaScript as alternative XSS vector
Attempt to upload executable files (PHP, JSP, ASP) to identify if RCE is possible
Check if uploaded files retain EXIF/metadata that could contain injected scripts

## MITRE ATT&CK
- T1190
- T1566.002
- T1566.003
- T1204.001

## Notes
This is a classic file upload validation bypass leading to XSS. The vulnerability is straightforward but impactful due to the trusted domain (images.mopub.com) used to serve the malicious content. The POC link in the report demonstrates the file was successfully uploaded and is publicly accessible. This affects all users of the MoPub platform who view app listings with malicious icons.

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
*Analysed by Claude on 2026-05-12*
