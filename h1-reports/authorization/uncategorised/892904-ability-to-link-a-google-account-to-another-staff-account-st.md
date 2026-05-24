# Account Takeover via Email Update in POS GraphQL Endpoint - Google Account Linking

## Metadata
- **Source:** HackerOne
- **Report:** 892904 | https://hackerone.com/reports/892904
- **Submitted:** 2020-06-06
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Broken Access Control, Privilege Escalation, Account Takeover, Insufficient Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
The POS GraphQL endpoint allows staff members to update other staff email addresses without proper authorization checks. By changing a staff member's email to an attacker's Google account email, the attacker can authenticate as that staff member via Google OAuth and gain unauthorized access to their account and permissions.

## Attack scenario
1. Attacker obtains POS staff access to a Shopify store configured with Google Apps SSO
2. Attacker identifies a target staff member or store owner who hasn't yet linked their account to Google
3. Attacker navigates to POS > Staff and initiates an email update request, capturing the GraphQL request to pos-channel.shopifycloud.com/graphql-proxy/admin
4. Attacker modifies the StaffMemberUpdate GraphQL operation to change target staff email to attacker's Google Apps email address
5. Attacker logs out and authenticates using Google OAuth with the modified email
6. Attacker gains full access to the target staff member's account with their associated permissions

## Root cause
Insufficient authorization validation on the StaffMemberUpdate GraphQL mutation. The endpoint validates that the requester has POS access but fails to verify they have permission to modify specific staff member records. Prior fixes addressed store owner updates but failed to restrict staff member updates, leaving lateral privilege escalation possible.

## Attacker mindset
An insider threat (staff member with POS access) seeking to expand their access by compromising other staff accounts or store owner accounts. Could also be leveraged with XSS against store owners. Attacker recognizes that Google OAuth linking circumvents password-based authentication, making this a reliable account takeover vector.

## Defensive takeaways
- Implement granular authorization checks on all GraphQL mutations - verify not just role/scope but specific resource ownership
- Require email change confirmation via both old and new email addresses to prevent unauthorized updates
- Add audit logging and alerting for email modifications on privileged accounts
- Enforce re-authentication and MFA verification before allowing email/SSO account changes
- Validate that OAuth email changes only link to unlinked accounts with proper confirmation workflows
- Apply consistent authorization fixes across all related endpoints - a fix to one operation should trigger security review of similar ones
- Implement rate limiting on account modification operations
- Require Google account pre-verification before allowing SSO linking to prevent takeover via email change

## Variant hunting
Check for similar email update vulnerabilities in other Shopify GraphQL endpoints (orders, customers, etc.)
Test if store owner can update their own email via the same endpoint (mentioned in report as still possible)
Investigate if other SSO providers (SAML, OIDC) have similar bypass vulnerabilities
Test if account email changes trigger proper OAuth account unlinking before new linking
Look for similar IDOR patterns in staff management APIs across other Shopify services
Check if XSS in POS interface can be exploited to execute unauthorized GraphQL mutations against store owners

## MITRE ATT&CK
- T1190
- T1548
- T1078
- T1555
- T1556
- T1199

## Notes
Report references prior fixes to reports 872380 and 867513 which addressed store owner email updates but created incomplete fix leaving staff members vulnerable. Attacker requires existing POS access, making this a lateral movement/privilege escalation vector rather than unauthenticated attack. Google OAuth linking is the critical attack vector - the email change alone would not grant access without SSO reliance. XSS angle mentioned suggests compound vulnerability potential.

## Full report
<details><summary>Expand</summary>

The https://pos-channel.shopifycloud.com/graphql-proxy/admin endpoint allows us to update a staff email address that is having a Shopify ID.

Taking that into consideration, if a store is setup to use **Google Apps** as login service and if a staff/store owner hasn't yet linked his account to a Google one (meaning he never logged in using Google), it is possible to update their email to our own Google email address resulting in us being able to log into their account. By doing so, our Google account ends up linked to the staff member/store owner. 

## Steps to reproduce 
1. As a staff member with **Point Of Sale** access, open up **Point of Sale** > **Staff** page and select the staff you want to link your Google account with.
2. Open up your browser network inspection tab and save its profile. Copy the CURL request that is being made to https://pos-channel.shopifycloud.com/graphql-proxy/admin **StaffMemberUpdate** operation.
3. From the copied CURL request, update the `email` field from the payload to your own email of the configured Google Apps domain.
4. Logout from the store and log back in using the `Google Apps` email you just set.

## Demo
{F857469}

## Impact

Recently, maybe when you guys fixed [872380](https://hackerone.com/reports/872380),  [867513](https://hackerone.com/reports/867513) or some other reports, you also fixed updating the email address of a store owner using the **StaffMemberUpdate** operation of https://pos-channel.shopifycloud.com/graphql-proxy/admin endpoint. However, the shop owner himself is still able to update his email address using that endpoint. Thus, by leveraging a XSS targeting the shop owner, we would technically be able to link it to our Google account, giving us access to shop owner features as described on https://help.shopify.com/en/manual/your-account
{F857468}

Besides that, without any XSS, that can exploited to link our Google account to any other staff account that isn't yet linked.

</details>

---
*Analysed by Claude on 2026-05-24*
