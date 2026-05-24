# SSRF on Local Storage of iOS Mobile Application

## Metadata
- **Source:** HackerOne
- **Report:** 746541 | https://hackerone.com/reports/746541
- **Submitted:** 2019-11-26
- **Reporter:** l0l1ch3ng
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Server-Side Request Forgery (SSRF), Local File Inclusion (LFI), Sensitive Data Exposure, Arbitrary File Access
- **CVEs:** None
- **Category:** web-api

## Summary
The iOS mobile application fails to properly validate and sanitize user-uploaded files, allowing attackers to craft malicious HTML/SVG payloads that trigger SSRF attacks via file:// protocol handlers. By uploading files with manipulated content and extensions, an attacker can bypass access controls and read arbitrary local files stored on the device or application sandbox.

## Attack scenario
1. Attacker uploads a benign file to the application's file storage feature
2. Attacker modifies the file content to include SVG/HTML with JavaScript payload (e.g., <svg/onload=document.write(document.location)>)
3. Attacker manipulates file extension to .html or similar executable format during upload
4. Application stores and serves the malicious file without proper content validation
5. Attacker accesses the uploaded file, triggering JavaScript execution in application context
6. JavaScript payload enumerates local paths and reads sensitive files via file:// protocol (e.g., <iframe src='file:///path/to/sensitive/file'>)

## Root cause
Insufficient input validation and content-type verification on file uploads; lack of sandboxing or content security policy (CSP) to prevent execution of user-uploaded content; failure to restrict file:// protocol access from within WebView contexts; inadequate file extension and MIME type enforcement

## Attacker mindset
An attacker with basic understanding of SSRF and file upload vulnerabilities seeks to exfiltrate sensitive application data (credentials, tokens, configuration files, user data) stored locally on the iOS device or within the application's sandbox by leveraging the file upload feature as a gadget to execute arbitrary requests.

## Defensive takeaways
- Implement strict content-type validation based on file magic bytes, not just extensions
- Enforce whitelist-based file type restrictions at upload and serving layers
- Disable or restrict file:// protocol access in WebView by setting appropriate delegate methods (shouldStartLoadWithRequest in UIWebView/WKWebView)
- Sanitize and escape all user-uploaded content; store uploads outside web-accessible directories
- Implement Content Security Policy (CSP) headers to restrict protocol schemes and resource loading
- Use separate storage domains for user uploads with restricted capabilities
- Apply strict same-origin policies and disable script execution in uploaded file contexts
- Implement file access controls and ensure uploaded files are not directly executable
- Conduct security review of WebView configuration and file handling logic
- Add logging and monitoring for suspicious file upload patterns and file access attempts

## Variant hunting
Test other file upload endpoints for similar SSRF/LFI vulnerabilities
Attempt to upload files with null bytes, double extensions (file.txt.html), or other bypass techniques
Check if other URI schemes (data://, jar://, vfile://) are accessible from WebView context
Test if application processes uploaded files with various image/document parsers that might interpret embedded payloads
Investigate if there are any URL scheme handlers registered by the application that could be exploited (e.g., custom://)
Examine whether path traversal sequences (../) in filenames bypass directory restrictions
Test for XXE (XML External Entity) injection if application processes XML files
Check if uploaded files can be accessed via predictable paths or directory listing
Attempt to upload symlinks or files with special permissions
Test if file access controls differ based on authentication state or user roles

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1567 - Exfiltration Over Web Service
- T1005 - Data from Local System
- T1083 - File and Directory Discovery
- T1041 - Exfiltration Over C2 Channel
- T1104 - Multi-stage Channels

## Notes
This vulnerability demonstrates a critical gap in iOS application security by allowing local file disclosure through SSRF. The attack leverages the application's own WebView to read arbitrary files using file:// protocol, suggesting the application did not properly isolate user-uploaded content or restrict protocol access. The vulnerability is particularly severe on mobile platforms where local storage may contain sensitive user data, authentication tokens, or cached credentials. The proof-of-concept is straightforward and likely reproducible on many similar applications with inadequate file upload handling.

## Full report
<details><summary>Expand</summary>

1. The tester uploaded the text file, containing "test ssrf" message, in order to proof SSRF attack.
2. Next, the tester uploaded the common file and then manipulate the content and extension file to html format in order to find the application path: <svg/onload=document.write(document.location)> 
3. The tester access that file and found the application path to use for SSRF local file disclosure.
4. Then, the tester uploaded the common file and then manipulate the content and extension file to html format in order to view the local file via SSRF attack: <iframe src="file://.../ssrfpoc.txt" width="400" height="400"></iframe> 
5. The tester access that file and found that this application allow you to access and read the local file successfully.

## Impact

This allow anyone to use other URLs such as that can access documents on the system/application (using file://) a.k.a Sensitive Data Exposure.

</details>

---
*Analysed by Claude on 2026-05-24*
