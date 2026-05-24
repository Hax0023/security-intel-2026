# DoS by Memory Exhaustion in net/imap Response Parser via Unvalidated Range Expansion

## Metadata
- **Source:** HackerOne
- **Report:** 2987782 | https://hackerone.com/reports/2987782
- **Submitted:** 2025-02-11
- **Reporter:** manun
- **Program:** Ruby
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service, Memory Exhaustion, Improper Input Validation, Resource Limit Bypass
- **CVEs:** None
- **Category:** memory-binary

## Summary
Net::IMAP versions 0.3.2 through 0.5.5 contain a DoS vulnerability where a malicious IMAP server can exhaust client memory by sending highly compressed uid-set ranges. The response parser uses Range#to_a without size validation, allowing attackers to force expansion of massive integer ranges into memory.

## Attack scenario
1. Attacker sets up or compromises an IMAP server or performs MITM on the connection
2. Attacker crafts a malicious IMAP response containing uid-set data with extremely large ranges (e.g., '1:2147483647')
3. Victim application using vulnerable net-imap connects to the server and sends IMAP commands
4. Server sends the malicious response with compressed uid-set ranges
5. Client's receiver thread automatically reads and processes the response
6. Response parser invokes Range#to_a on the uid-set, attempting to expand the entire range into an array, exhausting available memory and crashing the process

## Root cause
The response parser implementation fails to validate or limit the size of uid-set ranges before converting them to arrays using Range#to_a. No bounds checking exists on the expanded size of ranges, allowing unbounded memory allocation when processing server-controlled input.

## Attacker mindset
A malicious IMAP server operator or network attacker seeks to disrupt client applications by forcing resource exhaustion. This is a low-effort attack requiring only manipulation of protocol response data without authentication bypass or code execution.

## Defensive takeaways
- Implement strict size validation on all parsed ranges before expansion operations
- Use lazy evaluation or streaming processing instead of converting entire ranges to arrays
- Set configurable memory limits and maximum range sizes for protocol parsing
- Validate that range bounds are within reasonable protocol-defined limits
- Implement resource usage monitoring and circuit breakers for receiver threads
- Regularly audit protocol parsers for unbounded expansion operations on untrusted input

## Variant hunting
Search for similar Range#to_a or equivalent range expansion operations in other Ruby protocol libraries (POP3, SMTP, NNTP). Check for similar patterns in mail gem and other message parsing libraries. Examine any protocol implementations that convert protocol-specified ranges or counts into in-memory collections without validation.

## MITRE ATT&CK
- T1499.4
- T1190

## Notes
This vulnerability is particularly dangerous because it affects the automatic receiver thread—the malicious payload is processed asynchronously without explicit application invocation. The attack requires no authentication and can target any application using net-imap. The fix involves implementing bounds checking before Range#to_a expansion.

## Full report
<details><summary>Expand</summary>

Net::IMAP implements Internet Message Access Protocol (IMAP) client functionality in Ruby. Starting in version 0.3.2 and prior to versions 0.3.8, 0.4.19, and 0.5.6, there is a possibility for denial of service by memory exhaustion in `net-imap`'s response parser. At any time while the client is connected, a malicious server can send can send highly compressed `uid-set` data which is automatically read by the client's receiver thread. The response parser uses `Range#to_a` to convert the `uid-set` data into arrays of integers, with no limitation on the expanded size of the ranges. Versions 0.3.8, 0.4.19, 0.5.6, and higher fix this issue.

## Impact

This vulnerability causes Denial of Service by memory exhaustion for the projects using net-imap for connecting to an imap server.

</details>

---
*Analysed by Claude on 2026-05-24*
