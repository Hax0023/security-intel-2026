# Reflected XSS in twitterflightschool.com OAuth Callback Handler

## Metadata
- **Source:** HackerOne
- **Report:** 770349 | https://hackerone.com/reports/770349
- **Submitted:** 2020-01-08
- **Reporter:** jubabaghdad
- **Program:** Twitter Flight School
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
The Facebook OAuth callback endpoint at /authentication/fb_callback fails to properly sanitize the 'error_description' parameter, allowing attackers to inject arbitrary JavaScript code. An attacker can craft a malicious URL that executes arbitrary JavaScript in the victim's browser context, potentially stealing session cookies and performing actions on behalf of authenticated users.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the error_description parameter
2. Attacker distributes the URL via phishing email, social media, or compromised website
3. Victim clicks the link while authenticated to twitterflightschool.com
4. Victim's browser loads the callback page and renders unsanitized error_description content
5. JavaScript payload executes in victim's browser with access to cookies and session tokens
6. Attacker can steal session cookies, perform unauthorized actions, or redirect user to phishing page

## Root cause
The application reflects user-controlled input from the 'error_description' parameter into the HTML response without proper encoding or sanitization. The OAuth callback handler treats error parameters as trusted data and renders them directly in the page without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
An attacker would recognize OAuth callback handlers as common targets since they process parameters from external services and often have reduced validation. The error_description parameter is particularly attractive as developers may assume it originates from trusted OAuth providers. By crafting a phishing URL, the attacker can leverage user trust in the legitimate domain to execute malicious code.

## Defensive takeaways
- Implement strict output encoding for all user-controlled data using context-appropriate encoding (HTML entity encoding for HTML context)
- Apply input validation to reject or sanitize unexpected characters in OAuth callback parameters
- Implement Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Use templating engines with auto-escaping enabled by default
- Validate that error parameters conform to expected formats (whitelist approach)
- Consider using security-focused libraries for OAuth handling rather than custom implementations
- Implement X-XSS-Protection and X-Content-Type-Options headers as defense-in-depth
- Conduct regular security testing of authentication flow endpoints

## Variant hunting
Test other OAuth callback endpoints (/authentication/google_callback, /authentication/github_callback, etc.) for similar issues
Examine all error/warning/info parameters in callback handlers (error, error_code, error_description, state, etc.)
Check if other authentication flows (password reset, email verification) have similar unvalidated parameter reflection
Test for DOM-based XSS in JavaScript that processes callback parameters
Search for similar patterns in other endpoints that handle redirects or return URLs
Fuzz OAuth parameters with various encoding schemes (double encoding, Unicode, UTF-7) to bypass filters

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1005 - Data from Local System
- T1185 - Browser Session Hijacking

## Notes
This is a classic reflected XSS vulnerability in an authentication-critical endpoint. OAuth callback handlers are particularly sensitive as they process post-authentication requests. The vulnerability is easily exploitable and requires no user interaction beyond clicking a link. The use of img tag with onerror handler is a reliable payload that bypasses basic filters. Session hijacking via cookie theft is possible if HttpOnly flag is not set on session cookies.

## Full report
<details><summary>Expand</summary>

While testing twitterflightschool.com, I came across the below endpoint:

https://twitterflightschool.com/authentication/fb_callback?error=access_denied&error_code=200&error_description=

I noticed that it is possible to inject JS payload in "error_description=" parameter and trigger XSS in twitterflightschool.com


Reproduction Steps:
==============

Here we go
https://twitterflightschool.com/authentication/fb_callback?error=access_denied&error_code=200&error_description=%22%3E%3Cimg+src%3Dx+onerror%3Dprompt%28document.domain%29%3E

https://twitterflightschool.com/authentication/fb_callback?error=access_denied&error_code=200&error_description=%22%3E%3Cimg+src%3Dx+onerror%3Dprompt%28document.cookie%29%3E

## Impact

This is will allow the attacker to steal users cookies

</details>

---
*Analysed by Claude on 2026-05-12*
