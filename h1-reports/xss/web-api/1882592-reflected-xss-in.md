# Reflected XSS in National Levee Database Logout Page

## Metadata
- **Source:** HackerOne
- **Report:** 1882592 | https://hackerone.com/reports/1882592
- **Submitted:** 2023-02-22
- **Reporter:** 0xd3adc0de
- **Program:** Department of Defense (DoD) Bug Bounty
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the auth/logout.jsx endpoint where the 'home' GET parameter is not properly sanitized or validated before being used in a redirect or display context. An attacker can inject arbitrary JavaScript code that executes when a user clicks a link in the logout page, potentially compromising user sessions and credentials.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'home' parameter and embeds it in a phishing email or malicious website
2. Victim visits the crafted URL while authenticated to the application
3. The vulnerable logout.jsx page receives the 'home' parameter without sanitization
4. When victim clicks the 'Click here to return to your application' link, the JavaScript payload executes in their browser context
5. Attacker's JavaScript can steal session cookies, capture credentials, or perform actions on behalf of the user
6. Attacker gains unauthorized access to victim's account or sensitive DoD database information

## Root cause
The 'home' parameter is directly used in a redirect or link context without proper output encoding, URL validation, or content security policy enforcement. The application fails to validate that the parameter contains only safe URLs (whitelist approach) or properly encode the output.

## Attacker mindset
An attacker targeting government infrastructure would exploit this to gain unauthorized access to the national levee database, potentially for espionage, sabotage, or data exfiltration. The logout page is an attractive target because users may be less vigilant during logout and the parameter suggests redirect functionality.

## Defensive takeaways
- Implement strict URL validation - use a whitelist of allowed redirect domains or enforce relative URLs only
- Apply proper output encoding (HTML entity encoding) to all user-supplied parameters before rendering in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Implement parameterized redirection using safe library functions that validate URLs
- Add input validation to reject javascript: protocol and data: URIs
- Apply defense in depth with HTTPOnly and Secure flags on session cookies
- Conduct security code review of all authentication-related endpoints
- Implement automated security testing (SAST/DAST) in CI/CD pipeline

## Variant hunting
Check other authentication endpoints (login.jsx, register.jsx) for similar parameter-based XSS
Search for other redirect/return parameters ('redirect', 'next', 'returnUrl', 'back')
Test POST request variants of the same endpoint
Check for DOM-based XSS in client-side handling of the 'home' parameter
Look for stored XSS if the 'home' parameter is persisted anywhere
Test other subdomains on the same domain for identical vulnerable patterns

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1176

## Notes
This is a critical finding in government infrastructure. The national levee database is CISA-relevant critical infrastructure. Report indicates DoD scope suggesting high-value target. The vulnerability is trivial to exploit but has significant impact on sensitive systems. Report lacks specific remediation suggestions and appears incomplete (multiple redacted sections). No CVE assigned at time of report.

## Full report
<details><summary>Expand</summary>

**Description:**
XSS vulnerability found on one of `███████` subdomains. [ DoD scope]

After analyzing `https://████████████/` (national levee database) I found  `auth/logout.jsx` page that have `home` parameter in `GET` request.  `home` parameter vulnerable to XSS vulnerability.


Payload:
`https://█████████████████/auth/logout.jsx?home=javascript:(alert(%27XSS%20Success!%27))()`
████████


## References
https://owasp.org/www-community/attacks/xss/

## Impact

By exploiting this vulnerability an attacker can trick the users to execute XSS and steal user's cookies.
Launch advanced phishing attacks.
Execute browser-based attacks etc.

## System Host(s)
███████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
* Visit the following URL 
`https://████████████████/auth/logout.jsx?home=javascript:(alert(%27XSS%20Success!%27))()`

* click on `Click here to return to your application.`  and you will receive `XSS Success!` alert box.

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-12*
