# Unauthorized Access to Packaging Slip Templates and Product/Shipping Information via Missing Authorization Controls

## Metadata
- **Source:** HackerOne
- **Report:** 423198 | https://hackerone.com/reports/423198
- **Submitted:** 2018-10-13
- **Reporter:** anshuman_bh
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Missing Authorization, Broken Access Control, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A low-privileged staff member with no assigned permissions can access and edit packaging slip templates at `/admin/settings/packing_slip_template`, bypassing authorization controls implemented elsewhere in the application. By previewing edited templates, the staff member can view sensitive product and shipping information they should not have access to.

## Attack scenario
1. Attacker creates a low-privileged staff account in a Shopify sandbox store with zero permissions assigned
2. Attacker logs in as the staff member and confirms they cannot access any store functions or data
3. Attacker directly navigates to the unprotected endpoint `/admin/settings/packing_slip_template`
4. Attacker discovers the endpoint allows editing of packaging slip templates without authorization checks
5. Attacker edits the template and uses the preview function to view product details, SKUs, and shipping information
6. Attacker could modify templates to inject malicious content or redirect customers, or exfiltrate sensitive business data

## Root cause
The `/admin/settings/packing_slip_template` endpoint lacks proper authorization controls to verify user permissions before allowing template editing and preview operations. While other areas of the application implement authorization checks, this endpoint was either overlooked during development or intentionally bypassed, creating an inconsistency in the security model.

## Attacker mindset
An insider threat or malicious staff member seeks to bypass permission restrictions to gain unauthorized access to sensitive business information (product details, shipping data) or manipulate customer communications through template editing. The attacker recognizes the authorization bypass as a simple URL navigation attack requiring no technical exploitation.

## Defensive takeaways
- Implement consistent authorization checks across all administrative endpoints, not just primary feature areas
- Use a centralized permission/authorization framework to prevent inconsistencies between endpoints
- Conduct security code review specifically for endpoints that handle sensitive data (shipping, product information)
- Implement server-side permission validation on all data preview/export functions
- Add audit logging for all template edits and sensitive data access attempts
- Regularly audit user permissions and access patterns to detect anomalies
- Apply principle of least privilege: deny access by default unless explicitly permitted
- Test all administrative endpoints with low-privilege accounts as part of security testing

## Variant hunting
Check other `/admin/settings/*` endpoints for similar authorization bypasses
Review all preview/export functionality endpoints for authorization controls
Test data export features (CSV, PDF generation) with low-privilege accounts
Examine template editing endpoints across different modules (email templates, invoice templates, etc.)
Review any direct URL navigation patterns that bypass permission checks
Test other administrative configuration endpoints that should require specific permissions

## MITRE ATT&CK
- T1190
- T1078.001
- T1087
- T1526

## Notes
This is a clear example of broken access control (OWASP A01:2021). The vulnerability is notable because it exists despite the application having a robust permission system elsewhere, suggesting either incomplete implementation or security regression. The ability to view sensitive information via preview functionality demonstrates information disclosure beyond just unauthorized editing capability. The sandbox store context provides a testing environment but the same vulnerability would be critical in production stores.

## Full report
<details><summary>Expand</summary>

Hello, 

It was observed that it is possible to edit packaging slip templates and then view the product and shipping information in the packaging slip by a low privileged staff in a sandbox store by simply navigating to the URL `https://<store>.myshopify.com/admin/settings/packing_slip_template`. It appears that this endpoint does not have the proper authorization controls implemented as is the case throughout the rest of the application. 

In order to reproduce this, please follow the steps below:

* As a Storefront Admin, create a Sandbox Store and log in to it.

* Create a bunch of products and setup the shipping information at the endpoints `/admin/products` and `/admin/settings/shipping` respectively as shown below:

{F359765}

{F359766}

* Next, add a staff for this store and do not assign any permissions to that staff at the endpoint `/admin/settings/account` as shown below:

{F359767}

* Now, in a different browser, authenticate as the staff in this sandbox store and notice that you are not allowed to do anything as the Store admin because you don't have any permissions. 

{F359768}

* Now, as the staff, navigate to the endpoint `https://<store>.myshopify.com/admin/settings/packing_slip_template`. Notice that you can *edit* and save the packing slip template. And, then you can also preview the template as shown below:

{F359770}

{F359769}

* Notice that the PDF generated from the preview has the *product* information as well as the *shipping* information

## Impact

As a low privileged staff of a sandbox store (with no permissions), you are not supposed to edit or view any information of a store, if restricted by the store admin. A malicious low privileged staff can potentially leverage this vulnerability to edit packaging slip templates which can result in unauthorized information being sent to the customer. They can also view the product and shipping information of the store that they shouldn't have been able to otherwise.

</details>

---
*Analysed by Claude on 2026-05-24*
