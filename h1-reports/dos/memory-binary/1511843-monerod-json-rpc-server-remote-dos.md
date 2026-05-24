# monerod JSON RPC Server Remote Denial of Service via Unbounded Content-Length

## Metadata
- **Source:** HackerOne
- **Report:** 1511843 | https://hackerone.com/reports/1511843
- **Submitted:** 2022-03-15
- **Reporter:** m31007
- **Program:** Monero
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Memory Exhaustion, Resource Exhaustion, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The monerod JSON RPC server fails to validate or limit the Content-Length header in HTTP requests, allowing an unauthenticated attacker to trigger arbitrary memory allocation and exhaust system resources. This leads to Out-of-Memory conditions and process termination without requiring any credentials.

## Attack scenario
1. Attacker identifies monerod instance with exposed JSON RPC port (default 18081)
2. Attacker crafts HTTP request with excessively large Content-Length header (e.g., gigabytes)
3. monerod allocates memory proportional to declared Content-Length without validation
4. Attacker sends multiple requests or slowly drips data to maintain allocated memory
5. System memory becomes exhausted as monerod holds allocations
6. OOM killer terminates monerod process, causing denial of service

## Root cause
The HTTP request parsing logic in monerod's RPC server accepts the Content-Length header value without implementing upper bounds checks or per-request memory limits. The server attempts to allocate buffer space matching the declared length before validating actual request content.

## Attacker mindset
An attacker with network access to the RPC port seeks to disrupt blockchain operations and node availability. The attack requires no authentication, making it trivial to execute against exposed instances. The attacker may be a competitor, network disruptor, or malicious network neighbor.

## Defensive takeaways
- Implement strict Content-Length validation with configurable maximum request size limits
- Enforce per-request memory allocation caps independent of client-supplied headers
- Implement request timeout mechanisms and connection throttling per source IP
- Require authentication/authorization for RPC endpoints before processing HTTP bodies
- Use memory-efficient streaming parsers instead of buffering entire requests
- Bind RPC services to localhost or restricted networks by default
- Monitor memory usage patterns and implement circuit breakers for suspicious behavior
- Add logging and metrics for oversized requests to detect attack patterns

## Variant hunting
Look for similar issues in: (1) Other cryptocurrency daemons with JSON RPC interfaces (Bitcoin Core, Ethereum clients), (2) Any HTTP server accepting user-controlled Content-Length without limits, (3) RPC frameworks that auto-allocate buffers based on request headers, (4) WebSocket servers with similar message size handling, (5) gRPC services without message size restrictions

## MITRE ATT&CK
- T1190
- T1499
- T1561

## Notes
The vulnerability is straightforward but impactful due to lack of authentication requirement and ease of exploitation. The fix likely requires adding a configurable max_request_size parameter and validating Content-Length against it before allocation. Exposure is particularly dangerous for public nodes providing blockchain services. The report demonstrates good reproduction steps with attached exploit script.

## Full report
<details><summary>Expand</summary>

Monero daemon (monerod)  does not limit Content-length variable when processing incoming HTTP requests.
We can force monerod to allocate arbitrary amount of memory.


How to reproduce:
1) compile monero https://github.com/monero-project/monero
2) run it:
$ ulimit -Sv 1000000000
$ ./bin/monerod --rpc-login test:test  --rpc-bind-ip 0.0.0.0 --confirm-external-bind

3) run attached script m1.py
$ python2 ./m1.py 192.168.1.34

4) after some time OOM killer will stop monerod

## Impact

monerod process can be stopped remotely, no authentication is required. 
An access to JSON RPC port is enough.

</details>

---
*Analysed by Claude on 2026-05-24*
