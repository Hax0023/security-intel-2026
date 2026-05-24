# Broken Access Control: Member Users Can Access Billing Page via Direct URL

## Metadata
- **Source:** HackerOne
- **Report:** 946384 | https://hackerone.com/reports/946384
- **Submitted:** 2020-07-29
- **Reporter:** jhimansh
- **Program:** Rockset
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Horizontal Privilege Escalation, Missing Authorization Check
- **CVEs:** None
- **Category:** uncategorised

## Summary
A member-level user account can access the billing page by directly navigating to the URL (https://console.rockset.com/billing?tab=payment), despite billing functionality being intentionally hidden from the member's menu. The application implements client-side access control through menu visibility but lacks server-side authorization validation, allowing unauthorized access to sensitive billing information.

## Attack scenario
1. Attacker creates or gains access to a member-level account on the Rockset platform
2. Attacker observes that the billing page is not present in the navigation menu, as intended
3. Attacker manually constructs the billing page URL (https://console.rockset.com/billing?tab=payment) based on common naming patterns
4. Attacker navigates directly to the URL by typing it into the browser address bar
5. Server accepts the request without validating role-based permissions and serves the billing page
6. Attacker gains unauthorized access to billing information, payment methods, and financial data intended only for administrators

## Root cause
The application implements access control exclusively on the client-side by hiding UI elements from the navigation menu. Server-side endpoint authorization is missing, meaning the /billing route does not validate user roles or permissions before returning sensitive billing data. This violates the principle of never trusting client-side security controls.

## Attacker mindset
Opportunistic privilege escalation through direct URL manipulation. The attacker recognized that hidden UI elements do not equal proper access control and exploited this common security misconception. The attack requires minimal technical skill but demonstrates understanding of client-side vs server-side validation.

## Defensive takeaways
- Implement server-side authorization checks on all protected endpoints before serving sensitive data
- Never rely solely on client-side UI hiding (menu visibility) for access control
- Validate user roles and permissions on the backend for every request to protected resources
- Implement consistent authorization middleware across all API endpoints and routes
- Use role-based access control (RBAC) lists to define which user roles can access specific resources
- Log and audit access attempts to sensitive resources like billing pages
- Conduct regular security testing including direct URL access attempts with various user roles
- Implement explicit 403 Forbidden responses when unauthorized users attempt to access restricted resources

## Variant hunting
Test all hidden menu items by constructing direct URLs (admin pages, settings, reports, etc.)
Attempt to access API endpoints related to billing (/api/billing, /api/payments, /api/invoices)
Check if other admin-only pages are accessible via direct URL: /admin, /settings, /organization
Test with different user roles (viewer, editor, admin) to identify other broken authorization patterns
Examine URL parameters for privilege escalation (e.g., changing user_id, org_id, role in URLs)
Fuzz the billing page URL with various tab parameters to expose additional endpoints
Check if payment method modifications or billing updates are possible, not just viewing

## MITRE ATT&CK
- T1190
- T1548

## Notes
This is a classic example of security through obscurity failure. The report demonstrates good bug bounty methodology by providing clear reproduction steps and screenshots. The vulnerability severity should potentially be elevated to High given that billing information could include credit cards, payment history, and company financial data. The remediation provided by the reporter is accurate: server-side access control validation is required.

## Full report
<details><summary>Expand</summary>

## Summary: I am writing to submit a vulnerability found at https://console.rockset.com/. I created an admin account with email himanshujoshitest2018@gmail.com and added a member with email himanshujoshitest2019@gmail.com. I logged in from the member's account and realized that the Billing page is not visible in the menu, it is hidden as per the designed privileges of a member however when I visited https://console.rockset.com/billing?tab=payment page, it did open and I could view beyond a member's privilege. I am attaching screenshots which shows two users, one is an admin and other is a member and the member is able to view the add payment method page and other information. The billing page is kept hidden from the menu but if I directly open the billing URL, i can view the page instead of it being forbidden. 

## Steps To Reproduce:
1. Invite a member with member privileges. 
2. Login at console.rocket.com using member email address.
3. You will see that the billing page is not available in the menu.
4. Directly open https://console.rockset.com/billing?tab=payment page and it will be opened from the member's account however it is hidden from the menu. The access to this page is not yet forbidden. 

Attaching screenshots for your reference. There is one screenshot of admin's page and two screenshots of member's page in which the member has opened the billing page. 

Remediation:
Check the access-control while an URL is opened. 

Thanks!

## Impact

The impact here is medium however this is a access control issue and needs fixing. The billing information is not to be accessed by a someone with a member privilege and therefore the billing page is hidden from the menu however the member can still access the information which is not meant from a member.

</details>

---
*Analysed by Claude on 2026-05-24*
