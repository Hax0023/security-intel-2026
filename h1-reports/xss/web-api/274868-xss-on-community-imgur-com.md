# Reflected XSS on community.imgur.com Email Unsubscribe Parameter

## Metadata
- **Source:** HackerOne
- **Report:** 274868 | https://hackerone.com/reports/274868
- **Submitted:** 2017-10-05
- **Reporter:** madrobot
- **Program:** Imgur
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability was discovered on community.imgur.com in the email unsubscribe endpoint where the 'email' parameter is not properly sanitized or encoded. An attacker can craft a malicious URL containing JavaScript payload that executes in the victim's browser when visited.

## Attack scenario
1. Attacker identifies the vulnerable /email/unsubscribed endpoint on community.imgur.com
2. Attacker crafts a malicious URL with XSS payload in the email parameter: email=test%27%22%3E%3Csvg/onload=alert(document.domain)%3E
3. Attacker sends the malicious link to target users via email, social engineering, or forum posts
4. Victim clicks the link believing it's a legitimate unsubscribe confirmation
5. JavaScript payload executes in victim's browser with their session privileges
6. Attacker can steal session cookies, perform actions on behalf of user, or redirect to phishing site

## Root cause
The email parameter value is reflected directly into the HTML response without proper output encoding or input validation, allowing SVG/JavaScript injection

## Attacker mindset
An attacker would recognize that the unsubscribe endpoint takes user input (email address) and likely reflects it back to the user for confirmation. By breaking out of the expected context with quotes and angle brackets, they can inject arbitrary HTML/SVG elements with event handlers to execute JavaScript.

## Defensive takeaways
- Implement strict output encoding (HTML entity encoding) for all user-supplied data reflected in responses
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Apply input validation to reject or sanitize unexpected characters in email parameters
- Use templating engines with automatic escaping enabled
- Implement security headers like X-XSS-Protection
- Test all endpoints that accept and reflect user input for XSS vulnerabilities
- Use Security Headers such as X-Content-Type-Options: nosniff

## Variant hunting
Search for other unsubscribe/email confirmation endpoints on community.imgur.com
Test similar parameters (email, recipient, address, etc.) on email-related endpoints
Check for DOM-based XSS in JavaScript that processes email parameter client-side
Look for stored XSS if email addresses are saved and displayed elsewhere
Test other Imgur subdomains for similar unsubscribe functionality
Check if error pages reflect the email parameter without encoding

## MITRE ATT&CK
- T1190
- T1566

## Notes
This is a straightforward reflected XSS with basic bypass of quote filtering using HTML entity encoding (%27 for single quote, %22 for double quote). The payload uses SVG onload handler instead of traditional script tags, which may bypass some filters. The report lacks bounty amount and resolution timeline details.

## Full report
<details><summary>Expand</summary>

Hello __Team__

**Description:** 
I found a reflected cross site scripting on community.imgur.com
## Steps To Reproduce:
Visit
`https://community.imgur.com/email/unsubscribed?email=email@gmail.com%27%22%3E%3Csvg/onload=alert(document.domain)%3E`

{F226739}

__Regards__
Santhosh

</details>

---
*Analysed by Claude on 2026-05-12*
