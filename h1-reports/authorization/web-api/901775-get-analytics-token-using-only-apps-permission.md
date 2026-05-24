# Privilege Escalation: Analytics Token Extraction via Apps Permission

## Metadata
- **Source:** HackerOne
- **Report:** 901775 | https://hackerone.com/reports/901775
- **Submitted:** 2020-06-18
- **Reporter:** jmp_35p
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Privilege Escalation, Broken Access Control, Information Disclosure, Inadequate Permission Validation
- **CVEs:** None
- **Category:** web-api

## Summary
A staff member with only 'apps' permission could extract embedded analytics tokens from apps with analytics read capabilities, bypassing the requirement for explicit 'dashboard' or 'reports' permissions. This allowed unauthorized access to store analytics and reporting data through the Shopify Analytics API using the extracted token.

## Attack scenario
1. Attacker with 'apps' permission logs into Shopify admin
2. Attacker identifies a POS or other app installed with analytics read permissions
3. Attacker obtains the app's API key through admin interface or app configuration
4. Attacker crafts GraphQL query to extract the embedded legacyEasdkAnalyticsToken from the app installation
5. Attacker uses the extracted token in POST request to analytics.shopify.com /validate endpoint
6. Attacker executes analytics queries (SHOW orders, sales, discounts, etc.) without having explicit report/dashboard permissions

## Root cause
Insufficient permission validation during token generation and usage. The system allowed apps with analytics read permissions to embed tokens that could be extracted by users with minimal privileges, and the analytics endpoint did not properly validate that the token user had required permissions.

## Attacker mindset
A disgruntled staff member or low-privilege admin seeking to view sensitive business analytics and reporting data they should not have access to, potentially for competitive intelligence, data theft, or monitoring store performance beyond their authorization scope.

## Defensive takeaways
- Implement strict permission hierarchy - token extraction should require same permissions as token usage
- Do not embed sensitive tokens in responses accessible to lower-privilege users
- Validate user permissions at analytics API endpoint, not just token validity
- Separate app-level permissions from user-level permissions when accessing app data
- Implement token scope restrictions tied to user's actual permissions, not just app capabilities
- Audit GraphQL queries to prevent information disclosure of sensitive app credentials
- Add access logging for analytics token extraction and usage

## Variant hunting
Check if other embedded tokens (sales tokens, inventory tokens) are similarly extractable
Test if apps with other sensitive permissions expose tokens to under-privileged users
Examine other GraphQL queries in the admin API for similar token extraction patterns
Check if extracted tokens can be used outside original shop context
Test if permission checks are bypassed for other reporting/analytics endpoints
Investigate if customer/product data tokens are similarly exposed

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (GraphQL endpoint)
- T1548 - Abuse Elevation Control Mechanism (permission escalation)
- T1087 - Account Discovery (enumerating app APIs)
- T1526 - Enumerate Cloud Resources (discovering analytics tokens)
- T1021 - Remote Services (accessing analytics API with stolen token)

## Notes
This is a horizontal privilege escalation attack that exploits weak permission separation between app-level and user-level capabilities. The vulnerability chain involves three components: (1) GraphQL query exposing tokens, (2) ability to obtain app API keys, (3) weak validation on analytics endpoint. The legacyEasdkAnalyticsToken naming suggests this may be legacy code that was not properly updated with modern access control requirements.

## Full report
<details><summary>Expand</summary>

It seems apps that can read "analytics" have embedded analytic token. In order to access the /admin/reportify/token.json endpoint explicit dashboard or reports permission is required. A staff member with just "apps" permission can leverage the permissions of apps that can read reports to extract their embedded analyticsToken as long as the appropriate query which is provided below is used. The apikey of the POS app is used here as a variable (see token.png for more).

{"operationName":"EmbeddedAppAnalyticsToken","variables":{"apiKey":"a53cf2ce9b5dabf5dd222b3615c29569"},"query":"query EmbeddedAppAnalyticsToken($apiKey:String!){appByKey:appByKey(apiKey:$apiKey){id installation{id legacyEasdkAnalyticsToken __typename}__typename}}"}

Now, in order to read the store's reports the token gotten from above is used in the query below.
POST /validate?beta=true&dataOnly=false HTTP/1.1
Host: analytics.shopify.com
User-Agent: Mozilla/5.0 (X11; Linux x86_64; rv:76.0) Gecko/20100101 Firefox/76.0
Accept: application/json
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Content-Type: application/x-www-form-urlencoded;charset=UTF-8
Origin: https://foobar.myshopify.com


q%5B%5D=SHOW+orders%2C+gross_sales%2C+discounts%2C+returns%2C+net_sales%2C+shipping%2C+taxes%2C+total_sales+OVER+day+FROM+sales+SINCE+-30d+UNTIL+today+ORDER+BY+day&source=new-admin&token={token_here}

## Impact

Staff member can perform actions they don't have permission to

</details>

---
*Analysed by Claude on 2026-05-24*
