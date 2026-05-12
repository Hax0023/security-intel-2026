# Reflected XSS in media.indrive.com Login Response Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2503113 | https://hackerone.com/reports/2503113
- **Submitted:** 2024-05-13
- **Reporter:** zxwo
- **Program:** InDrive
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the login response endpoint of media.indrive.com where user-supplied input is echoed back without proper sanitization or encoding. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when visited, potentially leading to session hijacking, credential theft, or other malicious actions.

## Attack scenario
1. Attacker crafts a malicious URL: https://media.indrive.com/login/response/<XSS_PAYLOAD>
2. Attacker sends the URL to a target user via phishing email, social media, or other communication channels
3. Victim clicks the link and the browser loads the InDrive login page with the injected JavaScript payload
4. JavaScript executes in the victim's browser context with access to session cookies and sensitive data
5. Malicious script steals authentication tokens, session cookies, or personal information from the page
6. Attacker gains unauthorized access to victim's account or performs actions on their behalf

## Root cause
The application fails to properly sanitize or encode user input from the response parameter before reflecting it back in the HTML response. The endpoint likely directly concatenates user input into the page without using appropriate output encoding mechanisms (HTML entity encoding, JavaScript encoding, or Content Security Policy).

## Attacker mindset
An attacker targeting this vulnerability would be motivated by account takeover, credential harvesting, or delivering malicious payloads to InDrive users. The low barrier to exploitation (simply crafting a URL) makes this an attractive target for mass campaigns. The attacker could target users in social engineering attacks or distribute the payload via advertisements.

## Defensive takeaways
- Implement strict input validation and whitelist acceptable characters for all user inputs
- Apply context-appropriate output encoding: HTML entity encoding for HTML context, JavaScript encoding for JavaScript context
- Use security libraries and frameworks that provide automatic output encoding capabilities
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Validate and sanitize all data on the server-side, never rely on client-side validation alone
- Use HTTPOnly and Secure flags on session cookies to limit XSS impact
- Conduct regular security testing including automated scanning and manual penetration testing for XSS vulnerabilities
- Implement a Web Application Firewall (WAF) to detect and block common XSS patterns
- Use security headers (X-XSS-Protection, X-Content-Type-Options) as defense-in-depth measures

## Variant hunting
Test other endpoints with response/callback/redirect parameters for similar XSS patterns
Check login, logout, and authentication flow endpoints for reflected XSS vulnerabilities
Examine error handling pages and status message displays for unencoded reflections
Test other InDrive subdomains (app.indrive.com, api.indrive.com, etc.) for similar vulnerabilities
Look for DOM-based XSS in JavaScript that processes URL parameters
Test file upload functionality for stored XSS if responses display user filenames
Check search functionality and filter parameters for reflected XSS
Examine API endpoints that return JSON/XML with user-controlled data

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1056.004
- T1539
- T1185

## Notes
The report lacks detail on the specific JavaScript payload used and doesn't provide clear reproduction steps. The impact section is generic boilerplate rather than specific to this vulnerability instance. The vulnerability is in an authentication-related endpoint, making it particularly dangerous as it could compromise user accounts. The simplicity of the attack vector (no authentication required, just visiting a URL) makes this a critical finding. The reporter appropriately redacted sensitive information but should have provided more technical detail about the vulnerability itself.

## Full report
<details><summary>Expand</summary>

hi,
I find a rxss of media.indrive.com
just view:
```
https://media.indrive.com/login/response/██████
```
will execute javascript.
████

## Impact

1.Stealing user accounts: Malicious users can use XSS code to obtain various user accounts, including email accounts, social media accounts, etc. Stealing user cookie information: XSS attacks can steal the cookie information stored by the user in the browser, thereby posing as the user identity to enter the website.
2.Hijacking the user session: Attackers can use XSS code to hijack the user's browser session and perform arbitrary operations, such as making illegal transfers, forced publishing logs, sending emails, etc. Spreading worms and viruses: XSS attacks can inject malicious code to make the user's browser perform malicious operations, and even spread worms and viruses.
3.Forced pop-up advertising pages: Malicious users can use XSS code to forcefully pop up advertising pages, thereby gaining traffic or performing other malicious operations.
4.Altering page information: XSS attacks can arbitrarily alter page information, including deleting articles. Obtaining client information: XSS attacks can obtain client information, such as the user's browsing history, real IP, open ports, etc. Controlling the victim's machine to attack other websites: Malicious users can use XSS code to control the victim's machine and then launch attacks on other websites. Elevating user permissions: XSS attacks can use other vulnerabilities to expand attacks and even elevate user permissions, including further penetrating the website.

</details>

---
*Analysed by Claude on 2026-05-12*
