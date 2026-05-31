# HMAC Signature Verification Omits Endpoint and Payload - CoinMate API Request Forgery

## Metadata
- **Source:** HackerOne
- **Report:** 3670955 | https://hackerone.com/reports/3670955
- **Submitted:** 2026-04-13
- **Reporter:** glferreira-devsecops
- **Program:** CoinMate (coinmate.io)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** CWE-325: Missing Required Cryptographic Step, CWE-345: Insufficient Verification of Data Authenticity, CWE-347: Improper Verification of Cryptographic Signature, Cryptographic Binding Failure, Request Forgery via Signature Malleability
- **CVEs:** None
- **Category:** uncategorised

## Summary
CoinMate's API authentication uses HMAC-SHA256 signatures calculated only from nonce, clientId, and publicKey, completely omitting the HTTP endpoint and request body. An attacker can intercept and hijack a valid signature from a benign request, drop the original packet to preserve nonce freshness, then replay the same signature on a destructive endpoint with malicious parameters to execute unauthorized trades or withdrawals.

## Attack scenario
1. Attacker positions themselves on network path between victim and CoinMate API (MITM via rogue WiFi, ISP compromise, or browser extension)
2. Victim initiates legitimate read-only API request (e.g., GET /api/balances) with valid HMAC signature containing nonce N
3. Attacker intercepts the request and drops it before reaching CoinMate servers, preventing nonce consumption
4. Attacker extracts and reuses the valid HMAC signature, replacing endpoint with destructive path (e.g., POST /api/sellLimit) and injecting malicious parameters (amount, price, currencyPair)
5. Attacker forwards forged request to CoinMate backend with original signature and fresh nonce
6. CoinMate cryptographically verifies signature (valid because endpoint/payload not included in HMAC), checks nonce (unused), and executes unauthorized trade/withdrawal draining user funds

## Root cause
HMAC pre-image construction uses only identity components (nonce + clientId + publicKey) and excludes intent components (HTTP method, endpoint path, request body). This architectural flaw violates cryptographic binding principles by decoupling authentication from authorization scope, allowing signatures to be replayed across different operations with modified parameters.

## Attacker mindset
Sophisticated adversary with network interception capability (MITM position). Rather than brute-forcing or stealing keys, they exploit the cryptographic architecture to achieve maximum impact with minimum effort. They understand that nonce replay protection can be bypassed by dropping the original request, and they recognize that signature malleability enables cross-endpoint request forgery affecting financial transactions.

## Defensive takeaways
- Include all security-relevant request elements in HMAC calculation: HTTP method, full endpoint path, query parameters, and request body/payload
- Bind signatures to specific operations and resources to prevent cross-endpoint replay attacks
- Implement request integrity validation that ties cryptographic proof to actual intent, not just identity
- Use canonical request formatting (similar to AWS SigV4) to prevent parameter reordering or injection attacks
- Consider additional protections: endpoint whitelisting per API key, request body hashing, timestamp validation with tight windows
- For financial APIs, implement transaction-specific signatures that cannot be reused across different operations
- Add payload integrity checks independent of signature validation as defense-in-depth

## Variant hunting
Review other endpoints using same HMAC scheme for cross-endpoint hijacking potential (especially high-risk withdrawal/trading endpoints)
Test signature validity when modifying individual parameters (amount, currency, recipient) while keeping nonce/clientId constant
Attempt GET-to-POST signature reuse for parameters injection into more privileged operations
Verify if signatures include request headers (User-Agent, timestamp) or only body parameters
Test for nonce window exploitation: can repeated nonce values within short timeframe be accepted
Check if API Keys have operation-level restrictions that this vulnerability bypasses
Review webhook/callback signature verification for identical flaws
Audit historical transactions for anomalous trades matching timing of network interception windows

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1199: Trusted Relationship (MITM exploitation)
- T1040: Traffic Capture or Replay
- T1556: Alter Authentication Process
- T1187: Forced Authentication
- T0868: Manipulation of View

## Notes
Report includes detailed methodology for reproducing the vulnerability without false positives from nonce replay protection. Key insight: manual cURL testing fails not because signature validation works, but because nonce exhaustion occurs - the true vulnerability requires dropping the original request to preserve nonce freshness. Attached Python PoC demonstrates wire-level exploitation. This represents a fundamental cryptographic architecture flaw affecting all API operations, particularly high-risk financial transactions. Severity is amplified by financial impact (complete account compromise, fund drainage) and lack of user awareness during execution.

## Full report
<details><summary>Expand</summary>

