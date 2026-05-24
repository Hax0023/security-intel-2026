# Missing Permission Check on Transaction Signature Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 172733 | https://hackerone.com/reports/172733
- **Submitted:** 2016-09-28
- **Reporter:** supernatural
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Broken Access Control, Missing Authorization Check, Privilege Escalation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
An unauthenticated or low-privileged user can add digital signatures to transactions by directly calling the `/admin/secure_files.json` endpoint without proper permission validation. This allows unauthorized modification of transaction records and fraud through signature forgery.

## Attack scenario
1. Attacker identifies the `/admin/secure_files.json` endpoint through API reconnaissance or documentation
2. Attacker obtains a valid transaction ID from a target shop (via information disclosure or enumeration)
3. Attacker crafts a POST request with a malicious SVG file containing JavaScript payload as signature content
4. Attacker sets the `type` parameter to 'signatures' and includes the target `order_transaction_id`
5. Server processes request without validating attacker's permissions for transaction modification
6. Signature is successfully added to transaction and becomes visible on order page, appearing as legitimate

## Root cause
The endpoint lacks server-side authorization checks before processing signature uploads. The application validates the request format but fails to verify the user has 'manage_orders' or equivalent permissions required to modify transaction records.

## Attacker mindset
Opportunistic - discovered low-hanging fruit through endpoint exploration. Motivated by financial fraud (transaction tampering, forged authorization signatures) or competitive disruption.

## Defensive takeaways
- Implement granular permission checks on all admin endpoints before processing requests
- Verify user has appropriate scope/role for 'orders:manage' or 'transactions:write' before accepting signature uploads
- Add request validation to ensure transaction_id belongs to a shop the user has access to
- Log all signature upload attempts with user identity for audit trails
- Implement rate limiting on sensitive file upload endpoints
- Consider requiring additional authentication factors for transaction modification
- Validate file content does not contain executable code (SVG with scripts)

## Variant hunting
Check other file upload endpoints (`/admin/secure_files.json` variants) for similar authorization bypasses
Test permission checks on related transaction endpoints: `/admin/orders/{id}/transactions.json`
Examine other sensitive document types (PDFs, certificates, proofs) for authorization gaps
Verify CRUD operations on transactions enforce permissions consistently
Check if other user roles can bypass restrictions through parameter manipulation

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1548 - Abuse Elevation Control Mechanism
- T1078 - Valid Accounts (using unprivileged account)
- T1566 - Phishing (malicious signature in transaction)

## Notes
Report demonstrates clear authorization bypass with proof-of-concept payload. The SVG payload suggests attacker awareness of XSS vectors. Severity elevated because transaction signatures have legal/financial implications in commerce systems. Fix likely involved adding permission middleware to endpoint handler.

## Full report
<details><summary>Expand</summary>

Hi,

I found an endpoint for transaction signing
but user permission not checked on this endpoint
So an user without any permission in shop can add signature to transactions!


Endpoint: `/admin/secure_files.json`
Parameters:

````
{"secure_file":{"filetype":"svg","content":"PD94bWwgdmVyc2lvbj0iMS4wIiBzdGFuZGFsb25lPSJubyI/Pg0KPCFET0NUWVBFIHN2ZyBQVUJMSUMgIi0vL1czQy8vRFREIFNWRyAxLjEvL0VOIiAiaHR0cDovL3d3dy53My5vcmcvR3JhcGhpY3MvU1ZHLzEuMS9EVEQvc3ZnMTEuZHRkIj4NCjxzdmcgdmVyc2lvbj0iMS4xIiBiYXNlUHJvZmlsZT0iZnVsbCIgeG1sbnM9Imh0dHA6Ly93d3cudzMub3JnLzIwMDAvc3ZnIj4gIA0KICAgPHNjcmlwdCB0eXBlPSJ0ZXh0L2phdmFzY3JpcHQiPg0KICAgICAgYWxlcnQoZG9jdW1lbnQuZG9tYWluKTsNCiAgIDwvc2NyaXB0Pg0KPC9zdmc+","type":"signatures","order_transaction_id":"__Transaction_ID__"}}
````


Just fill `__Transaction_ID__`  in *order_transaction_id* and send request as user without permission
Response will be like this
````
{
  "secure_file": {
    "url": "https://shopify.s3.amazonaws.com/s/files/1/0917/1436/signatures/2e990586-6721-448a-a891-025471d6b2fe.svg?AWSAccessKeyId=AKIAJYM555KVYEWGJDKQ&Expires=1475694450&Signature=DmF7008ou7nn22ypD5Iyq%2BKomMQ%3D"
  }
}
````
when you back to order page or `/admin/orders/_order_id_/transaction.json`
signature file will be shown!

This should be limited to users who have access to transaction/order section!


Regards



</details>

---
*Analysed by Claude on 2026-05-24*
