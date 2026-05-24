# Anonymous Access to Payment Status Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 1546726 | https://hackerone.com/reports/1546726
- **Submitted:** 2022-04-21
- **Reporter:** codeslayer1337
- **Program:** Omise
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Broken Authentication, Broken Access Control, Information Disclosure
- **CVEs:** None
- **Category:** uncategorised

## Summary
The payment status endpoint at /payments/{payment_id}/status on api.omise.co is accessible without authentication, allowing unauthenticated users to query the status of any payment. This violates the principle of least privilege and exposes sensitive financial transaction information to unauthorized access.

## Attack scenario
1. Attacker discovers the payment status endpoint structure through API reconnaissance or documentation
2. Attacker crafts HTTP GET request to /payments/paym_test_5rjz482tky43reoil9f/status without authentication headers
3. Server responds with HTTP 200 and returns payment status JSON response
4. Attacker iterates through valid payment IDs using fuzzing or sequential enumeration techniques
5. Attacker correlates payment statuses with business intelligence to identify transaction patterns and customers
6. Attacker gains competitive intelligence or attempts social engineering attacks using payment information

## Root cause
Missing authentication and authorization checks on the payment status endpoint. The API endpoint was not properly gated to require valid user authentication and verification that the requesting user owns or has legitimate access to the payment record being queried.

## Attacker mindset
An attacker would recognize this as a reconnaissance opportunity to enumerate payment IDs and gather business intelligence. The low barrier to entry (no authentication required) makes this an attractive target for reconnaissance before launching more sophisticated attacks like payment manipulation or business espionage.

## Defensive takeaways
- Implement mandatory authentication on all API endpoints that handle sensitive data
- Add authorization checks to verify the requesting user owns the payment record or has explicit access
- Use opaque, non-sequential payment identifiers that cannot be easily enumerated
- Implement rate limiting on payment query endpoints to prevent reconnaissance attacks
- Add audit logging for all payment status requests to detect suspicious access patterns
- Conduct security code review of all authentication and authorization logic
- Implement API gateway-level access control policies
- Use API keys with proper scoping and expiration policies

## Variant hunting
Check other financial transaction endpoints (refunds, disputes, chargebacks) for similar authentication bypass
Test other payment providers' APIs for similar missing auth on transaction status endpoints
Enumerate other /payments/* endpoints for authentication requirements
Test for horizontal privilege escalation - can authenticated users access other users' payments
Check if payment IDs are predictable or sequential (enabling enumeration)
Test webhook endpoints which may have similar auth issues
Review invoice, receipt, and billing statement endpoints for similar vulnerabilities

## MITRE ATT&CK
- T1190
- T1526
- T1087
- T1566

## Notes
This is a critical authentication bypass on a financial API. The use of test payment ID in the example suggests this was discovered during testing but exploitation is trivial. The fact that payment status reveals transaction processing state could enable fraud detection evasion or social engineering attacks. Omise should have treated this with critical priority given PCI-DSS compliance implications.

## Full report
<details><summary>Expand</summary>

## Summary:
Found on the Payments Status function website, it can be accessed anonymously. payment status should only be accessible by accounts that make payments in a state that has successfully logged in.

## Steps To Reproduce:
access anonymously (without logging in) to the payment status function as in the example below

  1. Request:
GET /payments/paym_test_5rjz482tky43reoil9f/status HTTP/2
Host: api.omise.co
Sec-Ch-Ua: " Not A;Brand";v="99", "Chromium";v="100", "Google Chrome";v="100"
Sec-Ch-Ua-Mobile: ?0
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.127 Safari/537.36
Sec-Ch-Ua-Platform: "macOS"
Accept: */*
Sec-Fetch-Site: same-origin
Sec-Fetch-Mode: cors
Sec-Fetch-Dest: empty
Referer: https://api.omise.co/
Accept-Encoding: gzip, deflate
Accept-Language: en-US,en;q=0.9

2. Response:
HTTP/2 200 OK
Date: Thu, 21 Apr 2022 10:57:37 GMT
Content-Type: application/json; charset=utf-8
Content-Length: 18
X-Download-Options: noopen
X-Permitted-Cross-Domain-Policies: none
Referrer-Policy: strict-origin
Cache-Control: no-cache, no-store
Etag: W/"c9e654e8902aa47de7edcd7ab902ed16"
Set-Cookie: locale=en; path=/
X-Request-Id: 26180027472066089
Strict-Transport-Security: max-age=31536000; includeSubDomains

{"processed":true}

## Impact

Attackers can see payment status on the account's website without having to log in (anonymous)

Best regards,


CodeSlayer137

</details>

---
*Analysed by Claude on 2026-05-24*
