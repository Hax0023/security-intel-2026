# HTTP Request Smuggling due to CR-to-Hyphen conversion in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 922597 | https://hackerone.com/reports/922597
- **Submitted:** 2020-07-13
- **Reporter:** amitklein
- **Program:** Node.js
- **Bounty:** Unknown
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Header Parsing Inconsistency, CL.TE (Content-Length Transfer-Encoding) Desynchronization
- **CVEs:** CVE-2020-8201
- **Category:** uncategorised

## Summary
Node.js converts carriage return (CR) characters in HTTP request headers to hyphens before parsing, allowing HTTP request smuggling when a proxy server in front of Node.js interprets the malformed header differently. An attacker can craft requests with Content[CR]Length headers that proxies reject but Node.js accepts as Content-Length, causing request boundaries to desynchronize between the proxy and backend server.

## Attack scenario
1. Attacker crafts an HTTP request with a Content[CR]Length header (carriage return in place of normal characters) specifying a body length of 42 bytes
2. The request includes a first legitimate-looking GET request followed by 42 bytes of payload containing a second malicious GET request
3. Proxy server encounters the malformed Content[CR]Length header, rejects it as invalid, and assumes 0-length body with no body expected
4. Proxy forwards only the first GET request to Node.js backend, then waits for response
5. Node.js converts CR to hyphen, creating valid Content-Length header, and reads the expected 42 bytes as the body
6. Node.js then parses the second GET request from the buffered payload, processing the attacker's malicious request while proxy believes it's a separate request

## Root cause
Non-standard HTTP header parsing in Node.js that converts CR characters to hyphens, creating valid headers from malformed input. This differs from proxy behavior which rejects malformed headers entirely, causing interpretation divergence in request boundaries and body length calculations.

## Attacker mindset
Attacker exploits the difference in HTTP specification interpretation between proxy and backend server to inject hidden requests. By using the CR character (which most HTTP parsers reject), the attacker ensures their smuggled request is invisible to the proxy but processed by Node.js, enabling cache poisoning, session hijacking, or other downstream attacks.

## Defensive takeaways
- Implement strict HTTP header validation that rejects headers with invalid characters (CR, LF outside CRLF sequences) rather than silently converting them
- Ensure consistent HTTP specification compliance with strict RFC 7230 adherence across all server components
- Use explicit request termination and avoid relying on implicit body length assumptions
- Implement request smuggling detection mechanisms (CL.TE desynchronization detection)
- Add monitoring for suspicious header patterns including CR/LF characters in unexpected positions
- Consider using HTTP/2 which eliminates ambiguities in request framing
- Ensure proxy and backend servers use identical HTTP parsing logic or validate requests at gateway level

## Variant hunting
Search for other non-printing character conversions in HTTP header parsing (LF, NULL, TAB handling). Test other header fields that affect request boundaries: Transfer-Encoding, Content-Transfer-Encoding. Investigate similar character substitution behaviors in other languages/frameworks (Ruby, Python, Java). Look for instances where headers are normalized or sanitized differently than RFC specification requires.

## MITRE ATT&CK
- T1190
- T1598
- T1557

## Notes
Report lacks specific version information and patch details. The vulnerability demonstrates a fundamental principle: when multiple parsers interpret the same input, subtle differences in character handling can create security flaws. Node.js' lenient header parsing (converting invalid characters rather than rejecting) created a desynchronization opportunity. This type of vulnerability is particularly dangerous in microservices architectures with multiple proxies/gateways.

## Full report
<details><summary>Expand</summary>

> NOTE! Thanks for submitting a report! Please replace *all* the [square] sections below with the pertinent details. Remember, the more detail you provide, the easier it is for us to triage and respond quickly, so be sure to take your time filling out the report!

**Summary:** [add summary of the vulnerability]
Apparently, node.js converts CR in HTTP request headers to hyphen before parsing. This can lead to HTTP Request Smuggling as it is a non-standard interpretation of the header.

**Description:** [add more details about this vulnerability]
Consider an HTTP request with Content[CR]Length header . Suppose a proxy in front of node.js ignores the Content[CR]Length header (and therefore assumes a 0-length body). node, on the other hand, converts the CR to a hyphen and uses the value of the (newly formed...) Content-Length header. HTTP Request Smuggling ensues.

## Steps To Reproduce:
This is the HTTP stream that demonstrates the vulnerability:
GET / HTTP/1.1
Host: www.example.com
Content[CR]Length: 42
Connection: Keep-Alive

GET /proxy_sees_this HTTP/1.1
Something: GET /node_sees_this HTTP/1.1
Host: www.example.com

A proxy server that ignores the invalid Content[CR]Length header will assume that the body length is 0 (since there's no body length indication), and will thus transmit the stream up to (but not including) the GET /proxy_sees_this. It will wait for node to respond (which interestingly does happen, even though node.js does expect the body - perhaps on GET requests, the URL is invoked regardless of the body?), then the proxy forwards the second request (from its perspective) - the GET /proxy_sees_this. Node then silently discards the expected 42 bytes of the body of the first request, and thus starts parsing the 2nd request from GET /node_sees_this.
HTTP Request Smuggling ensues.

[Also, if you were able to find the piece of code responsible for this issue, please add a link to it in the source repository.]

## Impact: [add why this issue matters]
HTTP Request Smuggling can lead to web cache poisoning, session hijacking, cross site scripting, etc.

## Supporting Material/References:

  * List any additional material (e.g. screenshots, logs, references, commits, code examples, etc.).

## Impact

HTTP Request Smuggling can lead to web cache poisoning, session hijacking, cross site scripting, etc.

</details>

---
*Analysed by Claude on 2026-05-24*
