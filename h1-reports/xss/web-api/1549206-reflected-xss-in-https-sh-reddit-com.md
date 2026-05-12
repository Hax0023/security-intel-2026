# Reflected XSS in sh.reddit.com

## Metadata
- **Source:** HackerOne
- **Report:** 1549206 | https://hackerone.com/reports/1549206
- **Submitted:** 2022-04-24
- **Reporter:** abhiramsita
- **Program:** Reddit
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Reflected XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected cross-site scripting vulnerability exists in sh.reddit.com where user-controlled input is included in the HTTP response without proper sanitization. An attacker can execute arbitrary JavaScript in the victim's browser context by crafting a malicious URL, potentially stealing session cookies and sensitive data.

## Attack scenario
1. Attacker identifies that sh.reddit.com reflects unsanitized user input near a 'see more' option
2. Attacker crafts a malicious URL containing JavaScript payload in the vulnerable parameter
3. Attacker sends the crafted URL to a victim via email, social media, or other means
4. Victim clicks the link and navigates to the poisoned URL on sh.reddit.com
5. The JavaScript payload executes in the victim's browser with the site's privileges
6. Malicious script steals session cookies, authentication tokens, or performs actions on behalf of the victim

## Root cause
The application fails to properly encode or sanitize user input before including it in the HTML response. The vulnerable parameter is reflected directly into the page, likely near the 'see more' UI element, without HTML entity encoding or content security policy protections.

## Attacker mindset
An attacker would recognize this vulnerability as a low-effort, high-impact attack vector requiring only URL crafting and social engineering. They could automate payload delivery and harvest credentials at scale.

## Defensive takeaways
- Implement output encoding: HTML-encode all user-controlled data before rendering in HTML context
- Use context-aware encoding based on where data is reflected (HTML, JavaScript, URL, CSS contexts)
- Implement Content Security Policy (CSP) headers to restrict script execution sources
- Validate and sanitize all user inputs on the server-side
- Use templating engines with auto-escaping enabled
- Apply the principle of least privilege for cookies (HttpOnly, Secure, SameSite flags)
- Implement Security Headers (X-XSS-Protection, X-Content-Type-Options)
- Conduct regular security code reviews and penetration testing
- Use automated SAST/DAST tools to detect XSS vulnerabilities in CI/CD pipeline

## Variant hunting
Test all URL parameters and query strings for reflected XSS on sh.reddit.com and related subdomains
Check POST body parameters for stored/reflected XSS variants
Test different encodings (double encoding, Unicode, hex) to bypass filters
Look for similar reflection vulnerabilities in 'see more', pagination, and AJAX endpoints
Test for DOM-based XSS in client-side JavaScript handlers
Check for XSS in HTTP headers (Referrer, User-Agent) reflected in responses
Test for mutations/polyglot XSS payloads that bypass existing sanitizers

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1056.004
- T1185

## Notes
The writeup lacks technical depth - no specific parameter name, payload example, or reproduction steps are provided. The 'see more' hover interaction suggests the vulnerability may be triggered on DOM manipulation or JavaScript event handlers. Further investigation needed to determine if this is DOM-based XSS or reflected XSS. Report quality could be improved with screenshots, exact URL with payload, and browser/version information. Reddit's short URL service (sh.reddit.com) being vulnerable is concerning given its widespread use in sharing content.

## Full report
<details><summary>Expand</summary>

## Summary:
Reflected cross-site scripting (or XSS) arises when an application receives data in an HTTP request and includes that data within the immediate response in an unsafe way.

## Impact:
attacker can execute malicious java script and steal cookies 

## Steps To Reproduce:
[add details for how we can reproduce the issue]

Hi team ,

Navigate to below url 
scroll to page end find a option see more
Move mouse over there and observe the execution of javascript 
## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

## Impact

attacker can execute malicious java script and steal cookies

</details>

---
*Analysed by Claude on 2026-05-12*
