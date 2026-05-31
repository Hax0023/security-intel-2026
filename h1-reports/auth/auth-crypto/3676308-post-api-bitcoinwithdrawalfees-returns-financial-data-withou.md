# Unauthenticated Access to Private Bitcoin Withdrawal Fees Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 3676308 | https://hackerone.com/reports/3676308
- **Submitted:** 2026-04-15
- **Reporter:** glferreira-devsecops
- **Program:** CoinMate
- **Bounty:** Not specified in report
- **Severity:** Medium
- **Vuln:** Broken Authentication, Missing Access Control, Inconsistent Security Policy
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The POST /api/bitcoinWithdrawalFees endpoint returns real-time Bitcoin withdrawal fee data without authentication, despite being documented as a private USER OPERATION endpoint. This is the only private endpoint in CoinMate's API that lacks authentication enforcement, while all other similar endpoints correctly reject unauthenticated requests.

## Attack scenario
1. Attacker discovers endpoint is documented as private in official API documentation and client libraries
2. Attacker sends unauthenticated POST request to /api/bitcoinWithdrawalFees and receives HTTP 200 with fee data
3. Attacker confirms other private endpoints reject same request with 'Invalid request' error
4. Attacker verifies arbitrary/fake authentication parameters are ignored by endpoint
5. Attacker polls endpoint repeatedly to monitor withdrawal fee fluctuations for trading strategy or market intelligence
6. Attacker exploits CORS header (Access-Control-Allow-Origin: *) to query endpoint from arbitrary web origins

## Root cause
Authentication middleware or filter is misconfigured or missing for the /api/bitcoinWithdrawalFees endpoint. The endpoint bypasses HMAC-SHA256 signature verification that is correctly enforced on all other USER OPERATION endpoints. This suggests either: (1) endpoint was accidentally marked as public during deployment, (2) authentication decorator/annotation was not applied, or (3) routing configuration excludes this endpoint from authentication filter chain.

## Attacker mindset
An attacker would recognize this as a low-effort information disclosure vulnerability. While withdrawal fees appear non-sensitive, they could be used for: competitive intelligence on exchange fee structures, arbitrage analysis, or as reconnaissance for targeting this exchange. The fact it's documented as private makes the misconfiguration obvious during security review.

## Defensive takeaways
- Implement automated integration tests that verify all endpoints documented as USER OPERATION enforce authentication
- Create a security matrix mapping endpoints to required authentication and validate during CI/CD
- Apply authentication decorators/annotations at route definition to prevent misconfiguration
- Use allowlist-based approach: all endpoints require auth by default unless explicitly marked as public
- Audit all official client library implementations against actual API behavior to catch inconsistencies
- Regular security review of authentication middleware to ensure uniform enforcement across all private endpoints
- Restrict CORS headers - avoid using Access-Control-Allow-Origin: * for authenticated endpoints
- Implement endpoint-level access control tests in security regression suite

## Variant hunting
Check other endpoints with generic names (e.g., /api/fees, /api/ethereumWithdrawalFees) for similar authentication bypass
Test all POST endpoints to identify any others missing authentication enforcement
Review endpoints that were recently added or modified - these may have inconsistent security implementation
Check for pattern: private endpoints that return market data vs account data - fee endpoints might have been treated as public
Audit endpoints accepting optional authentication parameters to see if unauthenticated access is allowed when params missing
Test all withdrawal-related endpoints (deposit fees, transfer fees) for same misconfiguration

## MITRE ATT&CK
- T1190
- T1526
- T1589
- T1590

## Notes
Report is exceptionally well-documented with direct evidence from official GitHub repository. The comparison table showing this is the only endpoint in its category lacking authentication is compelling. Report includes proof that all three official client libraries treat it as private (postPrivate() method), confirming intended design. The HTTP 405 on GET method confirms endpoint exists and is POST-only. CORS misconfiguration amplifies impact by enabling cross-origin exploitation from browser-based attacks. Severity is Medium rather than High because fee data alone lacks direct financial or account compromise impact, though it could support reconnaissance for more serious attacks.

## Full report
<details><summary>Expand</summary>

