# Unrestricted File Upload in Chat Window - Remote Code Execution

## Metadata
- **Source:** HackerOne
- **Report:** 925513 | https://hackerone.com/reports/925513
- **Submitted:** 2020-07-16
- **Reporter:** ant_pyne
- **Program:** OWOX (bi.owox.com)
- **Bounty:** Not specified in report
- **Severity:** CRITICAL
- **Vuln:** Unrestricted File Upload, Remote Code Execution, Insufficient File Type Validation, Arbitrary File Upload
- **CVEs:** None
- **Category:** uncategorised

## Summary
The chat functionality in OWOX's web application fails to restrict file uploads, allowing attackers to upload executable files (.rb, .php) that can be automatically processed server-side. This enables remote code execution with server privileges, potentially compromising the entire application and underlying infrastructure.

## Attack scenario
1. Attacker authenticates to https://bi.owox.com with valid credentials
2. Attacker navigates to the Chat window interface
3. Attacker crafts a malicious PHP or Ruby file (e.g., web shell with system command execution capabilities)
4. Attacker uploads the malicious file through the file upload mechanism in chat
5. Attacker clicks send button; file is processed and stored on the server
6. Attacker accesses or triggers the uploaded file execution, achieving remote code execution in the server context

## Root cause
The application lacks server-side file type validation and execution prevention. The upload handler accepts dangerous executable file extensions (.php, .rb) without filtering, and stores them in a location where they can be automatically processed or accessed for execution by the web server.

## Attacker mindset
An authenticated attacker seeks to escalate privileges from user level to system level by abusing the file upload feature as a vector for remote code execution. The attacker recognizes that chat functionality often has weaker security controls and can exploit this to establish persistent access or launch further attacks against the infrastructure.

## Defensive takeaways
- Implement strict server-side whitelist validation for allowed file types (validate MIME types, magic bytes, and file extensions)
- Never store uploaded files in web-accessible directories or directories with execution permissions
- Disable script execution in upload directories via web server configuration (.htaccess, nginx config, web.config)
- Rename uploaded files to remove original extensions and use random identifiers
- Validate file content against expected file type signatures, not just extensions
- Implement file size limits and scan uploads with antivirus/malware detection
- Use a separate, isolated storage service for uploaded files outside the web root
- Log all file upload activities and monitor for suspicious patterns
- Apply principle of least privilege to file storage service accounts
- Conduct security code review of all file handling functions in chat and upload modules

## Variant hunting
Check if other file upload endpoints exist (profile pictures, documents, attachments) with similar vulnerabilities
Test for bypasses using double extensions (.php.jpg), null bytes (.php%00.jpg), or case variations (.pHP)
Investigate if uploaded files can be accessed directly via predictable paths
Check if other dangerous extensions are blocked or allowed (.exe, .sh, .py, .jsp, .asp, .phtml)
Test if file execution occurs automatically or only on access
Verify if file uploads are stored with execution permissions across different server configurations
Examine if chat file uploads bypass same restrictions applied to other upload features

## MITRE ATT&CK
- T1190
- T1505
- T1505.003
- T1071.001
- T1020
- T1041

## Notes
Report demonstrates high understanding of file upload vulnerability impacts including server-side RCE, client-side XSS, supply chain attacks, and library exploitation. The vulnerability is particularly dangerous because it's in a chat feature where users may have lower security expectations. Requires authentication but still critical as insider threats or compromised accounts can abuse this vector. No specific patch timeline or bounty amount mentioned in the report.

## Full report
<details><summary>Expand</summary>

#Summary:
The application allows the attacker to upload dangerous file types that can be automatically processed within the product's environment.

#Steps To Reproduce:
- Hit the browser and navigate to https://bi.owox.com and sign in.
- Open The Chat window.
- Upload any .rb or .php file .
- Click on send button.

## Impact

-> The impact of this vulnerability is high, supposed code can be executed in the server context or on the client side. The likelihood of detection for the
attacker is high. The prevalence is common. As a result the severity of this type of vulnerability is high.
->It is important to check a file upload module’s access controls to examine the risks properly.
-> Server-side attacks: The web server can be compromised by uploading and executing a web-shell which can run commands, browse system files,
browse local resources, attack other servers, or exploit the local vulnerabilities, and so forth.
->Client-side attacks: Uploading malicious files can make the website vulnerable to client-side attacks such as XSS or Cross-site Content Hijacking.
->Uploaded files can be abused to exploit other vulnerable sections of an application when a file on the same or a trusted server is needed (can again
lead to client-side or server-side attacks)
->Uploaded files might trigger vulnerabilities in broken libraries/applications on the client side (e.g. iPhone MobileSafari LibTIFF Buffer Overflow).
->Uploaded files might trigger vulnerabilities in broken libraries/applications on the server side (e.g. ImageMagick flaw that called ImageTragick!).
->Uploaded files might trigger vulnerabilities in broken real-time monitoring tools (e.g. Symantec antivirus exploit by unpacking a RAR file)
->A malicious file such as a Unix shell script, a windows virus, an Excel file with a dangerous formula, or a reverse shell can be uploaded on the server in
order to execute code by an administrator or webmaster later – on the victim’s machine.
->An attacker might be able to put a phishing page into the website or deface the website.
->The file storage server might be abused to host troublesome files including malwares, illegal software, or adult contents. Uploaded files might also
contain malwares’ command and control data, violence and harassment messages, or steganographic data that can be used by criminal organisations.
->Uploaded sensitive files might be accessible by unauthorised people.
->File uploaders may disclose internal information such as server internal paths in their error messages.

</details>

---
*Analysed by Claude on 2026-05-24*
