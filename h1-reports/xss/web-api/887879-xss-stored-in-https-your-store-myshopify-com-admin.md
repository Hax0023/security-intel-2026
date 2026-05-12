# Stored XSS in Shopify Admin Menu Items

## Metadata
- **Source:** HackerOne
- **Report:** 887879 | https://hackerone.com/reports/887879
- **Submitted:** 2020-05-31
- **Reporter:** lbro
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cross-Site Scripting (XSS) - Stored, Input Validation Bypass, Output Encoding Failure
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the Shopify admin menu creation interface where user-supplied input is not properly sanitized before storage and display. An attacker can inject malicious JavaScript through menu item names that executes in the context of any admin user viewing the menu management page.

## Attack scenario
1. Attacker accesses the Shopify store admin panel at /admin/menus/new
2. Attacker clicks 'Add menu item' button to create a new menu entry
3. Attacker inputs malicious payload in the menu item name field: "><img src="x" onerror="alert(document.cookie)">
4. Attacker provides a legitimate URL in the link field and clicks 'Add'
5. Attacker clicks 'Remove item' or navigates to trigger re-rendering of the menu interface
6. JavaScript payload executes in admin browser context, exfiltrating session cookies or performing unauthorized actions

## Root cause
The menu item name parameter is stored in the database without HTML entity encoding or sanitization. When the menu management interface renders stored menu items, the data is output directly into the DOM without proper escaping, allowing embedded HTML/JavaScript to execute.

## Attacker mindset
Opportunistic vulnerability hunter targeting admin interfaces where stored XSS can affect high-privilege users. Discovered input validation gap through basic payload injection testing in user input fields.

## Defensive takeaways
- Implement input validation to reject or sanitize HTML/JavaScript metacharacters in all user inputs
- Apply context-aware output encoding (HTML entity encoding) when rendering user-supplied data in HTML context
- Use templating engines with auto-escaping enabled by default
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Perform security code review of all admin panel input/output handling
- Add automated security testing for XSS in form submission workflows

## Variant hunting
Check similar admin interfaces: product descriptions, collection names, page titles, customer notes, order comments, and any other rich-text or user-input fields that may be persisted and displayed to authenticated users

## MITRE ATT&CK
- T1190
- T1566
- T1566.002

## Notes
Report quality is poor with minimal detail and grammar issues, but the vulnerability is clearly valid. PoC video referenced but not included in writeup. This affects store owners' admin accounts, potentially allowing session hijacking or account compromise through cookie theft.

## Full report
<details><summary>Expand</summary>

hello , 
i fond xss stored in  https://your store.myshopify.com/admin/
steps ;
1. go to ```https://swqdewd.myshopify.com/admin/menus/new```
2. click in Add menu item
3. add name ```"><img src="x" onerror="alert(document.cookie)">``` AND any link 
4. now click add 
5. click in remove item 
6. alert 
7. watch the vedio poc for more information

## Impact

xss attack .....

</details>

---
*Analysed by Claude on 2026-05-12*
