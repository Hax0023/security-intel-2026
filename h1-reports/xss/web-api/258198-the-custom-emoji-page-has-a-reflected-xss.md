# Reflected XSS in Custom Emoji Page Flash Message

## Metadata
- **Source:** HackerOne
- **Report:** 258198 | https://hackerone.com/reports/258198
- **Submitted:** 2017-08-09
- **Reporter:** co3k
- **Program:** Slack
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Reflected Cross-Site Scripting (XSS), Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflected XSS vulnerability exists on Slack's custom emoji customization page where the 'name' parameter is improperly sanitized when building flash messages. An attacker can inject arbitrary JavaScript code that executes in the victim's browser by crafting a malicious URL.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the 'name' parameter of the emoji customization page
2. Attacker sends the URL to a Slack user via phishing email, chat message, or other social engineering vector
3. Victim clicks the link while authenticated to Slack
4. The crafted 'name' parameter value is reflected in the flash message without proper HTML encoding
5. Victim's browser executes the injected JavaScript code in the context of the Slack domain
6. Attacker can steal session tokens, perform actions on behalf of the user, or harvest sensitive information

## Root cause
The application fails to properly encode or sanitize user-supplied input (the 'name' parameter) before including it in the flash message response. The input is directly interpolated into HTML context without escaping special characters like quotes and angle brackets.

## Attacker mindset
An attacker recognizes that success messages and flash notifications often display user input with minimal validation. By manipulating the 'name' parameter, they can break out of the expected string context and inject script tags. The use of URL encoding (%2F for /) attempts to bypass basic filters.

## Defensive takeaways
- Implement proper output encoding for all user-supplied data based on context (HTML, JavaScript, URL, CSS)
- Use established templating engines that auto-escape by default rather than manual string concatenation
- Apply Content Security Policy (CSP) headers to restrict inline script execution
- Validate and sanitize all query parameters and user input on both client and server side
- Implement allowlist-based validation for emoji names to restrict to expected characters
- Use HTTP-only and Secure flags on session cookies to prevent XSS token theft

## Variant hunting
Test other parameters on the emoji customization page (description, category, etc.) for similar XSS
Check admin and workspace settings pages for reflected XSS in flash messages
Test file upload features where filenames might be reflected in success messages
Examine error messages and validation feedback for reflected user input
Test other Slack customization pages (themes, apps, integrations) for the same pattern

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing
- T1566 - Phishing
- T1539 - Steal Web Session Cookie

## Notes
This is a classic reflected XSS vulnerability exploitable through URL manipulation. The flash message context is particularly dangerous as these are often displayed prominently without sanitization. The vulnerability requires user interaction (clicking the link) but social engineering makes this reliably achievable. The use of URL encoding in the PoC suggests potential filter evasion attempts.

## Full report
<details><summary>Expand</summary>

The Custom Emoji Page has a Reflected XSS in building flash message.

The following is the PoC.
https://{team}.slack.com/customize/emoji?added=1&name=vuln"><script>alert(0);<%2Fscript>

</details>

---
*Analysed by Claude on 2026-05-12*
