# Unrestricted File Upload Leads to Stored XSS and Potential RCE

## Metadata
- **Source:** HackerOne
- **Report:** 900179 | https://hackerone.com/reports/900179
- **Submitted:** 2020-06-17
- **Reporter:** 5050thepiguy
- **Program:** HackerOne (Undisclosed Organization)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Unrestricted File Upload, Stored Cross-Site Scripting (XSS), Remote Code Execution (RCE), Improper Input Validation, Insufficient Access Controls
- **CVEs:** None
- **Category:** web-api

## Summary
An unrestricted file upload vulnerability in the request form functionality allows authenticated users to upload arbitrary file types, including HTML and PHP files. Uploaded files are stored and accessible via direct URL, enabling attackers to execute stored XSS payloads and potentially achieve remote code execution through PHP shell creation.

## Attack scenario
1. Attacker navigates to the vulnerable /request?openform endpoint
2. Attacker completes the multi-step request form with malicious intent
3. At the file upload stage, attacker uploads a crafted HTML file containing JavaScript payload or a PHP shell script
4. Attacker submits the request form, causing the malicious file to be stored on the server
5. Attacker accesses the uploaded file via direct URL ($FILE/unsure1.html) or triggers it through the request modification interface
6. Stored XSS payload executes in victim's browser session, or PHP shell provides command execution capabilities for further system compromise

## Root cause
The application lacks proper file type validation and filtering on the upload endpoint. No whitelist of acceptable file extensions is enforced, no Content-Type verification occurs, and uploaded files are stored in a web-accessible directory with execution permissions enabled for scripting languages.

## Attacker mindset
An attacker seeks to compromise application availability, confidentiality, and integrity. The unrestricted upload capability is viewed as a gateway to both client-side attacks (XSS affecting other users) and server-side compromise (RCE via PHP execution), enabling credential theft, data exfiltration, lateral movement, and persistent backdoor installation.

## Defensive takeaways
- Implement strict whitelist-based file type validation using multiple verification methods (extension checking, MIME type validation, magic bytes inspection)
- Restrict uploads to documented business-required file types only (JPG, DOC, DOCX, PDF as suggested)
- Store uploaded files outside the web root or in a non-executable directory to prevent direct execution
- Disable script execution in upload directories via web server configuration (.htaccess, nginx rules, IIS settings)
- Rename uploaded files using randomized identifiers and store original names in database separately
- Implement strict Content-Disposition headers (attachment, not inline) to prevent in-browser execution
- Apply antivirus/malware scanning to uploaded files before storage
- Enforce proper access controls ensuring users can only access their own uploaded files
- Log and monitor file upload activities for anomalous patterns
- Conduct regular security testing of upload functionality in development and staging environments

## Variant hunting
Check for similar unrestricted upload endpoints in document management, profile, settings, or support ticket features
Test polyglot files (valid image + PHP code) to bypass basic extension checks
Investigate whether uploaded files bypass antivirus or security scanning mechanisms
Review if other scripting languages (.jsp, .asp, .aspx, .phtml) are executable in upload directories
Test double extension uploads (file.php.jpg) and null byte injection (file.php%00.jpg)
Verify if path traversal is possible during upload to write files to different directories
Check whether authenticated users with elevated privileges have additional upload capabilities
Examine if API endpoints for file upload have different or weaker validation than web forms
Test if uploaded files can overwrite existing critical application files
Investigate whether SVG, XML, or other markup files can be uploaded to trigger XXE or DOM-based XSS

## MITRE ATT&CK
- T1190
- T1199
- T1598
- T1566
- T1204
- T1059
- T1505
- T1571
- T1053
- T1133

## Notes
Report redacts sensitive information (URLs, organization name, document numbers). Evidence includes PoC video and HTML payload file demonstrating both XSS and PHP shell creation. The multi-step form process and document-based storage suggest this may be a Lotus Notes/Domino environment or similar document management system. The direct file access URL pattern ($FILE/hash/filename) confirms server-side storage vulnerability. Remediation should be prioritized as critical due to combined XSS+RCE impact and ease of exploitation.

## Full report
<details><summary>Expand</summary>

**Summary:**
Unrestricted file upload at████████/request?openform. When the user wants to upload a file the app allows the user to upload a HTML file leading to stored XSS and creation of a simple php script. A user can upload the HTML file and trigger XSS and trigger potential RCE with php shell. Please go to the ██████ Request that I created at -- ██████████AllOpenOrders/4F4D0C69EA2B33A58525858A001E2B8C?opendocument and select the file at the bottom "unsure1.html" to trigger payload to show XSS and php shell. You can also go directly to the uploaded file at ████0/4f4d0c69ea2b33a58525858a001e2b8c/$FILE/unsure1.html. Please see the attached PoC video as well. Thanks.

## Impact
The unrestricted file upload vulnerability leads to stored XSS and creation of php shell leading to potential RCE, which opens the door to numerous malicious attacks by the attacker. 

## Step-by-step Reproduction Instructions

1. Go to███/request?openform
2. Enter in the details for this page and you will automatically be redirected to the next page. Do the same thing here and enter in all the necessary information
3. Then, towards the bottom you are given the option to upload files so click "browse" and upload your payload
4. Click "submit request" then go back to █████████ModifyRequest.xsp and enter in the 14 digit Document Number. 
5. Scroll down to the bottom of your request and click the HTML payload.
6. Observe that XSS triggers and php shell is seen as well. 

## Product, Version, and Configuration (If applicable)
███
███request?openform

## Suggested Mitigation/Remediation Actions
Restrict file uploads to only necessary business requirements. If possible restrict uploads to JPG, DOC, DOCX, and PDF. Don't allowed upload of executable files.

##References
Please see attached PoC video
Please see attached PoC HTML page as well used for the payload

## Impact

The unrestricted file upload vulnerability leads to stored XSS and creation of php shell leading to potential RCE, which opens the door to numerous malicious attacks by the attacker.

</details>

---
*Analysed by Claude on 2026-05-24*
