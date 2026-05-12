# DOM-based Stored XSS in WooCommerce Order Page (State Field)

## Metadata
- **Source:** HackerOne
- **Report:** 507139 | https://hackerone.com/reports/507139
- **Submitted:** 2019-03-09
- **Reporter:** wild0ni0n
- **Program:** WooCommerce
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Stored XSS, DOM-based XSS, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored DOM-based XSS vulnerability exists in WooCommerce 3.5.6 where the `_shipping_state` and `_billing_state` fields in order pages fail to properly escape user input before rendering. An attacker can inject malicious JavaScript that executes whenever an admin views or edits the affected order.

## Attack scenario
1. Attacker with access to create/edit orders (e.g., compromised low-privilege account or via another vulnerability) navigates to WooCommerce order creation/edit page
2. Attacker clicks the pencil icon to expand Billing or Shipping section and selects a country
3. Attacker inputs JavaScript payload in the State field: "><img src=/ onerror="alert(location.host)"
4. Attacker saves the order by clicking Create or Update button, storing the malicious payload in the database
5. When an admin or authorized user navigates to edit this order, the stored JavaScript payload executes in their browser context
6. Attacker can steal admin session tokens, modify orders, create rogue admin accounts, or perform other actions with admin privileges

## Root cause
The WooCommerce plugin fails to properly escape/sanitize the `_shipping_state` and `_billing_state` field values when outputting them to the HTML DOM in the order edit page. The data is retrieved from the database and rendered directly into HTML attributes or content without applying appropriate escaping functions (e.g., esc_attr(), esc_html()).

## Attacker mindset
An attacker with order management permissions seeks to escalate privileges or compromise admin accounts by injecting persistent malicious code. The stored nature makes this particularly dangerous as it affects any admin viewing the order. This could be a malicious shop manager targeting site owners, or part of a supply-chain attack on WordPress/WooCommerce installations.

## Defensive takeaways
- Always escape output based on context (esc_attr for attributes, esc_html for content, wp_json_encode for JSON)
- Implement strict input validation for state/region fields - consider using predefined lists from geolocation libraries
- Apply Content Security Policy (CSP) headers to restrict inline script execution
- Perform security code review of all form handling, especially admin pages dealing with orders and sensitive data
- Use WordPress sanitization functions during both input (sanitize_text_field) and output stages
- Implement automated security testing in CI/CD pipeline to catch XSS before release
- Restrict order editing capabilities via role-based access control (RBAC)

## Variant hunting
Check other select/dropdown fields in WooCommerce (product categories, customer roles, etc.) for similar unescaped output
Search for similar patterns in billing address, shipping address, and customer profile pages
Test all custom meta fields in orders that accept user input and are displayed in admin
Examine product variations, coupon fields, and tax settings for identical vulnerabilities
Check WooCommerce extensions and plugins that add custom order fields
Review other WordPress plugins using similar state/country selection patterns

## MITRE ATT&CK
- T1190
- T1566
- T1204
- T1059

## Notes
This is a classic stored XSS that combines poor output encoding with admin panel access. The vulnerability requires some level of order management access, making it most dangerous with compromised shop manager accounts. The use of img tag with onerror handler demonstrates a common XSS bypass technique. WooCommerce should have used wp_kses_post() or appropriate esc_* functions when rendering these fields.

## Full report
<details><summary>Expand</summary>

I have found a stored DOM based XSS in the order page at WooCommerce 3.5.6.

The Data input from HTML element name `_shipping_state` and `_billing_state` in order page outputs data without escaping.When the victim read the page containing the payload, it executes the script.

# Steps to reproduce

1. From a Wordpress admin menu, naavigate to WooCommerce page.
2. Click to `Add order` (Or select to the exist order data, navigate to edit page.)
3. Click to pencil icon of  `Billing` or `Shipping` items, and expand input form.
4. Select to  `Select a country...` by Country item.
5. Input following value in State / Country item.

> "><img src=/ onerror="alert(location.host)"

6. Click Create button.(If navigated from the exist order, click update.)
7. Navigate to edit page, after then an alert displayed.
See also attached screenshot.

The security impact is the same as any typical XSS.

## Impact

The security impact is the same as any typical XSS.

</details>

---
*Analysed by Claude on 2026-05-12*
