# Denial of Service: nghttp2 use of uninitialized pointer in ALTSVC frame handling

## Metadata
- **Source:** HackerOne
- **Report:** 335608 | https://hackerone.com/reports/335608
- **Submitted:** 2018-04-10
- **Reporter:** jasnell
- **Program:** Node.js (nghttp2 dependency)
- **Bounty:** not specified
- **Severity:** high
- **Vuln:** use of uninitialized pointer, denial of service, memory safety
- **CVEs:** None
- **Category:** uncategorised

## Summary
A use-of-uninitialized-pointer vulnerability in nghttp2's ALTSVC frame handling allows remote attackers to crash Node.js processes by sending malformed ALTSVC and GOAWAY frames. The vulnerability affects both servers receiving malicious client frames and clients receiving frames from malicious servers, resulting in immediate process termination.

## Attack scenario
1. Attacker identifies Node.js service using nghttp2 for HTTP/2 handling
2. Attacker crafts malformed ALTSVC frame with uninitialized pointer conditions
3. Attacker sends crafted frame to target server (or server sends to client if attacker controls server)
4. nghttp2 processes frame without proper pointer initialization validation
5. Uninitialized pointer is dereferenced during frame processing
6. Process crashes, triggering denial of service

## Root cause
nghttp2 fails to properly initialize pointers before using them when processing ALTSVC frames, likely due to missing validation checks or incomplete initialization in the frame parsing logic. The vulnerability is triggered by specific malformed frame structures that bypass safety checks.

## Attacker mindset
An attacker seeks to achieve denial of service by exploiting memory safety issues in widely-used HTTP/2 libraries. By discovering a crash condition that requires minimal resources (just sending malformed frames), the attacker can reliably take down Node.js services without authentication or complex exploitation techniques.

## Defensive takeaways
- Always initialize all pointers and variables before use, enforce this through compiler warnings and code review
- Implement comprehensive fuzzing tests for all frame types in HTTP/2 parsers
- Use memory safety tools (AddressSanitizer, Valgrind) during development and CI/CD
- Validate all incoming frame structures against RFC specifications before processing
- Keep HTTP/2 library dependencies up-to-date and monitor security advisories
- Implement process monitoring and auto-restart mechanisms to mitigate DoS impact
- Apply input validation for all frame header fields and payload structures

## Variant hunting
Search for similar uninitialized pointer issues in other HTTP/2 frame types (HEADERS, SETTINGS, PUSH_PROMISE, etc.). Investigate whether other parsers in nghttp2 have similar initialization gaps. Test fuzzing of all frame type combinations with malformed payloads.

## MITRE ATT&CK
- T1499
- T1190

## Notes
This vulnerability was discovered during investigation of a related issue (335533). The nghttp2 author was already aware and working on a fix at time of report. The vulnerability demonstrates the importance of memory safety in network protocol parsers. Related to similar HTTP/2 vulnerabilities that have affected multiple implementations. Process-level DoS is particularly impactful in containerized and cloud environments where each process may handle critical workloads.

## Full report
<details><summary>Expand</summary>

While investigating https://hackerone.com/reports/335533 and while following the same reproduction steps, I uncovered a bug in nghttp2 that causes use of an uninitialized pointer for an altsvc frameresulting in crash. The error can be easily triggered by a remote attacker by sending malformed ALTSVC and GOAWAY frames to the server, or by a malicious server sending same to the client. For Node.js, the result is a crashed process. The report has been submitted to the nghttp2 author who is working on a fix and is working on a fixed release.

## Impact

Crashing the Node.js process causing a Denial of Service

</details>

---
*Analysed by Claude on 2026-05-24*
