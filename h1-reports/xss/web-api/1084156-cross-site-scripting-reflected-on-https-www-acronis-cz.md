# Reflected Cross Site Scripting (XSS) on Acronis.cz Request Form

## Metadata
- **Source:** HackerOne
- **Report:** 1084156 | https://hackerone.com/reports/1084156
- **Submitted:** 2021-01-22
- **Reporter:** darkdream
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (Reflected), HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
The Acronis.cz request form (poptavka-acronis) fails to sanitize user input in form fields, allowing attackers to inject arbitrary JavaScript and HTML code. This reflected XSS vulnerability can be exploited to steal session cookies, conduct phishing attacks, or redirect users to malicious websites.

## Attack scenario
1. Attacker identifies the vulnerable form at https://www.acronis.cz/poptavka-acronis/
2. Attacker crafts a malicious payload such as "><script>alert(1);</script> and injects it into a form field
3. Attacker sends the form with the injected payload, which gets reflected back in the server response without proper encoding
4. When a victim views the response, the JavaScript executes in their browser within the Acronis.cz origin
5. Attacker's script can now access cookies, session tokens, or redirect the user to a phishing page
6. Attacker harvests credentials or performs unauthorized actions on behalf of the victim

## Root cause
Insufficient input validation and output encoding. Form fields are not properly sanitized before being reflected in HTTP responses, and there is no Content Security Policy (CSP) to prevent inline script execution.

## Attacker mindset
An attacker would recognize that request forms are common entry points for user input. By testing basic XSS payloads with script tags and HTML elements, they quickly identify that the application trusts and reflects user input without sanitization, making it trivial to execute malicious code in victim browsers.

## Defensive takeaways
- Implement strict input validation on all form fields (whitelist allowed characters and formats)
- Apply proper output encoding/escaping based on context (HTML entity encoding for HTML context, JavaScript escaping for script context)
- Deploy a Content Security Policy (CSP) with strict directives to prevent inline script execution
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Implement server-side validation and never trust client-side validation alone
- Use templating engines that auto-escape output by default
- Conduct security code reviews focusing on all user input handling paths

## Variant hunting
Test all other form fields on the same page for reflected XSS
Check if the vulnerability exists in form submission confirmation pages
Test for DOM-based XSS if JavaScript dynamically processes form data
Investigate other request/quote forms on different Acronis country domains (de, uk, com, etc.)
Check for stored XSS if form data is saved to database and displayed elsewhere
Test for Mutation XSS (mXSS) with polyglot payloads
Verify if the vulnerability affects API endpoints accepting form data

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
This is a textbook reflected XSS vulnerability with straightforward exploitation. The form likely echoes user input directly without sanitization. The severity is High rather than Critical because it requires user interaction and affects individual sessions rather than the application infrastructure. The bounty amount was not disclosed in the report.

## Full report
<details><summary>Expand</summary>

Summary
You can post javascript and html code in form fields

steps :
1-go to vulnerability link : https://www.acronis.cz/poptavka-acronis/
2- enter this javascript code "><script>alert(1);</script> in form field for xss and enter <a+href="https://bing.com">Test</a> for html injection.

## Impact

Impact
1- Cookie stealing
2- Pishing attacks
3- URL redirection

</details>

---
*Analysed by Claude on 2026-05-12*
