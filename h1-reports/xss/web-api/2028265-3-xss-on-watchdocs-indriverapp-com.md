# Reflected XSS on watchdocs.indriverapp.com via JWT Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2028265 | https://hackerone.com/reports/2028265
- **Submitted:** 2023-06-16
- **Reporter:** maxdha
- **Program:** InDriver
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on watchdocs.indriverapp.com where user-controlled input in the 'jwt' parameter is not properly sanitized or encoded before being reflected in the response. An attacker can craft a malicious URL with JavaScript payload in the jwt parameter to execute arbitrary code in a victim's browser.

## Attack scenario
1. Attacker identifies the watchdocs.indriverapp.com webview endpoint accepts a 'jwt' parameter
2. Attacker crafts a malicious payload containing JavaScript: fw"%><img src=fwa onerror=alert(1)>
3. Attacker encodes the payload and embeds it in the jwt parameter of a URL
4. Attacker shares the malicious link via phishing email, social media, or other social engineering methods
5. Victim clicks the link while authenticated or in an active session
6. The payload executes in victim's browser context, allowing theft of session tokens, personal data, or account takeover

## Root cause
The application fails to properly validate, sanitize, or HTML-encode user input from the 'jwt' URL parameter before reflecting it in the HTML response. The parameter value is inserted directly into the DOM without escaping special characters that have meaning in HTML/JavaScript context.

## Attacker mindset
An attacker recognizes that URL parameters are often trusted implicitly and reflected without validation. By testing special characters like quotes and angle brackets, they identify the lack of output encoding and craft a payload that breaks out of the intended context to inject malicious HTML/JavaScript.

## Defensive takeaways
- Implement strict input validation: whitelist expected JWT format and reject invalid characters
- Always HTML-encode/escape output when reflecting user input in HTML context (use context-appropriate encoding)
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Use security libraries/frameworks that auto-encode output by default (e.g., template engines with auto-escaping)
- Never trust URL parameters; treat all external input as untrusted
- Implement Server-Side Request Forgery (SSRF) and XSS validation in security testing pipeline
- Use HTTPOnly and Secure flags on sensitive cookies to limit XSS impact
- Perform security code review focusing on data flow from user input to output

## Variant hunting
Test other URL parameters (phone, token, service) for similar XSS issues
Attempt event handler bypasses: onerror=, onclick=, onload=, onmouseover=
Test for filter evasion: uppercase/mixed-case tags, HTML entities, Unicode encoding, null bytes
Check other endpoints on watchdocs.indriverapp.com for reflected parameters
Test for Stored XSS if jwt parameter is persisted in logs or user accounts
Check for DOM-based XSS if client-side JavaScript processes the jwt parameter
Test polyglot payloads that work across multiple contexts

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
This is a straightforward reflected XSS with clear proof-of-concept. The jwt parameter name suggests the app expects JWT tokens but fails to validate format. The vulnerability is trivially exploitable via URL sharing. This represents a critical security issue given InDriver's ride-sharing context where phishing attacks could lead to account compromise. The report redacts sensitive identifiers (phone, token values) appropriately.

## Full report
<details><summary>Expand</summary>

## Summary:
Found an XSS

## Steps To Reproduce:

  1. Go to https://watchdocs.indriverapp.com/webview/v1/transport-change?phone=██████&token=█████████&service=intercity3&jwt=fw%22%3E%3Cimg%20src=fwa%20onerror=alert(1)%3E
  

## Supporting Material/References:
████

## Impact

Execute Javascript on any victim browser

</details>

---
*Analysed by Claude on 2026-05-12*
