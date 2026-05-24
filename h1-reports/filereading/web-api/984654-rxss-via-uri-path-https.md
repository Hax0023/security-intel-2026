# Reflected XSS Via URI Path Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 984654 | https://hackerone.com/reports/984654
- **Submitted:** 2020-09-17
- **Reporter:** 0xelkomy
- **Program:** Undisclosed
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the Orders endpoint where user-supplied input in the URI path is reflected back to the user without proper encoding or validation. An attacker can craft a malicious URL containing JavaScript payloads that execute in the victim's browser when the link is visited.

## Attack scenario
1. Attacker identifies that the /Orders/(input)/Login.aspx endpoint reflects user input from the URI path parameter
2. Attacker crafts a malicious URL with a JavaScript payload encoded in the path: https://target/Orders/(A(%22onerror='alert`xElkomy`'testabcd))/Login.aspx?ReturnUrl=/Orders
3. Attacker distributes the malicious link via email, social engineering, or injects it into web pages
4. Victim clicks the link or is redirected to it, causing the application to reflect the unencoded payload
5. JavaScript executes in the victim's browser with the victim's session context and privileges
6. Attacker can steal session tokens, perform actions on behalf of the user, inject malware, or redirect to phishing pages

## Root cause
The application fails to properly encode user input sourced from the URI path before reflecting it in the HTTP response. The path parameter is processed and output without HTML entity encoding or sanitization, allowing special characters and script tags to be interpreted by the browser.

## Attacker mindset
The researcher demonstrates a typical RXSS hunting approach: identifying dynamic parameters in URLs, testing special characters and quote escaping, and attempting payload injection. The mention of ad-jacking, session hijacking, and crypto mining shows understanding of practical XSS exploitation chains and monetization.

## Defensive takeaways
- Implement context-aware output encoding: HTML encode all user-supplied data before rendering in HTML context
- Apply strict input validation: whitelist acceptable characters and reject or sanitize path parameters containing quotes, brackets, or special characters
- Deploy Content Security Policy (CSP) headers with strict directives to prevent inline script execution and limit script sources
- Use HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Implement a Web Application Firewall (WAF) to detect and block common XSS payloads in URI parameters
- Conduct security code review of all endpoints that process and reflect user input, particularly URI path parameters
- Use templating engines with automatic escaping enabled
- Perform regular penetration testing focusing on parameter reflection vulnerabilities

## Variant hunting
Similar vulnerabilities likely exist in other endpoints accepting path parameters (e.g., /Products/, /Users/, /Accounts/). Test all dynamic URI segments for reflection. Check for bypasses using encoding variations (double encoding, Unicode, HTML entities), alternative event handlers, and tag variations. Investigate whether the ReturnUrl parameter is also vulnerable or exploitable in conjunction with the path parameter.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1056 - Input Capture
- T1557 - Adversary-in-the-Middle

## Notes
The report demonstrates basic XSS vulnerability discovery but lacks depth in technical analysis. The claimed impacts (ad-jacking, session hijacking, crypto mining) would require additional chaining with other vulnerabilities or misconfigurations. The suggested fixes are accurate but generic. The report does not include proof of concept screenshots or detailed technical breakdown, which would strengthen the submission. The vulnerability appears to be in legacy ASP.NET code based on the .aspx extension and path-based routing pattern.

## Full report
<details><summary>Expand</summary>

>Hello All I Found RXSS in your OWN Website

##Steps To Reproduce
Go to This Link
``https://██████/Orders/(A(%22onerror='alert%60xElkomy%60'testabcd))/Login.aspx?ReturnUrl=/Orders``

##Browsers
I test them on Firefox and Google Chrome.

##Fix:-
Filter input on arrival
Encode data on output
Use appropriate response headers
Content Security Policy.

Regards, xElkomy

## Impact

View any information that the user is able to view. Modify any information that the user is able to modify. Initiate interactions with other application users, including malicious attacks, that will appear to originate from the initial victim user. || And I can used this for
1-Ad-Jacking
2-Session Hijacking
3-Bypassing CSRF protection
4-Crypto Mining ::::)))

</details>

---
*Analysed by Claude on 2026-05-24*
