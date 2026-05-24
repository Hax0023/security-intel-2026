# Reflected XSS via File Upload in Reddit Zendesk Help Portal

## Metadata
- **Source:** HackerOne
- **Report:** 1816181 | https://hackerone.com/reports/1816181
- **Submitted:** 2022-12-24
- **Reporter:** greymanx1
- **Program:** Reddit
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper File Upload Validation, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in Reddit's Zendesk help portal file upload functionality. Attackers can upload malicious SVG or XML files containing JavaScript that executes when the file is downloaded and opened in a browser, potentially allowing session hijacking and account takeover.

## Attack scenario
1. Attacker crafts a malicious SVG or XML file containing embedded JavaScript/XSS payload
2. Attacker visits https://reddithelp.com/hc/en-us/requests/new and submits a support request with their own email
3. Attacker uploads the crafted SVG/XML file through the file upload field
4. Attacker tricks a Reddit user into downloading the uploaded file from their email notification
5. When the victim opens the file in their browser, the embedded JavaScript executes in the context of the Reddit domain
6. Attacker's malicious script steals session cookies, credentials, or performs unauthorized actions as the victim

## Root cause
The application fails to properly validate, sanitize, and restrict file types during upload. SVG and XML files are treated as safe when they can contain executable JavaScript. The lack of Content-Type validation and sandbox restrictions allows scripts to execute with the victim's privileges when files are accessed through email links.

## Attacker mindset
An attacker recognizes that file upload mechanisms often have weaker security controls than direct input fields. They exploit the trust users place in downloading files from legitimate services. By using SVG/XML formats that bypass basic file extension checks, they achieve code execution with minimal suspicion. The indirect delivery via email makes attribution more difficult.

## Defensive takeaways
- Implement strict file type validation using magic bytes/MIME type verification, not just file extensions
- Disable script execution in uploaded files by serving them with Content-Disposition: attachment and appropriate Content-Type headers
- Sanitize SVG files to remove executable elements (scripts, event handlers) or disallow SVG uploads entirely
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Serve uploaded files from a separate domain with sandbox restrictions
- Require file re-authentication when accessing sensitive uploaded content
- Implement antivirus/malware scanning on uploaded files
- Log and monitor unusual file upload patterns

## Variant hunting
Search for similar upload functionality in other Zendesk instances, support portals, or help platforms. Test other vector file formats (PDF, TIFF with embedded objects), HTML files, and polyglot files. Investigate whether the vulnerability affects other file types or document formats that support embedded scripts.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1566.002 - Phishing: Spearphishing Link
- T1204.001 - User Execution: Malicious Link
- T1185 - Man in the Browser

## Notes
The report demonstrates cross-browser compatibility for SVG but notes XML only works in non-Chrome browsers. This suggests Chrome may have additional protections. The vulnerability chain relies on social engineering (email-based delivery) combined with the XSS, increasing likelihood of successful exploitation. The Zendesk platform should be particularly strict about uploads since it handles support requests from all user types.

## Full report
<details><summary>Expand</summary>

## Summary:
Reflected XSS in " https://reddit.zendesk.com/hc/en-us/requests/new " via file upload

## Impact:

!!
attacker can send that email to victim and steal user account or cookies

Cross site scripting attacks can have devastating consequences. Code injected into a vulnerable application can exfiltrate data or install malware on the user’s machine. Attackers can masquerade as authorized users via session cookies, allowing them to perform any action allowed by the user account.

XSS can also impact a business’s reputation. An attacker can deface a corporate website by altering its content, thereby damaging the company’s image or spreading misinformation. A hacker can also change the instructions given to users who visit the target website, misdirecting their behavior.

* Perform any action within the application that the user can perform.
* View any information that the user is able to view.
* Modify any information that the user is able to modify.
* Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user.

Note ! 
svg work with all browsers
xml file work with all browsers except ( google chrome )


## Steps To Reproduce:

  1. go to " https://reddithelp.com/hc/en-us/requests/new  " and select any type of report
  2. type your email in email fileds and type any text in other fileds 
  3. in upload function upload  <svg>  or <xml> file I attached and send the request
 4. now go to your mail box go to reddit mail and select the file you uploaded 
 5. after downlaoded the file open it in browser it will fire !

## Supporting Material/References:

  * Upload this files to site

{F2089769}
{F2089770}

## Impact

Steal user cookie 
Account Takeover !
Perform any action within the application that the user can perform.
View any information that the user is able to view.
Modify any information that the user is able to modify.
Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user

</details>

---
*Analysed by Claude on 2026-05-24*
