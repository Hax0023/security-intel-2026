# Stored XSS in Banner Block Description

## Metadata
- **Source:** HackerOne
- **Report:** 1065964 | https://hackerone.com/reports/1065964
- **Submitted:** 2020-12-24
- **Reporter:** solov9ev
- **Program:** Unknown (HackerOne Report #1065964)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Inadequate Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the banner block description field where user-supplied input is not properly sanitized or encoded before being stored and rendered. An attacker can inject malicious JavaScript payload through the description field that executes in the context of other users' browsers when they view the template.

## Attack scenario
1. Attacker creates a new template in the application
2. Attacker adds a banner block to the template
3. Attacker injects XSS payload in the banner block description field: "><img src=1 onerror=alert(document.domain)>
4. Malicious payload is stored in the database without sanitization
5. When other users view the template, the stored XSS payload executes in their browser context
6. Attacker can steal session cookies, perform actions on behalf of users, or redirect to malicious sites

## Root cause
The application fails to properly validate and encode user input in the banner block description field. Input is stored unsanitized in the database and rendered directly in HTML context without output encoding (e.g., HTML entity encoding), allowing JavaScript execution.

## Attacker mindset
An attacker with template creation capabilities seeks to inject persistent malicious code that affects all users viewing the compromised template. The simplicity of the payload suggests testing for basic XSS protections, looking for unprotected input fields in the UI.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, particularly in rich text/description fields
- Apply HTML entity encoding to all untrusted data before rendering in HTML context
- Use a library like DOMPurify or similar to sanitize user input server-side
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply the principle of least privilege for template creation and editing permissions
- Conduct security code review of template rendering logic
- Implement automated security testing for XSS in all input fields

## Variant hunting
Test other block types (text, image, etc.) for similar XSS vulnerabilities
Check title, alt text, and metadata fields in banner blocks
Test different encoding contexts (JavaScript, URL, CSS, SVG)
Attempt SVG-based XSS: <svg onload=alert(1)>
Test event handler variations: onmouseover, onclick, onload
Check if Content Security Policy bypasses exist (data:, blob:)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1547 - Boot or Logon Autostart Execution

## Notes
This is a classic stored XSS vulnerability with high impact. The attacker does not need special privileges beyond basic template creation. The vulnerability affects all users who view the malicious template, making it a persistent threat. The PoC uses a simple image tag with onerror handler, suggesting the application may lack basic XSS protections.

## Full report
<details><summary>Expand</summary>

## Steps To Reproduce:

- Create a new template and add a banner block

{F1128944}

- Add a description to the banner block description: `"><img src=1 onerror=alert(document.domain)>`

- Malicious code executed

{F1128945}

## Proof Of Concept:

{F1128942}

## Impact

With this vulnerability, an attacker can for example steal users cookies or redirect users on malicious website.

</details>

---
*Analysed by Claude on 2026-05-12*
