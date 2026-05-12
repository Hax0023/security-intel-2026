# Self-XSS in Password Reset Email Input Field

## Metadata
- **Source:** HackerOne
- **Report:** 286667 | https://hackerone.com/reports/286667
- **Submitted:** 2017-11-02
- **Reporter:** zeesek
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** low
- **Vuln:** Cross-Site Scripting (XSS), Self-XSS, Input Validation Bypass
- **CVEs:** None
- **Category:** web-api

## Summary
A self-XSS vulnerability was discovered in Shopify's password reset functionality where HTML/CSS injection was possible in the email address input field. An attacker could inject arbitrary HTML tags like form elements, potentially enabling credential harvesting or other malicious actions through user interaction.

## Attack scenario
1. Attacker navigates to https://accounts.shopify.com/password-reset/new
2. Attacker enters malicious HTML/CSS payload in the email address field (e.g., <h1 style="color:blue;">text</h1>)
3. The application reflects the HTML without proper sanitization, rendering it in the page
4. Attacker could inject a <form> tag to create a fake login or credential harvesting form
5. User interacts with the injected form, potentially entering credentials or sensitive information
6. Attacker captures the submitted data or steals session tokens

## Root cause
Insufficient input validation and output encoding on the email input field. The application failed to sanitize HTML metacharacters or properly escape user input before rendering it in the DOM.

## Attacker mindset
The researcher identified that while initial color injection appears cosmetic, the potential to inject form elements could be weaponized for credential theft or phishing attacks. This demonstrates escalation from simple XSS to a more dangerous attack vector.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, especially email fields
- Apply proper output encoding based on context (HTML entity encoding for HTML context)
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Employ a robust HTML sanitization library if HTML input is required
- Implement server-side validation in addition to client-side checks
- Use frameworks with auto-escaping templates to reduce XSS surface
- Regularly test password reset and authentication flows for XSS vulnerabilities

## Variant hunting
Check other authentication endpoints (login, signup, account recovery) for similar XSS
Test email validation fields across all Shopify products and services
Attempt DOM-based XSS through URL parameters in password reset flows
Test for Stored XSS if email is saved in user profile or logs
Check if error messages also reflect unsanitized input
Test for XSS in password reset token parameter handling

## MITRE ATT&CK
- T1190
- T1566
- T1598

## Notes
This is a self-XSS (requires user interaction with attacker-controlled content), which significantly limits its impact. However, the reporter correctly identified the escalation potential to form injection for phishing. The severity is low because it requires user action and cannot directly compromise other users, but proper remediation is still necessary. The report demonstrates good vulnerability escalation thinking.

## Full report
<details><summary>Expand</summary>

Hi,
When I opened this domain of yours,
https://accounts.shopify.com/password-reset/new

I just put the following text into email address box,
<h1 style="color:blue;">█████</h1>
it change the colour of the text.

Well my point here is that if you could inject HTML, you might be able to add a <form> tag
to the page.
I also upload the picture as a proof.

Peace.

</details>

---
*Analysed by Claude on 2026-05-12*
