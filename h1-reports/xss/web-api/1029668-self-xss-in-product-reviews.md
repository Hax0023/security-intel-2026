# Self XSS in Product Reviews via Email Field Type Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 1029668 | https://hackerone.com/reports/1029668
- **Submitted:** 2020-11-09
- **Reporter:** tomorrow_future
- **Program:** Product Reviews App
- **Bounty:** Not specified
- **Severity:** Low
- **Vuln:** Cross-Site Scripting (XSS), Client-Side Input Validation Bypass, DOM-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability exists in the Product Reviews application where an attacker can inject malicious JavaScript by modifying the email input field type from 'email' to 'text' via browser developer tools, bypassing client-side validation. The injected payload executes in the context of the user's own session when the review is submitted.

## Attack scenario
1. Attacker installs or accesses the Product Reviews application
2. Attacker opens a product page and initiates writing a review
3. Attacker opens browser developer tools (F12) and locates the email input field
4. Attacker changes the input field type attribute from 'email' to 'text'
5. Attacker injects XSS payload in email field: "><img src=a onerror=alert(1)>123@sdf.com
6. Attacker fills other required review fields and submits the form, triggering XSS execution

## Root cause
The application relies solely on client-side HTML5 input type validation (type='email') without implementing server-side validation or output encoding. Since input type can be trivially modified via developer tools, malicious content bypasses validation and is stored/reflected without sanitization.

## Attacker mindset
An attacker discovers that frontend validation can be circumvented using browser tools. They recognize that if server-side validation is absent, arbitrary HTML/JavaScript can be injected. The attacker tests with a basic XSS payload to demonstrate execution capability.

## Defensive takeaways
- Implement mandatory server-side input validation for all user inputs, especially email fields
- Apply strict output encoding/escaping when displaying user-generated content (HTML entity encoding at minimum)
- Never rely solely on client-side or HTML5 input type validation
- Validate email format server-side using regex or library validators
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Sanitize user input before storage using established libraries (e.g., DOMPurify, bleach)
- Perform security code review focusing on input/output handling in review submission logic

## Variant hunting
Check other user input fields (review title, review text, name) for similar client-side validation bypasses
Attempt field type manipulation on other form inputs (number, date, tel, url)
Test if stored XSS persists when review is displayed to other users
Attempt DOM-based XSS in review display templates
Check for CSRF protection on review submission endpoint
Test HTML/JavaScript injection in other review-related features (ratings, comments)

## MITRE ATT&CK
- T1190
- T1059

## Notes
This is classified as 'Self XSS' because only the attacking user can trigger the payload in their own session. However, if the review is stored and displayed to other users without sanitization, it could escalate to Stored XSS with higher severity. The vulnerability demonstrates the critical importance of server-side validation and output encoding regardless of client-side protections.

## Full report
<details><summary>Expand</summary>

1、install app `Product Reviews`
{F1070556} 

2、Open a product and write a review

3、Press F12 on the keyboard，Change the type of email to text.

4、Write in email`"><img src=a onerror=alert(1)>123@sdf.com`.
{F1070565}

5、Write other required fields，then submit.
{F1070566}

## Impact

Self xss

</details>

---
*Analysed by Claude on 2026-05-12*
