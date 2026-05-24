# CryptoNote Remote Node Denial of Service via Excessive Block Request Count

## Metadata
- **Source:** HackerOne
- **Report:** 506595 | https://hackerone.com/reports/506595
- **Submitted:** 2019-03-08
- **Reporter:** anonimal
- **Program:** Monero/CryptoNote
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Memory Exhaustion
- **CVEs:** None
- **Category:** memory-binary

## Summary
A remote attacker can send NOTIFY_REQUEST_GET_OBJECTS messages with an arbitrarily large number of block IDs, causing the victim node to exhaust all available free memory and crash. This vulnerability affects all Monero versions and most CryptoNote implementations that lack proper input validation on block request counts.

## Attack scenario
1. Attacker identifies a remote Monero node running an affected version (v0.14.0.2 or earlier)
2. Attacker crafts a NOTIFY_REQUEST_GET_OBJECTS protocol message with an extremely large blocks array (e.g., millions of block IDs)
3. Attacker sends the malicious message to the target node over the P2P network connection
4. The node's cryptonote_protocol_handler processes the request without validating the request count
5. The node allocates memory to handle all requested block IDs, rapidly exhausting available RAM
6. The node crashes due to out-of-memory condition, resulting in denial of service

## Root cause
The NOTIFY_REQUEST_GET_OBJECTS request handler in cryptonote_protocol_handler.inl lacks input validation on the number of blocks being requested. The handler processes requests of arbitrary size without enforcing a maximum limit, allowing an attacker to trigger unbounded memory allocation.

## Attacker mindset
An attacker with network access to a public remote node could exploit this trivially to disrupt node availability. The theoretical nature suggests this wasn't actively exploited in the wild at disclosure, but the simplicity of the attack makes it a practical DoS vector. The attacker seeks to degrade network quality by taking nodes offline.

## Defensive takeaways
- Implement strict input validation and rate limiting on all P2P protocol handlers, especially those handling resource-intensive operations
- Define and enforce maximum request sizes for all protocol messages (e.g., CURRENCY_PROTOCOL_MAX_BLOCKS_REQUEST_COUNT = 500)
- Drop connections from peers requesting excessive resources rather than attempting to fulfill the request
- Implement per-peer rate limiting and connection throttling to prevent resource exhaustion attacks
- Add monitoring and alerting for abnormal memory usage patterns or connection behavior
- Regularly audit P2P protocol handlers for similar unbounded resource allocation vulnerabilities

## Variant hunting
Search for other NOTIFY_* handlers that process arrays without size validation
Examine NOTIFY_REQUEST_TXS handler for similar unbounded transaction ID requests
Review all handlers processing variable-length collections from untrusted peers
Check for similar issues in other blockchain P2P implementations using CryptoNote protocol
Investigate bandwidth exhaustion variants using legitimate but very large block requests

## MITRE ATT&CK
- T1498.1
- T1499
- T1190

## Notes
The vulnerability was discovered theoretically rather than through active exploitation. The fix is straightforward: cap block request counts to 500. The issue affects all CryptoNote implementations except Zano, which already had mitigation. Credit given to cryptozoidberg and anonimal. This highlights the importance of defensive coding in consensus-critical P2P protocol handlers where untrusted input from any network peer must be strictly validated.

## Full report
<details><summary>Expand</summary>

## Summary:

Remote node DoS. See patch below.

## Releases Affected:

All Monero versions, including the recent v0.14.0.2. Possibly all CryptoNote implementations that aren't Zano.

## Steps To Reproduce:

Since this is *currently* a theoretical attack, non-code PoC detailed in the patch below.

## Supporting Material/References:

Based against current `master` `49afbd0c53d29656689f319c7d3543204ead4e59`:

```diff
commit 6620d099800d8935596f59834ce389868b2851f0 (HEAD -> cryptonote)
gpg: Signature made Fri 08 Mar 2019 02:57:58 AM UTC
gpg:                using RSA key 12186272CD48E2539E2DD29B66A76ECF914409F1
gpg: using pgp trust model
gpg: Good signature from "anonimal <anonimal@getmonero.org>" [ultimate]
gpg:                 aka "anonimal <anonimal@kovri.io>" [ultimate]
gpg:                 aka "anonimal <anonimal@sekreta.org>" [ultimate]
gpg: binary signature, digest algorithm SHA256, key algorithm rsa4096
Author: anonimal <anonimal@getmonero.org>
Date:   Fri Mar 8 02:21:38 2019 +0000

    cryptonote_protocol_handler: prevent potential DoS
    
    Essentially, one can send such a large amount of IDs that core exhausts
    all free memory. This issue can theoretically be exploited using very
    large CN blockchains, such as Monero.
    
    Credit given to CryptoNote author 'cryptozoidberg' for the fix.

diff --git a/src/cryptonote_protocol/cryptonote_protocol_handler.h b/src/cryptonote_protocol/cryptonote_protocol_handler.h
index efd986b53..c9e35d2d9 100644
--- a/src/cryptonote_protocol/cryptonote_protocol_handler.h
+++ b/src/cryptonote_protocol/cryptonote_protocol_handler.h
@@ -52,6 +52,7 @@ PUSH_WARNINGS
 DISABLE_VS_WARNINGS(4355)
 
 #define LOCALHOST_INT 2130706433
+#define CURRENCY_PROTOCOL_MAX_BLOCKS_REQUEST_COUNT 500
 
 namespace cryptonote
 {
diff --git a/src/cryptonote_protocol/cryptonote_protocol_handler.inl b/src/cryptonote_protocol/cryptonote_protocol_handler.inl
index c8b43fb91..023d1b457 100644
--- a/src/cryptonote_protocol/cryptonote_protocol_handler.inl
+++ b/src/cryptonote_protocol/cryptonote_protocol_handler.inl
@@ -889,6 +889,16 @@ namespace cryptonote
   int t_cryptonote_protocol_handler<t_core>::handle_request_get_objects(int command, NOTIFY_REQUEST_GET_OBJECTS::request& arg, cryptonote_connection_context& context)
   {
     MLOG_P2P_MESSAGE("Received NOTIFY_REQUEST_GET_OBJECTS (" << arg.blocks.size() << " blocks, " << arg.txs.size() << " txes)");
+
+    if (arg.blocks.size() > CURRENCY_PROTOCOL_MAX_BLOCKS_REQUEST_COUNT)
+      {
+        LOG_ERROR_CCONTEXT(
+            "Requested objects count is too big ("
+            << arg.blocks.size() << ") expected not more then "
+            << CURRENCY_PROTOCOL_MAX_BLOCKS_REQUEST_COUNT);
+        drop_connection(context, false, false);
+      }
+
     NOTIFY_RESPONSE_GET_OBJECTS::request rsp;
     if(!m_core.handle_get_objects(arg, rsp, context))
     {
```

This is essentially from https://github.com/hyle-team/zano/blob/master/src/currency_protocol/currency_protocol_handler.inl#L364 and confirmation will be needed that Monero doesn't already mitigate this elsewhere.

I have the above patch in my branch ready for PR but if you want to create your own patch, please give credit to cryptozoidberg and myself (anonimal). Thank you.

## Impact

Remote node DoS.

</details>

---
*Analysed by Claude on 2026-05-24*
