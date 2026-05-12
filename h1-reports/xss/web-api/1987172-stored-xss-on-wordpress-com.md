# Stored XSS on wordpress.com via Crowdsignal Poll Embedding

## Metadata
- **Source:** HackerOne
- **Report:** 1987172 | https://hackerone.com/reports/1987172
- **Submitted:** 2023-05-14
- **Reporter:** riadalrashed
- **Program:** WordPress.com / Automattic
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insecure Third-Party Integration
- **CVEs:** None
- **Category:** web-api

## Summary
A Stored XSS vulnerability exists in wordpress.com through the Crowdsignal poll embedding feature. An attacker can inject malicious JavaScript code via poll answer fields that executes when the embedded poll is viewed on WordPress.com posts. This allows arbitrary script execution in victim browsers and potential credential theft or session hijacking.

## Attack scenario
1. Attacker creates a poll on app.crowdsignal.com with malicious payload in answer field: <img src=x onerror=alert(document.cookie)>
2. Attacker copies the Website Popup embed code from Crowdsignal
3. Attacker embeds the malicious poll into a WordPress.com post
4. Victim visits the WordPress.com post containing the embedded poll
5. The browser renders the poll widget, triggering the XSS payload stored in the answer field
6. Malicious JavaScript executes in victim's browser with access to cookies, session tokens, and page content

## Root cause
Insufficient output encoding/sanitization of user-supplied content in Crowdsignal poll answers when rendered within WordPress.com context. The embedding mechanism does not properly escape HTML special characters or validate/sanitize third-party content before rendering in DOM.

## Attacker mindset
Exploit weak input validation in third-party integrations to achieve persistent XSS. Leverage WordPress.com's trust in embedded third-party content to bypass CSP or filtering mechanisms. Target high-value WordPress.com users by embedding polls in popular posts.

## Defensive takeaways
- Implement strict Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize all user inputs server-side using allowlists for poll content (remove HTML/JavaScript)
- Use context-aware output encoding (HTML entity encoding) for all dynamic content
- Validate and sanitize third-party embed content before rendering in DOM
- Implement iframe sandboxing for third-party widgets with restricted permissions
- Apply Security review process for all third-party integrations and embed mechanisms
- Use auto-escaping template engines and avoid innerHTML for dynamic content
- Implement Subresource Integrity (SRI) checks for third-party scripts

## Variant hunting
Test other Crowdsignal input fields (poll titles, descriptions, custom HTML)
Probe other WordPress.com integration points with Crowdsignal and similar services
Attempt event handler injection in different contexts (onload, onmouseover, etc.)
Test SVG-based XSS vectors and other HTML5 attack surfaces
Check if other embed types (forms, surveys) have similar vulnerabilities
Investigate whether stored XSS persists across different WordPress.com instances
Test polyglot/encoding bypass techniques (UTF-8, Base64, Unicode escapes)

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1204.001

## Notes
The vulnerability chain spans two services (Crowdsignal and WordPress.com), indicating insufficient trust boundary enforcement. The use of image onerror handler is a common XSS technique that bypasses some basic filters. The stored nature of the vulnerability means all visitors to the post are affected, not just the attacker's targets. Report lacks bounty information and appears to show redaction of additional details.

## Full report
<details><summary>Expand</summary>

## Summary:

Hi team

I found Stored XSS in wordpress.com via  app.crowdsignal.com


## Platform(s) Affected:
 wordpress.com

## Steps To Reproduce:
1 . Go to https://app.crowdsignal.com/dashboard and create a poll
2 . Put the payload as answer <img src=x onerror=alert(document.cookie)>
3.  Go to Share Your Poll and Copy  the Website Popup
4.Go to https://wordpress.com/posts add new post
5. App Website Popup 
6. Save it
7.Open the page and the XSS will fired

█████████

## Impact

The attacker can use this issue to execute malicious script code in the victim user browser also redirect the victim user to malicious sites

</details>

---
*Analysed by Claude on 2026-05-12*
