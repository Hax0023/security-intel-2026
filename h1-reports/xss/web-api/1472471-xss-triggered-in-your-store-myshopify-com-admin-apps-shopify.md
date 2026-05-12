# Stored XSS in Shopify Email Editor Template Branding

## Metadata
- **Source:** HackerOne
- **Report:** 1472471 | https://hackerone.com/reports/1472471
- **Submitted:** 2022-02-06
- **Reporter:** danishalkatiri
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS), Stored XSS, Input Validation Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability was discovered in the Shopify Email app's template branding editor where user-supplied input containing HTML/JavaScript payloads was not properly sanitized before being saved and executed. An attacker could inject malicious scripts through the template branding configuration that would execute in the context of the Shopify admin panel when the template is viewed.

## Attack scenario
1. Attacker gains access to a Shopify store's admin panel (either as authorized user or via account compromise)
2. Attacker navigates to the Shopify Email app's template branding configuration page
3. Attacker enters a malicious payload (e.g., '<img src=xx onerror=alert(document.domain)>') in the template field
4. Attacker clicks Save to persist the XSS payload to the database
5. When any user (or the attacker) selects the corresponding template ID, the stored payload executes in their browser
6. Attacker can steal session cookies, admin credentials, or perform actions on behalf of the victim

## Root cause
Insufficient input validation and output encoding in the template branding editor. User-supplied input was stored in the database without proper sanitization, and was later rendered without HTML entity encoding or Content Security Policy protections.

## Attacker mindset
An attacker with admin access seeks to escalate privileges or persist access by injecting malicious scripts that execute whenever the affected template is accessed. This could be leveraged to steal authentication tokens or compromise other admin accounts.

## Defensive takeaways
- Implement strict input validation on all user-supplied fields in the template editor
- Apply HTML entity encoding to all user input before rendering in HTML context
- Use Content Security Policy headers to prevent inline script execution
- Implement a whitelist-based HTML sanitization library (e.g., DOMPurify) for user-generated content
- Apply output encoding contextually based on where data will be rendered (HTML, JavaScript, URL, CSS)
- Conduct security code review of all template/editor functionality in the Shopify Email app
- Implement automated XSS detection in the SDLC pipeline

## Variant hunting
Check other template configuration fields for similar XSS vulnerabilities
Test template preview/rendering functionality for reflected XSS
Examine email template HTML generation for injection points
Review other Shopify app editors for similar stored XSS patterns
Test dynamic template variables (F-tags) for XSS exploitation
Check for XSS in email subject, from name, and reply-to fields

## MITRE ATT&CK
- T1190
- T1598
- T1566

## Notes
The report contains redacted content (indicated by symbols like ███ and ██████████). The vulnerability appears to affect stored data using field identifiers like F1607675 and F1607682, suggesting a parameterized template system. The attack requires prior admin access but creates a persistent threat affecting all users who interact with the compromised template.

## Full report
<details><summary>Expand</summary>

Hi team,
I have found `Store` Xss in shopify-email

#Reproduction Instructions /
1.Configure `shopify-email` for Shopify stores at https://apps.shopify.com/shopify-email
2.Goto `Your-store.myshopify.com/admin/apps/shopify-email/template-branding` 
3.Change F1607675 with "><img src=xx onerror=alert(document.domain)> click `Save`.
4.Now Select any F1607682.
#██████████

#Proof of Concept
███
████

## Impact

Stored XSS triggered.

</details>

---
*Analysed by Claude on 2026-05-12*
