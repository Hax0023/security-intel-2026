# Reflected XSS in Oberlo Authentication Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 569241 | https://hackerone.com/reports/569241
- **Submitted:** 2019-05-06
- **Reporter:** 0xprial
- **Program:** Oberlo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Input Validation Failure, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered in the authentication endpoint (app.oberlo.com/auth) where the 'shop' parameter is not properly sanitized or encoded before being rendered in the DOM. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser within the authentication context, potentially compromising sensitive session tokens and user data.

## Attack scenario
1. Attacker crafts a malicious URL with XSS payload in the shop parameter: https://app.oberlo.com/auth?shop=</noscript><img src=x onerror=prompt(document.domain)>
2. Attacker distributes the malicious link via phishing email, social engineering, or forum posts targeting Oberlo users
3. Victim clicks the link while authenticated or during the authentication process
4. The payload executes in the victim's browser within the app.oberlo.com domain context
5. Attacker's JavaScript can access sensitive data like authentication tokens, session cookies, or perform actions on behalf of the user
6. Attacker exfiltrates credentials or performs unauthorized actions in the user's account

## Root cause
The 'shop' parameter in the authentication endpoint is reflected directly into the HTML response without proper input validation, HTML entity encoding, or Content Security Policy (CSP) protection. The application fails to sanitize user-controlled input before rendering it in the DOM.

## Attacker mindset
An attacker would recognize that the authentication endpoint is a high-value target since it processes user credentials and session data. By injecting XSS into the auth flow, they can intercept authentication tokens or session cookies at a critical point when users are logging in, maximizing the likelihood of successful credential theft.

## Defensive takeaways
- Implement strict input validation and whitelist allowed characters for all user-supplied parameters
- Apply HTML entity encoding/escaping to all user-controlled data before rendering in HTML context
- Deploy a strong Content Security Policy (CSP) header to prevent inline script execution
- Use templating engines with auto-escaping enabled by default
- Implement HTTPOnly and Secure flags on session cookies to prevent XSS-based theft
- Conduct security testing and code review specifically targeting authentication endpoints
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Implement output encoding context-aware to the location where data is rendered (HTML, JavaScript, URL, CSS)

## Variant hunting
Test other parameters in the auth endpoint for XSS vulnerabilities (redirect, return_url, state, etc.)
Try stored XSS variants by testing if the shop parameter is stored in user profiles or databases
Test for DOM-based XSS in JavaScript code that processes URL parameters
Attempt to bypass filters using encoding variations (double encoding, Unicode, HTML5 entities)
Test other Oberlo endpoints (/login, /register, /callback) for similar parameter injection
Look for CSRF protection bypass combined with XSS for account takeover
Test if the vulnerability persists when parameters are URL-encoded or in different formats

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1040
- T1056.004

## Notes
This is a straightforward reflected XSS with clear proof-of-concept. The vulnerability is in a critical authentication context, escalating risk significantly. The report lacks details on bounty amount and full remediation timeline. Best practice: use parameterized rendering with framework-level protections rather than manual encoding.

## Full report
<details><summary>Expand</summary>

Hi team ,
I found a reflected xss on https://app.oberlo.com domain .

##Reproduce :
* Visit **https://app.oberlo.com/auth?shop=%3C/noscript%3E%3Cimg%20src=x%20onerror=prompt(document.domain)%3E** in latest version of firefox browser .
* You will see popup like attacked screenshot : {F485407}

**Tested in Latest version of firefox**

## Impact

As this is a **auth** so this xss can lead to some serious issues like stealing users **auth** token or stealing browser data/cookies .

Best Regards
**Prial**

</details>

---
*Analysed by Claude on 2026-05-12*
