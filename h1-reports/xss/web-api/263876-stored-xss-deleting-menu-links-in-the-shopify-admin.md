# Stored XSS in Shopify Admin Menu Links via Title Fields

## Metadata
- **Source:** HackerOne
- **Report:** 263876 | https://hackerone.com/reports/263876
- **Submitted:** 2017-08-28
- **Reporter:** hack_im
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Shopify Admin panel where user-supplied input in menu and menu item title fields is not properly sanitized or encoded before being rendered. An attacker can inject malicious SVG/JavaScript payloads through the 'Title in Add menu' and 'Menu Item Title' fields that execute when the menu is viewed by any user.

## Attack scenario
1. Attacker logs into or gains access to a Shopify store's admin panel
2. Attacker navigates to the menu management section and creates a new menu or menu item
3. Attacker enters malicious payload in the Title field: // # "><svg/onload=prompt(1)>
4. The payload is stored in the database without proper sanitization
5. When any admin user views the menu or menu items, the JavaScript payload executes in their browser context
6. Attacker can escalate to session hijacking, account takeover, or privilege escalation depending on admin permissions

## Root cause
Shopify failed to implement proper input validation and output encoding for the menu title fields in the admin panel. The application stores user input directly without sanitization and renders it without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
An attacker with admin/editor access to a Shopify store could exploit this to compromise other administrators or gain persistence. This could be used for account takeover, data exfiltration, or malicious admin actions on behalf of compromised accounts.

## Defensive takeaways
- Implement strict input validation on all user-supplied data with whitelisting of allowed characters
- Apply HTML entity encoding to all user-controlled output before rendering in HTML context
- Use Content Security Policy (CSP) headers to prevent inline script execution
- Sanitize input using well-tested libraries (DOMPurify, bleach) rather than regex patterns
- Implement Context-Aware Output Encoding (encode differently for HTML, JavaScript, URL contexts)
- Add server-side validation in addition to client-side checks
- Implement security headers like X-XSS-Protection and X-Content-Type-Options
- Use templating engines with auto-escaping enabled by default

## Variant hunting
Check all other title/name fields in menu management (descriptions, URLs)
Test other admin panel sections that accept user input (product titles, collection names, page content)
Check if issue affects customer-facing menus or only admin panel
Test comment fields, notes, or metadata fields in related features
Examine bulk upload/import features for CSV/JSON injection possibilities
Test for DOM-based XSS in JavaScript that handles menu data client-side

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1204

## Notes
Report lacks detail and appears to rely on video PoC for explanation. The payload uses SVG onload handler to bypass basic XSS filters. The storage in database and persistence across sessions makes this Stored XSS rather than Reflected. Attack requires authenticated access but impacts all users viewing the menu. The mirror Shopify store provided suggests the vulnerability was reproduced on a test environment.

## Full report
<details><summary>Expand</summary>

Hello Team,

I found a stored xss issue.

PoC (unlisted): https://youtu.be/MjnKyFgqTTo

watch my PoC than you'll understood everything.

Payloads: // # "><svg/onload=prompt(1)>

Looks Like this issue available at " Title in Add menu " and also available at "Title" in " Menu Item "

Mirror: https://azizvai.myshopify.com/

Thanks

</details>

---
*Analysed by Claude on 2026-05-12*
