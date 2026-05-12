# WooCommerce: Persistent XSS via Customer Address (State/County)

## Metadata
- **Source:** HackerOne
- **Report:** 530499 | https://hackerone.com/reports/530499
- **Submitted:** 2019-04-07
- **Reporter:** foobar7
- **Program:** WooCommerce
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Output Encoding, Persistent XSS
- **CVEs:** None
- **Category:** web-api

## Summary
WooCommerce plugin version 3.5.7 fails to properly encode customer state/county information in the WordPress admin backend, allowing authenticated users to inject persistent XSS payloads. When an administrator views the compromised customer account, the malicious script executes with admin privileges, potentially leading to code execution via plugin file manipulation.

## Attack scenario
1. Attacker creates or obtains a customer account on a WooCommerce-enabled WordPress site
2. Attacker navigates to checkout or account address settings and enters malicious payload in the County/State field (e.g., '"\><img src=x onerror=alert(1) x=y)
3. Payload is stored in the database without proper sanitization
4. Administrator visits the user management page (wp-admin/users.php) and clicks on the attacker's customer profile
5. Malicious script executes in the administrator's browser context with full admin privileges
6. Attacker can steal admin credentials, modify plugin files to establish persistence, or perform arbitrary administrative actions

## Root cause
The WooCommerce plugin echoes the state/county field value directly to HTML output in the admin user edit page without applying proper output encoding functions (e.g., esc_attr(), esc_html()). The input validation filters some characters (like closing angle bracket) but insufficient filtering combined with lack of output encoding allows the bypass.

## Attacker mindset
An attacker with basic customer account access exploits the privilege gap between customer and administrator roles. By storing malicious payload in a non-obvious field (address), they evade immediate detection while targeting the administrator interface. The attack leverages the assumption that administrators are trusted users, making them less security-conscious when viewing customer details.

## Defensive takeaways
- Always apply context-appropriate output encoding (esc_attr, esc_html, esc_js) when displaying user-supplied data in HTML
- Never rely solely on input validation/filtering; implement defense-in-depth with both input sanitization and output encoding
- Audit admin pages and backend interfaces for XSS vulnerabilities, as admin users often have elevated privileges
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if encoding is missed
- Use WordPress escaping functions consistently throughout the plugin codebase
- Conduct security review of custom form fields and address-related functionality that handles user input
- Test customer-modifiable fields for stored XSS in all admin display locations

## Variant hunting
Check other address fields (postal code, city, address line 1-2) for similar encoding issues
Review order notes and customer meta fields for similar unencoded output in admin
Audit all customer-facing editable fields that appear in wp-admin output
Test billing vs shipping address fields separately for differential encoding
Check API endpoints that return customer address data for JSON context encoding
Review WooCommerce REST API endpoints for similar output encoding issues
Test other user role pages (shop manager, vendor) for similar vulnerabilities
Check invoice/receipt generation and PDF export features for persistent XSS

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1204.001
- T1059.004
- T1047

## Notes
The vulnerability requires customer account creation capability, which is common in WooCommerce installations. The CVSS score of 7.2 reflects network accessibility without authentication for the initial payload injection step (customer account creation), though exploitation of admin requires the admin to visit the user profile. The missing closing '>' character in the payload indicates WAF/filter evasion techniques were employed. This is a classic stored XSS vulnerability in a plugin with millions of installations, making it high-impact.

## Full report
<details><summary>Expand</summary>

Persistent XSS via customer address (state/county)
================================

CVSS
----

High 7.2 [CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N](https://www.first.org/cvss/calculator/3.0#CVSS:3.0/AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:N)

Description
-----------

The current version (3.5.7) of the WooCommerce WordPress plugin echoes the state/county of a customer in the admin backend without encoding, leading to persistent XSS.

For a successful attack, an attacker needs a customer account, though it is to be expected that account creation is available for users in a considerable amount of setups.

If the victim is an administrator on a default WordPress setup, an attacker can exploit the issue to gain code execution on the server by eg sending a request to edit a WordPress plugin file.

POC
---

Setup: Install the WooCommerce plugin & open registration / add a user (permissions do not matter, I used "customer"). 

To place the payload:

1. Login as a customer at http://192.168.0.101/wordpress/my-account/
2. To place a payload, either:
    - add an item to cart & proceed to checkout. Under "Billing Details", select UK as country and enter `'"><img src=x onerror=alert(1) x=y` as `County` (note the missing `>` which is required as tags are filtered).
    - Alternatively, simply change the address under account settings at `http://192.168.0.101/wordpress/my-account/edit-address/`.

To trigger the payload:

1. Go to `http://192.168.0.101/wordpress/wp-admin/users.php` and click on the customer, or directly visit `http://192.168.0.101/wordpress/wp-admin/user-edit.php?user_id=4`, where `4` is the customers ID.

## Impact

With a successful attack, an attacker can read data available to the attacked user or perform arbitrary request in the name of the attacked user. 

With a default setup, an attacker can gain code execution on the server by eg editing a WordPress plugin file.

</details>

---
*Analysed by Claude on 2026-05-12*
