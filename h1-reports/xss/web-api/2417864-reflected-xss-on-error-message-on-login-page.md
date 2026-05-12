# Reflected XSS on Error Message on Login Page

## Metadata
- **Source:** HackerOne
- **Report:** 2417864 | https://hackerone.com/reports/2417864
- **Submitted:** 2024-03-15
- **Reporter:** kurogai
- **Program:** Unknown (Redacted)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on the login page where the 'error' query parameter is displayed without proper sanitization or encoding. An attacker can inject arbitrary JavaScript code that will execute in the victim's browser, potentially leading to session hijacking, credential theft, or account compromise.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'error' parameter
2. Attacker sends the link to target users via email, phishing, or social engineering
3. Victim clicks the link and arrives at the login page
4. The error parameter value is reflected unsanitized into the HTML response
5. Victim's browser parses and executes the injected JavaScript
6. Attacker's script steals session cookies, credentials, or redirects to phishing page

## Root cause
The application reflects user-supplied input from the 'error' query parameter directly into the HTML response without proper output encoding or HTML entity escaping, allowing arbitrary HTML/JavaScript injection.

## Attacker mindset
Low barrier to entry - easily discoverable via parameter fuzzing or manual testing. High impact on login pages where users are likely to interact with error messages. Can be leveraged for credential harvesting, session hijacking, or malware distribution with minimal effort.

## Defensive takeaways
- Implement output encoding for all user-controlled data reflected in HTML context using htmlspecialchars() or equivalent library functions
- Use a templating engine with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Validate and sanitize all query parameters server-side
- Apply input validation to reject or sanitize suspicious characters in error parameters
- Conduct security code review of all pages that display user input or query parameters
- Implement Web Application Firewall (WAF) rules to detect XSS patterns

## Variant hunting
Check other pages and parameters for similar unencoded reflections (success, message, callback, redirect, etc.)
Test other endpoints that display dynamic content from query parameters
Look for parameters in registration, password reset, or other authentication flows
Search for DOM-based XSS in JavaScript that processes query parameters
Examine error pages, 404 pages, and search functionality for reflection points

## MITRE ATT&CK
- T1190
- T1566.002
- T1598
- T1557.001

## Notes
This is a straightforward reflected XSS vulnerability on a critical authentication endpoint. The login page context makes this particularly dangerous as users expect to be on the legitimate site and may not notice injected content. The redaction of domain/program information suggests this may be from a private program. The suggested mitigation is correct but incomplete - context-aware output encoding should be paired with CSP and input validation for defense-in-depth.

## Full report
<details><summary>Expand</summary>

Greetings!

I've found a reflected XSS on a login page on█████ . The vulnerable link is: `https://███████/users/login?error=<img src='x' onerror="alert(document.domain)">`

█████████

## Impact

An attacker can inject crafted javascript that can steal user cookies, impersionate, steal information, deface the website and redirect user to another domain

## System Host(s)
██████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Access `https://██████/users/login?error=<img src='x' onerror="alert(document.domain)">`

## Suggested Mitigation/Remediation Actions
Sanitize the output with htmlspecialchars();



</details>

---
*Analysed by Claude on 2026-05-12*
