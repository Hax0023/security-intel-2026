# Potential XSS in redirect_url Parameter on learn.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 2653342 | https://hackerone.com/reports/2653342
- **Submitted:** 2024-08-12
- **Reporter:** kindone
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect
- **CVEs:** None
- **Category:** web-api

## Summary
An XSS vulnerability exists in the redirect_url parameter of https://learn.acronis.com/portal/licensing-check endpoint, allowing authenticated attackers to inject and execute arbitrary JavaScript code. By crafting a malicious redirect_url with javascript: protocol handlers, attackers can bypass client-side protections and execute code in the victim's browser context.

## Attack scenario
1. Attacker identifies the redirect_url parameter is processed without proper validation on the licensing-check endpoint
2. Attacker crafts a malicious URL: https://learn.acronis.com/portal/licensing-check?redirect_url=javascript:alert(document.domain)
3. Attacker tricks authenticated victim into clicking the malicious link via phishing or social engineering
4. Victim's browser loads the page and processes the redirect_url parameter
5. JavaScript payload executes in victim's authenticated session context with access to sensitive data
6. Attacker can steal session tokens, cookies, or perform unauthorized actions on behalf of victim

## Root cause
The redirect_url parameter is not validated or sanitized before being used in a redirect mechanism. The application fails to: (1) enforce same-origin policy for redirects, (2) block javascript: protocol handlers, (3) properly encode/escape user input, and (4) validate URL scheme and domain allowlist.

## Attacker mindset
An attacker recognizes that redirect parameters are commonly overlooked in security reviews and frequently suffer from insufficient validation. By leveraging an authenticated user's session, the attacker can execute code with elevated privileges, making this particularly valuable for credential theft or account takeover scenarios.

## Defensive takeaways
- Implement strict allowlist validation for redirect URLs - only permit same-origin redirects or predefined trusted domains
- Reject URLs with javascript:, data:, vbscript:, and other dangerous protocol handlers
- Use URL parsing libraries to validate scheme and domain components before redirecting
- Encode redirect URLs in response headers rather than embedding in HTML attributes
- Implement Content Security Policy (CSP) headers to mitigate XSS execution impact
- Conduct security code review of all redirect handling logic across the application
- Test redirect parameters as part of regular security testing and bug bounty processes
- Log and monitor suspicious redirect attempts for detection of active exploitation

## Variant hunting
Search for all redirect/forward parameters: redirect_url, returnUrl, return_to, next, target, goto, redirect, continue, url, referer, back
Test alternative protocol handlers: data:, vbscript:, file:, about:, blob:, and obfuscated variants
Try encoding bypasses: URL encoding (javascript%3a), double encoding, unicode escaping, mixed case (jAvAsCrIpT:)
Test on other Acronis subdomains and applications for similar vulnerable redirect patterns
Check if vulnerability persists after logout or in pre-authenticated flows
Attempt DOM-based XSS vectors if parameter is processed by client-side JavaScript
Test reflected XSS in other parameters that may feed into redirect logic

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1539 - Steal Web Session Cookie
- T1056 - Capture Credentials

## Notes
This vulnerability requires authentication but can be weaponized through phishing links targeting authenticated users. The use of javascript: protocol is a straightforward bypass of naive redirect validation. The researcher correctly identified this as a security issue; however, Acronis may argue whether this requires authentication as a limiting factor. The bug appears to be reported to HackerOne but no resolution status is indicated in the provided content.

## Full report
<details><summary>Expand</summary>

## Summary
An XSS vulnerability has been identified on https://learn.acronis.com/ in the redirect_url parameter. By manipulating the redirectUrl parameter, it is possible to inject arbitrary JavaScript code

## Steps To Reproduce
1) Log in to your https://learn.acronis.com/ account

2) Navigate to the following URL:
https://learn.acronis.com/portal/licensing-check?redirect_url=javascript:alert(document.domain)
 
3) Observe that an alert box displaying the current domain (document.domain) appears, indicating that the JavaScript code was executed.

{F3517115}

## Suggested Fix:
Validate and sanitize the redirectUrl parameter to ensure that it does not contain any malicious content. This can be done by:

  -  Restricting the parameter to only allow URLs that belong to the same origin.
  -  Encoding or escaping any user input before including it in the URL.

## Impact

An attacker can perform the following actions using this vulnerability:

   - Steal sensitive information, such as cookies, session tokens, or other sensitive data.
 -   Perform actions on behalf of the victim by exploiting their authenticated session.

</details>

---
*Analysed by Claude on 2026-05-12*
