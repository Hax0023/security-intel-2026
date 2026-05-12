# Stored XSS in Question Submission Form

## Metadata
- **Source:** HackerOne
- **Report:** 1901706 | https://hackerone.com/reports/1901706
- **Submitted:** 2023-03-12
- **Reporter:** vidaamuyarchi
- **Program:** question.com
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the question submission functionality at https://www.question.com/ask/ where user-supplied input containing JavaScript payloads is stored and executed in the browser of subsequent visitors. The vulnerability allows attackers to inject malicious iframe elements with event handlers that execute arbitrary JavaScript code.

## Attack scenario
1. Attacker navigates to https://www.question.com/ask/ question submission page
2. Attacker enters a question containing the payload '<iframe onload=alert(document.domain)>'
3. Attacker submits the question form
4. The malicious payload is stored in the application's database without proper sanitization
5. When any user (including the victim or other visitors) views the submitted question, the iframe onload event triggers
6. Arbitrary JavaScript executes in the victim's browser context, allowing data theft, session hijacking, or credential harvesting

## Root cause
The application fails to properly validate and encode user input before storing it in the database and rendering it in HTML responses. The question text is inserted directly into the DOM without sanitization, allowing JavaScript execution.

## Attacker mindset
An attacker seeks to compromise visitor sessions by injecting persistent malicious scripts into user-generated content, leveraging the trusted nature of the application to execute code in victims' browsers with the same origin privileges.

## Defensive takeaways
- Implement strict input validation using allowlists for permitted characters and HTML tags
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user-supplied content
- Use a Content Security Policy (CSP) with strict directives to prevent inline script execution
- Employ a robust HTML sanitization library (e.g., DOMPurify, sanitize-html) to strip dangerous elements while preserving safe formatting
- Implement server-side validation in addition to client-side checks
- Use Security Headers like X-XSS-Protection, X-Content-Type-Options, and X-Frame-Options
- Conduct regular security testing and code reviews focusing on user input handling
- Apply principle of least privilege to user-submitted content permissions

## Variant hunting
Test other user input fields (comments, profile descriptions, tags) for similar XSS vulnerabilities
Attempt reflected XSS in search parameters or query strings
Check for DOM-based XSS in JavaScript event handlers and dynamic content updates
Test attribute-based payloads: onmouseover, onerror, onclick, onkeydown
Try encoding bypass techniques: HTML entities, Unicode, JavaScript escaping
Test SVG-based XSS vectors and data URI schemes
Verify if HTML tags beyond iframe are filterable (script, img, svg, object, embed)

## MITRE ATT&CK
- T1190
- T1566
- T1567
- T1195

## Notes
The writeup contains formatting issues and incomplete information (typos: 'Nave' instead of 'Navigate', 'Tigred' instead of 'Triggered', 'domail' instead of 'domain'). The POC section is redacted (████). The vulnerability demonstrates a classic persistent XSS attack with moderate complexity to exploit but significant impact. Reproduction is straightforward across multiple browsers, making this a reliable exploit vector for mass compromise of site visitors.

## Full report
<details><summary>Expand</summary>

Hi Team I'm Find the Stored Xss On your Site

Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.

Steps To Reproduce:

1.  Go To Your Site https://www.question.com/
2. Nave https://www.question.com/ask/
5. Ask a Question Enter the Payload ```<iframe onload=alert(document.domail)>```
3.  Click to Sumit Question & Redirect to https://www.question.com/iframe-onload-alert-9-1631390.html
4. XSS was Tigred you See the Popup

POC

████

Tested on Firefox and chrome.

## Impact

The attacker can steal data from whoever checks the report.

</details>

---
*Analysed by Claude on 2026-05-12*
