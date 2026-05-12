# Self-Stored XSS + Login CSRF

## Metadata
- **Source:** HackerOne
- **Report:** 1092678 | https://hackerone.com/reports/1092678
- **Submitted:** 2021-02-02
- **Reporter:** biest
- **Program:** HackerOne
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Cross-Site Request Forgery (CSRF), Client-Side Validation Bypass, Insufficient Input Sanitization
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can bypass client-side username length validation using browser developer tools to inject XSS payloads into the username field. When combined with CSRF, an attacker can force a victim to login to the attacker's account, resulting in arbitrary JavaScript execution in the victim's browser context.

## Attack scenario
1. Attacker identifies username field has client-side max-length validation (8-20 characters)
2. Attacker uses browser inspect element to modify maxlength attribute to 100
3. Attacker injects malicious payload such as "><img src onerror=confirm(document.cookie)> into username field
4. Attacker generates CSRF PoC HTML using Burp Suite that automatically logs victim into attacker's account
5. Victim visits attacker-controlled page containing CSRF PoC, triggering login to attacker's account
6. Stored XSS payload executes in victim's browser, stealing cookies or performing unauthorized actions

## Root cause
Server-side validation missing for username input, relying solely on client-side HTML5 maxlength attribute. No HTML encoding or sanitization of username before storage and rendering.

## Attacker mindset
Exploit common development oversight of relying on client-side validation. Combine XSS with CSRF to maximize impact by forcing victims into compromised accounts. Use browser dev tools as attack vector since validation exists only on client.

## Defensive takeaways
- Implement server-side input validation for all user inputs, never trust client-side validation
- HTML-encode or sanitize all user-supplied data before storing and rendering
- Use allowlists for username characters rather than relying on length restrictions alone
- Implement CSRF tokens and validate origin/referer headers for state-changing operations
- Apply Content Security Policy (CSP) headers to prevent inline script execution
- Store usernames in a way that prevents interpretation as HTML/JavaScript
- Implement HttpOnly and Secure flags on session cookies to reduce XSS impact

## Variant hunting
Check other user profile fields for similar validation bypass (email, display name, bio)
Test if password reset endpoint has same vulnerability
Verify if admin account creation has same client-side validation issues
Check for stored XSS in comment/message fields with similar bypasses
Test if file upload filename field has similar client-side validation
Hunt for CSRF tokens that are predictable or missing on other state-changing endpoints
Look for other HTML5 constraint attributes that can be manipulated (pattern, type)

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1539
- T1539

## Notes
This vulnerability is particularly dangerous because it combines two attack vectors. The initial XSS is stored in the username field, affecting not only the attacker but also anyone who views the attacker's profile. The CSRF component ensures victims will be logged into the attacker's account when visiting a malicious page, guaranteeing the XSS execution. The PoC demonstrates the vulnerability is easily reproducible and doesn't require advanced techniques.

## Full report
<details><summary>Expand</summary>

**Description:**
User can set username between 8-20 alphanumeric characters, but with the help of inspect element attacker can manipulate ```██████=``` & can insert a  xss payload resulting in self stored xss & with the help of  login csrf  attacker can force the victim into attacker's account causing successful execution of javascript.

█████████

Payload used = ```"><img src onerror=confirm(document.cookie)>```

## Impact

Able to execute javascript in victim's browser

## System Host(s)
█████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
1. Visit [Sign in](███████) and sign in
2. Click on Change username -->  Open inspect element --> change max length of new username and confirm username to ```100```
3. Now enter the payload in``` new username```  and  ```confirm username``` field & click on submit --> Sign out
4.  Enter the credentials to sign in --> Intercept request using burp --> Action --> Engagement Tools --> Generate Csrf poc --> Copy html.
5. Open notepad & paste --> save as .html file
6. Open the html file in any browser to confirm the vulnerability.

Poc attached :-

███████

## Suggested Mitigation/Remediation Actions
Sanitization of input must be done



</details>

---
*Analysed by Claude on 2026-05-12*
