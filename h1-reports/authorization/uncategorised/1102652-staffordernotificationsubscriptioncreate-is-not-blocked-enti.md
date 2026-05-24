# staffOrderNotificationSubscriptionCreate Not Properly Blocked for Staff with Settings Permission

## Metadata
- **Source:** HackerOne
- **Report:** 1102652 | https://hackerone.com/reports/1102652
- **Submitted:** 2021-02-13
- **Reporter:** ngalog
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authorization Bypass, Insufficient Access Control, GraphQL Permission Bypass
- **CVEs:** None
- **Category:** uncategorised

## Summary
A GraphQL mutation endpoint `staffOrderNotificationSubscriptionCreate` fails to properly enforce access controls, allowing staff members with only Settings permission to subscribe arbitrary email addresses to order notifications despite receiving an 'Access denied' error message. The mutation executes successfully despite the misleading error response, creating unauthorized notification subscriptions that persist in the admin panel.

## Attack scenario
1. Attacker authenticates as a staff member with Settings permission
2. Attacker crafts a GraphQL mutation calling staffOrderNotificationSubscriptionCreate with a target email address
3. Attacker sends the mutation to the GraphQL endpoint at /admin/internal/web/graphql/core
4. Server responds with 'Access denied' error message indicating insufficient permissions
5. Despite the error message, the mutation silently executes and creates the subscription
6. Attacker verifies the unauthorized email is now added to order notifications in /admin/settings/notifications

## Root cause
The authorization check for staffOrderNotificationSubscriptionCreate performs validation and returns an error message to the client, but the permission check occurs after the mutation logic has already executed. This creates a race condition or logic flaw where the mutation commits changes before fully validating permissions, or the validation only blocks the response without rolling back the action.

## Attacker mindset
An insider threat or compromised staff account could exploit this to subscribe malicious email addresses to receive sensitive order notifications. This could be used for reconnaissance, espionage, or to forward notifications to external parties. The misleading error message provides plausible deniability that the action failed.

## Defensive takeaways
- Implement permission checks at the mutation resolver level BEFORE executing any business logic or database operations
- Ensure authorization failures either prevent execution entirely or properly rollback any changes with transactional integrity
- Align error messages with actual system behavior - do not return success indicators masked as errors
- Validate that required scopes (read_notification_settings, order access) are enforced consistently across all mutation endpoints
- Implement audit logging for all notification subscription changes to detect unauthorized modifications
- Use explicit allow-lists rather than implicit deny patterns for sensitive operations
- Test permission boundaries for all GraphQL operations, not just Query fields

## Variant hunting
Check other staffOrder* mutations for similar permission bypass vulnerabilities
Test all notification subscription endpoints (SMS, Slack, webhooks) for the same flaw
Look for mutations where error responses are returned but state changes persist
Examine other Settings permission-gated operations that may suffer from pre-check execution
Test whether the vulnerability applies to other recipient types beyond EMAIL
Check if the subscription can be confirmed/activated without proper permissions

## MITRE ATT&CK
- T1078 - Valid Accounts (leveraging staff credentials)
- T1190 - Exploit Public-Facing Application (GraphQL endpoint abuse)
- T1087 - Account Discovery (adding external email addresses)
- T1098 - Account Manipulation (modifying notification settings)

## Notes
This is a classic example of authorization checks being applied at the API response layer rather than the business logic layer. The error message serves as a false negative, misleading developers into thinking the operation failed when it actually succeeded. The attacker receives immediate feedback that the operation 'failed' but can verify success by checking the admin UI, making this difficult to detect through normal testing. The vulnerability appears specific to the internal web GraphQL endpoint used by Shopify's admin dashboard.

## Full report
<details><summary>Expand</summary>

Hi,

I found that the GraphQL call `staffOrderNotificationSubscriptionCreate` is not blocked from the staff member with Settings permission

## Steps to reproduce
- Login as a staff member with `Settings` permission
- Make this GraphQL call to `https://yoursubdomain.myshopify.com/admin/internal/web/graphql/core?operation=SwitcherNoStores`

```
{"query": "mutation{staffOrderNotificationSubscriptionCreate(notificationRecipientIdentifier:\"testingforshopify@ngailong.com\",notificationRecipientType:EMAIL){staffOrderNotificationSubscription{id}}} "}
```

- The response you see should be `Access denied for staffOrderNotificationSubscription field. Required access: `read_notification_settings` access scope. Also: User must have access to orders.`, and you would think this means a dead end, but reality is you have already added the order notification to the settings
- Visit `/admin/settings/notifications` as an admin, you should notice the email `testingforshopify@ngailong.com` is added to the order notification already

## Screenshot video
{F1194404}

## Impact

I found that the GraphQL call `staffOrderNotificationSubscriptionCreate` is not blocked from the staff member with Settings permission

</details>

---
*Analysed by Claude on 2026-05-24*
