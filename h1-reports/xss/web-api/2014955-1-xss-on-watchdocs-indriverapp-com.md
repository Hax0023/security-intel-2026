# XSS on watchdocs.indriverapp.com via redirect parameter

## Metadata
- **Source:** HackerOne
- **Report:** 2014955 | https://hackerone.com/reports/2014955
- **Submitted:** 2023-06-06
- **Reporter:** maxdha
- **Program:** inDriver
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS, Improper Input Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the /webview/v1/refresh-jwt endpoint where the 'redirect' parameter is not properly sanitized before being rendered in the page. An attacker can inject arbitrary JavaScript code via a malicious URL that will execute in the victim's browser when visited.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the redirect parameter
2. Attacker sends the link to victim via phishing email, social engineering, or advertisement
3. Victim clicks the link and visits watchdocs.indriverapp.com/webview/v1/refresh-jwt?redirect=%22%3E%3Cimg%20src=faw%20onerror=alert(1)%3E
4. The redirect parameter value is reflected unsanitized into the page HTML
5. Browser parses the injected img tag and executes the onerror handler JavaScript
6. Attacker's malicious JavaScript executes with victim's privileges (session cookies, local storage, credentials)

## Root cause
The application fails to properly encode or validate the 'redirect' parameter before including it in the page output. The parameter is directly concatenated into HTML without context-aware escaping, allowing breaking out of attributes or tags.

## Attacker mindset
An attacker would recognize this endpoint as handling redirects post-authentication and see an opportunity to steal session tokens, credentials, or perform account takeover by injecting a payload that exfiltrates sensitive data or performs actions on behalf of the authenticated user.

## Defensive takeaways
- Implement strict input validation on all URL parameters, especially those used in redirects
- Apply context-aware output encoding (HTML entity encoding for HTML context)
- Use Content Security Policy (CSP) headers to restrict inline script execution
- Validate redirect URLs against a whitelist of allowed domains
- Use security-focused templating engines that auto-escape by default
- Implement HTTPOnly and Secure flags on session cookies to limit XSS impact
- Perform security code review of all redirect/URL handling logic

## Variant hunting
Test other endpoint parameters for similar XSS patterns (state, callback, return_to, etc.)
Check for DOM-based XSS variants where redirect parameter is processed via JavaScript
Test different encoding schemes to bypass basic filters (Unicode, double encoding, etc.)
Search for similar patterns in other indriver.com subdomains
Test alternative payload vectors (svg, iframe, script tags) for context-specific bypasses

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1185

## Notes
This is a straightforward reflected XSS with high impact on a subdomain handling authentication flows. The vulnerability is easily exploitable and requires minimal user interaction. The watchdocs endpoint appears to handle JWT refresh operations, making this particularly dangerous for account compromise.

## Full report
<details><summary>Expand</summary>

## Summary:
XSS on watchdocs.indriverapp.com

## Steps To Reproduce:

  1. Go to https://watchdocs.indriverapp.com/webview/v1/refresh-jwt?redirect=%22%3E%3Cimg%20src=faw%20onerror=alert(1)%3E
  2. An alert window will popup
  




{F2401964}

## Impact

Allow executing js code on users browsers

</details>

---
*Analysed by Claude on 2026-05-12*
