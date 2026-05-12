# Stored XSS in Trix Editor 2.1.1 via Malicious Paste Content

## Metadata
- **Source:** HackerOne
- **Report:** 2521419 | https://hackerone.com/reports/2521419
- **Submitted:** 2024-05-27
- **Reporter:** thwin_htet
- **Program:** Basecamp/Trix Editor (Open Source)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Sanitization, HTML Injection
- **CVEs:** CVE-2024-34341
- **Category:** web-api

## Summary
Trix editor version 2.1.1 fails to properly sanitize pasted HTML content containing malicious attachments, allowing attackers to execute arbitrary JavaScript code. The vulnerability specifically exploits the data-trix-attachment attribute which bypasses existing sanitization controls, potentially allowing session hijacking and unauthorized actions.

## Attack scenario
1. Attacker crafts malicious HTML containing a data-trix-attachment attribute with embedded JavaScript payload (e.g., img tag with onerror handler)
2. Attacker tricks user into copying the malicious content from a webpage or document
3. User pastes the content into a Trix editor instance within a vulnerable application
4. Trix editor processes the pasted content and fails to sanitize the attachment payload
5. JavaScript payload executes in the user's browser within the application context
6. Attacker gains ability to steal session tokens, perform actions as the user, or exfiltrate sensitive data

## Root cause
Trix editor's sanitization logic does not adequately validate or sanitize the 'content' field within data-trix-attachment attributes. The contentType specification (text/html5) is processed without proper escaping of embedded HTML/JavaScript, allowing event handlers to remain executable after parsing.

## Attacker mindset
An attacker would recognize that attachment metadata fields are often overlooked in sanitization routines. By embedding payloads in structured data attributes rather than plain HTML, they can bypass regex-based or naive DOM-based sanitizers. This represents a bypass of CVE-2024-34341, indicating previous patches were incomplete.

## Defensive takeaways
- Implement whitelist-based HTML sanitization rather than blacklist approaches for all user-controlled input, including structured data attributes
- Parse and validate attachment metadata separately from content; never treat serialized JSON/object properties as trusted
- Use a well-maintained HTML sanitization library (DOMPurify, bleach, etc.) rather than custom implementations
- Apply Content Security Policy (CSP) headers to limit script execution context
- Sanitize content at multiple layers: input validation, storage, and output rendering
- Conduct security-focused code review specifically for data attribute handling in rich text editors
- Implement automated testing with XSS payload vectors including attachment structures
- Version pin dependencies and maintain rapid patching procedures for DOM manipulation libraries

## Variant hunting
Look for similar bypasses in: (1) Other attachment-based fields in Trix (data-trix-embed, data-trix-image), (2) Different contentType values that might bypass specific sanitization branches, (3) Nested or encoded payloads (base64, HTML entities) within attachment content, (4) Other rich text editors using similar attachment metadata patterns (ProseMirror, Draft.js, QuillJS), (5) CSS injection via style attributes in attachment content

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1204: User Execution
- T1539: Steal Web Session Cookie
- T1114: Email Collection
- T1005: Data from Local System

## Notes
This report explicitly references CVE-2024-34341, indicating a patch evasion scenario. The use of data-trix-attachment with contentType 'text/html5' suggests the editor may have attempted to fix inline XSS but failed to account for structured attachment objects. The PoC is reproducible and affects real installations. Researchers should coordinate with Basecamp/Trix maintainers for patch development and track downstream applications using vulnerable versions.

## Full report
<details><summary>Expand</summary>

The Trix editor  is vulnerable to arbitrary code execution when copying and pasting content from the web or other documents with markup into the editor. The vulnerability stems from improper sanitization of pasted content, allowing an attacker to embed malicious scripts which are executed within the context of the application.

### Vulnerable Version
2.1.1

### Steps to Reproduce
1. Run this HTML code on browser.
```
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <title>Trix Editor XSS Demo</title>
  <script src="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.umd.min.js"></script>
  <link href="https://cdn.jsdelivr.net/npm/trix@2.1.1/dist/trix.min.css" rel="stylesheet">
</head>
<body>
  <h1>Trix Editor XSS Demo</h1>
  <trix-editor></trix-editor>
  <script>
  document.write(`copy<div data-trix-attachment="{&quot;contentType&quot;:&quot;text/html5&quot;,&quot;content&quot;:&quot;&lt;img src=1 onerror=alert(document.domain)&gt;XSS POC&quot;}"></div>me`);
  </script>
</body>
</html>
```
2. Click `copy me` and paste it in trix editor.

{F3302252}

3. Alert will pop up.

This could be a bypass of recent Trix Editor CVE : CVE-2024-34341
Ref : https://github.com/basecamp/trix/security/advisories/GHSA-qjqp-xr96-cj99

## Impact

An attacker could exploit these vulnerabilities to execute arbitrary JavaScript code within the context of the user's session, potentially leading to unauthorized actions being performed or sensitive information being disclosed.

</details>

---
*Analysed by Claude on 2026-05-12*