# ZERO-DAY VULNERABILITY REPORT
**Asset:** `coinmate.io` (Core REST API - https://coinmate.io/api)
**Vulnerability Type:** CWE-325 (Missing Required Cryptographic Step) / CWE-345 (Payload Malleability & Request Forgery)
**Severity Category:** High (CVSS v3.0: 8.1 - AV:N/AC:L/PR:N/UI:R/S:U/C:H/I:H/A:N)

> **Important Triage Note:** To prevent false negatives during verification, please carefully read the "Attacker Execution Methodology" section before attempting manual reproduction. Manual re-use of cURL signatures will fail due to the Database's Nonce Replay Protection. We have provided an automated Python PoC to simulate the precise network conditions of the exploit.

---

## 1. Executive Summary & Impact

The CoinMate API employs HMAC-SHA256 signatures for authentication. However, a systemic architectural flaw exists in how the backend constructs the HMAC pre-image.

Currently, the signature is calculated strictly using:
`HMAC(private_key, nonce + clientId + publicKey)`

**CRITICAL FINDING: The cryptographic signature completely omits the HTTP Endpoint (URL Path) and the Request Body (Payload/Parameters).**

Because identity (the Signature) is not bound to intent (the Payload/Endpoint), the implementation lacks integrity and non-repudiation.

### The Attack Vector (Man-in-the-Middle)
An attacker intercepting network traffic (e.g., via a rogue public WiFi, compromised ISP layer, or malicious browser extension) can steal a valid API signature intended for a harmless, read-only action (such as `/api/balances`). 
By **dropping** the harmless request from reaching Coinmate, the attacker prevents the `nonce` from being consumed by your database. The attacker then injects malicious POST parameters (e.g., `amount`, `price`, `currencyPair`) and forwards the hijacked signature to a destructive trading or withdrawal endpoint (e.g., `/api/sellLimit`). 

The Coinmate backend mathematically verifies the HMAC, sees a valid, unburned Nonce, and executes the forged payload on the destructive endpoint without realizing the data was altered in transit.

**Security Impact:** Complete compromise of API-connected accounts. An attacker can drain funds, execute Flash Crashes via market manipulation, and bypass all intended API Key endpoint restrictions, resulting in catastrophic loss of user assets.

---

## 2. Exploitation Flow (Malleability Diagram)

```text
[Victim Device] -----> (Initiates: POST /api/balances with Signature X & Nonce 1) -----> [Attacker]
                                                                                             |
                                                                [Attacker DROPS the packet]
                                                                [Attacker HIJACKS Signature X]
                                                                [Attacker INJECTS 'sellLimit' parameters]
                                                                                             |
[Coinmate Database] <----- (Attacker Forges: POST /api/sellLimit with Signature X) <---------/
         |
[Coinmate verifies Signature X is mathematically valid]
[Coinmate executes the SELL ORDER based on the Attacker's forged parameters]
```

---

## 3. Steps to Reproduce (Using Attached E2E PoC)

**Why Manual cURL Testing Often Fails (False Positives):**
If a security analyst tries to test this by sending a valid request to `/balances`, taking the signature from that successful request, changing the URL/body, and sending it again via cURL to `/sellLimit`, the backend will reject it with `"Access denied"`. **This is NOT because the signature validation caught the changed payload; it is because the backend's Anti-Replay mechanism saw that the `nonce` was already used.** 

In a real attack, the attacker intercepts and *drops* the first request, preserving the freshness of the nonce.

**To irrefutably prove the vulnerability, use the attached automated Python validation script:**

1. Download the attached `02_Coinmate_Exploit_E2E_Validator_Script.py`.
2. Open the script and insert your active isolated testing API Keys into the `CLIENT_ID`, `PUBLIC_KEY`, and `PRIVATE_KEY` variables.
3. Ensure Python and the requests library are installed (`pip install requests`).
4. Run the script: `python3 02_Coinmate_Exploit_E2E_Validator_Script.py`

### What the Script Automatically Proves (Wire-by-Wire):
*   **Action 1 (Safeguard Check):** The script validates your keys by hitting `/balances`.
*   **Action 2 (Proving the Nonce Trap):** The script intentionally reuses the signature from Action 1. It receives `Access denied`, demonstrating to the analyst the exact behavior of Nonce Exhaustion.
*   **Action 3A (Body Malleability Isolation):** The script injects malicious POST parameters (`MALICIOUS_INJECTION=HACKED_DATA`) into a secure request. CoinMate processes it perfectly, proving the Hash completely ignores the Payload Body.
*   **Action 3B (Zero-Day Cross-Endpoint Hijacking):** The script generates a *fresh* signature for `/balances`, intercepts it internally, injects forged trading variables (`currencyPair=BTC_EUR`), and redirects the payload to a completely different endpoint (`/api/openOrders`).
*   **Conclusion:** Coinmate processes the hijacked payload and returns `200 OK` (or a business logic error inside a 200 response), officially bypassing the Cryptographic HMAC constraints and proving the CWE-325 and CWE-345 vulnerabilities simultaneously across two different vectors.

---

## 4. Required Remediation (API Authentication Upgrade)

To secure the Mainnet API, CoinMate must immediately deprecate the current signature logic and adopt the industry standard for cryptographic API validation (utilized by Binance, Kraken, and Coinbase).

The CoinMate backend must be updated to expect and verify signatures that include the full request context:
`HMAC = SHA256( private_key, nonce + HTTP_METHOD + REQUEST_PATH + POST_BODY_STRING + clientId + publicKey )`

By enforcing this structure, any MITM attacker attempting to alter an `/api/balances` request into an `/api/openOrders` request will instantly break the Hash integrity, causing the backend to throw a legitimate cryptography exception.

---
**Scope Declaration:** This vulnerability resides entirely within CoinMate's proprietary backend API architecture algorithms. It is not a vulnerability in a third-party application, but rather a systemic flaw in the core REST API authentication framework.

## Impact

Complete compromise of API-connected accounts. An attacker can drain funds, execute Flash Crashes via market manipulation, and bypass all intended API Key endpoint restrictions, resulting in catastrophic loss of user assets. Because identity (the Signature) is not bound to intent (the Payload/Endpoint), the implementation lacks integrity and non-repudiation.

</details>

---
*Analysed by Claude on 2026-05-31*
