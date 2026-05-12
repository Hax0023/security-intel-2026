# Stored XSS at Module Name

## Metadata
- **Source:** HackerOne
- **Report:** 1126433 | https://hackerone.com/reports/1126433
- **Submitted:** 2021-03-15
- **Reporter:** 20kilograma
- **Program:** Unknown
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the module name field where user input is not properly sanitized or encoded before being stored and displayed. An attacker can inject malicious JavaScript code through the module name parameter that executes in the browsers of other users viewing the module settings.

## Attack scenario
1. Attacker identifies the module creation/update functionality that accepts a 'module name' parameter
2. Attacker crafts a malicious payload exploiting HTML injection: "><div onmouseover="alert('XSS');">Hello :)
3. Attacker creates or updates a container with the malicious payload in the module name field
4. The payload is stored in the backend database without proper sanitization
5. When any user (including administrators) views the module settings or configuration page, the stored XSS payload is reflected in the response
6. The victim's browser executes the JavaScript payload, allowing the attacker to steal session tokens, credentials, or perform actions on behalf of the user

## Root cause
The application fails to properly validate and encode user input in the module name field. The input is stored directly in the database and rendered in HTML responses without escaping special characters or removing event handlers.

## Attacker mindset
An attacker would recognize that module configuration pages are frequently accessed by administrators and users, making this an ideal persistence vector. The simplicity of the payload execution suggests the attacker performed basic fuzzing to test for XSS vulnerabilities in user-controlled fields.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, rejecting or sanitizing HTML special characters
- Apply proper output encoding (HTML entity encoding) when rendering user-controlled data in HTML context
- Use a security-focused templating engine that provides automatic context-aware encoding
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Apply the principle of least privilege - restrict module name editing to authorized users only
- Perform regular security code reviews focusing on data flow from input to output
- Implement automated security testing (SAST/DAST) to detect XSS vulnerabilities
- Use a Web Application Firewall (WAF) with XSS detection rules as a secondary control

## Variant hunting
Check other user input fields (container name, description, tags, labels, metadata) for similar XSS vulnerabilities
Test module configuration pages for reflected XSS in query parameters or request bodies
Review all CRUD operations on modules and containers for improper output encoding
Test file upload functionality for XSS through file names or metadata
Check API endpoints that return module data to verify proper encoding in JSON/XML responses
Test for DOM-based XSS in JavaScript that processes module names client-side
Look for similar patterns in other administrative panels or configuration pages

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This is a classic stored XSS vulnerability with high impact potential since module settings are typically accessed by administrators. The simplicity of the payload and exploitation method suggests inadequate security controls around input sanitization. The vulnerability could be leveraged for account takeover, privilege escalation, or lateral movement within the application.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello, I found stored xss at module name with this payload ```"><div onmouseover="alert('XSS');">Hello :)```

## Steps To Reproduce:
1. Add new container, it doesn't matter which is it
2. Paste this payload  in the module name```"><div onmouseover="alert('XSS');">Hello :)```
3. Update it then check the module name again in setting
4. Alert Popup

## Stored XSS
Stored cross-site scripting (also known as second-order or persistent XSS) arises when an application receives data from an untrusted source and includes that data within its later HTTP responses in an unsafe way.

## Impact

Execute Js in victims browser

</details>

---
*Analysed by Claude on 2026-05-12*
