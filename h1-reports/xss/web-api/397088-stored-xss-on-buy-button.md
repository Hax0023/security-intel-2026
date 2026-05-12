# Stored XSS on Buy Button via Currency Formatting

## Metadata
- **Source:** HackerOne
- **Report:** 397088 | https://hackerone.com/reports/397088
- **Submitted:** 2018-08-19
- **Reporter:** tony_tsep
- **Program:** HackerOne (specific program not disclosed in excerpt)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the currency formatting settings where administrative users can inject malicious JavaScript through the 'HTML with currency' field. The payload executes when the buy button is rendered, allowing account takeover of other users.

## Attack scenario
1. Attacker gains access to staff/admin account or compromises one
2. Navigate to Settings > General > Store currency settings
3. Inject XSS payload in 'HTML with currency' formatting field (e.g., '€{{amount}} "><img src=x onerror=prompt(document.domain)>')
4. Payload is stored in application database without sanitization
5. When any user views the buy button, the stored JavaScript executes in their browser
6. Attacker can steal session tokens, redirect to phishing page, or perform actions as the victim

## Root cause
The application fails to properly sanitize and encode user input in currency formatting settings. While the {{amount}} template variable is replaced, the surrounding HTML is rendered without escaping, allowing arbitrary HTML/JavaScript injection. Output encoding is not applied when rendering the currency format on the buy button.

## Attacker mindset
A malicious staff member or account compromiser exploits administrative privileges to inject persistent XSS. The attacker recognizes that currency formatting touches multiple user-facing elements and uses template syntax context to bypass basic filters.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-supplied content, especially in admin/settings panels
- Apply output encoding (HTML entity encoding) to all dynamic content regardless of source
- Use a templating engine that enforces automatic escaping by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Validate and whitelist allowed HTML tags and attributes if HTML is intentionally supported
- Apply principle of least privilege - restrict currency formatting changes to minimal necessary roles
- Use security-focused templating (e.g., Jinja2 with autoescape, Handlebars with escaping)
- Implement regular security testing of all admin/settings functionality

## Variant hunting
Check other formatting fields (tax, discount, product descriptions) for similar XSS
Test other admin settings panels that accept user input (email templates, notifications, branding)
Examine any field accepting template syntax ({{variable}}) for context-based escaping bypasses
Search for other places buy button currency formatting is rendered
Test if payload executes differently in different contexts (email, PDF, dashboard)
Check for similar vulnerabilities in user-editable content that affects multiple accounts

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Phishing for Information: Spearphishing Link
- T1539 - Steal Web Session Cookie
- T1056.004 - Interaction with User: Web
- T1204.001 - User Execution: Malicious Link

## Notes
This is a privilege escalation + persistence vulnerability. Staff account compromise leads to widespread impact. The template syntax ({{amount}}) likely triggered false sense of security, assuming only variable substitution would occur. Severity depends on whether staff-only features can impact regular users (which they can via stored XSS on public buy button).

## Full report
<details><summary>Expand</summary>

I found an XSS vulnerability on buy button.
**Steps to reproduce**
Go to Settings > General > Store currency > Change formatting and add on "HTML with currency" the payload `€{{amount}} "><img src=x onerror=prompt(document.domain)>`
After that go to buy button and you will see that the payload triggers there.

## Impact

A staff member can takeover another account.

</details>

---
*Analysed by Claude on 2026-05-12*
