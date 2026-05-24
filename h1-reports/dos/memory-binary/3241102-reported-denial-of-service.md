# Denial of Service via Invalid block_blob Parameter in calc_pow RPC Endpoint

## Metadata
- **Source:** HackerOne
- **Report:** 3241102 | https://hackerone.com/reports/3241102
- **Submitted:** 2025-07-08
- **Reporter:** jehrenhofermagicgrants
- **Program:** Monero
- **Bounty:** Waived by MAGIC Grants/Ada Logics
- **Severity:** medium
- **Vuln:** Denial of Service, Improper Input Validation, Uncontrolled Process Termination
- **CVEs:** None
- **Category:** memory-binary

## Summary
The calc_pow RPC endpoint in Monero's monerod daemon crashes when provided with an insufficiently sized block_blob parameter that does not meet the 43-byte minimum requirement for Cryptonight variant 1. An attacker can remotely trigger an exit(1) call via a crafted JSON-RPC request, causing denial of service by crashing the server.

## Attack scenario
1. Attacker identifies the publicly exposed calc_pow RPC endpoint on a Monero node
2. Attacker crafts a JSON-RPC request with a block_blob parameter containing fewer than 43 bytes of hex data
3. Request is sent to http://target:18081/json_rpc with the malicious calc_pow method
4. The RPC handler processes the request and calls get_block_longhash() without validating blob size
5. The cn_slow_hash function in slow-hash.c detects insufficient data and calls exit(1)
6. The monerod process terminates immediately, disrupting service availability

## Root cause
Input validation for the block_blob parameter is missing at the RPC handler level in core_rpc_server.cpp. The crypto validation layer (slow-hash.c) implements a hard exit(1) when cryptonight processing encounters invalid data sizes, but does not gracefully return an error. The RPC endpoint passes unsanitized user input directly to cryptographic functions without bounds checking.

## Attacker mindset
An attacker could repeatedly send malformed block_blob requests to any exposed Monero RPC port to repeatedly crash nodes, disrupting the blockchain network or targeting specific mining operations. This is a trivial attack requiring no special resources or knowledge of Monero internals.

## Defensive takeaways
- Implement strict input validation at RPC handler entry points before passing data to downstream functions
- Replace hard exit(1) calls in library/crypto code with proper error return codes or exceptions
- Add size bounds checking for binary blob parameters (block_blob, seed_hash) early in the RPC call stack
- Validate that parsed block_blob meets minimum length requirements (43 bytes for Cryptonight v1) before cryptographic processing
- Consider rate limiting or authentication on sensitive RPC endpoints like calc_pow
- Use fuzzing-guided testing (as Ada Logics did) as part of security validation for network-exposed APIs

## Variant hunting
Search for other RPC endpoints accepting binary blob parameters without size validation (get_block_header_by_hash, verify_signature, etc.)
Audit all cryptographic function entry points for implicit assumptions about input size that could lead to exit() calls
Test other parameters in calc_pow (seed_hash, major_version) for similar DoS vectors
Check if similar validation gaps exist in wallet RPC endpoints or P2P protocol handlers
Review fuzzing coverage for all RPC methods that accept variable-length binary data

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1499: Endpoint Denial of Service

## Notes
This vulnerability was discovered through systematic fuzzing by Ada Logics under contract with MAGIC Grants' Monero Fund. The fix is straightforward validation, but the discovery highlights the value of fuzzing-driven security research. The issue affects availability but not confidentiality or integrity. monerod operators running public RPC endpoints are at risk. The suggested patch adds a 43-byte minimum length check before cryptographic processing begins.

## Full report
<details><summary>Expand</summary>

*This submission is being made by [MAGIC Grants](https://magicgrants.org), a public charity that supports critical infrastructure. The MAGIC Monero Fund, one of our committees, [recently contracted](https://donate.magicgrants.org/monero/projects/fuzzing-monero-rpc) [Ada Logics](https://adalogics.com/) to perform fuzzing work on Monero's RPC endpoints. This submission has been forwarded from Ada Logics to the Monero team. We waive the opportunity for a monetary reward.*

---

PoC:

1) start monerod on a local machine
2) perform the following RPC call:

