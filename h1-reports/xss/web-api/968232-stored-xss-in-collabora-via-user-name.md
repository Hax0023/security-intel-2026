# Stored XSS in Collabora via User Name Display

## Metadata
- **Source:** HackerOne
- **Report:** 968232 | https://hackerone.com/reports/968232
- **Submitted:** 2020-08-27
- **Reporter:** meliodas19
- **Program:** Nextcloud/Collabora
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in Collabora (CODE) when displaying user names during collaborative document editing. An attacker can inject malicious JavaScript in their user profile name that executes when victims open a shared document with the attacker present. This affects Nextcloud 19.0.1 and allows arbitrary script execution in the context of other users' browsers.

## Attack scenario
1. Attacker creates or compromises a Nextcloud account and sets the display name to a malicious payload: <img src=a onerror=alert(window.parent.location)>
2. Attacker creates a new document in Collabora and shares it with targeted victims (admin or other users)
3. Shared document appears in victims' file listings and they are notified of the share
4. Victim opens the shared document in Collabora editor while attacker also has it open
5. When the victim's client loads the document view, it displays the attacker's user name with the injected HTML/JavaScript
6. Browser executes the onerror payload, allowing attacker to access parent window location, session tokens, or perform other malicious actions

## Root cause
User display names are not properly sanitized or HTML-encoded before being rendered in the Collabora document editing interface. The application concatenates user name input directly into the DOM without escaping special characters or validating the content.

## Attacker mindset
Leverage collaborative features where user identity information is displayed to other users. Exploit trust relationships - victims are more likely to open documents shared by known contacts. Use image onerror handler as reliable XSS vector. Target privileged users (admins) to maximize impact.

## Defensive takeaways
- Always HTML-encode user-supplied input before rendering in web interfaces, especially in collaborative tools
- Implement strict Content Security Policy (CSP) to prevent inline script execution
- Validate user display names against whitelist of allowed characters (alphanumeric, spaces, common punctuation)
- Sanitize names using established libraries (DOMPurify, bleach, etc.) rather than custom filtering
- Perform security testing specifically for stored XSS in all user-facing input fields
- Use iframe sandboxing with restrictive permissions for collaborative editing features
- Implement regular security audits of shared document and collaborative editing code paths

## Variant hunting
Check for XSS in other user-identifying fields: email addresses, user comments, document titles
Test XSS payloads in real-time collaboration cursors/indicators showing other users' positions
Examine notification systems that display user names or activities
Check document metadata, revision history, and audit logs for similar issues
Test different Collabora integration points (Writer, Calc, Impress) for variant vulnerabilities
Investigate how user names are displayed in presence indicators during collaborative sessions

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing: Spearphishing Link (social engineering to open document)
- T1539 - Steal Web Session Cookie
- T1056 - Input Capture (keylogging via XSS)
- T1005 - Data from Local System

## Notes
Report demonstrates practical exploitation requiring victim interaction but leveraging natural collaboration workflow. Severity elevated by targeting admins and persistence through shared documents. The use of image onerror is reliable across browsers and bypasses some basic XSS filters looking only for script tags. Nextcloud/Collabora should implement defense-in-depth with both input validation and output encoding.

## Full report
<details><summary>Expand</summary>

Affected: collabora and nextcloud

Ubuntu 18.04.5 LTS
Nextcloud 19.0.1 snap version
collabora (CODE)

The name of the user is displayed when him joins to edit the document allowing the attacker trigger xss.

## Impact

* Set the name of the attacker account to <img src=a onerror=alert(window.parent.location)>
* Create a new document → share the document with admin or another victim → the document will appear automatically in the files of the victim as shared
* The attacker opens the document and waits until the victim also opens the document when opening it the payload is executed

{F965228}

</details>

---
*Analysed by Claude on 2026-05-12*
