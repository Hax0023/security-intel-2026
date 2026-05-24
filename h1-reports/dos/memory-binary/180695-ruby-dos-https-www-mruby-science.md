# Ruby DoS via Large String Input

## Metadata
- **Source:** HackerOne
- **Report:** 180695 | https://hackerone.com/reports/180695
- **Submitted:** 2016-11-07
- **Reporter:** bugdelivery
- **Program:** Ruby/mruby
- **Bounty:** Not specified in report
- **Severity:** medium
- **Vuln:** Denial of Service, Resource Exhaustion, Buffer Overflow
- **CVEs:** None
- **Category:** memory-binary

## Summary
A researcher discovered that sending a large string input (49,000+ 'A' characters) to the mruby.science service causes a denial of service, preventing new code execution. The vulnerability likely stems from inadequate input validation or memory management in string processing, allowing resource exhaustion.

## Attack scenario
1. Attacker identifies the mruby.science web service accepts user input for code execution
2. Attacker crafts a malicious request containing 49,000 repetitive characters ('A')
3. Request is sent to the vulnerable service
4. String processing in Ruby/mruby consumes excessive memory or CPU resources
5. Service becomes unresponsive and crashes or hangs
6. Legitimate users cannot execute new code, causing denial of service

## Root cause
Insufficient input size validation and inefficient string handling in mruby's parser or evaluator, allowing excessively large inputs to exhaust system resources without proper bounds checking.

## Attacker mindset
Simple reconnaissance to identify resource limits and service stability; testing for basic DoS vectors without sophisticated fuzzing; opportunistic discovery of crash conditions.

## Defensive takeaways
- Implement strict input size limits on user-supplied code or strings
- Add resource quotas (memory, CPU time) for code execution contexts
- Implement request size throttling at the application and infrastructure level
- Use rate limiting to prevent rapid repeated requests
- Monitor resource usage and set alerts for anomalies
- Sanitize and validate all external input before processing
- Implement timeout mechanisms for string parsing operations

## Variant hunting
Test other string operations (concatenation, regex, encoding), deeply nested data structures, extremely long method names, repetitive pattern payloads, Unicode/UTF-8 edge cases, and alternative character sets beyond ASCII 'A'

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1499 - Endpoint Denial of Service

## Notes
Report is minimal with limited technical detail. The researcher notes the service is currently unavailable, suggesting the crash may have been confirmed but the report lacks specifics on payload encoding, response behavior, memory/CPU metrics, and crash logs. HackerOne report #180695 indicates this was early in responsible disclosure timeline.

## Full report
<details><summary>Expand</summary>

Hi,
When I sent 49000x "A" I was probably able to crash service running on https://www.mruby.science since new code can't be executed for now. Could you please verify what happened? Thanks.

</details>

---
*Analysed by Claude on 2026-05-24*
