# Unrestricted File Upload Leads to Stored XSS and Potential RCE

## Metadata
- **Source:** HackerOne
- **Report:** 900179 | https://hackerone.com/reports/900179
- **Submitted:** 2020-06-17
- **Reporter:** 5050thepiguy
- **Program:** HackerOne
- **Bounty:** Unknown
- **Severity:** critical
- **Vuln:** Unrestricted File Upload, Stored Cross-Site Scripting (XSS), Remote Code Execution (RCE), Insufficient File Type Validation, Arbitrary File Write
- **CVEs:** None
- **Category:** web-api

## Summary
An unrestricted file upload vulnerability in the request form allows attackers to upload arbitrary files including HTML and PHP files. Uploaded files are stored in a web-accessible directory and can be directly accessed, enabling stored XSS attacks and potential remote code execution through PHP shell execution.

## Attack scenario
1. Attacker navigates to the vulnerable file upload endpoint at /request?openform
2. Attacker fills in required form fields and reaches the file upload section
3. Attacker crafts a malicious HTML file containing XSS payload and/or PHP code for shell execution
4. Attacker uploads the malicious file, which bypasses insufficient validation checks
5. Attacker accesses the uploaded file directly via predictable URL path (/$FILE/filename.html)
6. Payload executes in victim's browser (XSS) or on server (PHP RCE), allowing command execution and data theft

## Root cause
The application fails to implement proper file upload validation including: lack of file type/extension whitelisting, no MIME type verification, insufficient file content inspection, and storage of uploaded files in a web-accessible directory with direct execution permissions.

## Attacker mindset
An attacker would recognize that file uploads are a critical attack surface and exploit weak validation to achieve code execution. The ability to upload executable files directly and access them via predictable URLs suggests the application was not designed with security-first principles. The attacker exploits both client-side execution (XSS) and server-side execution (PHP) opportunities.

## Defensive takeaways
- Implement strict whitelist-based file type validation using both extension checks and MIME type verification
- Store uploaded files outside the web root directory to prevent direct execution
- Disable script execution in upload directories via web server configuration (.htaccess, nginx config)
- Implement Content-Security-Policy headers to mitigate XSS impact
- Rename uploaded files to remove original extensions and use random names to prevent predictability
- Validate file content/magic bytes in addition to extensions
- Implement file size limits and scan uploads with antivirus/malware detection
- Log and monitor file upload activities for suspicious patterns
- Use separate domain for serving user uploads to isolate from main application

## Variant hunting
Check for similar unrestricted uploads in other forms (/modify, /create, /update endpoints)
Test upload endpoints with polyglot files (PHP+PDF, JPG+PHP combinations)
Attempt double extension bypasses (.php.jpg, .phtml, .php5, .phar)
Test null byte injection in filenames (.php%00.jpg)
Check for path traversal in upload functionality (../../shell.php)
Test for race conditions between upload validation and file write
Verify if uploaded files inherit dangerous permissions or ownership
Check if uploaded files are processed/served with dangerous handlers

## MITRE ATT&CK
- T1190
- T1071
- T1059
- T1105
- T1195
- T1199
- T1566

## Notes
This is a classic unrestricted file upload vulnerability combining multiple high-impact issues. The combination of stored XSS and RCE potential makes this critical severity. The predictable file path structure (/4f4d0c69ea2b33a58525858a001e2b8c/$FILE/) suggests poor security architecture. The application appears to be Lotus Domino or similar enterprise platform based on URL patterns and file storage conventions.

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
*Analysed by Claude on 2026-05-12*
