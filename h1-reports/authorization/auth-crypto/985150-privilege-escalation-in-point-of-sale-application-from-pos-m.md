# Privilege Escalation in POS Application via Nested Navigation to Admin Panel

## Metadata
- **Source:** HackerOne
- **Report:** 985150 | https://hackerone.com/reports/985150
- **Submitted:** 2020-09-18
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Privilege Escalation, Broken Access Control, Insecure Direct Object References (IDOR), Authentication Bypass
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A staff member with limited 'Manage Staff Role' permissions in the Point of Sale application can escalate privileges to full admin access by navigating through embedded management links and nested role pages. This allows unauthorized access to sensitive store owner functions including staff management, login service updates, and shop ownership transfer.

## Attack scenario
1. Attacker gains physical access to POS terminal with limited 'Manage Staff Role' credentials
2. Attacker modifies a full-permissions staff member's PIN through the Staff management interface
3. Attacker locks the application and logs back in with the modified PIN, obtaining full permissions
4. Attacker navigates to Staff > Edit POS APP ACCESS > Manage POS Roles to access role management
5. Attacker clicks through nested links: View Full Permissions role > Assigned Staff > Manage Shopify Admin Access
6. Attacker reaches Plan & Permissions admin panel via breadcrumb navigation, gaining access to ownership transfer and other store owner features

## Root cause
Insufficient access control validation on navigation between POS application and admin panel. The application fails to verify that the user's current permission context should allow navigation to sensitive admin pages. Nested links and breadcrumb navigation bypass role-based access controls by allowing traversal from restricted POS interface to unrestricted admin sections.

## Attacker mindset
Opportunistic insider threat with physical access to POS terminal. Exploits trust placed in limited-role staff by discovering unintended navigation paths. Seeks to escalate from operational role to administrative control for shop takeover or data theft.

## Defensive takeaways
- Implement strict server-side access control verification on all admin panel endpoints, regardless of navigation source
- Segregate POS application from admin panel with hard security boundaries; disable embedded navigation links to sensitive areas
- Validate user permissions at each breadcrumb/navigation click rather than relying on embedded links
- Enforce separate authentication contexts between POS and admin panels; do not allow permission inheritance across application boundaries
- Implement audit logging for all privilege escalation attempts and cross-application navigation
- Require additional authentication factors (e.g., owner password) for sensitive operations like ownership transfer, even from authenticated sessions
- Conduct security review of all nested role management interfaces and embedded admin links
- Implement physical security controls for POS terminals to limit unauthorized access attempts

## Variant hunting
Check other embedded management links within POS for similar navigation bypasses to restricted admin pages
Test breadcrumb navigation on other admin panels to see if they bypass role-based access controls
Investigate whether other restricted staff roles can reach sensitive admin areas through similar nested link chains
Look for other embedded iframe or nested application links that might allow privilege escalation
Test if modifying staff member permissions through POS interface bypasses owner-level approval requirements
Check whether direct URL manipulation to admin endpoints bypasses POS permission restrictions

## MITRE ATT&CK
- T1078 - Valid Accounts (using legitimate staff credentials with escalated privileges)
- T1021.001 - Remote Services: Remote Desktop Protocol (physical POS access)
- T1548.004 - Abuse Elevation Control Mechanism: Bypass User Account Control (privilege escalation)
- T1647 - Preamble (privilege escalation through UI navigation)
- T1199 - Trusted Relationship (exploiting trust in staff role)
- T1021 - Remote Services (accessing admin panel from restricted POS context)

## Notes
Report demonstrates critical security flaw in application architecture. The vulnerability chains multiple control failures: inadequate role-based access control, insufficient context validation across application boundaries, and unprotected navigation paths. The physical access requirement and knowledge of staff credentials somewhat limits exposure, but the severity remains critical due to potential shop ownership transfer. Report references HackerOne report 985150 on Shopify bug bounty program.

## Full report
<details><summary>Expand</summary>

I was playing a bit with the Point Of Sale application and it came to my attention that it is possible to navigate from the Point Of Sale Application up to the Plan & Permission in the admin. I am not sure if this is  intentional, but since it leads to potentially take over a shop, I'm reporting it.

Within he Point Of Sale application, a staff with full admin permissions can open the Point Of Sale channel using the embedded **Magage POS roles** link. By doing so and by using some nested links, it is possible to navigate up to the Plan & Permissions admin view giving him access to some store owner permissions:
 1. Add staff account
 1. Manage staff account
 1. Update login service
 1. Transfer ownership (requires the shop owner password but could be used to bypass the 2FA protection)

Given that, a POS staff with only Manage Role could escalate his privileges up to Full Permissions and potentially even take over the shop if knows the admin password.

## Steps to reproduce
1. Create a Staff with Full Permissions
1. Create a POS user with only Manage Staff permissions
1. From the Point Of Sale Application, log-in with the admin user then enter the PIN of the POS User from Step 2
1. Go to **Staff**, select the staff with Full Permissions from Step 1 and change its PIN to 1234
1. Lock the application screen and log back in using the 1234 PIN, giving you Full Permissions access within the Application
1. Go to **Staff**, select any staff, edit its **POS APP ACCESS** and click on **Manage POS Roles**
1. From the Roles listing page, open the Full Permissions staff's role and scroll at the bottom down so you can see the **Assigned Staff** section and click on the Staff
1. Scroll at the bottom again and click on **Manage Shopify admin access**, this is opening up the staff page from **Plan and Permissions**.
1. At the top of the page, click on breadcrumb navigation **Plan and Permissions** link bringing you to the `https://shop.myshopify.com/admin/settings/account`

At this point, as the Point Of Sale application is using the physically authenticated user, you're given access to store owner features as mentioned earlier.

## Impact

A staff with **Manager Staff Role** within the Point Of Sale application can escalate his privilege to a Full Permission staff and could potentially transfer the shop ownership by using the **Transfer ownership** link within the **Plans & Permissions** page.

</details>

---
*Analysed by Claude on 2026-05-24*
