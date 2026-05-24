# Self-DoS via Template Injection in Password Reset Email Field

## Metadata
- **Source:** HackerOne
- **Report:** 1265344 | https://hackerone.com/reports/1265344
- **Submitted:** 2021-07-16
- **Reporter:** sudo_bash
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Server-Side Template Injection (SSTI), Client-Side Template Injection (CCTI), Information Disclosure, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
A template injection vulnerability exists in the password reset form on access.acronis.com where user-supplied input in the email field is processed through a template engine (likely AngularJS) without proper sanitization. The injected payload reflects in the page response, allowing an attacker to execute template expressions and potentially escalate to XSS or information disclosure.

## Attack scenario
1. Attacker navigates to https://access.acronis.com/reset_password/new
2. Attacker crafts malicious email input containing template injection syntax: sudo_bash{{8*8}}@wearehackerone.com
3. Attacker submits the password reset form with the malicious payload
4. Server processes the input and reflects it unsanitized in the page response
5. Template engine evaluates the injected expression {{8*8}}, demonstrating code execution
6. Attacker can escalate to XSS, information disclosure, or account takeover through more complex payloads

## Root cause
Insufficient input validation and output encoding on the email field. The application fails to sanitize user input before passing it to the template engine, allowing arbitrary template expressions to be evaluated. The reflected output is not properly HTML-encoded.

## Attacker mindset
Reconnaissance and exploitation of template injection to gain code execution. An attacker would systematically test injection points, progressively craft payloads to bypass filters, and attempt to escalate from template injection to XSS or server-side code execution.

## Defensive takeaways
- Implement strict input validation on email fields using regex patterns and whitelist only valid email formats
- Apply output encoding/escaping appropriate to the context (HTML encoding for HTML context)
- Use template engines securely by disabling or restricting dangerous functions and expressions
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Avoid reflecting user input directly in templates; use parameterized/safe template functions
- Conduct security testing on all form inputs, especially those in authentication flows
- Employ template sandbox/restricted evaluation modes if using expression languages

## Variant hunting
Test other authentication forms (login, registration, account recovery) for similar injection points
Check other email input fields throughout the application (contact forms, profile settings, etc.)
Test other input fields with template injection payloads: {{7*7}}, {{_proto_}}, ${7*7}, etc.
Attempt polyglot payloads combining XSS and template injection syntax
Test for server-side template injection by attempting file read payloads: {{config}}, {{env}}, etc.
Look for similar patterns in subdomains and sister applications

## MITRE ATT&CK
- T1190
- T1059
- T1202
- T1598
- T1566

## Notes
This vulnerability demonstrates a common pattern where authentication-related forms receive less rigorous security testing than they should. The self-referential nature (reflected back to user) limits direct impact but creates an XSS vector. The description mentions 'AngularJs CCTI may lead to xss', indicating the attacker already considered escalation paths. The generic greeting in the submission suggests this may have been a mass reconnaissance effort.

## Full report
<details><summary>Expand</summary>

## Summary
HI acronis security team , how are you
I hope everyone is OK in the other side of the screen .
I found Template Injection in [https://access.acronis.com/reset_password/new] via the mail input .

## Steps To Reproduce:

 1. Open [https://access.acronis.com/reset_password/new] and Enter the mail Payload : sudo_bash{{8*8}}@wearehackerone.com
 2. After submite the mail , The resulte will Reflect in the page with the mail adress .

## Impact

- AngularJs CCTI may lead to xss .

</details>

---
*Analysed by Claude on 2026-05-24*
