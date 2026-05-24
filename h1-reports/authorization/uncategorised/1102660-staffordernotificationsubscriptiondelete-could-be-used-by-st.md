# Unauthorized Staff Order Notification Deletion via Improper Permission Validation

## Metadata
- **Source:** HackerOne
- **Report:** 1102660 | https://hackerone.com/reports/1102660
- **Submitted:** 2021-02-13
- **Reporter:** ngalog
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Access Control, Insufficient Authorization Checks, Privilege Escalation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with only `Settings` permission can delete staff order notification subscriptions that should require `Order` permission. The GraphQL mutation `staffOrderNotificationSubscriptionDelete` fails to properly validate the caller's permissions before allowing the deletion of order notifications.

## Attack scenario
1. Attacker gains staff account credentials with only `Settings` permission level
2. Attacker identifies the notification subscription GID from the admin settings page URL or through enumeration
3. Attacker crafts a GraphQL mutation query targeting `staffOrderNotificationSubscriptionDelete` with the target subscription GID
4. Attacker sends the mutation to the GraphQL endpoint without proper authorization headers being validated
5. Server processes the request and deletes the subscription without verifying the caller has `Order` permission
6. Order notifications are removed, disrupting legitimate staff order management workflows

## Root cause
The `staffOrderNotificationSubscriptionDelete` GraphQL resolver performs insufficient authorization checks. It likely validates that the user is a staff member but fails to check whether they possess the specific `Order` permission required for managing order notifications. The permission check probably only verifies `Settings` permission or has no permission check at all.

## Attacker mindset
A disgruntled employee or competitor with limited staff access can disrupt order notification systems affecting business operations. By exploiting the permission gap, they can escalate their limited `Settings` access to modify order-related configurations, causing operational disruption without triggering alerts for unauthorized `Order` permission actions.

## Defensive takeaways
- Implement granular permission checks at the resolver level for all GraphQL mutations, validating required permissions before executing any operation
- Use a centralized authorization middleware that enforces permission requirements consistently across all mutations and queries
- Map each mutation explicitly to required permissions (e.g., staffOrderNotificationSubscriptionDelete requires `Order` permission)
- Add audit logging for all permission-protected operations to detect unauthorized access attempts
- Implement integration tests that verify each mutation enforces correct permission boundaries
- Perform security review of all GraphQL mutations to identify similar authorization bypass vulnerabilities
- Use role-based access control (RBAC) patterns with explicit deny-by-default for sensitive operations

## Variant hunting
Check other notification-related mutations (staffNotificationSubscriptionDelete, etc.) for similar permission validation bypasses
Review all order-related GraphQL mutations to see if `Settings` permission incorrectly allows modifications
Examine whether `Settings` permission is being treated as a super-permission that grants access to protected resources
Test if GID enumeration is possible to discover other notification subscriptions without proper authorization
Check if other permission combinations (e.g., `Finances` with `Settings`) can access `Order`-protected mutations
Verify if similar privilege escalation exists in other Shopify admin GraphQL endpoints

## MITRE ATT&CK
- T1190
- T1548
- T1078

## Notes
The vulnerability demonstrates a common authorization pattern flaw where permission checks are either missing or inconsistent. The reporter efficiently identified the issue by understanding the permission model and testing boundary conditions. The use of GID as an identifier requires authentication but not proper authorization, a classic privilege escalation pattern. The GraphQL endpoint structure and operation naming conventions made the attack straightforward to execute.

## Full report
<details><summary>Expand</summary>

Hi,

The staff order notification should be under the control of staff members with `Order` permission but I found that the staff member with just `Settings` permission can also delete the order notifications using the GID

Steps to reproduce
- Login as a staff member with `Settings` permission
- Make this GraphQL call to `https://yoursubdomain.myshopify.com/admin/internal/web/graphql/core?operation=SwitcherNoStores`

```
{"query": "mutation{staffOrderNotificationSubscriptionDelete(staffOrderNotificationSubscriptionId:\"gid://shopify/StaffOrderNotificationSubscription/82867191864\"){userErrors{message}}} "}
```

- Note: you can find the `82867191864` id from `/admin/settings/notifications` as an admin account, in the `Staff order notifications` section, after adding a order notification and the id is in the URL

- The response you see should be `{"staffOrderNotificationSubscriptionDelete":{"userErrors":[]}}`, and this means you have deleted the subscription already

## Impact

The staff order notification should be under the control of staff members with `Order` permission but I found that the staff member with just `Settings` permission can also delete the order notifications using the GID

</details>

---
*Analysed by Claude on 2026-05-24*