$ curl http://127.0.0.1:18081/json_rpc -d '{"jsonrpc":"2.0","id":"0","method":"calc_pow","params":{"major_version": 7, "height": 5, "block_blob": "010101", "seed_hash": "1111111111111111111111111111111111111111111111111111111111111111"}' -H 'Content-Type: application/json'


The monerod server will crash with the message "Cryptonight variant 1 needs at least 43 bytes of data".

The issue happens because "block_blob" does not produce a 43 byte hex string.

The DoS issue is the "_exit(1)" here: https://github.com/monero-project/monero/blob/17f6fb871c09507cd13c23fdecd9cbcca3f01326/src/crypto/slow-hash.c#L139

The problem is that the RPC arguments can control execution so that this exit is reached.

The way to fix this issue is likely to just place some checking earlier in the callstack.

This was found by the fuzzing harness we're developing and the callstack from Monero's code is:

```
    #0 0x562d9ed19751 in __sanitizer_print_stack_trace /src/llvm-project/compiler-rt/lib/asan/asan_stack.cpp:87:3
    #1 0x562d9ec1e6e8 in fuzzer::PrintStackTrace() /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerUtil.cpp:210:5                                                                                                                          
    #2 0x562d9ec01a83 in fuzzer::Fuzzer::CrashCallback() /src/llvm-project/compiler-rt/lib/fuzzer/FuzzerLoop.cpp:231:3
    #3 0x7fb1be04251f  (/lib/x86_64-linux-gnu/libc.so.6+0x4251f) (BuildId: d5197096f709801829b118af1b7cf6631efa2dcd)
    #4 0x7fb1be0969fb in __pthread_kill_implementation nptl/./nptl/pthread_kill.c:43:17
    #5 0x7fb1be0969fb in __pthread_kill_internal nptl/./nptl/pthread_kill.c:78:10
    #6 0x7fb1be0969fb in pthread_kill nptl/./nptl/pthread_kill.c:89:10
    #7 0x7fb1be042475 in gsignal signal/../sysdeps/posix/raise.c:26:13
    #8 0x7fb1be0287f2 in abort stdlib/./stdlib/abort.c:79:7
    #9 0x562da0002d62 in cn_slow_hash /src/monero/monero/src/crypto/slow-hash.c:911:5
    #10 0x562d9fb9e2b6 in cn_slow_hash /src/monero/monero/src/crypto/hash.h:74:5
    #11 0x562d9fb9e2b6 in cryptonote::get_block_longhash(cryptonote::Blockchain const*, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> > const&, crypto::hash&, unsigned long, int, crypto::hash cons
t*, int) /src/monero/monero/src/cryptonote_core/cryptonote_tx_utils.cpp:702:7
    #12 0x562d9f1add90 in cryptonote::core_rpc_server::on_calcpow(epee::misc_utils::struct_init<cryptonote::COMMAND_RPC_CALCPOW::request_t> const&, std::__1::basic_string<char, std::__1::char_traits<char>, std::__1::allocator<char> >&, epee::json_rpc::error&, epee::net_utils::connection_context_base const*) /src/monero/monero/src/rpc/core_rpc_server.cpp:2098:5
```

For fuzzing purposes we use this diff to patch out the issue (line numbers may be a slight off as we have some more patches around):

--- a/src/rpc/core_rpc_server.cpp
+++ b/src/rpc/core_rpc_server.cpp
```
@@ -2074,6 +2075,12 @@ namespace cryptonote
       error_resp.message = "Wrong block blob";
       return false;
     }
+    // std::cout << "Blob data: " << blockblob.size() << " bytes" << std::endl;
+    if (blockblob.size() < 43) {
+      error_resp.code = CORE_RPC_ERROR_CODE_WRONG_BLOCKBLOB;
+      error_resp.message = "Wrong block blob";      
+      return false;
+    }
     if(!m_core.check_incoming_block_size(blockblob))
     {
       error_resp.code = CORE_RPC_ERROR_CODE_WRONG_BLOCKBLOB_SIZE;
```

## Impact

Potential denial of service; potential monerod crash

</details>

---
*Analysed by Claude on 2026-05-24*
