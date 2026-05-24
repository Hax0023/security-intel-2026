# Multiple Stored XSS on sandbox.veris.in via Veris Frontdesk Android App

## Metadata
- **Source:** HackerOne
- **Report:** 121275 | https://hackerone.com/reports/121275
- **Submitted:** 2016-03-08
- **Reporter:** itly
- **Program:** Veris (sandbox.veris.in)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
Multiple stored XSS vulnerabilities were discovered in the Veris Frontdesk Android application that allows attackers to inject malicious JavaScript payloads through check-in form fields ('Who do you wish to meet?' and 'Additional Information'). The unsanitized input is stored in the backend database and reflected without proper encoding on the visitor-log portal, enabling arbitrary code execution in the context of authenticated users' browsers.

## Attack scenario
1. Attacker opens the Veris Frontdesk Android application and initiates a check-in process
2. Attacker enters legitimate details (first name, last name, phone number) to pass initial validation
3. Attacker injects XSS payload '<img src=x onerror=alert(3)>' into the 'Who do you wish to meet?' field
4. Attacker completes the check-in submission, which stores the malicious payload in the backend database
5. Authorized user (receptionist/admin) logs into sandbox.veris.in and navigates to the visitor-log page
6. The visitor-log page retrieves and displays the stored payload without encoding, triggering arbitrary JavaScript execution in the user's browser

## Root cause
The application fails to implement proper input sanitization on the Android client side and lacks output encoding on the web portal. User-supplied input from form fields is stored directly in the database and rendered as HTML without escaping special characters or encoding entities.

## Attacker mindset
An attacker with basic web security knowledge seeks to demonstrate that user-controlled input can persist in the system and execute arbitrary code. The attacker leverages the cross-platform nature of the application (mobile to web) to bypass potential client-side protections, targeting administrative users who access the visitor-log portal.

## Defensive takeaways
- Implement strict input validation on both client and server side to reject or sanitize malicious payloads
- Apply context-appropriate output encoding (HTML entity encoding) when rendering user-supplied data in web contexts
- Use Content Security Policy (CSP) headers to restrict inline script execution and mitigate XSS impact
- Validate and sanitize data at the API/backend layer regardless of client-side protections
- Implement security headers (X-XSS-Protection, X-Content-Type-Options) on the web portal
- Use templating engines with automatic escaping enabled by default
- Conduct security testing across all entry points, particularly those accepting user input from mobile applications

## Variant hunting
Search for similar unencoded output in other portal pages displaying user-generated content such as: visitor notes, feedback forms, profile information, support tickets, or any admin/dashboard pages that retrieve and display data from user inputs. Test other mobile app input fields (name fields, address, email, custom information) for the same vulnerability vector. Check if the web application has other endpoints consuming data from the mobile app without proper sanitization.

## MITRE ATT&CK
- T1190
- T1598.003
- T1566.002

## Notes
This is a classic stored XSS vulnerability spanning a mobile-to-web application architecture. The vulnerability affects authenticated users accessing the admin/staff portal, making it particularly dangerous as it can compromise user sessions and perform actions on behalf of authorized users. The use of multiple vulnerable fields increases the attack surface. The simplicity of the payload suggests the application has no input filtering or output encoding mechanisms in place.

## Full report
<details><summary>Expand</summary>

Hello Team,

I have found multiple cross site scripting vulnerabilities on sanbox.veris.in due to the malicious input injected through veris frontdesk android app.

Vulnerable App : Veris Frontdesk Android App

Vulnerable Input Fields: 1) Who do you wish to meet?
                                2) Additional Information

Payload used: <img src=x onerror=alert(3)> and <img src=x onerror=alert(4)>

Reflects where: https://sandbox.veris.in/portal/visitor-log/

Steps to Reproduce:

1. Open Veris Front Desk App.
2. Go to Check In.
3. Enter the required details like first name, last name and phone number.
4. Proceed to Next.
5. Inject the above mentioned payload in vulnerable input fields.
6. Submit it and Check In.
7. Login to your account on sandbox.veris.in
8. Go to https://sandbox.veris.in/portal/visitor-log/
9. Tadaa! XSS Triggers.

Proof of Concept: Please find the attached screenshots.

Do evaluate it and inform me accordingly.

Best Regards,

Hely H. Shah



</details>

---
*Analysed by Claude on 2026-05-24*
