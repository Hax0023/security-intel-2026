# Stored XSS in SMTP User Creation at smtp2go.com/settings/users

## Metadata
- **Source:** HackerOne
- **Report:** 912865 | https://hackerone.com/reports/912865
- **Submitted:** 2020-07-01
- **Reporter:** testerpro
- **Program:** smtp2go
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Input Validation Bypass, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the SMTP user creation functionality where user-supplied input in the username field is not properly sanitized or encoded. The malicious payload persists in the application database and executes when the user is referenced in webhooks, allowing attackers to steal session cookies or perform unauthorized actions.

## Attack scenario
1. Attacker creates an account on smtp2go.com and authenticates to the dashboard
2. Attacker navigates to Settings > SMTP Users and creates a new SMTP user
3. Attacker enters XSS payload in the username field (e.g., &#00;</form><input type="date" onfocus="alert(1)">)
4. Attacker saves the malicious user entry, which is stored unfiltered in the database
5. Attacker creates or configures a webhook and selects the malicious user from the dropdown
6. When the webhook interface loads or processes the user data, the XSS payload executes in the attacker's or victim's browser, potentially exfiltrating cookies or session tokens

## Root cause
The application fails to implement proper input validation and output encoding on the username field in the SMTP user creation form. User input is stored directly in the database without sanitization, and when rendered in subsequent pages (webhooks), it is not properly HTML-encoded, allowing script execution.

## Attacker mindset
An attacker would identify this vulnerability to gain persistent access to user sessions, steal authentication cookies, or perform unauthorized actions through the compromised account. The stored nature makes it particularly valuable as it affects all users who interact with the malicious user record.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, including whitelist-based validation for usernames
- Apply proper output encoding (HTML entity encoding) when rendering user-controlled data in HTML contexts
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Implement context-aware encoding for different output contexts (HTML, JavaScript, CSS, URL)
- Perform server-side validation and sanitization, not relying solely on client-side controls
- Escape special HTML characters in username fields before storage or display
- Conduct regular security testing including XSS-focused test cases for all user input fields

## Variant hunting
Check other user input fields (email, phone, etc.) for similar XSS vulnerabilities
Test other settings pages that accept user input (API keys, webhooks configuration, etc.)
Examine webhook payload templates and user references for stored XSS
Look for DOM-based XSS in JavaScript that processes user data dynamically
Test password reset, profile update, and account settings pages for stored XSS
Check email template functionality and user references within templates
Investigate any other dropdown/selection fields that display stored user data

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1059 - Command and Scripting Interpreter
- T1185 - Man in the Browser
- T1056 - Input Capture
- T1539 - Steal Web Session Cookie

## Notes
The vulnerability demonstrates a classic stored XSS scenario where insufficient input sanitization combined with improper output encoding creates a persistent security risk. The use of HTML entity encoding bypasses (&#00;) shows sophistication in payload crafting. The webhook feature provides a reliable trigger point for payload execution. This vulnerability would affect all users viewing or managing the malicious user account, making it a high-impact issue for multi-tenant SaaS applications.

## Full report
<details><summary>Expand</summary>

Vulnerability :
A. Type:- Cross Site Scripting (Stored) 
B. Description:- Stored XSS, also known as persistent XSS, is the more damaging than non-persistent XSS. It occurs when a malicious script is injected directly into a vulnerable web application.
Summary :
When you will create a particular user you will have to enter username and you can enter Xss payload than on webhooks it will fire that XSS.
As the website is not filtering the input provided by the user, that's why this problem is there.
Thank You.
## Steps To Reproduce:
[add details for how we can reproduce the issue]

  1. Create an account https://app.smtp2go.com and LOG IN using username and password.
  2. After that you will be redirected to dashboard and click on settings and then click on SMTP users.
  3. Click on Add SMTP USER and enter &#00;</form><input type&#61;"date" onfocus="alert(1)"> this payload on username and save it.
 4. After that down below click on webhooks and then continue and then ADD WEBHOOK and then from users select that user which we had created earlier and it will fire the pop up.  
I had attached the PoC you can see it.

## Supporting Material/References:


  * [attachment / reference]

## Impact

If one of these users executes malicious content, the attacker may be able to perform privileged operations on behalf of the user or gain access to sensitive data belonging to the user such as steal Cookies of user,etc.

</details>

---
*Analysed by Claude on 2026-05-12*
