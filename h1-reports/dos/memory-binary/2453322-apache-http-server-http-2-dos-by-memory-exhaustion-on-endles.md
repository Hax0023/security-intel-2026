# Apache HTTP Server: HTTP/2 DoS by Memory Exhaustion on Endless Continuation Frames

## Metadata
- **Source:** HackerOne
- **Report:** 2453322 | https://hackerone.com/reports/2453322
- **Submitted:** 2024-04-08
- **Reporter:** bart
- **Program:** Apache HTTP Server
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Denial of Service, Memory Exhaustion, Resource Exhaustion
- **CVEs:** CVE-2024-27316
- **Category:** memory-binary

## Summary
Apache httpd improperly handles HTTP/2 continuation frames that exceed header size limits. When a client continuously sends header frames without stopping, the server buffers them in nghttp2 to generate an HTTP 413 response, leading to unbounded memory consumption and denial of service. An attacker can exhaust server memory by sending endless HTTP/2 continuation frames.

## Attack scenario
1. Attacker establishes HTTP/2 connection to vulnerable Apache httpd server
2. Attacker sends initial HTTP/2 HEADERS frame with size near or exceeding the configured limit
3. Server begins buffering the oversized headers in nghttp2 library to prepare HTTP 413 response
4. Attacker continuously sends CONTINUATION frames extending the header block without completion
5. Server continues buffering each continuation frame, accumulating memory consumption
6. Memory exhaustion occurs, causing server crash or severe performance degradation

## Root cause
The nghttp2 library buffers HTTP/2 headers that exceed size limits to generate informative error responses. However, there is no mechanism to limit total buffered data or enforce a maximum number of continuation frames, allowing an attacker to trigger unbounded memory allocation by continuously sending frames.

## Attacker mindset
An attacker seeks to disable a web service through resource exhaustion. HTTP/2 continuation frames provide an efficient vector as multiple small frames accumulate in memory buffers, and the error handling logic itself becomes the attack surface. The attacker exploits the server's intention to provide detailed error responses.

## Defensive takeaways
- Implement strict limits on total buffered header data across all continuation frames
- Add maximum frame count or timeout constraints for incomplete header blocks
- Consider dropping connections that exceed header size limits rather than detailed error responses
- Monitor memory usage patterns and implement circuit breakers for abnormal allocation
- Update nghttp2 and Apache httpd to patched versions
- Configure resource limits per connection to prevent single client exhaustion
- Implement rate limiting on header frame reception

## Variant hunting
Check for similar unbounded buffering in other HTTP/2 frame types (SETTINGS, PUSH_PROMISE)
Investigate if HTTP/1.1 request header limits have similar implementation flaws
Review other protocol parsers using nghttp2 for identical vulnerability patterns
Test trailer headers handling in HTTP/2 for continuation frame DoS
Examine gRPC implementations over HTTP/2 for header handling weaknesses

## MITRE ATT&CK
- T1190
- T1499
- T1499.4

## Notes
CVE-2024-27316 affects HTTP/2 implementations in Apache httpd. The vulnerability demonstrates how error handling mechanisms designed for user experience can become attack vectors. Similar issues likely exist in other HTTP/2 parsers. The fix likely involves implementing bounded buffering or early termination on header size violations rather than attempting to generate detailed error responses.

## Full report
<details><summary>Expand</summary>

I'd like to report Apache httpd vulnerability (CVE-2024-27316) that was recently fixed.
* Advisory: https://httpd.apache.org/security/vulnerabilities_24.html

## Impact

HTTP/2 incoming headers exceeding the limit are temporarily buffered in nghttp2 in order to generate an informative HTTP 413 response. If a client does not stop sending headers, this leads to memory exhaustion.

</details>

---
*Analysed by Claude on 2026-05-24*
