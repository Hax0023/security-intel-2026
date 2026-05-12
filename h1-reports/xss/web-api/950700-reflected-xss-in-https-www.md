# Reflected XSS in Dynamic URL Parameter Handling

## Metadata
- **Source:** HackerOne
- **Report:** 950700 | https://hackerone.com/reports/950700
- **Submitted:** 2020-08-04
- **Reporter:** nirajgautamit
- **Program:** Undisclosed (HackerOne #950700)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in a dynamic URL parameter that fails to properly sanitize or encode user input before rendering it in the page context. An attacker can craft a malicious URL containing JavaScript code that executes in the victim's browser when the link is visited.

## Attack scenario
1. Attacker crafts a malicious URL with JavaScript payload in the URL parameter (e.g., onmouseover=alert event handler)
2. Attacker distributes the URL via phishing email, social media, or other social engineering techniques
3. Victim clicks the link and visits the affected page
4. Server reflects the unsanitized parameter directly into the HTML response without encoding
5. Victim's browser parses the malicious payload and executes the JavaScript in the context of the vulnerable domain
6. Attacker gains ability to steal session cookies, perform CSRF actions, redirect to phishing pages, or establish persistent backdoor access

## Root cause
The application fails to properly encode or sanitize user-supplied input from URL parameters before outputting it in the HTML response. The parameter containing the payload is reflected directly into the page without HTML entity encoding, allowing the browser to interpret the injected code as executable JavaScript.

## Attacker mindset
Opportunistic vulnerability discovery and responsible disclosure. The attacker identified a common web vulnerability pattern (reflected XSS via URL parameters) and demonstrated it with a straightforward proof-of-concept to alert the security team of the risk.

## Defensive takeaways
- Implement context-aware output encoding for all user input (HTML entity encoding for HTML context, JavaScript encoding for JS context)
- Use parameterized templating engines that automatically escape output by default
- Implement Content Security Policy (CSP) headers to restrict JavaScript execution and mitigate XSS impact
- Validate and sanitize all user input on both client and server side
- Perform security code review focusing on dynamic URL parameter handling and template rendering
- Use Web Application Firewalls (WAF) to detect and block XSS payloads
- Implement HTTP security headers (X-XSS-Protection, X-Content-Type-Options)
- Conduct regular penetration testing and vulnerability scanning for XSS flaws

## Variant hunting
Test other URL parameters for similar reflection patterns
Try different XSS payloads: script tags, img onerror, svg onload, iframe injection
Test for DOM-based XSS in JavaScript processing of URL parameters
Check for stored XSS if parameters are persisted in user profiles or shared content
Test for second-order reflection through database storage and retrieval
Examine error pages and 404 handlers for reflected XSS opportunities
Test different encoding bypasses (double encoding, unicode, HTML5 event handlers)

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1657

## Notes
This is a straightforward reflected XSS vulnerability with clear proof-of-concept demonstration across multiple browsers (Firefox and Chrome). The payload uses event handler injection (onmouseover) with template literal syntax to bypass basic filters. The vulnerability requires no authentication and can be exploited via social engineering to distribute malicious links. This is a classic web vulnerability that should be remediated through proper output encoding and input validation.

## Full report
<details><summary>Expand</summary>

Hello Security Team,
I would like to report the XSS vulnerability on your system.
Steps To Reproduce:
Visit the following POC link and move your mouse allover index page: 
https://www.████/(Z(%22onmouseover=alert%60%60%20%22))/████████/█████.aspx

1. Tested on firefox browser:

███████
2.Tested on google chrome browser:

█████████

## Impact

An XSS attack allows an attacker to execute arbitrary JavaScript in the context of the attacked website and the attacked user. This can be abused to steal session cookies, perform requests in the name of the victim, or for phishing attacks.

</details>

---
*Analysed by Claude on 2026-05-12*
