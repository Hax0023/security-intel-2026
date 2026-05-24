# File Upload XSS via Java Applet (.class/.jar) - Slackatwork

## Metadata
- **Source:** HackerOne
- **Report:** 97657 | https://hackerone.com/reports/97657
- **Submitted:** 2015-11-04
- **Reporter:** hassham
- **Program:** Slackatwork (slackatwork.com)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Improper File Upload Validation, Cross-Site Scripting (XSS) via Active Content, Arbitrary File Upload, Insufficient MIME Type Validation, Java Applet Execution
- **CVEs:** None
- **Category:** web-api

## Summary
The application's file upload function fails to properly validate file types, allowing an attacker to upload Java applet (.class) files despite claiming to accept only image files. When these malicious applets are loaded by a browser from the trusted origin, they execute with elevated privileges, enabling XSS attacks and session hijacking.

## Attack scenario
1. Attacker identifies file upload functionality on slackatwork.com (company logo upload)
2. Attacker crafts malicious Java applet (.class file) containing code to steal session cookies or modify page content
3. Attacker bypasses client-side and server-side validation by either spoofing MIME type (image/jpeg) or exploiting insufficient extension checking
4. Applet file is uploaded successfully and stored in publicly accessible directory (/wp-content/uploads/job-manager-uploads/company_logo/)
5. Attacker tricks user into visiting a page that embeds the applet (via iframe, object tag, or direct browsing)
6. Browser loads Java applet from trusted domain without security warnings; applet executes with user's privileges, stealing session tokens or account data

## Root cause
The application implements insufficient file upload validation by: (1) relying on file extension or MIME type checking that can be bypassed, (2) failing to validate actual file content/magic bytes, (3) storing uploaded files in a web-accessible directory with execution capabilities enabled, (4) not implementing whitelist-based file type restrictions, (5) misconfiguration allowing Java applets to run with privileges of the hosting domain

## Attacker mindset
An attacker recognizes that Java applets executed from a trusted origin bypass browser security models. By exploiting weak file upload validation and MIME type spoofing (uploading .class file as image/jpeg), they gain persistent XSS capability. The attacker's goal is account takeover through session hijacking, data theft, or malware distribution.

## Defensive takeaways
- Implement strict whitelist-based file upload validation - only allow specific safe extensions (pdf, txt, jpg, png, gif)
- Validate actual file content via magic bytes/file signatures, not just extension or MIME type headers
- Store uploaded files outside the web root or in a non-executable directory
- Set appropriate HTTP headers (Content-Disposition: attachment) to force download instead of inline execution
- Disable Java applet execution in browsers or require explicit user consent with warnings
- Implement Content Security Policy (CSP) headers to restrict script execution and object embedding
- Scan uploaded files with antivirus/malware detection engines
- Apply strict file permissions (non-executable) to upload directories
- Use randomized filenames and remove original extensions from user uploads
- Consider using a dedicated file upload service with sandboxing

## Variant hunting
Check for other executable file types: .swf (Flash), .exe, .dll, .jar (Java archives), .cab (ActiveX), .vbs, .scr
Test if other file upload functions in the application (profile pictures, attachments, documents) have the same validation flaws
Verify if uploaded files retain original names or if filename traversal (../../../) is possible
Check if .htaccess or web.config files can be uploaded to reconfigure handler mappings
Test polyglot files (image + applet) or double extension bypasses (.class.jpg)
Investigate if direct file access via directory listing is possible
Review if file upload APIs or bulk upload features have different validation logic
Check for TOCTOU race conditions between validation and storage

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (file upload vulnerability)
- T1204 - User Execution (applet loaded by user click/visit)
- T1566 - Phishing (social engineering to visit malicious page)
- T1539 - Steal Web Session Cookie (applet steals session tokens)
- T1547 - Boot or Logon Autostart Execution (applet with persistence)
- T1071 - Application Layer Protocol (C2 communication via applet)
- T1005 - Data from Local System (applet exfiltrates user data)

## Notes
This report was likely from 2015 (Java applet era). Java applets are now deprecated in modern browsers, but the underlying principle remains critical: arbitrary executable file uploads are catastrophic. The MIME type mismatch (class file uploaded as image/jpeg) proves the server trusts client-supplied headers. WordPress/file-manager plugins are common targets for similar bypasses. This should have been P1/Critical due to immediate account takeover capability.

## Full report
<details><summary>Expand</summary>

The web application supports file uploads and I was able to upload a Java Applet (.class/.jar) file. If a web browser loads a Java applet from a trusted site, the browser provides no security warning. If an attacker can upload a CLASS/JAR file with an applet, the file is executed even if the web page, which embeds the applet is located on a different site. An attacker could use a file upload function to build an XSS attack using active content.

The impact of this vulnerability
Malicious users may inject JavaScript, VBScript, ActiveX, HTML or Flash into a vulnerable application to fool a user in order to gather data from them. An attacker can steal the session cookie and take over the account, impersonating the user. It is also possible to modify the content of the page presented to the user.


Here is the link of the file i was able to upload with class extension:-

Successfully uploaded file Applet3863.class with content type image/jpeg.

The file is available at: http://slackatwork.com/wp-content/uploads/job-manager-uploads/company_logo/2015/11/Applet3863.class. 


</details>

---
*Analysed by Claude on 2026-05-24*
