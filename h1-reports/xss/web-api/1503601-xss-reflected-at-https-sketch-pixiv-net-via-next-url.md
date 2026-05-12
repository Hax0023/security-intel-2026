# Reflected XSS via next_url Parameter on sketch.pixiv.net

## Metadata
- **Source:** HackerOne
- **Report:** 1503601 | https://hackerone.com/reports/1503601
- **Submitted:** 2022-03-08
- **Reporter:** find_me_here
- **Program:** Pixiv
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (Reflected), Improper Input Validation, Unsafe URL Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the resign_request/success endpoint where the next_url parameter is not properly sanitized before being used in the page. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser context when visited.

## Attack scenario
1. Attacker identifies the resign_request/success endpoint accepts a next_url parameter
2. Attacker crafts a malicious URL with JavaScript payload: javascript:alert/**/(document.domain)
3. Attacker tricks victim into clicking the link or visits it themselves (social engineering, phishing)
4. Victim's browser processes the JavaScript protocol handler in the next_url parameter
5. Arbitrary JavaScript executes in victim's browser with full application privileges
6. Attacker can steal session cookies, perform unauthorized actions, or redirect to phishing page

## Root cause
The next_url parameter is reflected in the page output without proper URL validation, encoding, or sanitization. The application fails to validate that the URL is a safe relative or whitelisted domain before rendering it.

## Attacker mindset
Looking for low-hanging fruit in URL parameters used for redirection or navigation, particularly in authentication flows where users may be less suspicious of unusual URLs. The use of JavaScript protocol handlers bypasses basic URL parsing checks.

## Defensive takeaways
- Implement strict URL validation - whitelist allowed redirect domains rather than blacklisting
- Validate that next_url is a relative path or matches allowed domains before use
- Use URL parsing libraries to detect and reject javascript:, data:, and other dangerous protocols
- Encode all user-controlled data before outputting to HTML/JavaScript context
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Sanitize and validate all parameters, especially those used in redirects

## Variant hunting
Check other endpoints with redirect/next_url parameters (login, logout, callback URLs)
Test for DOM-based XSS variants using different protocol handlers (vbscript:, data:, etc.)
Look for similar vulnerable parameters: redirect_uri, return_url, goto, continue, back, ref
Test URL encoding bypasses and double-encoding techniques
Check for blind XSS via event handlers in URL fragments

## MITRE ATT&CK
- T1190
- T1566
- T1204

## Notes
Report appears minimal in detail and analysis. The vulnerability is straightforward reflected XSS via improper URL parameter handling. The javascript: protocol bypasses naive URL validation. This is a common vulnerability type in web applications, especially in authentication/session management flows. The payload uses comment syntax (/**/) to bypass certain filters but the core issue is lack of validation.

## Full report
<details><summary>Expand</summary>

Hi,

I Found XSS Reflected at https://sketch.pixiv.net/ Via Success URL

##Follow Me :)

##Steps :
1. Open the URL below:
https://sketch.pixiv.net/resign_request/success?next_url=javascript%3Aalert%2F**%2F(document.domain)

2. Pop ups appear :)

## Impact

If an attacker can control a script that is executed in the victim's browser, then they can typically fully compromise that user. Amongst other things, the attacker can: Perform any action within the application that the user can perform

</details>

---
*Analysed by Claude on 2026-05-12*