## Summary

The `POST /api/bitcoinWithdrawalFees` endpoint returns real-time Bitcoin withdrawal fee data **without requiring any authentication**, despite being explicitly documented as a **"USER OPERATION"** (private endpoint) in the [official CoinMate API documentation](https://github.com/coinmate-io/coinmate-api-examples/blob/main/resources/doc.md#bitcoin-withdrawal-fees-bitcoinwithdrawalfees).

This is the **only** private endpoint that does not enforce authentication. All other `USER OPERATION` endpoints (e.g., `/api/balances`, `/api/openOrders`, `/api/bitcoinDepositAddresses`) correctly reject unauthenticated requests with `{"error": true, "errorMessage": "Invalid request"}`.

## Root Cause

The authentication middleware/filter on the `/api/bitcoinWithdrawalFees` endpoint is misconfigured, allowing the request to bypass HMAC-SHA256 signature verification. This is confirmed by the fact that all three official API client libraries (Java, TypeScript, Python) invoke this endpoint via their `postPrivate()` methods, which attach `clientId`, `nonce`, `publicKey`, and `signature` parameters.

## Evidence from Official Documentation

From [`resources/doc.md` (line 1230-1246)](https://github.com/coinmate-io/coinmate-api-examples/blob/main/resources/doc.md):

```
## Bitcoin withdrawal fees [/bitcoinWithdrawalFees]
**USER OPERATION**

### POST [POST]
+ Request (application/x-www-form-urlencoded)

        clientId=1038&nonce=15270794730&signature=94933BF157B9405A1C2F330902987300B3A73DE620023E1782635AAF16984729
```

The documentation explicitly shows authentication parameters (`clientId`, `nonce`, `signature`) as **required** for this endpoint.

## Evidence from Official Client Libraries

**TypeScript** ([CoinmateClient.ts](https://github.com/coinmate-io/coinmate-api-examples/blob/main/typescript/src/client/CoinmateClient.ts)):
```typescript
async getBitcoinWithdrawalFees(): Promise<CoinmateResponse<any>> {
    return this.httpClient.postPrivate('/bitcoinWithdrawalFees');
    //                      ^^^^^^^^^^^ — treated as PRIVATE
}
```

**Java** ([CoinmateClient.java](https://github.com/coinmate-io/coinmate-api-examples/blob/main/java/main/java/org/example/coinmate/client/CoinmateClient.java)):
```java
public JsonObject getBitcoinWithdrawalFees() throws IOException {
    return httpClient.postPrivate("/bitcoinWithdrawalFees", Map.of());
    //                ^^^^^^^^^^^ — treated as PRIVATE
}
```

## Steps to Reproduce

### Step 1: Send unauthenticated request to the vulnerable endpoint

```
curl -s -X POST https://coinmate.io/api/bitcoinWithdrawalFees
```

**Response (HTTP 200 — data returned WITHOUT authentication):**
```json
{
  "error": false,
  "errorMessage": null,
  "data": {
    "low": 0.000011,
    "high": 0.000019,
    "timestamp": 1776286189432
  }
}
```

### Step 2: Confirm other private endpoints correctly reject unauthenticated requests

```
curl -s -X POST https://coinmate.io/api/balances
```

**Response (correctly blocked):**
```json
{
  "error": true,
  "errorMessage": "Invalid request",
  "data": null
}
```

### Step 3: Confirm the endpoint ignores arbitrary authentication parameters

```
curl -s -X POST https://coinmate.io/api/bitcoinWithdrawalFees \
  -d "clientId=999&publicKey=FAKE_KEY&nonce=12345&signature=AAAAAAAAAAAAAAAAAAAAAA"
```

**Response (still returns data — authentication is completely bypassed):**
```json
{
  "error": false,
  "errorMessage": null,
  "data": {
    "low": 0.000011,
    "high": 0.000019,
    "timestamp": 1776286189615
  }
}
```

This confirms the authentication middleware is **not invoked at all** for this endpoint.

### Step 4: Confirm GET is not allowed (POST-only API endpoint)

```
curl -s -X GET https://coinmate.io/api/bitcoinWithdrawalFees
```

**Response (HTTP 405):**
```json
{
  "type": "about:blank",
  "title": "Method Not Allowed",
  "status": 405,
  "detail": "Method 'GET' is not supported.",
  "instance": "/api/bitcoinWithdrawalFees"
}
```

## Authentication Enforcement Comparison

| Endpoint | Classification | Auth Required? | Unauthenticated Response |
|:---------|:--------------|:--------------:|:-------------------------|
| POST /api/balances | USER OPERATION | Yes | "Invalid request" |
| POST /api/openOrders | USER OPERATION | Yes | "Invalid request" |
| POST /api/traderFees | USER OPERATION | Yes | "Invalid request" |
| POST /api/bitcoinDepositAddresses | USER OPERATION | Yes | "Invalid request" |
| POST /api/transactionHistory | USER OPERATION | Yes | "Invalid request" |
| POST /api/tradeHistory | USER OPERATION | Yes | "Invalid request" |
| POST /api/orderHistory | USER OPERATION | Yes | "Invalid request" |
| POST /api/transferHistory | USER OPERATION | Yes | "Invalid request" |
| **POST /api/bitcoinWithdrawalFees** | **USER OPERATION** | **No** | **Returns data** |

The endpoint is the only one in its category that fails to enforce authentication.

## Cross-Origin Exploitation

The response includes `Access-Control-Allow-Origin: *`, meaning any website on the internet can read this data cross-origin via JavaScript:

```javascript
// Any website can execute this:
fetch('https://coinmate.io/api/bitcoinWithdrawalFees', {method: 'POST'})
  .then(r => r.json())
  .then(d => console.log('Fee data:', d.data));
```

See the attached `cors_poc.html` for a working demonstration.

## Recommended Fix

Apply the same authentication middleware used by all other `USER OPERATION` endpoints to `/api/bitcoinWithdrawalFees`.

## Impact

## Security Impact

**1. Broken Access Control (OWASP A01:2021):**
A private endpoint designed to require HMAC-SHA256 authentication (`clientId` + `nonce` + `publicKey` + `signature`) is fully accessible without any credentials. This demonstrates a gap in the authentication enforcement layer — the endpoint was classified as `USER OPERATION` in the official documentation, its official client libraries (TypeScript, Java, Python) all invoke it via `postPrivate()`, and the documented request example includes full authentication parameters. Yet the server does not validate any of them.

**2. Information Disclosure of Internal Operational Data:**
The endpoint exposes real-time internal fee calculation data that changes dynamically:
- `low`: Current minimum BTC withdrawal fee (e.g., 0.000011 BTC)
- `high`: Current maximum BTC withdrawal fee (e.g., 0.000019 BTC)  
- `timestamp`: Exact millisecond server-side timestamp of the last fee recalculation

This data reflects CoinMate's internal fee engine state and is not equivalent to static fee schedules published on marketing pages.

**3. Cross-Origin Data Theft via CORS Misconfiguration:**
The response includes `Access-Control-Allow-Origin: *`, which means any malicious website can silently read this data via JavaScript without the user's knowledge. A phishing page or compromised ad could harvest fee data in the background. See the attached `cors_poc.html` for a working demonstration.

**4. Authentication Framework Inconsistency:**
This is the **only** `USER OPERATION` endpoint (out of 14+ tested) that does not enforce authentication. All others (`/api/balances`, `/api/openOrders`, `/api/traderFees`, `/api/bitcoinDepositAddresses`, `/api/transactionHistory`, `/api/tradeHistory`, `/api/orderHistory`, `/api/transferHistory`) correctly reject unauthenticated requests with `{"error": true, "errorMessage": "Invalid request"}`. This inconsistency strongly indicates a configuration error rather than an intentional design decision, and raises the concern that other endpoints may have similar gaps that have not yet been discovered.

**5. Potential for Broader Impact:**
If the root cause is a missing filter/interceptor registration for this specific path, the same class of misconfiguration could affect other endpoints that were recently added, refactored, or moved between public and private scopes.

</details>

---
*Analysed by Claude on 2026-05-31*
