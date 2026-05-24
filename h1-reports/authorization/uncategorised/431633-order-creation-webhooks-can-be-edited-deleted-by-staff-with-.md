# Order Creation Webhooks can be edited/deleted by STAFF with `Settings` only permission

## Metadata
- **Source:** HackerOne
- **Report:** 431633 | https://hackerone.com/reports/431633
- **Submitted:** 2018-10-31
- **Reporter:** h13-
- **Program:** Shopify Bug Bounty Program
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authorization/Access Control, Privilege Escalation, Inconsistent Permission Enforcement
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with only the 'Settings' permission is restricted from creating Order-related webhooks but can modify and delete Order Creation webhooks that were previously created by authorized users. This inconsistency allows unauthorized staff to alter critical order notification configurations, potentially disrupting business workflows or enabling attacks.

## Attack scenario
1. Owner assigns 'Settings' only permission to a staff member who should not have order management capabilities
2. Owner creates a webhook for 'Order Creation' events pointing to a legitimate external service URL
3. Staff member logs into the admin dashboard and navigates to Settings > Notifications
4. Staff member identifies and clicks on the Order Creation webhook, opening the edit modal
5. Staff member modifies the webhook URL to point to an attacker-controlled server
6. Attacker receives all order creation events with sensitive order data (customer info, payment details, items ordered) that they should not have access to

## Root cause
The authorization check for webhook creation ('POST' requests creating new webhooks) is properly implemented to verify the user has 'Orders' permission in addition to 'Settings'. However, the authorization checks for webhook modification ('PUT/PATCH') and deletion ('DELETE') operations on existing webhooks only verify 'Settings' permission, creating a privilege escalation gap.

## Attacker mindset
An insider threat actor or compromised staff account could exploit this to redirect sensitive order notifications to attacker infrastructure without creating audit trails of permission violations. The attacker gains access to order data they shouldn't have permission to see, while appearing to be performing legitimate administrative tasks.

## Defensive takeaways
- Apply consistent authorization logic across all CRUD operations - if 'Orders' permission is required to CREATE an Order webhook, it must also be required to READ, UPDATE, and DELETE Order webhooks
- Implement feature-based access control where webhook management permissions are tied to the underlying feature permissions (Order webhooks require Orders permission)
- Add audit logging to all webhook modifications including URL changes, deletions, and view access
- Use role-based access control matrices to prevent authorization logic from being scattered across different endpoints
- Test each CRUD operation for every resource with minimal permission sets to catch authorization gaps
- Implement server-side permission checks rather than relying on UI-level restrictions (staff could bypass through direct API calls)

## Variant hunting
Check if other webhook types (Product, Customer, Shop) have similar permission inconsistencies where creation is restricted but modification is not
Audit other Settings-only permissions to see if they suffer from the same READ/UPDATE/DELETE bypass
Test if staff can view webhook contents (GET requests) without proper permissions, leading to information disclosure
Check if webhook test/trigger functionality is available to staff without proper permissions
Verify if webhook history/logs are accessible to staff without Orders permission
Test other resources that reference order-related operations (e.g., fulfillment webhooks, refund webhooks)

## MITRE ATT&CK
- T1078.003 - Valid Accounts (compromised staff account)
- T1556 - Modify Authentication Process (redirect order notifications)
- T1538 - Steal Web Session Cookie (potential for privilege escalation)
- T1078.001 - Default Accounts (if staff account has excessive default permissions)
- T1526 - Exposure Through API (webhook redirection exposes order data)

## Notes
This is an inconsistent authorization enforcement vulnerability rather than a complete authorization bypass. The application correctly prevents unauthorized webhook CREATION but fails to enforce the same restrictions on MODIFICATION and DELETION. This is a common pattern in RBAC implementations where developers forget to apply the same permission checks across all operations. The report references a prior related report (#430285) indicating this may be part of a broader permission model issue in the platform.

## Full report
<details><summary>Expand</summary>

Hi,

A STAFF with just `Settings` permission can only create 1 type of webhook called `Shop Update` as seen below.

{F368739}

Attempting to create a `Order Creation` webhook via burp proxy gives a 403 -Forbidden response with the message indicating that `You do not have permission to create webhooks with orders/create ` as seen below.

{F368743}

So technically from the above results it means that any STAFF with just `Settings` permission is restricted to create any webhooks related to `Order` or __make modifications/deletions to Order webhooks__ created by Owner or other permitted users.

From my testing I observed that a STAFF member with just `Settings` only permission could modify `Order` webhooks if the web-hooks were created previously by Owner or other permitted users. These Order webhooks can also be deleted by the STAFF member.

__STEPS__

1.Onwer assigns `Settings` only permission to STAFF.
2.Owner creates a webhook for `Order Creation`.
{F368756}
{F368757}
3.STAFF logs into Store Admin and then navigates to Settings>>Notifications. STAFF can see the `Order Creation` webhook which was created by Owner.
{F368758}
4.STAFF then clicks on the wehbook. This opens a modal box where STAFF can make modifications in he URL. STAFF then clicks on `Save Webhook`
{F368759}
{F368760}
As you can see from the above screen shot, the `Order creation` webhook was modified by STAFF.

5.The STAFF can also delete a `Order Creation` webhook.
{F368762}
{F368763}

## Impact

From my previous report #430285, @jack_mccracken stated the below

>Order notifications are restricted to staff members with the `Orders` permission.

A Webhook is technically an event which is which triggered due to some activity. In this case, the event `Order Creation` webhook will trigger a notification to the specified URL in webhook. The fact that a STAFF user with just `Settings` permission isn't allowed to create a `Order Creation` webhook indicates that the STAFF must also need `Orders` permission to create it.

But from my testing, it was possible for a STAFF with just `Settings` permission to edit/delete a `Order Creation` webhook which IMO should not be authorized to the STAFF member.

Let me know what you think about it.

Thanks.
@h13-

</details>

---
*Analysed by Claude on 2026-05-24*
