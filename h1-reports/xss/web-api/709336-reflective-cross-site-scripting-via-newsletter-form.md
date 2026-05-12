# Reflective Cross-Site Scripting via Newsletter Form on Shopify Store

## Metadata
- **Source:** HackerOne
- **Report:** 709336 | https://hackerone.com/reports/709336
- **Submitted:** 2019-10-08
- **Reporter:** gam817
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Reflective XSS, Improper Input Validation, Insufficient Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A reflective XSS vulnerability exists in the newsletter form on Shopify stores (*.myshopify.com) where unsanitized query parameters are reflected in HTML attributes without proper encoding. The vulnerability allows attackers to inject JavaScript that executes automatically on page load via crafted URLs without requiring user interaction beyond clicking a link.

## Attack scenario
1. Attacker crafts a malicious URL containing JavaScript payload in the contact[email] parameter with onfocus and autofocus attributes
2. Attacker sends the URL to target users via email, chat, or social media
3. User clicks the link believing it's legitimate
4. Malicious URL is loaded in victim's browser with active Shopify session
5. JavaScript payload executes automatically due to autofocus attribute triggering onfocus handler
6. Attacker's script can steal session cookies, perform unauthorized actions, or redirect to phishing page

## Root cause
User-supplied input from query parameters (contact[email] and form_type parameters) is reflected directly into HTML without proper sanitization or encoding. The application fails to escape special characters and HTML attributes, allowing attribute injection attacks.

## Attacker mindset
An attacker would recognize that form parameters are directly reflected in responses and test for special character handling. By injecting HTML event handlers with autofocus to bypass user interaction requirements, the attacker creates a highly effective phishing and session hijacking vector requiring only a single click from the victim.

## Defensive takeaways
- Implement robust input validation on all query parameters and form inputs
- Apply context-appropriate output encoding (HTML entity encoding for HTML context)
- Use a templating engine with automatic escaping enabled by default
- Implement Content Security Policy (CSP) headers to restrict inline script execution
- Validate and sanitize all user input before reflection, especially in HTML attributes
- Apply the principle of least privilege - disallow event handler attributes in form fields
- Use security headers like X-XSS-Protection and X-Content-Type-Options
- Conduct regular security testing including fuzzing of form parameters

## Variant hunting
Similar reflective XSS vulnerabilities likely exist in other Shopify form endpoints (contact forms, search, product filters). Attackers should fuzz all query parameters and form fields with special characters (', ", <, >, &), event handlers (onclick, onload, onerror), and encoding bypasses. Test both GET and POST methods, and check for reflected values in different HTML contexts (attributes, text nodes, JavaScript strings).

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1589

## Notes
The vulnerability is particularly dangerous because it requires no user interaction beyond clicking a malicious link (due to autofocus attribute), making it suitable for mass phishing campaigns targeting Shopify store administrators. The report demonstrates a new store vulnerability, suggesting the issue affects all Shopify stores by default. The lack of specified bounty amount may indicate either undisclosed settlement or potential issues with report handling.

## Full report
<details><summary>Expand</summary>

*.myshopify.com is vulnerable to a reflective cross-site scripting attack in the newsletter form. This can be crafted to trigger on a page load without any further user interaction.

The following example url shows this vulnerability:
```
https://testbuguser.myshopify.com/?contact[email]%20onfocus%3djavascript:alert(%27xss%27)%20autofocus%20a=a&form_type[a]aaa
```

This was tested on a newly registered store "testbuguser.myshopify.com"

If you require any additional details, please do not hesitate to bump.

## Impact

This attack could be leveraged to compromise administrative sessions or perform actions on behalf of users with the same level of privilege as the user.

</details>

---
*Analysed by Claude on 2026-05-12*
