# Stored XSS in Company Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 187410 | https://hackerone.com/reports/187410
- **Submitted:** 2016-12-01
- **Reporter:** imran_hadid
- **Program:** HackerOne Report #187410
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the company name field where malicious JavaScript payloads are not properly sanitized or encoded. The injected payload executes in the message room context after user login, affecting any user viewing the compromised company name.

## Attack scenario
1. Attacker registers an account or gains access to edit company profile information
2. Attacker injects malicious XSS payload in the Company Name field: "><IMG SRC=x onerror=javascript:alert("XSS")>
3. Application stores the unsanitized payload in the database without validation
4. When any authenticated user navigates to the message room, the company name is rendered without proper encoding
5. Browser executes the injected JavaScript code in the context of the logged-in user's session
6. Attacker can steal session cookies, perform actions as the victim, or deface the interface

## Root cause
The application fails to implement proper input validation and output encoding for the company name field. User-supplied input is stored directly in the database and rendered as HTML without sanitization, allowing script injection.

## Attacker mindset
An attacker would recognize that company profile fields are often displayed to multiple users without sanitization. By injecting a payload in a high-visibility field, they achieve persistent code execution affecting all users who view the message room, maximizing impact with minimal effort.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields using whitelist approaches
- Apply proper output encoding (HTML entity encoding) when rendering user data in templates
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize HTML input using established libraries (e.g., DOMPurify, OWASP ESAPI)
- Store data separately from presentation logic; encode at render time, not storage time
- Implement server-side validation in addition to client-side checks
- Regular security testing including automated XSS scanning in CI/CD pipeline

## Variant hunting
Test all user profile fields (name, description, bio, company name, etc.) for XSS
Check comment/review sections where company information is displayed
Test file upload features where metadata might be rendered
Examine notification systems that may display company names
Test API endpoints that return company data without proper encoding
Check archived/historical message views for persistent XSS
Test different message room types or filtering options

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539

## Notes
The POC demonstrates a simple IMG tag with onerror handler bypassing quote escaping through HTML entity encoding (&quot;). The vulnerability affects message rooms specifically, suggesting the company name is displayed prominently in that section. The random generation mentioned suggests the payload triggers multiple times, increasing user impact and detection likelihood.

## Full report
<details><summary>Expand</summary>

Hello Team.

I found a Store XSS. Where the company name is the vulnerable to XSS. If you give this below XSS script as Company name, you will get the XSS pop up after the login in message option where it'll randomly generated at the message room.
“><IMG SRC=x onerror=javascript:alert(&quot;XSS-by-Imran&quot;)> 

 Here is the POC:
https://youtu.be/dqrH2WhIgtk

Thanks


</details>

---
*Analysed by Claude on 2026-05-12*
