# Reflected XSS in OWOX BI Dashboard via URL Path Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 732987 | https://hackerone.com/reports/732987
- **Submitted:** 2019-11-09
- **Reporter:** imthehackerlor
- **Program:** OWOX
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the OWOX BI dashboard where user-supplied input in the URL path (project ID parameter) is not properly sanitized or encoded before being reflected in the page output. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser after login, allowing arbitrary code execution.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload embedded in the project ID parameter (e.g., 6177527534dc114eb07fa829e4ce4d28%3Cimg%20src=xss%20onerror=prompt('XSS')%3E)
2. Attacker distributes the URL to victims via phishing email, chat, social media, or other social engineering channels
3. Victim clicks the link and visits the OWOX BI dashboard page
4. Victim logs into their OWOX account (XSS requires authentication context)
5. Browser renders the page with the unencoded payload in the DOM, triggering the onerror event handler
6. JavaScript code executes in the victim's browser context, potentially stealing session cookies, credentials, or performing unauthorized actions

## Root cause
The application fails to properly validate, sanitize, and HTML-encode user input from the URL path parameter before reflecting it back in the HTTP response. The project ID parameter is directly incorporated into the page without server-side validation or output encoding mechanisms.

## Attacker mindset
An attacker could exploit this to steal authenticated user sessions, redirect users to phishing pages, modify page content to trick users into revealing sensitive information, or perform unauthorized administrative actions on behalf of the victim within the OWOX application.

## Defensive takeaways
- Implement strict input validation on the server side to ensure the project ID matches expected format (alphanumeric, specific length)
- Apply HTML entity encoding to all user-controlled data before reflecting it in HTML context
- Use a Content Security Policy (CSP) header to restrict script execution and prevent inline script injection
- Implement HTTPOnly and Secure flags on session cookies to mitigate session hijacking
- Apply output encoding based on context (HTML encoding for HTML context, JavaScript encoding for JS context, URL encoding for URLs)
- Conduct a comprehensive security audit of all user input points across the application
- Implement automated security testing (SAST/DAST) in the development pipeline to catch XSS vulnerabilities early
- Use security frameworks and libraries that provide built-in XSS protection mechanisms

## Variant hunting
Look for similar URL path parameters in other endpoints (e.g., /ui/{id}/reports, /ui/{id}/settings); Test other URL segments that might accept user input without validation; Examine query parameters for the same vulnerability; Check if the vulnerability exists in other authentication states or user roles; Test for stored XSS variants where the project ID might be persisted in a database

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002
- T1539

## Notes
The vulnerability requires authentication, which slightly reduces risk compared to unauthenticated XSS but still poses significant threat as attackers can target specific user groups. The PoC uses img tag with onerror handler, but other XSS vectors could work (script tags, svg, iframe, etc.). The vulnerability impacts all users regardless of project access level, making it broadly exploitable within the OWOX user base.

## Full report
<details><summary>Expand</summary>

Hi team,

I have found an XSS at https://bi.owox.com/ui/6177527534dc114eb07fa829e4ce4d28/dashboard/?trial=activated
Because the input is not properly filtered, resulting in XSS being executed
Vulnerable area: 
-----
``6177527534dc114eb07fa829e4ce4d28``
The URL will now be: https://bi.owox.com/ui/6177527534dc114eb07fa829e4ce4d28%3Cimg%20src=xss%20onerror=prompt('XSS')%3E/dashboard/?trial=activated

PoC
---
1, go to https://bi.owox.com/ui/6177527534dc114eb07fa829e4ce4d28%3Cimg%20src=xss%20onerror=prompt('XSS')%3E/dashboard/?trial=activated
2, Log in and ``XSS`` will execute
██████████

Tested browser
---
Firefox 
Chrome

## Impact

This vulnerability is aimed at all victims and they do not need to be involved in the ``Project``. Just paste this URL and login, XSS will automatically execute.
Therefore, it will have a ``high impact``, because before XSS is executed, the application will ask the user to login.
+ The attacker can execute JS code.
████████
████████

Documents related to ``Impact``
---
https://portswigger.net/web-security/cross-site-scripting/reflected
https://portswigger.net/web-security/cross-site-scripting/exploiting

Recommendation
----
+ Revisit the entire application and validate the user input at server side.
+ Sanitize the data collected from input fields before further processing.
+ Filter out special and meta-characters from user input.

Best regards,
@dat

</details>

---
*Analysed by Claude on 2026-05-12*
