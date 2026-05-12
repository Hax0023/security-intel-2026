# Stored XSS via AngularJS Template Injection in Referral Contacts Address Field

## Metadata
- **Source:** HackerOne
- **Report:** 141463 | https://hackerone.com/reports/141463
- **Submitted:** 2016-05-27
- **Reporter:** yaworsk
- **Program:** drchrono
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Template Injection, AngularJS Expression Injection
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the referral contacts address field where user input is processed as AngularJS template expressions without proper sanitization. An attacker can inject malicious AngularJS code using double bracket syntax [[constructor.constructor('code')()]] which executes arbitrary JavaScript when the contact page is loaded.

## Attack scenario
1. Attacker creates a doctor account on drchrono platform
2. Attacker navigates to the referral contacts management page (/messages/referrals/contacts/)
3. Attacker adds a new contact with malicious payload in the address field: [[constructor.constructor('alert(document.cookie)')()]]
4. Attacker saves the contact and verifies the XSS executes by reloading the page
5. When an admin or authorized user visits the referral contacts overview page, the stored payload executes in their browser context
6. Attacker steals admin session cookies or performs account takeover actions with admin privileges

## Root cause
User input from the address field is rendered as AngularJS template expressions using double bracket interpolation [[...]] syntax without proper HTML escaping or Content Security Policy. AngularJS 1.1.5 allows accessing the constructor property to execute arbitrary code through Function constructor.

## Attacker mindset
An attacker with low-privilege access (ability to create referral contacts) exploits template injection to achieve privilege escalation by compromising admin accounts. The stored nature means the payload persists and can affect multiple users, making it attractive for account takeover and lateral movement.

## Defensive takeaways
- Implement strict output encoding/escaping for all user-controlled data rendered in templates, especially with AngularJS which uses interpolation syntax
- Use AngularJS built-in sanitization ($sanitize, ng-bind-html with $sce.trustAsHtml only for trusted content)
- Disable AngularJS expression evaluation in user-controlled fields or use text binding (ng-bind) instead of interpolation ({{}})
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Validate and sanitize input on the server-side; never trust client-side validation
- Keep AngularJS and all dependencies updated to latest patched versions
- Use modern frameworks with built-in XSS protection over older AngularJS 1.x versions
- Implement input validation to reject or encode special characters like brackets, quotes, and constructor references
- Apply principle of least privilege - restrict who can create/modify referral contacts

## Variant hunting
Test other address-like fields (phone, zip code, email) for similar AngularJS injection
Check all user input fields in messages, contacts, and referral modules for template injection
Test alternative AngularJS payload techniques: {{constructor}}, $event.view.eval(), scope.$apply()
Look for fields using ng-repeat, ng-bind, ng-click that might process user input as expressions
Test for DOM-based template injection in client-side rendered content
Check for similar vulnerabilities in other endpoints that display user-generated content

## MITRE ATT&CK
- T1190
- T1203
- T1598
- T1566

## Notes
This vulnerability demonstrates the dangers of client-side template engines processing untrusted input. AngularJS 1.x is known to have expression injection vulnerabilities, and this case specifically abuses the constructor property to execute arbitrary functions. The attack requires only basic user permissions and affects any user viewing the stored payload, making it a high-impact vulnerability for a healthcare application handling sensitive data.

## Full report
<details><summary>Expand</summary>

Hi All,
I've found a stored XSS vulnerability via an Angular Template Injection in the messages referral address field.

##Description
After visiting ``https://1337test.drchrono.com/messages/referrals/contacts/```, you can enter new contact information. In the field for the address, if enter [[5*5]], when the referrals contact overview will show the address as 25. This indicates an injection. 

Opening the browser console and using the command angular.version, we can see you are using 1.1.5. So, entering the address for a contact as ```[[constructor.constructor('alert(document.cookie)')()]]```, saving and reloading the page, an stored XSS is executed {F96481}

##Steps to reproduce
1. Create a doctors account
2. Visit ```https://1337test.drchrono.com/messages/referrals/contacts/```
3. Add a new contact
4. In the address field, enter ```[[constructor.constructor('alert(1)')()]]```

Confirm the alert pop up with **1** in it.

##Vulnerability
The stored xss could be used for a complete account take over if an admin visited this contact page. An attacker only needs permission to create a referral contact to store the payload. In the example image, I've printed all cookies to the screen but this could easily be sent to a remote endpoint.

Please let me know if you have any questions.
Pete

</details>

---
*Analysed by Claude on 2026-05-12*
