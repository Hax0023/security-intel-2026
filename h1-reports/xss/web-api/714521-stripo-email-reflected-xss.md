# Reflected XSS in stripo.email Template URL

## Metadata
- **Source:** HackerOne
- **Report:** 714521 | https://hackerone.com/reports/714521
- **Submitted:** 2019-10-15
- **Reporter:** trazer
- **Program:** stripo.email
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in stripo.email's template URL path where user-controlled input is not properly sanitized or encoded before being reflected in the HTTP response. An attacker can inject arbitrary JavaScript code via URL manipulation that executes in the victim's browser when the malicious link is visited.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload encoded as %3E%22%27%3E%3Cscript%3Ealert%281578%29%3C%2Fscript%3E appended to the template path
2. Attacker shares the malicious link via email, social media, or social engineering to target victims
3. Victim clicks the link while authenticated to stripo.email or in an active session
4. The browser sends the request to stripo.email with the payload in the URL path parameter
5. Server reflects the unencoded payload back in the HTML response without proper sanitization
6. Victim's browser interprets and executes the JavaScript alert(1578), confirming XSS execution and potential for credential theft or session hijacking

## Root cause
The template URL path parameter is reflected directly into the HTTP response without proper HTML entity encoding or input validation. The application likely uses the URL parameter to generate page content (breadcrumbs, page title, or other dynamic elements) but fails to escape special characters that have meaning in HTML/JavaScript context.

## Attacker mindset
An attacker would recognize that the application reflects URL parameters back to users and test for encoding failures. By URL-encoding the XSS payload, they bypass basic client-side filters and demonstrate the vulnerability. This could be leveraged for credential harvesting, malware distribution, or account takeover via session stealing.

## Defensive takeaways
- Implement strict output encoding on all user-controlled data reflected in HTML context using language-appropriate functions (e.g., htmlspecialchars in PHP, encodeURIComponent in JavaScript)
- Apply Content Security Policy (CSP) headers to restrict script execution and inline content
- Validate and sanitize all URL path parameters on the server side before processing
- Use a templating engine with auto-escaping enabled by default
- Implement input validation with whitelist approach for URL parameters where possible
- Conduct regular security testing including automated XSS scanning in CI/CD pipeline
- Deploy Web Application Firewall (WAF) rules to detect and block common XSS patterns

## Variant hunting
Test other template URLs or dynamic routes that accept parameters in the path
Try alternative XSS payloads: %3Cimg%20src=x%20onerror=alert(1)%3E, %3Csvg%20onload=alert(1)%3E
Test reflected parameters in query strings (?template=...) if available
Check for DOM-based XSS by analyzing JavaScript that processes URL fragments
Test for stored XSS if user can save or share templates with injected payloads
Examine other email template platforms for similar path-based reflection vulnerabilities

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1059.007

## Notes
This is a straightforward reflected XSS vulnerability with clear exploitation path. The use of URL encoding suggests the attacker tested bypassing basic client-side filters. The vulnerability is in a non-authenticated context (template preview pages typically accessible without login), increasing impact. The alert() proof-of-concept demonstrates execution but doesn't show the full attack potential (cookie stealing, credential harvesting). Requires user interaction (clicking link) making it suitable for phishing campaigns targeting stripo.email users or administrators.

## Full report
<details><summary>Expand</summary>

hello securitty team tested windows 10 and firefox 69.0.3 (64 bit)

test url: <https://stripo.email//templates/merry-christmas-email-template-winter-inspiration-gifts-flowers-industry >

payload: %3E%22%27%3E%3Cscript%3Ealert%281578%29%3C%2Fscript%3E

Proof Url : 
```
https://stripo.email//templates/merry-christmas-email-template-winter-inspiration-gifts-flowers-industry%3E%22%27%3E%3Cscript%3Ealert%281578%29%3C%2Fscript%3E
```
Proof Url open firefox 

{F608355}

## Impact

https://www.owasp.org/index.php?title=Reflected_XSS

</details>

---
*Analysed by Claude on 2026-05-12*
