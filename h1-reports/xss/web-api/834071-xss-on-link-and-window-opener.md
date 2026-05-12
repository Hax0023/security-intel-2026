# XSS via Unsafe Path Parameter in Slack Feedback Form

## Metadata
- **Source:** HackerOne
- **Report:** 834071 | https://hackerone.com/reports/834071
- **Submitted:** 2020-03-29
- **Reporter:** pisarenko
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cross-Site Scripting (XSS), Open Redirect, Unsafe window.opener Usage
- **CVEs:** None
- **Category:** web-api

## Summary
The Slack feedback submission endpoint at api.slack.com/feedback/submit fails to sanitize the 'path' parameter, allowing attackers to inject javascript: URIs or arbitrary URLs. This enables XSS execution or open redirect attacks when the path parameter is processed by the application, potentially via window.opener manipulation.

## Attack scenario
1. Attacker crafts an HTML form that submits to https://api.slack.com/feedback/submit with a hidden 'path' input containing a javascript: payload or malicious URL
2. Attacker hosts this form on a controlled domain or injects it via another vulnerability
3. Victim visits the attacker's page or clicks a link to it
4. Form auto-submits via JavaScript, sending the malicious path parameter to Slack's feedback endpoint
5. Slack's backend or frontend processes the path parameter without proper validation/sanitization
6. If processed client-side: XSS executes in victim's browser; if used in redirect: victim is redirected to attacker's phishing/malware site

## Root cause
Insufficient input validation and output encoding of the 'path' parameter in the feedback submission form. The application fails to validate that the path contains a safe URL scheme and does not sanitize or encode the value before using it in DOM operations or redirects.

## Attacker mindset
An attacker seeks to leverage a trusted service (Slack) to launch client-side attacks without domain restrictions. Using form submission bypasses some CORS protections and allows delivery of malicious payloads that execute with the victim's Slack session context, potentially stealing credentials or session tokens via window.opener access.

## Defensive takeaways
- Implement strict whitelist validation for URL parameters - only allow http/https schemes and validate against known safe domains
- Apply Content Security Policy (CSP) headers to prevent inline script execution and restrict javascript: URI usage
- Sanitize and encode all user-controlled input before insertion into DOM or use as redirect targets
- Use URL.parse() or similar APIs to validate URL structure before processing
- Implement Sub-Resource Integrity (SRI) and frame-ancestors directives to prevent clickjacking
- Validate referrer and origin headers to detect cross-origin form submission attacks
- Never trust the 'path' parameter for redirects without explicit validation against a whitelist

## Variant hunting
Check other Slack API endpoints for similar path/redirect parameter validation issues
Test data: parameters with data:, blob:, and other exotic URI schemes
Look for other form-based submissions that might accept user-controlled redirect targets
Search for window.opener usage patterns that could be exploited for cross-origin attacks
Test if path parameter is reflected in error messages (reflected XSS vector)
Investigate whether the feedback endpoint performs any client-side URL handling or window operations

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003

## Notes
The report demonstrates two distinct attack vectors: javascript: URI injection (leading to XSS) and open redirect via URL injection. The mention of 'window.opener' suggests the attacker may be able to access the opener window from the redirected page, enabling session hijacking or credential theft. The vulnerability is particularly critical because it's on Slack's own API domain, giving injected code Slack's origin privileges. The report references an attachment (F765317) that likely contains proof-of-concept code. This appears to be a form-based CSRF-like attack that bypasses some browser protections by leveraging a legitimate endpoint.

## Full report
<details><summary>Expand</summary>

Hi possible xss and error when clicking on the link .

`<form name="pisarenko" action="https://api.slack.com/feedback/submit" method="POST">
<input type='hidden' name='crumb' value="1"> 
<input type='hidden' name='path' value="javascript:alert()"> 
<input type='hidden' name='vote' value="Yes"> 
</form>
<script>document.pisarenko.submit();</script>`

or 

`<form name="pisarenko" action="https://api.slack.com/feedback/submit" method="POST">
<input type='hidden' name='crumb' value="1"> 
<input type='hidden' name='path' value="https://servisvk.com/exploit/opener.php"> 
<input type='hidden' name='vote' value="Yes"> 
</form>
<script>document.pisarenko.submit();</script>`

## Impact

Redirection from the original site to an evil site or execution of js code

Please check that the domain is `slack`

{F765317}

</details>

---
*Analysed by Claude on 2026-05-12*
