# Reflected XSS on reddit.com via URL Path

## Metadata
- **Source:** HackerOne
- **Report:** 1051373 | https://hackerone.com/reports/1051373
- **Submitted:** 2020-12-05
- **Reporter:** criptex
- **Program:** Reddit (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the verification endpoint at /verification/ path on reddit.com where user-supplied input is not properly sanitized before being rendered in the response. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when they visit the link and interact with the 'verify email' button.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the path parameter (e.g., /verification/asd',%20alert(document.location),%20%27)
2. Attacker shares the URL via social engineering (email, messaging, forums) to trick users into clicking it
3. Victim clicks the link and is redirected to reddit.com with the malicious payload in the URL
4. Victim clicks the 'verify email' button or the page loads the verification logic
5. The unvalidated path parameter is reflected into the HTML/JavaScript context without encoding
6. The attacker's JavaScript payload executes in victim's browser with same-origin privileges, allowing cookie/session theft or further attacks

## Root cause
The /verification/ endpoint fails to properly sanitize or encode user-supplied input from the URL path before including it in the response. The verification parameter is likely directly concatenated into JavaScript or HTML without proper escaping, allowing special characters and script tags to break out of the intended context.

## Attacker mindset
An attacker would recognize that verification endpoints often receive user input and frequently process it without strict validation. They would test path traversal and special character injection to identify contexts where output encoding is missing. The simplicity of the payload (using quotes and alert) suggests automated scanning or basic manual testing could discover this.

## Defensive takeaways
- Implement strict input validation on all URL parameters, especially in sensitive paths like verification endpoints
- Apply context-appropriate output encoding (HTML encoding, JavaScript encoding, URL encoding) to all user-supplied data before rendering
- Use a Content Security Policy (CSP) with strict directives to prevent inline script execution and restrict script sources
- Sanitize user input using established libraries (e.g., DOMPurify, OWASP Java Encoder) rather than implementing custom validation
- Implement server-side validation as the primary defense; client-side validation is insufficient
- Use templating engines with auto-escaping enabled by default
- Conduct regular security testing including XSS-focused penetration testing on authentication/verification flows

## Variant hunting
Test other endpoints with user input in path parameters: /reset/, /confirm/, /activate/, /validate/. Check for similar issues in query parameters on verification endpoints. Test special characters like backticks, angle brackets, and event handlers. Look for reflected parameters in email verification flows, password reset flows, and two-factor authentication endpoints.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Social Engineering

## Notes
This is a straightforward reflected XSS with moderate complexity to exploit but high impact. The PoC uses alert() for proof of concept but could easily be replaced with document.cookie exfiltration or other malicious payloads. The reliance on user interaction ('verify email' button) slightly reduces severity but does not eliminate the vulnerability. The report lacks specific bounty amount and response timeline information.

## Full report
<details><summary>Expand</summary>

Hi I found a XSS-R

To reproduce the issue please click the poc link and then press the "verify email" button

PoC:

https://www.reddit.com/verification/asd',%20alert(document.location),%20%27

## Impact

With the help of XSS an attacker can steal your cookies, in many cases steal sessions, download malware onto your system and send a custom request.
Users can be socially engineered by the attacker by redirecting them from the real website to a fake one and there are many more attack scenarios that an expert attacker can perform with XSS.
It is also possible to inject html thus modifying the original page

</details>

---
*Analysed by Claude on 2026-05-12*
