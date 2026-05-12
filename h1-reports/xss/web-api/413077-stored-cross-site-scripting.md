# Stored Cross-Site Scripting (XSS) in User Registration Full Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 413077 | https://hackerone.com/reports/413077
- **Submitted:** 2018-09-23
- **Reporter:** sakhauathr99
- **Program:** easycontactnow.com
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Stored XSS, Persistent XSS, Type-I XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the user registration form where unsanitized input from the 'full name' field is permanently stored in the database and executed in the victim's browser when accessed. An attacker can inject malicious JavaScript code during account creation that persists and executes for any user viewing that account's profile or dashboard.

## Attack scenario
1. Attacker navigates to easycontactnow.com and clicks 'Try For Free' to access the signup page
2. In the 'full name' field, attacker enters malicious payload: "><script>alert(1)</script>
3. Attacker completes remaining registration fields and submits the form
4. Server fails to sanitize/validate the input and stores the payload in the database
5. Attacker verifies email and logs into the dashboard
6. Malicious script executes in the attacker's browser, and any admin or user viewing this account's data also triggers the payload

## Root cause
The application fails to implement proper input validation and output encoding on the full name field during user registration. User-supplied data is stored directly in the database without sanitization and rendered without HTML entity encoding when displayed.

## Attacker mindset
Low-skill attacker demonstrating basic XSS exploitation for proof-of-concept, likely motivated by bug bounty rewards or vulnerability disclosure recognition. The simple payload and apologetic tone suggest a junior researcher.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields (whitelist alphanumeric + safe characters only)
- Apply HTML entity encoding/escaping on all output rendering contexts
- Use Content Security Policy (CSP) headers to restrict script execution
- Implement a Web Application Firewall (WAF) to detect and block XSS patterns
- Sanitize input using established libraries (DOMPurify, OWASP ESAPI)
- Conduct regular security testing including SAST/DAST for XSS vulnerabilities
- Implement HTTPOnly and Secure flags on session cookies to limit impact
- Apply the principle of least privilege to user input handling

## Variant hunting
Test other user input fields: email, address, phone, company name for similar XSS
Attempt DOM-based XSS in client-side JavaScript handling of user data
Test stored XSS in user profile edit/update endpoints
Check if other users can view/share profiles containing malicious payloads
Test attribute-based XSS: value='><script>alert(1)</script> in form fields
Attempt polyglot payloads and encoding bypass techniques (SVG, iframe, event handlers)

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
Video POC demonstrates execution in authenticated user context. Vulnerability requires account creation but no email verification bypass needed for persistence. High impact due to stored nature affecting multiple users. Reporter used basic PoC methodology with video evidence strengthening the submission.

## Full report
<details><summary>Expand</summary>

Hellow team 
I got Stored based XSS on your web :D

Here Is Step :

1. Go to https://www.easycontactnow.com/
2. Click "Try For Free" (Sign Up)
3. It will told you "Enter your details to get started". 
   So Enter your full name like : "><script>alert(1)</script>
   Then put all the other details.
4. Then Confirm your id and login.
5. Then Click dashboard and other thing :) 
6. Tada script executed done :D

POC : https://www.youtube.com/watch?v=gYyCAxaB6w0

Sorry for my bad english. 

Thanks :)

## Impact

Stored attacks are those where the injected script is permanently stored on the target servers, such as in a database, in a message forum, visitor log, comment field, etc. The victim then retrieves the malicious script from the server when it requests the stored information. Stored XSS is also sometimes referred to as Persistent or Type-I XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
