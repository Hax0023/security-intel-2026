# Stored XSS on app.crowdsignal.com via Thank You Header

## Metadata
- **Source:** HackerOne
- **Report:** 1842822 | https://hackerone.com/reports/1842822
- **Submitted:** 2023-01-22
- **Reporter:** 0xwega74
- **Program:** Crowdsignal
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in the Crowdsignal project publishing feature where malicious JavaScript can be injected into the 'Thank You Header' field. The payload is stored server-side and executed in the browser of any user who completes and submits a published survey form, reaching the thank you page.

## Attack scenario
1. Attacker logs into app.crowdsignal.com and creates a new survey project
2. Attacker adds survey questions and initiates the publish process
3. Attacker intercepts the publish request and modifies the 'Thank You Header' parameter to include a malicious payload: <a href='javascript:alert(document.domain);'>Click Me</a>
4. The malicious payload is stored on the server without proper sanitization or encoding
5. Victim completes and submits the published survey, redirecting to the thank you page
6. Victim clicks the embedded link and the stored JavaScript payload executes in their browser context, potentially stealing credentials, session tokens, or performing actions on their behalf

## Root cause
The application fails to properly sanitize and encode user-supplied input in the 'Thank You Header' field before storing it in the database. Additionally, the field is rendered without adequate output encoding when displayed to survey respondents, allowing injected HTML/JavaScript to execute.

## Attacker mindset
An attacker with a Crowdsignal account could create legitimate-looking surveys to distribute widely, then inject malicious payloads into the thank you page to compromise survey respondents. This could be leveraged for credential theft, malware distribution, or account takeover of users visiting the thank you page.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields, including the 'Thank You Header'
- Apply context-appropriate output encoding (HTML entity encoding for HTML context) when rendering user-supplied data
- Use a Content Security Policy (CSP) to prevent inline script execution and restrict script sources
- Implement server-side HTML sanitization libraries (e.g., OWASP HTML Sanitizer) for fields that require rich text
- Perform security code review of all form publishing features and thank you page rendering logic
- Add automated testing for XSS payloads in all user input fields during development and regression testing

## Variant hunting
Similar vulnerabilities may exist in other customizable fields within the project creation workflow such as: survey descriptions, project names, success messages, email notification templates, custom CSS fields, or any other user-configurable text that appears to survey respondents. Additionally, check if the vulnerability exists across different subdomain variations (your-subdomain.crowdsignal.net).

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
The report demonstrates a clear attack chain from account compromise to widespread impact. The vulnerability is particularly dangerous because it affects end-users (survey respondents) rather than just account holders, potentially reaching a large audience. The attacker's ability to intercept and modify the request suggests either weak CSRF protections or the use of an HTTP proxy during an unencrypted transmission phase.

## Full report
<details><summary>Expand</summary>

## Summary:
Hi, I hope you're having a good day.

I found an Stored XSS at app.crowdsignal.net.

## Platform(s) Affected:
app.crowdsignal.net

## Steps To Reproduce:

  1. Go to https://app.crowdsignal.com/dashboard and create a project
  1. Add any thing to the project and publish the project and intercept the request while publishing.
  1. Edit the Thank You Header with this payload `<a href='javascript:alert(document.domain);'>Click Me</a>`
  1. Open the Project you published and fill the form and click submit you will be redirected to thank you page click at the button and the XSS will fired.

## Supporting Material/References:

████████

## Impact

Stored XSS

</details>

---
*Analysed by Claude on 2026-05-12*
