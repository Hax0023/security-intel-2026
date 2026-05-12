# Reflected XSS in WebPuff5.4 Login Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 1390131 | https://hackerone.com/reports/1390131
- **Submitted:** 2021-11-02
- **Reporter:** f6x
- **Program:** Unknown (Redacted)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the WebPuff5.4 Login endpoint where the 'url' parameter is not properly sanitized or encoded, allowing arbitrary JavaScript execution. An attacker can craft a malicious URL containing script tags that execute in the victim's browser when the login page is visited.

## Attack scenario
1. Attacker discovers the 'url' parameter in the login page is vulnerable to XSS injection
2. Attacker crafts a malicious URL with JavaScript payload encoded in the url parameter (e.g., <script>alert(9868)</script>)
3. Attacker sends the crafted URL to victims via phishing email, social media, or other social engineering vectors
4. Victim clicks the link and visits the malicious URL on the legitimate domain
5. The injected JavaScript executes in the victim's browser context with access to cookies, session tokens, and sensitive data
6. Attacker can steal authentication credentials, redirect to fake login pages, or deploy malware

## Root cause
The 'url' parameter in the Login endpoint is reflected directly into the HTML response without proper sanitization or HTML entity encoding. The application fails to validate the parameter format and does not encode special characters that have meaning in HTML/JavaScript context.

## Attacker mindset
An opportunistic attacker discovered an unprotected parameter during reconnaissance of a newly identified IP address. They tested basic XSS payloads and found the application naively reflects user input without sanitization, enabling straightforward exploitation for credential theft or malware distribution.

## Defensive takeaways
- Implement strict input validation - whitelist allowed characters and URL formats for the 'url' parameter
- Apply context-appropriate output encoding (HTML entity encoding) for all user-controlled data reflected in HTML
- Use a security-focused template engine or framework that auto-escapes by default
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Perform security code review of all parameter handling in authentication-related endpoints
- Use parameterized/safe redirect functions instead of reflecting user input in redirect logic
- Conduct regular penetration testing focusing on parameter injection vulnerabilities

## Variant hunting
Test all parameters in the Login endpoint (username, password, signIn) for similar XSS weaknesses
Check other URL parameters or hidden fields that might reflect user input
Test different XSS payload variations (event handlers, SVG-based XSS, DOM-based XSS)
Investigate if the vulnerability exists in other endpoints or pages in WebPuff5.4
Check if the application filters certain characters - attempt bypass using encoding (URL encoding, Unicode, double encoding)
Test for stored XSS if user input is persisted in any form
Examine the URL redirect functionality for open redirect vulnerabilities

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002
- T1566.001
- T1204.001

## Notes
This is a straightforward reflected XSS vulnerability with clear proof-of-concept. The report lacks detail about the affected organization and remediation timeline. The attacker used URL encoding and case variation (ScRiPt) to obfuscate the payload, suggesting some basic evasion awareness. The 'url' parameter appears to be intended for post-login redirects, making this a common architectural flaw where redirect URLs are not properly validated.

## Full report
<details><summary>Expand</summary>

**Description:**
Hi i found a XSS at a new IP Address (ssl points to ███hostname)


https://███████/WebPuff5.4/Login?signIn=Sign%20In&password=g00dPa%24%24w0rD&url=login.jsp%27%22()%26%25%3Cacx%3E%3CScRiPt%20%3Ealert(9868)%3C/ScRiPt%3E&username=tMtFQiRt

## References
https://owasp.org/www-community/attacks/xss/

## Impact

With the help of xss a hacker or attacker can perform social engineering on users by redirecting them from real website to fake one. hacker can steal their cookies and download a malware on their system, and there are many more attacking scenarios a skilled attacker can perform with xss.

## System Host(s)
███████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
click here and a alert will popup https://█████/WebPuff5.4/Login?signIn=Sign%20In&password=g00dPa%24%24w0rD&url=login.jsp%27%22()%26%25%3Cacx%3E%3CScRiPt%20%3Ealert(9868)%3C/ScRiPt%3E&username=tMtFQiRt

## Suggested Mitigation/Remediation Actions
Sanitize special character in the url



</details>

---
*Analysed by Claude on 2026-05-12*
