# Information Disclosure via HTML Comment Injection in Homepage Title

## Metadata
- **Source:** HackerOne
- **Report:** 57125 | https://hackerone.com/reports/57125
- **Submitted:** 2015-04-18
- **Reporter:** shhnjk
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Information Disclosure, HTML Injection, Server-Side Template Injection (SSTI), Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
An attacker can inject HTML comments into the Homepage Title field in General settings to break out of HTML context and leak sensitive data that would normally be hidden or encoded. By setting the title to '<!--' and name to '">' with HTML tags, confidential tokens and session information become exposed in the rendered homepage.

## Attack scenario
1. Attacker gains access to Shopify admin panel (via compromise or authorized access)
2. Attacker navigates to General Settings page
3. Attacker sets Homepage Title field to '<!--' (opening HTML comment)
4. Attacker sets Name field to '">' plus HTML tag content that references sensitive variables
5. When homepage renders, the comment tag breaks the template context and exposes backend variables
6. Sensitive data such as cart_token, checkout_token, email, or session_hash becomes visible in page source/DOM

## Root cause
The application fails to properly sanitize and encode user input in the Homepage Title and Name fields before rendering them in HTML context. The backend likely inserts these values directly into HTML templates without escaping special characters like < > -- ", allowing attackers to break out of the intended context.

## Attacker mindset
An attacker with admin access seeks to extract sensitive backend data that should never be exposed. By using HTML comment syntax to break template rendering, they can access internal tokens and session identifiers that could be used for further attacks or sold for profit.

## Defensive takeaways
- Implement strict input validation and sanitization for all user-controllable fields
- Use parameterized templates or templating engines that auto-escape output by default
- Apply context-aware output encoding (HTML entity encoding for HTML context)
- Validate that settings fields contain only expected character sets (alphanumeric, basic punctuation)
- Never trust user input, especially for fields that will be rendered in HTML
- Implement Content Security Policy (CSP) headers to limit impact of injection attacks
- Regular security testing including injection attack vectors (HTML, JavaScript, template injection)
- Audit all admin settings that affect page rendering for similar vulnerabilities

## Variant hunting
Test other admin settings fields (Page Title, Meta Descriptions, Footer text) with HTML comment injection
Try JavaScript event handler injection: '"><script>alert(1)</script>'
Test template expression injection: '{{ sensitive_var }}' or '${sensitive_var}'
Attempt SSTI payloads specific to backend template engine (if Liquid/Jinja2/etc.)
Try Unicode/encoding bypasses: %3C%21%2D%2D (URL encoded comments)
Test attribute breaking: '" data-x="' to inject attributes
Check if same vulnerability exists in other store settings or product/collection metadata
Verify if file upload fields have similar template injection issues

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1110: Brute Force
- T1583: Acquire Infrastructure
- T1592: Gather Victim Identity Information
- T1005: Data from Local System

## Notes
The vulnerability is particularly dangerous because it exposes cryptographic tokens (cart_token, checkout_token, session_hash) that could enable account takeover or transaction fraud. The fact that these sensitive values exist in template context suggests inadequate separation of concerns between configuration data and sensitive runtime data. Ticket reference 1559798 suggests this was tracked internally by Shopify.

## Full report
<details><summary>Expand</summary>

Hi there

Go to General setting (https://your-domain.myshopify.com/admin/settings/general), set Homepage Title to <!-- and change Name to "> plus HTML Tag like words. Some data will be leaked in the place of Title in the home page. This is dangerous because sometimes title contains highly confidential data such as cart_token, checkout_token, email, session_hash, and so on. Ticket ID is 1559798.

</details>

---
*Analysed by Claude on 2026-05-24*
