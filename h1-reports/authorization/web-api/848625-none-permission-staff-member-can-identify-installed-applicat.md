# Unauthorized Information Disclosure: Non-Permission Staff Member Can Identify Installed Applications and Product Configuration

## Metadata
- **Source:** HackerOne
- **Report:** 848625 | https://hackerone.com/reports/848625
- **Submitted:** 2020-04-13
- **Reporter:** sreeju_kc
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Information Disclosure, Broken Access Control, Insufficient Authorization Checks
- **CVEs:** None
- **Category:** web-api

## Summary
A staff member without application permissions can identify if the Digital Downloads app is installed on a store and determine which products are configured with it by directly accessing app delivery URLs. The vulnerability allows unauthorized information disclosure through direct endpoint access that lacks proper permission validation. Non-privileged staff members can extract product IDs from the store's page source and use them to query application configuration endpoints.

## Attack scenario
1. Attacker creates a staff account with no permissions on target store (test.myshopify.com)
2. Attacker visits any product page on the target store and extracts product IDs from the HTML source code via view-source
3. Attacker accesses the Digital Downloads app delivery URL with the extracted product ID: https://delivery.shopifyapps.com/products/{PRODUCT_ID}
4. If the app is installed and the product is configured, the app returns identifying information (e.g., 'Digital Downloads/Tt')
5. Attacker repeats with multiple product IDs to map which products have the app configured
6. Attacker gains intelligence about store's app installation and configuration without proper authorization

## Root cause
The app delivery endpoint at delivery.shopifyapps.com/products/{ID} performs insufficient authorization validation and does not verify that the requesting user has application permissions before returning configuration information. The application trusts the product ID as sufficient context without checking user roles/permissions against the store.

## Attacker mindset
An insider threat or disgruntled employee with minimal access seeks to gather competitive intelligence about a store's technology stack and app configurations. They recognize that product IDs are publicly visible in page source and exploit the app endpoint's lack of permission checks to identify installed applications.

## Defensive takeaways
- Implement permission checks on all app delivery endpoints that return configuration or identification information
- Validate that the requesting user has appropriate app-specific permissions before returning any app metadata or product configuration details
- Apply the principle of least privilege: staff members should not receive product ID information unless they have relevant permissions
- Implement role-based access control (RBAC) across all app-related endpoints, not just the admin interface
- Audit third-party app delivery infrastructure for authorization bypass vulnerabilities
- Consider hiding product IDs from page source for users without appropriate permissions
- Log and monitor access to app configuration endpoints from accounts with no app permissions

## Variant hunting
Check other Shopify apps' delivery endpoints for similar authorization bypasses using product/resource IDs
Test if staff members can access other app types (Premium App, Private App) delivery URLs without permissions
Attempt to enumerate all installed apps by iterating through known app identifier patterns in delivery URLs
Verify if the vulnerability extends to other resource types beyond products (collections, orders, etc.)
Test if authenticated but unprivileged users can access other sensitive configuration endpoints
Check if the vulnerability applies to different staff permission levels (read-only, limited access, etc.)
Investigate if app data is exposed through other vectors (API endpoints, webhooks, cached responses)

## MITRE ATT&CK
- T1526 - Gather Victim Host Information (discovering installed apps)
- T1087 - Account Discovery (identifying configured products)
- T1592 - Gather Victim Host Information (reconnaissance of target infrastructure)
- T1040 - Network Sniffing (accessing unprotected endpoints)
- T1538 - Cloud Service Discovery (identifying Shopify app configurations)

## Notes
This is a well-documented information disclosure vulnerability with clear impact. The reporter provides an excellent step-by-step POC demonstrating the attack chain. The core issue is that permission checks are only implemented in the UI layer, not enforced at the API/delivery endpoint layer. The vulnerability requires the attacker to be a legitimate staff member with some access to the store, making it an insider threat scenario. The fix should involve server-side authorization validation on all information-returning endpoints.

## Full report
<details><summary>Expand</summary>

Hello,
To see if a store has application installed and which products its configured the staff member should have application permission otherwise nothing is visible but i found a way that let none permission staff member to identify if the store has installed Digital Downloads and if the application configured on a particular products.

POC:
1)Create two user A and B, login to A and create a store, test.myshopify.com
2)Add user B as staff member to test.myshopify.com with no permission.
3)From user A, go test.myshopify.com and create two product called Tt and PP
4)Install Digital Downloads for this store and configure Tt to this app.
5)Login back to user B and create an independent store, test100.myshopify.com and install Digital Downloads on this store.
6)Now go to user A store (test.myshopfy.com) and click app and click Digital downlands and right click on the product, you will get below urli
https://delivery.shopifyapps.com/products/3785077260000
7)Copy paste to this url from user B account (login as user B) and you can see that a message as below.
Digital Downloads/Tt
This indicate that Digital Downloads is installed on test.myshopfy.com store (which this user has 0 permission) and configured on the product Tt.
8)If you user the same url with PP product id, nothing is shown

User B can get products ids via source page of user A store as user B is staff member even though none permission 

view-source:https://test.myshopify.com/products/tt

<script id="__st">var __st={"a":2616790000,"offset":-14400,"reqid":"fff-bbb-ccc-bbb-qqq","pageurl":"test-myshopify.com\/products\/tt","u":"184d9400000a","p":"product","rtyp":"product","rid":3785077260000};</script>

## Impact

This is an information disclosure, none permission member staff should not know which application is installed and what product is configured for this application.

Please find the screen shots

</details>

---
*Analysed by Claude on 2026-05-24*
