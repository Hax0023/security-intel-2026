# Reflected XSS in WordPress.com Account Setup via redirect_to Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2055132 | https://hackerone.com/reports/2055132
- **Submitted:** 2023-07-07
- **Reporter:** secureighty
- **Program:** WordPress.com (Automattic)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the WordPress.com account setup flow at /start/account/user endpoint where the redirect_to parameter is not properly sanitized. An authenticated attacker can inject arbitrary JavaScript code via a crafted URL that executes in the victim's browser context when they click continue.

## Attack scenario
1. Attacker crafts malicious URL with javascript: protocol in redirect_to parameter: https://wordpress.com/start/account/user?variationName=free&redirect_to=javascript:alert(document.domain)
2. Attacker sends this URL to authenticated WordPress.com users via phishing email or social engineering
3. Victim clicks the link while already logged into WordPress.com
4. Victim navigates to the malicious URL and clicks the 'continue' button
5. JavaScript payload executes in victim's browser with their session context and privileges
6. Attacker can steal authentication cookies, session tokens, or perform account takeover actions

## Root cause
Insufficient input validation and output encoding on the redirect_to parameter. The application likely constructs a redirect without properly validating the URL scheme or sanitizing the parameter value before rendering it in the HTML/JavaScript context.

## Attacker mindset
An attacker identified that the redirect_to parameter was being processed without proper validation of URL schemes. They recognized that by using the javascript: protocol instead of http/https, they could bypass standard redirect protections and inject executable code. The requirement for prior authentication suggests the attacker was testing privilege boundaries or seeking to escalate existing access.

## Defensive takeaways
- Implement strict URL validation for all redirect parameters - whitelist allowed URL schemes (http, https only)
- Use a URL parsing library to validate redirect targets against a whitelist of allowed domains
- Never trust user-supplied redirect parameters without explicit validation
- Apply proper output encoding when rendering redirect URLs in any context
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Use security headers like X-Content-Type-Options and X-Frame-Options
- Perform security testing of all parameter handling in authentication/authorization flows
- Consider using POST instead of GET for sensitive operations to prevent URL-based attacks

## Variant hunting
Test other parameters in the /start/account/user endpoint (variationName, etc.) for XSS
Check other WordPress.com endpoints with redirect_to or similar parameters (login, logout, signup flows)
Test data: protocol for potential file:// access in other contexts
Look for SVG/XML-based XSS vectors in redirect handling
Test double-encoding and encoding bypasses (e.g., %6a%61%76%61%73%63%72%69%70%74:)
Test other authentication flows and session-dependent endpoints for similar issues
Check if the vulnerability exists pre-authentication as well

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
This is a post-authentication XSS which reduces impact scope but still critical for account compromise. The javascript: protocol bypass suggests the redirect validation was overly simplistic. The researcher noted supporting materials were redacted (█████), likely containing proof-of-concept or additional technical details. The vulnerability chain involves both XSS and open redirect properties.

## Full report
<details><summary>Expand</summary>

## Summary:
xss after login at https://wordpress.com/start/account/user?variationName=free&redirect_to=javascript:alert(document.domain)

## Platform(s) Affected:
web

## Steps To Reproduce:

  1. auth normally
  1. go to https://wordpress.com/start/account/user?variationName=free&redirect_to=javascript:alert(document.domain) **while already authenticated** and click continue
  1. xss procs

## Supporting Material/References:

█████

## Impact

XSS can be used to steal cookies, modify html content, and much more

</details>

---
*Analysed by Claude on 2026-05-12*
