# XSS Reflected on reddit.com via url path

## Metadata
- **Source:** HackerOne
- **Report:** 1051373 | https://hackerone.com/reports/1051373
- **Submitted:** 2020-12-05
- **Reporter:** criptex
- **Program:** Reddit
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Reflected
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in Reddit's email verification endpoint where unsanitized user input from the URL path is rendered in the response without proper encoding. An attacker can craft a malicious link containing JavaScript payload that executes in the victim's browser when clicked.

## Attack scenario
1. Attacker crafts malicious URL with JavaScript payload in the verification path parameter
2. Attacker social engineers victim to click the link via email, chat, or forum post
3. Victim clicks link and is redirected to reddit.com/verification endpoint with injected payload
4. Victim's browser renders the page and executes the attacker's JavaScript code
5. Attacker's script steals session cookies, authentication tokens, or sensitive data
6. Attacker uses stolen credentials to impersonate victim or perform unauthorized actions

## Root cause
Insufficient input validation and output encoding on the email verification endpoint. User-supplied input from the URL path is reflected directly into the HTML response without proper sanitization or encoding, allowing arbitrary JavaScript execution.

## Attacker mindset
The attacker identified a common web application weakness by fuzzing the verification endpoint with special characters and JavaScript syntax. They recognized that the path parameter was reflected unsanitized and crafted a simple alert payload to demonstrate the vulnerability. The ease of exploitation and high-value target (Reddit) made this an attractive bug bounty submission.

## Defensive takeaways
- Implement strict input validation on all URL parameters and path components
- Apply context-appropriate output encoding (HTML entity encoding for HTML context)
- Use a Content Security Policy (CSP) to restrict inline script execution
- Employ automated security scanning to detect reflected XSS in common endpoints
- Implement httpOnly and Secure flags on sensitive cookies to prevent JavaScript access
- Conduct security code review of verification/authentication endpoints
- Use templating engines with auto-escaping capabilities to prevent reflected XSS

## Variant hunting
Test other verification endpoints (/verification/, /verify/, /email-verification/) for similar issues
Check if other path-based parameters reflect user input without encoding
Test for DOM-based XSS in JavaScript that processes verification parameters
Attempt bypass techniques: UTF-8 encoding, Unicode escapes, HTML entity encoding variations
Search for similar reflection patterns in password reset, account recovery, or confirmation flows
Test SVG/event handlers and data URLs as alternative XSS vectors in the endpoint
Check if stored XSS is possible if verification data is persisted in user profiles

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
The PoC is straightforward - the path `/verification/asd',%20alert(document.location),%20%27` directly executes the alert when the page loads. The vulnerability demonstrates poor security practices in handling sensitive endpoints. The writeup lacks specific version/timestamp information and remediation details, but the vulnerability is clearly reproducible. This is a classic reflected XSS that could have been caught with basic input validation and output encoding practices.

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
*Analysed by Claude on 2026-05-24*
