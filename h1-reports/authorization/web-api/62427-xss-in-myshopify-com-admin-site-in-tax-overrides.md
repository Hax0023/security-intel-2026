# Stored XSS in Tax Overrides via Collection Names on myshopify.com Admin

## Metadata
- **Source:** HackerOne
- **Report:** 62427 | https://hackerone.com/reports/62427
- **Submitted:** 2015-05-14
- **Reporter:** nismo
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Stored Cross-Site Scripting (XSS), Improper Input Validation, Improper Output Encoding
- **CVEs:** None
- **Category:** web-api

## Summary
A stored XSS vulnerability exists in the myshopify.com admin tax overrides feature where user-supplied collection names containing JavaScript payloads are not properly sanitized or encoded. When a user attempts to delete a tax override, the unsanitized collection name is reflected in the DOM, executing arbitrary JavaScript in the admin context.

## Attack scenario
1. Attacker creates a product collection with a name containing XSS payload: "><IMG SRC=x onerror=prompt(7)>
2. Attacker navigates to Settings > Taxes and selects 'Add a tax override'
3. Attacker selects 'Add Tax Override for Rest of World' and chooses the malicious collection from the dropdown
4. System stores the tax override configuration without sanitizing the collection name
5. Attacker triggers the 'Delete Entire Override' (delete/recycle bin button)
6. Malicious collection name is rendered unsafely in the delete confirmation dialog, executing the XSS payload

## Root cause
The tax override deletion interface fails to HTML-encode or sanitize the collection name parameter before rendering it in the DOM. The collection name, which was previously stored without validation, is output directly into the page when the delete action is triggered.

## Attacker mindset
An authenticated admin user seeks to escalate privileges or steal session tokens from other admins. By exploiting the tax override feature, they can inject persistent XSS that triggers when other admins attempt to manage tax settings. The attack chain demonstrates reconnaissance of input vectors and understanding of Shopify's admin interface.

## Defensive takeaways
- Implement strict input validation on all user-supplied data, including collection names, at the point of creation
- Apply HTML entity encoding (e.g., htmlspecialchars, encodeHTMLEntities) to all user-controlled data before rendering in HTML context
- Use parameterized rendering or template engines that auto-escape by default
- Validate that collection names match expected format constraints (alphanumeric, hyphens, spaces only)
- Implement Content Security Policy (CSP) headers to mitigate XSS impact
- Apply defense-in-depth: sanitize both on input and output stages
- Conduct security code review of admin interface components handling user-generated content

## Variant hunting
Search other Shopify admin settings pages for similar patterns: discounts, shipping overrides, custom fields that accept user input and later display in modals/dialogs
Test other dropdown/select components that may store and re-render collection or product names
Check webhook payload displays and admin notifications for similar issues
Review all admin pages where deletions trigger confirmation dialogs displaying stored data
Test tax configurations with other special characters and encoding bypasses (SVG, iframe payloads)
Look for similar issues in other Shopify admin features using collection selection patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1598 - Phishing - Spearphishing Link (to trick other admins into clicking malicious links containing XSS context)
- T1539 - Steal Web Session Cookie (via XSS payload harvesting admin session tokens)

## Notes
This is a classic stored XSS vulnerability in a second-order context. The payload is stored when creating the collection, but only triggers when rendered during the tax override deletion flow. The vulnerability likely affects any admin user with access to tax settings. Low CVSS scoring would be incorrect given the admin context and potential for session hijacking. The simplicity of the POC (basic IMG tag payload) suggests the application has minimal security controls on output encoding.

## Full report
<details><summary>Expand</summary>

POC:
If you create a collection such as "><IMG SRC=x onerror=prompt(7)> and then go to Settings / Taxes and select "Add a tax override" then on the "Add Tax Override for Rest of World" select the previously created collection of "><IMG SRC=x onerror=prompt(7)> you can see it on the screen (addtax.png).

If you press the recycle bin "Delete Entire Override" (delete.png) then  XSS is happening (xss.png)

Thanks


</details>

---
*Analysed by Claude on 2026-05-24*
