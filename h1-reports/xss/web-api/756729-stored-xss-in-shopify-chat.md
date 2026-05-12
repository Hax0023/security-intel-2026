# Stored XSS in Shopify Chat via Malicious JavaScript URL

## Metadata
- **Source:** HackerOne
- **Report:** 756729 | https://hackerone.com/reports/756729
- **Submitted:** 2019-12-12
- **Reporter:** mosuan
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Unsafe URL Handling
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Shopify Chat application where malicious JavaScript URLs can be injected through chat messages and executed when clicked by users. The vulnerability allows attackers to execute arbitrary JavaScript in the context of both regular users and shop administrators through chat interactions.

## Attack scenario
1. Attacker installs or gains access to the Shopify Chat application on a target shop
2. Attacker crafts a malicious payload using javascript: protocol (e.g., 'javascript:alert(1)//https://dqdqdqdqdq.myshopify.com')
3. Attacker sends the payload as a chat message through Shopify Chat or Shopify Ping
4. The payload is stored in the application's backend without proper sanitization
5. When the shop owner or administrator views the chat message and clicks the link, the JavaScript executes
6. Attacker gains code execution in the victim's browser with their privileges (potentially admin access)

## Root cause
The Shopify Chat application fails to properly validate and sanitize user-supplied URLs in chat messages before storing them. The application does not implement proper URL scheme validation (blocking javascript:, data:, etc.) and does not encode/escape URLs for safe rendering in HTML context.

## Attacker mindset
An attacker would recognize that chat applications often transmit user-generated content without sufficient validation. By leveraging the javascript: protocol handler combined with URL encoding tricks, they can bypass basic sanitization and achieve stored XSS. The fact that administrators interact with chat makes this particularly valuable for account takeover.

## Defensive takeaways
- Implement strict URL scheme validation - whitelist only http:// and https:// protocols, reject javascript:, data:, vbscript:, and other executable schemes
- Apply proper output encoding when rendering URLs in HTML context - use HTML entity encoding and URL encoding as appropriate
- Sanitize all user-supplied input before storing in database, not just before display
- Implement Content Security Policy (CSP) headers to prevent inline script execution
- Use URL parsing libraries to validate URLs rather than regex or string matching
- Apply defense-in-depth: validate on client, sanitize on server, encode on output
- Implement security testing focused on protocol handlers in messaging applications

## Variant hunting
Look for similar issues in: other Shopify communication features (Shop Messages, Notes), third-party chat integrations (Zendesk, Intercom), any user-to-user messaging functionality that renders URLs, admin notification systems that parse user input, and webhook integrations that process and display external URLs.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1598: Phishing - Spearphishing Link
- T1566: Phishing - Phishing via Application

## Notes
This is a classic stored XSS vector that bypasses some filters by using the javascript: protocol handler. The impact is elevated because shop administrators are the likely victims, potentially leading to unauthorized access to sensitive shop data and customer information. The use of URL comments (// followed by valid domain) suggests an attempt to make the malicious URL appear legitimate.

## Full report
<details><summary>Expand</summary>

1.install app `Shopify Chat`
2.Click chat on the shop homepage or Shopify Ping to send poc `javascript:alert(1)//https://dqdqdqdqdq.myshopify.com`
3.Click url, alert
{F657395}

## Impact

1.Front end user Self-XSS
2.Administrator XSS foreground user

</details>

---
*Analysed by Claude on 2026-05-12*
