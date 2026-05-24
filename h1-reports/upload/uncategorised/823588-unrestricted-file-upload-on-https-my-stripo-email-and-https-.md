# Unrestricted File Upload via JPEG Extension Bypass on Stripo Email Platform

## Metadata
- **Source:** HackerOne
- **Report:** 823588 | https://hackerone.com/reports/823588
- **Submitted:** 2020-03-18
- **Reporter:** doctor_spooky
- **Program:** Stripo Inc
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Unrestricted File Upload, Arbitrary File Upload, File Type Validation Bypass, Remote Code Execution (RCE), Authentication Required but High Impact
- **CVEs:** None
- **Category:** uncategorised

## Summary
Two critical unrestricted file upload vulnerabilities were discovered on my.stripo.email and stripo.email that allow authenticated attackers to upload malicious PHP files by renaming them with JPEG extensions. The web application performs only client-side or weak extension validation, enabling bypass of extension-based filtering. Uploaded PHP shells can be executed to achieve remote code execution and complete system compromise.

## Attack scenario
1. Attacker creates an account on my.stripo.email or accesses the template order feature on stripo.email
2. Attacker downloads a PHP web shell (e.g., r57 shell) and renames the file with a .jpg or .jpeg extension to bypass extension-based validation
3. On my.stripo.email: Attacker navigates to profile settings and uploads the PHP-as-JPEG file as a profile picture, which is accepted by the server
4. On stripo.email: Attacker navigates to template-order feature and uploads the PHP-as-JPEG file in the drop zone, bypassing extension checks
5. Attacker accesses the uploaded file URL and requests it with .php extension or manipulates the path to execute the PHP code
6. PHP shell executes with web server privileges, allowing attacker to run arbitrary commands, read sensitive files, pivot to backend systems, and achieve full server compromise

## Root cause
The application implements inadequate file type validation relying solely on file extension checking rather than validating actual file content (magic bytes). The server accepts files with image extensions (.jpeg) without verifying the actual MIME type or file content, and likely executes uploaded files or stores them in web-accessible directories with executable permissions.

## Attacker mindset
An attacker seeks to gain unauthorized code execution on the target web server. By understanding that extension-based filtering is commonly implemented but easily bypassed, the attacker leverages simple file renaming as a low-effort technique to upload executable code. The attacker recognizes that many web applications execute files based on extension rather than content validation, making this a high-probability attack vector for remote access and complete system takeover.

## Defensive takeaways
- Implement strict file content validation using magic bytes/file signatures (MIME type checking) rather than relying on file extensions
- Store uploaded files outside the web root or in a non-executable directory with proper access controls and permissions
- Configure web server to prevent script execution in upload directories via .htaccess or web server configuration (deny script execution in upload folders)
- Use a whitelist approach for allowed file types and validate against this list on the server side
- Rename uploaded files to random names and remove original file extensions to prevent direct access and execution
- Implement file size limits and scan uploaded files with antivirus/malware detection before storage
- Use security headers like Content-Disposition: attachment to force download instead of execution
- Perform both client-side and server-side validation, never rely solely on client-side checks
- Implement proper access controls to ensure authenticated users cannot upload to sensitive directories
- Log and monitor file upload activities for suspicious patterns

## Variant hunting
Search for similar file upload implementations across the platform: template galleries, user profile images, document management features, attachment uploads, and any other file input mechanisms. Test for bypass techniques: double extensions (.php.jpg), null byte injection (.php%00.jpg), case variation (.pHp), alternative executable extensions (.phtml, .php3-5, .phar), .htaccess uploads for configuration override, and polyglot files combining image and executable content. Verify if other image formats (PNG, GIF, SVG) containing code are also executable.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1578 - Modify Cloud Compute Infrastructure
- T1583 - Acquire Infrastructure
- T1608 - Stage Capabilities
- T1505 - Server Software Component
- T1570 - Lateral Tool Transfer
- T1059 - Command and Scripting Interpreter

## Notes
This vulnerability is authentication-dependent but critical due to RCE implications. The report lacks specific information about the bounty amount and remediation timeline. The vulnerability demonstrates a common security misconfiguration where developers trust file extensions without validating actual content. The presence of two upload vectors (profile picture and template order) suggests systemic validation weakness across the application.

## Full report
<details><summary>Expand</summary>

Hi Stripo Inc, I found 2 Unrestricted File Upload Vulnerabilities on your website.

First Vulnerability:
>Step to Reproduce 
1. Create an account in "https://my.stripo.email"
2. Simply Download a php shell from internet and open with text editor.  ex: r57 shell  
3. Then save it as JPEG file. 
4. Go back to your stripo account and click on your profile icon on the top right corner of the website and go to show profile.
(Try saving it as default .php document it does not let you to upload the php malicious shell )
5. Upload your shell saved as JPEG as profile picture.
6. After that this message will pop up on the screen "User icon has been saved".

Second Vulnerability:
>Step to Reproduce 
1. Go to the URL "https://stripo.email/template-order/"
2. Scroll down to "Click or Drop file here"
3. Try Uploading .php shell downloaded earlier. (It does not allow you to upload php malicious shells)
4. Now Upload the Shell that saved as JPEG.
5. You will allow to upload Malicious shells saved as JPEG (image)

Please look at the Attached images.

## Impact

The consequences of unrestricted file upload can vary, including complete system takeover, an overloaded file system or database, forwarding attacks to back-end systems, and simple defacement.Here is the list of attacks that the attacker might do:
--Compromise the web server by uploading and executing a web-shell which can run commands, browse system files, browse local resources, attack 
   other servers, and exploit the local vulnerabilities, and so forth.
--Put a phishing page into the website.
--Put a permanent XSS into the website.
--Bypass cross-origin resource sharing (CORS) policy and exfiltrate potentially sensitive data.
--Upload a file using malicious path or name which overwrites critical file or personal data that other users access. For example; the attacker might --- 
--replace the .htaccess file to allow him/her to execute specific scripts.

Take a look at the "https://owasp.org/www-community/vulnerabilities/Unrestricted_File_Upload"  for full documentation.

</details>

---
*Analysed by Claude on 2026-05-24*
