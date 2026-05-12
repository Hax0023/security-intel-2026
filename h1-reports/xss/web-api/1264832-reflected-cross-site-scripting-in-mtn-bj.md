# Reflected Cross-Site Scripting (XSS) in MTN.BJ File Upload

## Metadata
- **Source:** HackerOne
- **Report:** 1264832 | https://hackerone.com/reports/1264832
- **Submitted:** 2021-07-16
- **Reporter:** alimanshester
- **Program:** MTN Benin (mtn.bj)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in MTN Benin's file upload functionality where malicious JavaScript can be injected through specially crafted image filenames. The payload executes in the user's browser when the uploaded filename is reflected on the page without proper sanitization or encoding.

## Attack scenario
1. Attacker crafts a malicious filename containing JavaScript payload: "><img src=x onerror=alert(document.cookie);.jpg
2. Attacker tricks user into visiting MTN.BJ website and navigating to affected file upload page
3. User enters email address and completes form fields with arbitrary data
4. User uploads image file with malicious filename containing XSS payload
5. Server stores or reflects the filename on the page without sanitization
6. Browser interprets and executes embedded JavaScript, allowing theft of cookies, session tokens, or credential harvesting

## Root cause
The application fails to properly validate, sanitize, and encode user-supplied input (filename) before reflecting it back to the user's browser. The filename parameter is likely directly inserted into HTML context without escaping or validation, allowing script injection through HTML/JavaScript metacharacters.

## Attacker mindset
Opportunistic attacker seeking to steal user credentials, session tokens, or sensitive information. Attacker leverages trust in legitimate domain (mtn.bj) to bypass browser security assumptions. May be conducting reconnaissance for credential harvesting or account takeover attacks.

## Defensive takeaways
- Implement strict input validation on all file uploads - whitelist allowed filename formats and reject suspicious characters (quotes, angle brackets, semicolons)
- Apply HTML entity encoding/escaping when displaying filenames or any user-controlled data in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Validate file extensions server-side and reject executable or suspicious extensions
- Sanitize filenames by removing or replacing special characters that could be interpreted as code
- Implement proper output encoding based on context (HTML encoding, JavaScript encoding, URL encoding)
- Use security testing in SDLC to identify XSS vulnerabilities before production deployment
- Consider using a Web Application Firewall (WAF) to detect and block XSS attempts

## Variant hunting
Similar vulnerabilities likely exist in other user input fields (email parameter, form inputs) and other pages on mtn.bj. Investigate: (1) All file upload functionality across the application, (2) Dynamic page generation where user input is reflected, (3) Search functionality that displays user queries, (4) Error messages that include user-supplied data, (5) Profile/account pages displaying user-entered information, (6) API endpoints that return user input

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1041 - Exfiltration Over C2 Channel

## Notes
The report lacks critical details: specific URL is redacted, no video or screenshot evidence provided in accessible form, no bounty amount disclosed. The vulnerability is straightforward but potentially high-impact due to cookie/session theft capabilities. The application should implement a secure file upload handler with proper validation at multiple layers (client-side validation, server-side validation, output encoding). The fact this made it to production suggests lack of security testing in development pipeline.

## Full report
<details><summary>Expand</summary>

Hello Team 
I have found a Reflected XSS vulnerability in mtn.jb by file name 


## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. go to : 
████
  2. enter any email and press  Suivant
  3. fill all the inputs by any data .
  4. in file upload upload any photo with payload file name : "><img src=x onerror=alert(document.cookie);.jpg

  5 . the payload executed in the page  


Supporting Material/References:
1 - video showing poc 
2 - screenshot

## Impact

An attacker can use XSS to send a malicious script to an unsuspecting user. The end user’s browser has no way to know that the script should not be trusted, and will execute the script. Because it thinks the script came from a trusted source, the malicious script can access any cookies, session tokens, or other sensitive information retained by the browser and used with that site. These scripts can even rewrite the content of the HTML page

</details>

---
*Analysed by Claude on 2026-05-12*
