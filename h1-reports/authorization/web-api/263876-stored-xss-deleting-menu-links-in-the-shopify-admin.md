# Stored XSS in Shopify Admin Menu Links via Title Field

## Metadata
- **Source:** HackerOne
- **Report:** 263876 | https://hackerone.com/reports/263876
- **Submitted:** 2017-08-28
- **Reporter:** hack_im
- **Program:** Shopify
- **Bounty:** Not disclosed in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Insufficient Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in the Shopify Admin interface affecting menu creation and menu item title fields. An attacker could inject malicious JavaScript payloads that would execute in the context of any admin user viewing the affected menu, potentially leading to session hijacking or admin account compromise.

## Attack scenario
1. Attacker with store admin access navigates to the 'Add menu' section in Shopify Admin
2. Attacker injects malicious payload '// # "><svg/onload=prompt(1)>' into the Title field
3. Payload is stored in the database without proper sanitization or encoding
4. Any admin user viewing the created menu or menu items triggers the stored XSS
5. Malicious JavaScript executes in the admin's browser with their session privileges
6. Attacker gains ability to perform arbitrary admin actions, modify store settings, or steal credentials

## Root cause
The Shopify Admin application failed to properly sanitize and encode user-supplied input in the menu Title field before storing it in the database. Additionally, the output was not properly escaped when rendering the menu management interface, allowing injected SVG/JavaScript payloads to execute.

## Attacker mindset
An attacker with initial admin access (or lower privilege user) seeks to escalate impact by creating persistent malware that affects all admins viewing the menu. The use of SVG onload event handlers bypasses basic script tag filters. The comment-based payload obfuscation ('// #') suggests attempt to evade basic XSS detection patterns.

## Defensive takeaways
- Implement strict input validation using whitelisting for all user-supplied text fields, especially those stored in database
- Apply context-aware output encoding: use HTML entity encoding for HTML context, JavaScript encoding for JS context
- Employ a robust Content Security Policy (CSP) header to mitigate XSS impact even if injection occurs
- Use templating engines with auto-escaping enabled by default
- Implement security-focused code review processes specifically targeting stored XSS in admin interfaces
- Conduct regular security testing including SAST/DAST tools configured to detect stored XSS patterns
- Apply the principle of least privilege - limit admin capabilities by role and function
- Sanitize input using established libraries (DOMPurify, OWASP ESAPI) rather than custom filters

## Variant hunting
Check other title/name fields in Shopify Admin (product titles, collection names, customer groups, discount codes)
Test menu description fields, subtitle fields, or any rich-text editors in admin interface
Examine permission/role management interfaces for similar injection points
Test special characters and event handlers: onmouseover, onerror, onchange, onclick
Verify if the vulnerability affects different input types: file names, API credentials descriptions, webhook titles
Check if SVG/XML payloads work in other contexts (img src, iframe src attributes)
Test polyglot payloads combining multiple formats to bypass filters

## MITRE ATT&CK
- T1190
- T1204.001
- T1598.003
- T1566.002
- T1021.004

## Notes
The reporter provided limited technical detail but included a PoC video. The payload uses SVG onload handler which is more reliable than traditional script tags for bypassing basic filters. The vulnerability affects multiple fields ('Add menu Title' and 'Menu Item Title'), suggesting a systemic encoding issue across the menu management feature. This is a critical finding for admin interfaces as it enables lateral privilege escalation and persistence. The use of a public mirror URL in the report is concerning for responsible disclosure practices.

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
*Analysed by Claude on 2026-05-24*
