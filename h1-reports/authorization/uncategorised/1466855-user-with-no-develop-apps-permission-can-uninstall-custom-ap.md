# Authorization Bypass: User without 'Develop apps' Permission Can Uninstall Custom Apps

## Metadata
- **Source:** HackerOne
- **Report:** 1466855 | https://hackerone.com/reports/1466855
- **Submitted:** 2022-02-01
- **Reporter:** ayyoub
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Authorization Bypass, Broken Access Control, Insufficient Permission Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
A staff member with only 'Manage and install apps and channels' permission can uninstall custom apps despite lacking the required 'Develop apps' permission. This authorization check failure allows unauthorized users to remove applications, potentially disrupting business operations and development workflows.

## Attack scenario
1. Attacker creates or obtains staff account with only 'Manage and install apps and channels' permission
2. Attacker identifies the GraphQL endpoint and appUninstall mutation used by Shopify
3. Attacker obtains the target custom app's ID (gid://shopify/App/[appId])
4. Attacker crafts the UninstallCustomApp GraphQL mutation with the target app ID
5. Attacker sends the mutation request without 'Develop apps' permission
6. System processes the uninstall request without validating required permission, removing the custom app

## Root cause
The appUninstall GraphQL resolver lacks proper authorization checks to verify the 'Develop apps' permission before processing uninstall requests. The permission validation either checks only for 'Manage and install apps' or fails to enforce the stricter 'Develop apps' requirement for custom app removal.

## Attacker mindset
A disgruntled employee with limited app management permissions seeks to disrupt development operations, or a competitor with insider access aims to sabotage integrations by removing critical custom apps without proper authorization.

## Defensive takeaways
- Implement granular permission checks at the resolver level for all sensitive mutations, not just at UI layer
- Enforce a whitelist of required permissions for appUninstall mutation and validate ALL required permissions
- Ensure consistency between documented permission requirements and actual code enforcement
- Add audit logging for all app uninstall operations to detect unauthorized attempts
- Implement integration tests validating that users lacking required permissions receive 401/403 errors
- Use authorization middleware/decorators to prevent bypassing permission checks in GraphQL endpoints
- Regularly audit permission hierarchy and mutation authorization matrices

## Variant hunting
Check other app management mutations (appInstall, appUpdate, appDelete) for similar authorization bypasses
Test if other sensitive operations requiring 'Develop apps' permission allow users with only 'Manage and install apps' access
Look for inconsistency between documented permission model and actual permission enforcement across different API endpoints
Search for mutations operating on developer resources that may lack proper role-based access control
Test permission combinations: verify mutations properly handle permission edge cases and hierarchies

## MITRE ATT&CK
- T1190
- T1114
- T1078.004

## Notes
The vulnerability is relatively straightforward—a classic authorization bypass where a privileged operation lacks proper permission validation. The fix likely requires adding a permission check for 'Develop apps' to the appUninstall resolver. The reporter provided excellent reproduction steps including the exact GraphQL mutation payload, making this immediately actionable for the Shopify security team.

## Full report
<details><summary>Expand</summary>

Hi,

You know user must have Develop apps permission to Uninstall  Develop apps 
to test this just create staff with `Manage and install apps and channels`

{F1601504}

send this mutation just change appId by your id

```
{"operationName":"UninstallCustomApp","variables":{"appId":"gid://shopify/App/6431893"},"query":"mutation UninstallCustomApp($appId: ID!) {\n  appUninstall(input: {id: $appId}) {\n    app {\n      id\n      __typename\n    }\n    userErrors {\n      field\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}
```

## Impact

User with no Develop apps permission can Uninstall Custom App

</details>

---
*Analysed by Claude on 2026-05-24*
