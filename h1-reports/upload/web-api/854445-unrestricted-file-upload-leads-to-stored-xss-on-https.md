# Unrestricted File Upload Leading to Stored XSS in Certificate Upload Feature

## Metadata
- **Source:** HackerOne
- **Report:** 854445 | https://hackerone.com/reports/854445
- **Submitted:** 2020-04-20
- **Reporter:** sensoyard
- **Program:** HackerOne (undisclosed program)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Unrestricted File Upload, Stored Cross-Site Scripting (XSS), Missing Content-Type Validation, Improper File Type Validation
- **CVEs:** None
- **Category:** web-api

## Summary
The certificate upload functionality fails to validate file content-type, allowing attackers to upload HTML files containing malicious scripts. When other users access the uploaded certificate, the stored XSS payload executes in their browser context, potentially compromising user sessions and sensitive data.

## Attack scenario
1. Attacker registers an account on the vulnerable platform
2. Attacker navigates to the certification/certificate upload feature
3. Attacker uploads a malicious HTML file containing JavaScript payload (disguised as xss.html) instead of a legitimate certificate file
4. The application stores the HTML file without validating content-type or file extension, making it accessible via direct URL
5. When other users or administrators view the uploaded certificate attachment, the malicious script executes in their browser with their session privileges
6. Attacker's JavaScript payload can steal cookies, session tokens, perform actions on behalf of the victim, or harvest sensitive information

## Root cause
The application implements file upload functionality without proper validation mechanisms. Specifically: (1) No content-type validation on the server-side, (2) No file extension whitelist enforcement, (3) Uploaded files are served with content-type that allows browser execution, (4) No sandboxing or content security policies applied to uploaded file downloads

## Attacker mindset
An attacker recognizes that certificate upload features often have relaxed security controls since they appear low-risk. By combining unrestricted upload with direct file accessibility, they can inject persistent XSS payloads that affect any user viewing the certificate. This is particularly valuable if administrators or multiple users access certificates, multiplying the attack surface.

## Defensive takeaways
- Implement strict whitelist-based file type validation on both client and server-side (check file extensions AND MIME types)
- Validate file content against expected file signatures (magic bytes) rather than relying solely on headers
- Store uploaded files outside the web root or in a non-executable directory
- Serve uploaded files with Content-Disposition: attachment headers to force downloads instead of rendering
- Implement Content-Security-Policy headers to prevent inline script execution
- Rename uploaded files with random identifiers and remove original extensions
- Use a dedicated file storage service separate from application code
- Implement antivirus/malware scanning on uploaded files
- Apply least privilege principles to file access permissions

## Variant hunting
Check other upload features (profile pictures, documents, attachments) for similar content-type validation bypass
Test if SVG file uploads are allowed - SVG can contain embedded JavaScript
Attempt uploading files with double extensions (file.html.pdf) or null byte injection
Check if PDF uploads are validated - PDFs can contain JavaScript
Test polyglot files that are valid images but also valid HTML/JavaScript
Verify if uploaded files are served from same domain or separate domain
Check if Content-Security-Policy headers are present in file responses
Test CORS configuration on file endpoints for potential cross-origin attacks

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1204 - User Execution
- T1566 - Phishing
- T1059 - Command and Scripting Interpreter
- T1608 - Stage Capabilities
- T1657 - Financial Theft
- T1539 - Steal Web Session Cookie

## Notes
This vulnerability demonstrates a critical gap in input validation where multiple security controls failed simultaneously. The fact that files are directly accessible via URL (https://███/████/registration-service/files/███████.html) indicates they are served from a web-accessible location without proper content-type controls. The use of registration/certificate upload as the attack vector is notable because such features are often overlooked during security reviews. The report's simplicity and directness (basic HTML XSS payload) suggests the vulnerability was trivial to exploit, indicating lack of basic security testing.

## Full report
<details><summary>Expand</summary>

**Summary:**

When the user want to upload a "certificate", the web app doesn't check the content-type of the file. A user can upload any kind of file (binary,html,...)

## Step-by-step Reproduction Instructions

1. Create an account at https://██████/████████/app/registration/basic-info

2. When you are connected, click on "certification"

Upload this file as xss.html and save the modifications: 

```html
<!DOCTYPE html>
<html>
  <head>
    <title>Simple Test</title>
    <meta name="viewport" content="initial-scale=1.0">
    <meta charset="utf-8">
  </head>
  <body>
    <script>
	alert(document.cookie	)
	</script>
  </body>
</html>
```
3 . Go back to the "certification tab " and open the attachement in a new tab

POC :https://███/████/registration-service/files/███████.html

## Suggested Mitigation/Remediation Actions
Restrict the content-type of the uploaded files

## Impact

The unrestricted file upload vulnerability leads to stored xss.

</details>

---
*Analysed by Claude on 2026-05-24*
