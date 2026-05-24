# Node.js HTTP/2 Large Settings Frame Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 446662 | https://hackerone.com/reports/446662
- **Submitted:** 2018-11-18
- **Reporter:** galgo
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Denial of Service, Resource Exhaustion, Unvalidated Input Processing
- **CVEs:** None
- **Category:** memory-binary

## Summary
The HTTP/2 module in Node.js fails to properly validate and rate-limit incoming SETTINGS frames, allowing attackers to send oversized SETTINGS frames with many parameters to exhaust CPU resources. A single attacker can achieve 100% CPU utilization on one core by opening multiple connections and sending large SETTINGS payloads, with no connection timeout enforcement.

## Attack scenario
1. Attacker establishes multiple HTTP/2 connections to target Node.js HTTP/2 server
2. Attacker crafts SETTINGS frames with excessively large payloads (e.g., 14400 bytes) containing numerous settings entries
3. Attacker sends the malicious SETTINGS frames across the established connections repeatedly
4. Server processes each SETTINGS frame without proper validation, consuming CPU cycles for parsing and handling
5. Attacker continues sending frames as server does not enforce connection timeouts or rate limiting
6. Target server becomes unresponsive as one CPU core reaches 100% utilization, causing denial of service

## Root cause
The HTTP/2 SETTINGS frame handler in Node.js does not implement proper input validation limits or rate limiting on frame size and parameter count. Additionally, the lack of connection idle timeouts allows sustained attacks without interruption.

## Attacker mindset
An attacker looking to disrupt availability of HTTP/2 services with minimal resources. By exploiting the RFC 7540 section 10.5 attack vector, they can achieve high impact DoS from a single machine without needing sophisticated botnet infrastructure.

## Defensive takeaways
- Implement strict validation on SETTINGS frame payload size and enforce RFC 7540 compliance limits
- Add rate limiting and throttling mechanisms for incoming SETTINGS frames per connection
- Enforce connection idle timeouts to prevent sustained low-rate attacks
- Monitor CPU usage per connection and implement per-connection resource limits
- Add logging and alerting for abnormal SETTINGS frame patterns
- Set maximum limits on the number of settings parameters allowed in a single frame

## Variant hunting
Similar frame-based DoS attacks may exist in HTTP/2 implementations affecting other frame types (HEADERS, DATA, WINDOW_UPDATE). Check for undersized timeout configurations, missing rate limiters on other protocol handlers, and validate frame size enforcement across all frame types in HTTP/2 stacks.

## MITRE ATT&CK
- T1190
- T1498

## Notes
This vulnerability aligns with documented HTTP/2 attack vectors in RFC 7540 section 10.5. The issue was likely fixed in subsequent Node.js versions through input validation improvements and timeout enforcement. Testing confirmed reproducibility with Node 8.11.3.

## Full report
<details><summary>Expand</summary>

Hi,
 
I would like to report a vulnerability in the http2 module of Node.js. 
 
In section 10.5 of the HTTP/2 RFC an attack is described where an attacker is sending large SETTINGS frames that includes many settings inside it. 
We tested this scenario by opening many connections to the server and sending a SETTINGS frame with payload size of 14400 bytes and we were able to overload one CPU core with 100% usage with a single machine. 
Another important thing to mention is that node doesn’t close the connection to the server after some time so the attacker is able to continue sending those large SETTINGS frames.

This was tested against Node version 8.11.3
You can the code that was used to start the http2 server and also the script that we used for attacking it attached.

## Impact

Denial of Service

</details>

---
*Analysed by Claude on 2026-05-24*
