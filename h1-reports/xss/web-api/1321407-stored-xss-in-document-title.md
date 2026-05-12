# Stored XSS in Document Title

## Metadata
- **Source:** HackerOne
- **Report:** 1321407 | https://hackerone.com/reports/1321407
- **Submitted:** 2021-08-27
- **Reporter:** thd3rboy
- **Program:** Localize (HackerOne Report #1321407)
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the document title field of the Localize application, allowing authenticated users to inject malicious JavaScript that persists on the server and executes in other users' browsers. The vulnerability enables attackers to steal cookies, execute arbitrary JavaScript, and access sensitive information by crafting specially formatted document titles with HTML/JavaScript payloads.

## Attack scenario
1. Attacker authenticates to the Localize application with a valid account
2. Attacker navigates to the documents section and creates a new project
3. Attacker selects 'documents' as the translation target and uploads a document
4. Attacker inputs malicious payload ("><img src=x onerror=alert(document.domain)>) in the Document Title field
5. Attacker saves the document, and the payload is stored on the server without sanitization
6. When other users or the attacker views the document list, the XSS payload executes in their browser context, enabling cookie theft or session hijacking

## Root cause
The application fails to properly sanitize and encode user input in the document title field before storing it in the database. Additionally, the application does not implement proper output encoding when rendering the title, allowing the injected HTML and JavaScript to be interpreted by the browser instead of being treated as plain text.

## Attacker mindset
An authenticated attacker seeks to escalate their privileges or compromise other users by injecting persistent malicious code. The attacker recognizes that document titles are typically displayed to multiple users, making this an effective vector for large-scale compromise. The use of image tag with onerror handler is a simple evasion technique to bypass basic input filters.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, including document titles, with whitelist-based filtering
- Apply context-aware output encoding (HTML entity encoding) to all dynamically rendered content before displaying to users
- Utilize a Content Security Policy (CSP) to restrict script execution and prevent inline JavaScript from executing
- Implement a Web Application Firewall (WAF) to detect and block known XSS payloads
- Use security-focused templating engines that auto-escape output by default
- Conduct regular security testing including DOM-based XSS testing and stored XSS scanning
- Enforce HTML sanitization libraries (e.g., DOMPurify, sanitize-html) on both client and server-side
- Apply the principle of least privilege to limit user permissions for document creation/modification

## Variant hunting
Test other document-related fields (description, metadata, tags) for similar Stored XSS vulnerabilities
Check project names and user profile fields for stored XSS
Test file upload functionality for XSS in filename or file metadata
Investigate comment/annotation features that may have similar encoding flaws
Test translated content fields and version history displays
Look for DOM-based XSS in document rendering/preview functionality
Test for mutation-based XSS using alternate encoding (Unicode, hex) bypasses

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1566.002

## Notes
This is an authenticated Stored XSS vulnerability with significant impact potential. The simple payload demonstrates inadequate input sanitization. The vulnerability affects all users who view the malicious document, making it a high-impact issue. The application's use of staging environment (localizestaging.com) suggests this was tested before production deployment, indicating good security awareness by the researcher.

## Full report
<details><summary>Expand</summary>

Summary :

Stored attacks are those where the injected script is permanently stored on the target servers, such as in a database, in a message forum, visitor log, comment field, etc. The victim then retrieves the malicious script from the server when it requests the stored information. Stored XSS is also sometimes referred to as Persistent or Type-I XSS.

Vulnerable URL : https://app.localizestaging.com/documents

Payload XSS : 
"><img src=x onerror=alert(document.domain)> 

Step to Reproduces :
1. Login to your account
2. Create Project
3. What are you translating? (select documents)
4. Upload Document
5. Input XSS payload in Document Title = "><img src=x onerror=alert(document.domain)> 
6. Save it
7. XSS triggered

## Impact

Can steal Cookie, Can run javascript code, and get information sensitive

</details>

---
*Analysed by Claude on 2026-05-12*
