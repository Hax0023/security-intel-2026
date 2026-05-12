# Reflected XSS in gratipay.com npm package handler

## Metadata
- **Source:** HackerOne
- **Report:** 262852 | https://hackerone.com/reports/262852
- **Submitted:** 2017-08-24
- **Reporter:** tungpun
- **Program:** Gratipay
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in gratipay.com's npm package handling endpoint that fails to properly sanitize user-supplied input in the URL path. An attacker can inject arbitrary HTML/JavaScript code that executes in the victim's browser when they visit a crafted malicious link.

## Attack scenario
1. Attacker identifies that gratipay.com processes npm package names from the URL path parameter (/on/npm/{package_name})
2. Attacker discovers that input validation is insufficient and HTML/JavaScript can be injected via null bytes and SVG tags
3. Attacker crafts a malicious URL: https://gratipay.com/on/npm/cx%00A<svg onload=alert(1)>
4. Attacker distributes the link via social engineering, forums, or email to target users
5. Victim clicks the link and the injected JavaScript executes in their browser context
6. Attacker can steal session cookies, perform actions on behalf of the user, or redirect to phishing pages

## Root cause
The application fails to properly validate and encode user input from the npm package name parameter before reflecting it in the HTTP response. The null byte injection (%00) and unescaped SVG/JavaScript tags bypass client-side or inadequate server-side filtering mechanisms.

## Attacker mindset
An attacker would recognize that user-controlled input in URL paths is often reflected without proper sanitization, especially in routing parameters. The use of null bytes as a bypass technique suggests testing against common WAF/filter patterns. The simplicity of the payload indicates basic XSS testing methodology.

## Defensive takeaways
- Implement strict input validation on all URL parameters, rejecting null bytes and special characters not expected in package names
- Use proper output encoding/escaping (HTML entity encoding) for all user-supplied data reflected in responses
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Implement server-side input whitelisting for package names (alphanumeric, hyphens, underscores only)
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Conduct regular security testing and code review for reflection vulnerabilities
- Consider using a templating engine with automatic escaping enabled by default

## Variant hunting
Test other /on/* endpoints (e.g., /on/github/, /on/twitter/) for similar reflection patterns
Try alternative null byte representations (%00, \x00, \u0000)
Test with other SVG event handlers: onmouseover, onerror, onload variants
Attempt polyglot payloads combining different encoding schemes
Check for stored XSS if user input gets persisted in any way
Test content-type sniffing possibilities in response headers

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing

## Notes
This is a straightforward reflected XSS with a simple PoC. The use of null bytes suggests either testing against filters or potential parser confusion. The vulnerability affects any user who can be tricked into clicking a malicious link. No authentication is required to exploit this vulnerability, increasing its risk surface.

## Full report
<details><summary>Expand</summary>

# Summary

I would like to report a Reflected XSS on gratipay.com.

# Browsers Verified In

  * Firefox 55.0.2 (up to date)

# Steps To Reproduce

  Goto this URL:
`https://gratipay.com/on/npm/cx%00A<svg onload=alert(1)>`

{F215426}

</details>

---
*Analysed by Claude on 2026-05-12*
