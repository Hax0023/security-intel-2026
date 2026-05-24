# Staff Members Can Extend Shopify Trial Period Without Admin Permission

## Metadata
- **Source:** HackerOne
- **Report:** 947728 | https://hackerone.com/reports/947728
- **Submitted:** 2020-07-30
- **Reporter:** risinghunter
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Insufficient Access Control, Privilege Escalation, Authorization Bypass, GraphQL Authorization Flaw
- **CVEs:** None
- **Category:** uncategorised

## Summary
Staff members with minimal permissions (e.g., only 'report' access) can extend the shop's trial period by 14 days without admin approval by directly calling the TrialSelfExtend GraphQL mutation. The endpoint lacks proper authorization checks to verify if the staff member has appropriate permissions for subscription/billing-related operations.

## Attack scenario
1. Attacker gains staff access to a Shopify store, either through social engineering, compromised credentials, or legitimate employment
2. Attacker is provisioned with a restricted staff account having only 'report' permission with no billing/subscription access
3. Attacker discovers or is aware of the TrialSelfExtend GraphQL mutation endpoint available at /admin/internal/web/graphql/core
4. Attacker crafts and sends a GraphQL POST request with the TrialSelfExtend mutation while authenticated as the restricted staff account
5. The endpoint processes the request without validating if staff member has authorization for trial extension operations
6. Trial period is successfully extended by 14 days, allowing unauthorized manipulation of store subscription terms

## Root cause
The TrialSelfExtend GraphQL mutation endpoint performs insufficient authorization checks. It validates that a user is authenticated but fails to verify that the authenticated user possesses the required permissions (likely admin-only or specific billing-related permissions) before executing the trial extension logic.

## Attacker mindset
A disgruntled employee or unauthorized staff member could extend the trial period to delay paid subscription charges, reduce operational costs for the store, or sabotage the business. Alternatively, an attacker with compromised staff credentials could abuse this to extend trials without owner knowledge.

## Defensive takeaways
- Implement granular authorization checks for all GraphQL mutations, not just authentication verification
- Require explicit 'subscription_management' or 'billing' permissions before allowing trial extension operations
- Apply principle of least privilege: staff permissions should be clearly defined and restricted by default
- Audit all endpoints that modify subscription or billing state for proper authorization controls
- Consider role-based access control (RBAC) for sensitive operations like trial extensions
- Log and monitor all trial extension attempts, including by which staff member and timestamp
- Implement server-side permission caching with TTL to catch permission changes in real-time
- Test authorization boundaries for each GraphQL mutation with various permission levels

## Variant hunting
Look for other GraphQL mutations in /admin/internal/web/graphql/core endpoint that modify account state, billing, subscription, or plan-related data. Test mutations like: PlanChange, SubscriptionCancel, ChargeCreate, ExtendTrial, etc. with minimally-permissioned staff accounts. Also check for similar authorization bypasses in REST API endpoints under /admin/api/*/shop.json or subscription-related endpoints.

## MITRE ATT&CK
- T1078 - Valid Accounts (using legitimate staff credentials)
- T1190 - Exploit Public-Facing Application (GraphQL endpoint exploitation)
- T1548 - Abuse Elevation Control Mechanism (privilege escalation through missing authorization)
- T1110 - Brute Force (credential compromise leading to staff access)
- T1021 - Remote Services (leveraging internal admin service endpoints)

## Notes
The report demonstrates a clear authorization flaw in Shopify's internal GraphQL API. The fact that the endpoint is accessible via internal proxy (/admin/internal/web/) suggests it may have been assumed to be sufficiently protected by network isolation, but this assumption failed. The sensitive nature of trial period extension (directly impacts billing/revenue) makes this a notable security issue. The attacker included redacted GraphQL query details and staff permission screenshots showing the permission model. Remediation likely requires adding permission checks to the TrialSelfExtend resolver before executing business logic.

## Full report
<details><summary>Expand</summary>

Description: my store 14 days trial subscription remains only for 2 days and I see  Shopify also offers shop admin to extend shop trial period to another 14 days. so, I found an issue in which staff with no permission also able to extend trial period without admin permission

steps to reproduce :
--
1). add staff only "report" permission
{F930056}
2). then added staff isn't able to do any activity related to subscription/plan
{F930054}
3). run following TrialSelfExtend Graphql request through added staff account 
███████

```
POST /admin/internal/web/graphql/core HTTP/1.1
Host: risinghunter.myshopify.com
Connection: close
Content-Length: 218
accept: application/json
X-CSRF-Token: H9hN7Wt7-0Q1PwBhOsOIZMpEcCnp0WZQw8BM
content-type: application/json
User-Agent: Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36
X-Shopify-Web-Force-Proxy: 1
Origin: https://risinghunter.myshopify.com
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Accept-Encoding: gzip, deflate
Accept-Language: en-GB,en-US;q=0.9,en;q=0.8,ru;q=0.7
Cookie: new_admin=1; new_theme_editor_disabled.sig=c0lGzzh0MFBQ5fCQTfz7yqvtriw; new_theme_editor_disabled=1; _abv=0; _master_udr=eyJfcmFpbHMiOnsibWVzc2FnZSI6IkJBaEpJaWxpT1dWbU4yWmtOQzFsTVdFMUxUUmlOekV0WWprMVppMW1PV1ExTm1Jd00yRXhZMllHT2daRlJnPT0iLCJleHAiOiIyMDIyLTA3LTI4VDA3OjEwOjAyLjAyOFoiLCJwdXIiOiJjb29raWUuX21hc3Rlcl91ZHIifX0%3D--aaa21a6f8ca759e8780b581506af5e6b544b851d; _secure_admin_session_id_csrf=9b14248b770db62cc190e3e264362b12; _secure_admin_session_id=9b14248b770db62cc190e3e264362b12; koa.sid=vOD0te0oCONZnKFY8VZeCFGM5sWIbwYB; koa.sid.sig=-qd5DD-YfKDTMZz7LHyxOu7MMsE; _orig_referrer=; _shopify_y=be3905ce-c786-4135-a98c-f4c292fed5bf; _y=be3905ce-c786-4135-a98c-f4c292fed5bf; _landing_page=%2Fadmin%2Fauth%2Flogin%3Faccountnumber%3D0%26from_signup%3Dtrue; __ssid=831ecb8b-307e-4640-af0a-80bfa7b89894; _y=be3905ce-c786-4135-a98c-f4c292fed5bf; _shopify_y=be3905ce-c786-4135-a98c-f4c292fed5bf; _shopify_fs=2020-07-17T04%3A36%3A57.584Z; cart_ver=%3A0; secure_customer_sig=; cart_sig=; new_theme_editor_disabled=1; _ga=GA1.2.1368468577.1594960719; _abv=0; _ab=1; storefront_digest=██████████; _secure_session_id=05214efc7671b79b95c5540b7cde58c2; __cfduid=dd29f3357820fab55e8a97634eec973941595927106

{"operationName":"TrialSelfExtend","variables":{},"query":"mutation TrialSelfExtend {\n  trialSelfExtend {\n    message\n    userErrors {\n      field\n      message\n      __typename\n    }\n    __typename\n  }\n}\n"}
```
4). after running above request you get the response "14 days extension added to your trial period"
{F930055}

## Impact

staff can able to extend Shopify trial period without admin permission

</details>

---
*Analysed by Claude on 2026-05-24*
