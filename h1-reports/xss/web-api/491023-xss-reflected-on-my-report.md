# Reflected XSS on my_reports Dashboard

## Metadata
- **Source:** HackerOne
- **Report:** 491023 | https://hackerone.com/reports/491023
- **Submitted:** 2019-02-04
- **Reporter:** r0hack
- **Program:** Semrush
- **Bounty:** Not specified in writeup
- **Severity:** high
- **Vuln:** Cross-Site Scripting (Reflected), Improper Input Validation, HTML Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists in the my_reports dashboard endpoint that fails to properly sanitize user input in the document parameter. An attacker can inject malicious JavaScript code that executes in the victim's browser context when the crafted URL is visited, enabling session cookie theft.

## Attack scenario
1. Attacker crafts malicious URL with XSS payload injected into the document parameter: /my_reports/api/v1/document">{{img_tag}}/user_id
2. Attacker sends phishing link to victim user via email or social engineering
3. Victim clicks the link while authenticated to Semrush
4. Browser renders the page with injected img tag containing onerror handler
5. onerror event fires, executing JavaScript to exfiltrate document.cookie
6. Attacker obtains valid session cookies and gains unauthorized account access

## Root cause
The my_reports API endpoint fails to properly HTML-encode or validate the document parameter before including it in the response. Double quotes are not escaped, allowing attribute injection and event handler execution.

## Attacker mindset
Account takeover and unauthorized access to user reports/analytics data. Session cookies provide direct authentication bypass without needing credentials. The reflective nature means the attack requires victim interaction but leaves minimal logs if not properly monitored.

## Defensive takeaways
- Implement output encoding for all user-controlled data reflected in HTML context (HTML entity encoding minimum)
- Use Content Security Policy (CSP) headers to restrict script execution from inline sources
- Validate and sanitize all API parameters, particularly those used in document paths
- Implement HTTPOnly and Secure flags on session cookies to prevent JavaScript access
- Use frameworks with automatic XSS protection (modern templating engines auto-escape by default)
- Perform security testing of all API endpoints, not just UI pages
- Implement WAF rules to detect and block common XSS patterns in parameters

## Variant hunting
Check other /api/v1/ endpoints for similar parameter injection vulnerabilities
Test all dashboard report parameters for reflected XSS
Look for similar patterns in export, download, or document generation endpoints
Test if HTML encoding is applied inconsistently across different parameter types
Check stored XSS variants if parameters are saved in user preferences or reports
Test polyglot payloads that work across different API response formats (JSON, HTML, XML)
Enumerate other user-controlled path parameters in API routes

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1056 - Adversary-in-the-Middle
- T1539 - Steal Web Session Cookie
- T1204 - User Execution

## Notes
Writeup is in Russian. The vulnerability demonstrates a gap in API security practices - while client-side validation or sanitization might exist, server-side reflection without encoding is the root issue. The use of img src with onerror is a classic technique bypassing some basic XSS filters. The /api/v1/ path suggests REST API architecture which sometimes receives less security scrutiny than main application endpoints.

## Full report
<details><summary>Expand</summary>

Еще раз привет. На этот раз, кроме HTML-инъекции проходит полноценный XSS в дашбоарде пользователя.

Payload: https://www.semrush.com/my_reports/api/v1/document%22%3E%3Cimg%20src=x%20onerror=alert(document.cookie)%3E/4007861

PoC: На скрине

## Impact

Кража сессионных куков.

</details>

---
*Analysed by Claude on 2026-05-12*
