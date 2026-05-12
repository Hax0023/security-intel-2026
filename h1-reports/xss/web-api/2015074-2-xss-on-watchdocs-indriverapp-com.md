# Reflected XSS on watchdocs.indriverapp.com via JWT Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2015074 | https://hackerone.com/reports/2015074
- **Submitted:** 2023-06-06
- **Reporter:** maxdha
- **Program:** inDriver
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Unsafe HTML Rendering
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on watchdocs.indriverapp.com where user-supplied input in the 'jwt' URL parameter is not properly sanitized before being rendered in the DOM. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when visited.

## Attack scenario
1. Attacker identifies the webview endpoint at watchdocs.indriverapp.com/webview/v1 accepts multiple parameters including 'jwt'
2. Attacker crafts a malicious URL with XSS payload in the jwt parameter: %22%3E%3Cimg%20src=raw%20onerror=alert(%22hackerone%22)%3E
3. Attacker tricks a user into clicking the malicious link via phishing, social engineering, or posting in forums
4. User's browser loads the page and the unvalidated jwt parameter is reflected into the HTML/JavaScript context
5. The injected img tag with onerror handler executes arbitrary JavaScript in the user's browser session
6. Attacker can steal session tokens, credentials, redirect to phishing pages, or perform actions on behalf of the user

## Root cause
The application fails to properly sanitize or encode user-supplied input from the 'jwt' URL parameter before inserting it into the DOM. The parameter appears to be directly reflected without HTML entity encoding or Content Security Policy protection.

## Attacker mindset
An attacker would recognize that webview endpoints often pass authentication tokens as URL parameters without proper output encoding. By breaking out of the expected context (closing quotes with %22%3E) and injecting HTML/JavaScript, they can achieve arbitrary code execution. The use of img onerror is a simple but effective XSS vector.

## Defensive takeaways
- Implement strict input validation and output encoding - HTML encode all user input before rendering in HTML context
- Use a robust Content Security Policy (CSP) header to prevent inline script execution
- Avoid passing sensitive tokens (JWT, auth tokens) in URL parameters; use secure HTTP-only cookies instead
- Implement a Web Application Firewall (WAF) to detect and block XSS patterns
- Use templating engines that auto-escape by default rather than manual string concatenation
- Apply security headers: X-XSS-Protection, X-Content-Type-Options, X-Frame-Options
- Conduct regular security testing including DAST and manual code review of parameter handling

## Variant hunting
Look for other endpoints accepting URL parameters (phone, token, service, locale) that may also be vulnerable. Test parameters like 'service', 'locale', and 'phone' for similar XSS payloads. Check for DOM-based XSS where parameters are used in JavaScript code. Search for other webview endpoints across inDriver domains.

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The payload demonstrates HTML breaking and event handler injection. The use of %22 (quote), %3E (>), and img tag with onerror suggests the developer was not properly encoding output. The presence of authentication tokens (phone, token, jwt) in URL parameters is also a separate security concern. This is a straightforward reflected XSS with high impact due to access to user session context.

## Full report
<details><summary>Expand</summary>

## Summary:
I've found an XSS on https://watchdocs.indriverapp.com/

## Steps To Reproduce:


  1. Visit https://watchdocs.indriverapp.com/webview/v1?phone=████████&token=██████████&service=cargo&locale=en&jwt=%22%3E%3Cimg%20src=raw%20onerror=alert(%22hackerone%22)%3E#/
  1. You'll get an XSS alert



## Supporting Material/References:
███

## Impact

Execute javascript on user browser

</details>

---
*Analysed by Claude on 2026-05-12*
