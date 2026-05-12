# XSS in Shopify Email App via Code Copy Functionality

## Metadata
- **Source:** HackerOne
- **Report:** 1339356 | https://hackerone.com/reports/1339356
- **Submitted:** 2021-09-14
- **Reporter:** shaktiranjan867
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Cross-Site Scripting (XSS), Code Injection, DOM-based XSS
- **CVEs:** None
- **Category:** web-api

## Summary
A DOM-based XSS vulnerability exists in the Shopify Email app editor where malicious JavaScript payloads injected into email fields (subject, preview text, or body) are executed when the content is copied to clipboard. The vulnerability bypasses initial execution checks but triggers when the code is extracted, suggesting improper sanitization during copy operations.

## Attack scenario
1. Attacker navigates to Shopify Email app editor endpoint
2. Attacker inputs XSS payload like '/><img src=x onerror=alert(document.domain)>' into email subject, preview text, or body fields
3. Payload is stored without immediate execution, appearing to be safely sanitized
4. Attacker selects and copies the malicious code from the editor interface
5. Copy operation triggers JavaScript execution via clipboard API or DOM manipulation
6. Attacker gains ability to execute arbitrary scripts in victim's browser context, potentially stealing session tokens or performing unauthorized actions

## Root cause
Improper input sanitization and output encoding in the email editor component. The application likely sanitizes HTML on initial render but fails to re-sanitize content during copy/paste operations. The copy functionality may directly access unsanitized DOM nodes or use unsafe methods to transfer content to clipboard without proper escaping.

## Attacker mindset
An attacker discovered that Shopify's sanitization only applies at display time. By triggering a copy operation, they bypass the sanitization layer, likely because the clipboard interaction accesses raw DOM content or uses an unsafe API. This represents a classic case of trusting client-side sanitization without proper output encoding at every interaction point.

## Defensive takeaways
- Implement server-side input validation and sanitization, not relying solely on client-side filters
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize content at every output point, including clipboard operations and copy events
- Use safe clipboard APIs that escape or encode content before transfer
- Apply HTML entity encoding to all user-supplied content rendered in HTML context
- Implement proper output encoding for different contexts (HTML, JavaScript, CSS, URL)
- Use security libraries like DOMPurify for robust HTML sanitization
- Test XSS payloads across all user interaction patterns, not just initial input

## Variant hunting
Test XSS payloads in paste operations (Ctrl+V) to see if sanitization differs
Try SVG-based payloads in copy operations: '<svg onload=alert(1)>'
Test event handlers in different contexts: oncopy, onpaste, ondrag, ondrop
Attempt payload mutation during clipboard operations using different encoding
Check if other email fields (from, to, cc, bcc) have similar vulnerabilities
Test in different browsers to see if native clipboard handling varies
Try bypassing with Unicode/encoding variations before copying
Test persistence: does the XSS execute when the email is reopened?

## MITRE ATT&CK
- T1190
- T1566
- T1204.001

## Notes
This is a interesting polyglot vulnerability combining DOM-based XSS with clipboard API interactions. The fact that sanitization appears to work until copy is triggered suggests either a race condition or different code paths for display vs. clipboard handling. The reporter's observation about 'it's not executing directly but when copying' is crucial context indicating context-aware sanitization bypass. The endpoint structure (s1-aug.myshopify.com/admin/apps/shopify-email/editor/) suggests this is in a restricted admin area, limiting exposure but still allowing account compromise if attacker has editor access.

## Full report
<details><summary>Expand</summary>

Hello Team,
i have found a Xss on the Shopify email app, but it's a bit wired, it's not executing directly but when i am coping the code it is getting executed.

step-1:  Navigate to https://s1-aug.myshopify.com/admin/apps/shopify-email/editor/3694417
step-2:  Add the xss pay load anywhere  like subject, preview text or in the selection body section. "/><img src=x onerror=alert(document.domain)>
step-3: copy the written code

Xss will be fired.

## Impact

Code injection leads to xss

</details>

---
*Analysed by Claude on 2026-05-12*
