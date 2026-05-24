# Staff Member with No Permission Can Delete POS Staff from Account Settings

## Metadata
- **Source:** HackerOne
- **Report:** 860348 | https://hackerone.com/reports/860348
- **Submitted:** 2020-04-27
- **Reporter:** kunal94
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Broken Access Control, Insufficient Authorization, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A staff member with no administrative permissions can delete Shopify POS staff accounts from the account settings page, bypassing intended authorization checks. The vulnerability exists because the delete operation for POS staff lacks proper permission validation on the backend, allowing any authenticated staff member to remove POS staff regardless of their assigned permissions.

## Attack scenario
1. Attacker logs in as a staff member with minimal or no permissions assigned
2. Attacker navigates to /admin/settings/account page where POS staff are displayed
3. Attacker identifies POS staff member accounts listed in the account settings
4. Attacker clicks the delete button on any POS staff account
5. Backend processes the delete request without validating the attacker's permissions
6. POS staff account is successfully deleted despite attacker lacking authorization

## Root cause
The backend API endpoint handling POS staff deletion fails to validate the requesting user's permissions before processing the delete operation. Authorization checks are either missing entirely or insufficiently restrictive, allowing any authenticated staff member to execute privileged operations regardless of their role or assigned permissions.

## Attacker mindset
An attacker with basic staff account access seeks to disrupt business operations by removing POS staff members. The exploit requires minimal effort (clicking delete) and no special tools, making it attractive for opportunistic attacks. The attacker may be a disgruntled employee or someone with temporary access seeking to cause disruption.

## Defensive takeaways
- Implement server-side authorization checks on all sensitive endpoints, not just the UI
- Verify user permissions before processing delete/modification requests for any staff-related resources
- Use role-based access control (RBAC) consistently across all features, including POS staff management
- Validate that only users with admin or appropriate POS staff management permissions can delete staff
- Audit API endpoints for missing authorization logic and conduct security code review
- Implement proper permission inheritance and validation in GraphQL resolvers
- Log all staff deletion attempts with user attribution for accountability and forensics
- Test authorization on all CRUD operations with different user roles

## Variant hunting
Check if other staff-related operations (edit, create, view) lack proper authorization
Test if the vulnerability exists for other account settings modifications
Investigate if similar issues exist in other Shopify POS or admin endpoints
Check GraphQL mutations for POS staff operations to see if mutations lack permission validation
Test if location-based staff can delete staff from other locations
Verify if the issue affects staff member operations in the main admin vs POS-specific areas
Check if permission bypass is possible through direct API calls versus UI interactions

## MITRE ATT&CK
- T1190
- T1578

## Notes
The researcher noted severity as 'low' but this appears understated; unauthorized deletion of staff accounts constitutes broken access control (OWASP Top 10 #1). The vulnerability is straightforward to exploit and impacts business operations directly. The researcher's mention of using Burp to modify responses to enable the feature suggests the beta flag feature gating might have also been weak. This is a classic case of trusting client-side UI visibility checks while backend fails to enforce authorization.

## Full report
<details><summary>Expand</summary>

Hello Team

#Description
Shopify POS also has staff settings only for POS purposes where an admin can add POS Shopify staff along with fname,lname, email address, and generated pin.
Reference - https://help.shopify.com/en/manual/sell-in-person/pos-classic/setup/staff-settings
After creation, Shopify POS staff displays in /admin/settings/account, and Vulnerability arises when staff members with no permission can delete Shopify POS staff from account settings.

#Step To Reproduce

+ Go to the Shopify POS app from the admin session.
{F805568}

+ Currently, I've Shopify Plus Partner Sandbox/Monthly, so in a sandbox environment, staff POS staff settings are not enabled, however, we can modify response and enable the POS staff member feature on the sandbox environment to test.

+ Intercept Shopify POS app area from burp suite and notice the GRAPHQL response

**Request**

`POST /graphql-proxy/admin HTTP/1.1
Host: pos-channel.shopifycloud.com
`

`{"operationName":"Overview","variables":{},"query":"query Overview {\n  shop {\n    currencyCode\n    ianaTimezone\n    countryCode\n    features {\n      retailPackage\n      __typename\n    }\n    staffPermissionsBetaFlag: beta(name: \"pos_web_admin_staff_user_permissions\")\n    accountSetupQuestionsAnswers {\n      answer\n      handle\n      __typename\n    }\n    plan {\n      trial\n      __typename\n    }\n    accountOwner {\n      email\n      __typename\n    }\n    __typename\n  }\n  locations(first: 50) {\n    edges {\n      node {\n        name\n        id\n        addressVerified\n        hasActiveInventory\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n  products(first: 1) {\n    edges {\n      node {\n        id\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}
`

**Response**
```
{"data":{"shop":{"currencyCode":"INR","ianaTimezone":"America\/New_York","countryCode":"IN","features":{"retailPackage":true,"__typename":"ShopFeatures"},"staffPermissionsBetaFlag":false,"accountSetupQuestionsAnswers":[{"answer":"No locations yet","handle":"number_locations","__typename":"AccountSetupQuestionsAnswer"},{"answer":"1","handle":"offline_brick_and_mortar","__typename":"AccountSetupQuestionsAnswer"},{"answer":"1","handle":"offline_markets_fairs","__typename":"AccountSetupQuestionsAnswer"},{"answer":"1","handle":"offline_temp_shops","__typename":"AccountSetupQuestionsAnswer"}],"plan":{"trial":false,"__typename":"ShopPlan"},"accountOwner":{"email":"kunal94@wearehackerone.com","__typename":"StaffMember"},"__typename":"Shop"},"locations":{"edges":[{"node":{"name":"khudirampally, bagdogra","id":"gid:\/\/shopify\/Location\/35202859030","addressVerified":false,"hasActiveInventory":true,"__typename":"Location"},"__typename":"LocationEdge"},{"node":{"name":"test","id":"gid:\/\/shopify\/Location\/35202891798","addressVerified":true,"hasActiveInventory":true,"__typename":"Location"},"__typename":"LocationEdge"}],"__typename":"LocationConnection"},"products":{"edges":[{"node":{"id":"gid:\/\/shopify\/Product\/4351723438102","__typename":"Product"},"__typename":"ProductEdge"}],"__typename":"ProductConnection"}},"extensions":{"cost":{"requestedQueryCost":60,"actualQueryCost":12,"throttleStatus":{"maximumAvailable":600000.0,"currentlyAvailable":599988,"restoreRate":30000.0}}}}
```

+ In the response, we have `"staffPermissionsBetaFlag":false`, use Burp Match and Replace rule on response body and set the value from `"staffPermissionsBetaFlag":false` to `"staffPermissionsBetaFlag":true`.

{F805580}

+ Again refresh the page and we have access to Shopify POS Staff manage area.
{F805581}

+ Navigate to  "Manage POS staff" and add POS staff
{F805609}

+ Save it and when you go to `/admin/settings/account` and we can see Shopify POS staff down below:
{F805612}

+ Next, Logged in as staff member with no permission, and navigate to `/admin/settings/account`, down below staff member can also see POS staff account, open POS staff account area, and click on delete, and the account will be deleted successfully.

{F805625}

+ I have set the severity as low since I don't know about the level of POS staff's impact on the Shopify store.



Thanks
Kunal

## Impact

+ User with no permission at all can delete "Shopify POS staff" completely.

</details>

---
*Analysed by Claude on 2026-05-24*
