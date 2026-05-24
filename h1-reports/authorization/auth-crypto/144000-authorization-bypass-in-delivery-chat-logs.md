# Authorization Bypass in Delivery Chat Logs - Instacart

## Metadata
- **Source:** HackerOne
- **Report:** 144000 | https://hackerone.com/reports/144000
- **Submitted:** 2016-06-10
- **Reporter:** michiel
- **Program:** Instacart
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Object Level Authorization (BOLA), Insufficient Access Control, Information Disclosure
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An authorization flaw in the `/api/v2/order_deliveries/:order_delivery_id/order_change_logs` endpoint allows any authenticated Instacart user to access chat logs and order details from other users' deliveries by manipulating the order_delivery_id parameter. This exposes private messages between customers, shoppers, and drivers, as well as order information and Firebase authentication tokens.

## Attack scenario
1. Attacker logs into their legitimate Instacart account via mobile app
2. Attacker views their own order's chat logs, intercepting the API request with Burp Suite to identify the endpoint pattern and parameter format
3. Attacker systematically modifies the order_delivery_id parameter to sequential or enumerated IDs (e.g., 261932226 → 261972220, 261972221, etc.)
4. API responds with full chat logs and order data for other users' deliveries without verifying the requester's ownership
5. Attacker harvests sensitive information including private messages, product details, and Firebase tokens from multiple orders
6. Attacker potentially uses Firebase tokens to access additional data or perform lateral attacks

## Root cause
The API endpoint implements no server-side authorization checks to verify the requesting user owns or has permission to access the specified order_delivery_id. The application relies solely on the client to send valid IDs, assuming users will only request their own data. No access control logic validates the relationship between the authenticated user and the requested resource.

## Attacker mindset
Opportunistic account takeover and reconnaissance. An attacker with valid credentials identifies the authorization bypass as a low-effort, high-reward vulnerability requiring minimal technical sophistication. The sequential nature of IDs suggests bulk enumeration is feasible. Firebase tokens represent a secondary exploitation vector for privilege escalation or lateral movement.

## Defensive takeaways
- Implement explicit authorization checks on every API endpoint that accesses user-scoped resources, verifying the authenticated user owns or has explicit permission to access the requested object
- Use object-level access control matrices that map user IDs to resource IDs server-side before returning any data
- Avoid exposing raw sequential or predictable IDs in APIs; use UUIDs, GUIDs, or other non-enumerable identifiers to increase attack complexity
- Validate authorization at multiple layers: authentication (who are you), then authorization (what can you access)
- Implement comprehensive audit logging for API access to order data, enabling detection of enumeration attacks
- Conduct security testing specifically targeting BOLA vulnerabilities by systematically manipulating resource identifiers with different authenticated contexts
- Redact or never return authentication tokens (Firebase, JWT, etc.) in API responses to external clients
- Apply rate limiting to API endpoints that accept resource IDs to impede enumeration attacks

## Variant hunting
Check other API endpoints following the pattern `/api/v2/order_deliveries/:id/*` for similar authorization bypasses (order_details, invoice, refunds, etc.)
Test user profile endpoints with modified user IDs to access other users' account information, addresses, payment methods
Examine endpoints accepting both user_id and resource_id parameters to verify both are validated
Review order history endpoints to determine if pagination or filtering can be exploited to leak other users' orders
Investigate Firebase API endpoints directly to assess if returned tokens enable unauthorized data access
Test previous/historical order delivery IDs to determine if authorization checks vary by order age
Check if HTTP method variations (POST, PUT, DELETE on the same endpoint) have different authorization logic

## MITRE ATT&CK
- T1190
- T1566
- T1110
- T1530
- T1526
- T1538

## Notes
This is a classic BOLA vulnerability in REST APIs. The reporter demonstrated responsible disclosure by providing clear reproduction steps and attempting Firebase token exploitation. The sequential ID space suggests bulk enumeration of potentially thousands of deliveries. Firebase token exposure warrants investigation into Firebase security rules and real-time database access controls. The lack of bounty amount specification may indicate this was a private program or the report was resolved before public disclosure.

## Full report
<details><summary>Expand</summary>

An authorization issue in the mobile app API allows any Instacart user to gain access to other users' order delivery chat logs. The `/api/v2/order_deliveries/:order_delivery_id/order_change_logs` endpoint does not sufficiently check if the user has permissions to access that particular order's chat logs. 

# Steps to Reproduce
I used Burp Suite to intercept the traffic between my iPhone and the Instacart API. When I found the "View 
Chat Logs" button on one of my past orders, I noticed it triggered the following API request:

```
GET /api/v2/order_deliveries/261932226/order_change_logs HTTP/1.1
Host: www.instacart.com
Accept: */*
[...]
```

This request is answered by the API with a JSON blob that contains chat messages that were exchanged between the buyer and the shopper. As well as a few other details like when the order was placed and if any changes were made to the order due to out of stock items. 

However, if you change the ID in the URL to something else, you will notice the API actually responds with the chat log and order data, regardless of who made the order. I tried with `261972220` and you can confirm this delivery does not belong to the user with account ███, but for instance `261972226` does.

# Risk
This vulnerability leaks private messages exchanged between shopper, driver, and customer. It may also include product names that were on the order if something had to be changed about the order. 

Here is an example:
{F98768}

This could lead to greater compromise, since the API returns the Firebase tokens for a few objects as well. So far I have not been able to do anything interesting with the Firebase tokens, but I'm not a Firebase expert. 

Here is an example (id: 261972220):

```
michiel@msp ~ $ curl https://instacart.firebaseio.com/order_deliveries/xy8TcFsDZiKm1JwnqqFp.json
{"46671792":"","46671794":"","46671795":"","46671802":"","46671804":"","46872067":"","46872104":"","46872195":"","46872357":""}%
```

# Mitigation
Implement an authorization check that makes sure only a users' own orders can be accessed.

</details>

---
*Analysed by Claude on 2026-05-24*
