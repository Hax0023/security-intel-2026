# HTTP Multi-Header Compression Denial of Service

## Metadata
- **Source:** HackerOne
- **Report:** 1886139 | https://hackerone.com/reports/1886139
- **Submitted:** 2023-02-24
- **Reporter:** monnerat
- **Program:** HTTP Client/Server (likely a specific HTTP library or implementation)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Denial of Service, Resource Exhaustion, Improper Input Validation
- **CVEs:** CVE-2023-23916
- **Category:** memory-binary

## Summary
An HTTP server can send responses with multiple Transfer-Encoding and/or Content-Encoding headers, each causing buffer allocation. While individual header values are limited, the number of header occurrences is unbounded, allowing attackers to exhaust all available memory on the client. This results in a complete denial of service through resource exhaustion.

## Attack scenario
1. Attacker crafts HTTP response with dozens/hundreds of Content-Encoding headers (e.g., repeated 'gzip' headers)
2. Attacker also includes multiple Transfer-Encoding headers in the same response
3. Client receives response and processes each header independently without deduplication
4. For each header occurrence, vulnerable implementation allocates a new buffer/decoder structure
5. Memory allocation continues until system exhausts available RAM
6. Client process crashes or system becomes unresponsive, causing denial of service

## Root cause
The HTTP parser/client implementation lacks proper validation and deduplication of compression headers. The code likely iterates through all header occurrences and allocates resources for each without checking for duplicates or enforcing a maximum header count limit. The vulnerability exists because while individual encoding values are constrained, there is no mechanism to limit the total number of encoding header fields.

## Attacker mindset
An attacker would recognize that HTTP specifications allow multiple headers with the same name, and if the implementation naively processes each occurrence, they can trigger unbounded resource allocation. The attacker aims to craft a minimal payload (single HTTP response) that causes maximum client-side damage without needing multiple requests.

## Defensive takeaways
- Implement maximum limits on the number of Transfer-Encoding and Content-Encoding header occurrences (recommend 1 per type)
- Deduplicate compression headers or reject responses with duplicate encoding headers
- Validate that only one Transfer-Encoding and one Content-Encoding header exist per HTTP response
- Implement memory limits and resource quotas for decompression operations
- Add timeouts for decompression/decoding operations to prevent infinite loops
- Follow HTTP specifications strictly: RFC 7230/7231 recommend single occurrences of these headers
- Monitor and log responses with unusual header patterns for security analysis

## Variant hunting
Test with other repeatable headers that trigger resource allocation (Accept-Encoding variations)
Check if multiple Content-Length headers can cause confusion and resource issues
Investigate whether custom headers with similar processing patterns are vulnerable
Test HTTP/2 implementations for similar multi-header exhaustion (pseudo-headers, HPACK compression)
Examine WebSocket upgrade headers for analogous resource exhaustion vectors
Check if HTTP trailers can be abused similarly for compression-related DoS
Test proxy implementations for similar header accumulation vulnerabilities

## MITRE ATT&CK
- T1190
- T1499
- T1499.1

## Notes
This is a client-side DoS vulnerability rather than server-side. The vulnerability affects any HTTP client library that doesn't properly validate or limit encoding headers. Similar patterns should be checked in other header types that trigger resource allocation. The fix is straightforward but requires careful implementation to avoid breaking legitimate edge cases.

## Full report
<details><summary>Expand</summary>

A server can send an HTTP response with many occurrences of Transfer-Encoding and/or Content-Encoding headers. Each listed encoding allocates a buffer. The number of encodings listed within each header is already limited but the number of headers is not, allowing an HTTP response to consume all available memory.

## Impact

Consumes all available memory, resulting in a DoS.

</details>

---
*Analysed by Claude on 2026-05-24*
