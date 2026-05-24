# HTTP Request Smuggling via Space Before Colon in Header Name

## Metadata
- **Source:** HackerOne
- **Report:** 1238709 | https://hackerone.com/reports/1238709
- **Submitted:** 2021-06-20
- **Reporter:** mkg
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, HTTP Parser Differential Handling, RFC 7230 Non-Compliance
- **CVEs:** CVE-2021-22959
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js 16.3.0 accepts HTTP headers with a space between the header name and colon (e.g., 'Content-Length : 5'), violating RFC 7230. When placed behind a proxy that rejects or handles such malformed headers differently, this enables HTTP Request Smuggling attacks where the proxy and Node.js interpret the request boundary differently.

## Attack scenario
1. Attacker crafts HTTP request with space before colon in Content-Length header (e.g., 'Content-Length : 23')
2. Request is sent to proxy server that correctly rejects or ignores the malformed header
3. Proxy forwards request to backend Node.js server which accepts the malformed header
4. Proxy and Node.js disagree on request boundaries: proxy sees two separate requests, Node.js interprets request body differently
5. Attacker injects a smuggled request in the body that Node.js processes as a new request
6. Smuggled request bypasses proxy security controls, leading to cache poisoning, credential theft, or unauthorized actions

## Root cause
The llhttp HTTP parser does not strictly enforce RFC 7230 Section 3.2.4 which explicitly requires rejecting requests with whitespace between header field-name and colon. The parser accepts this malformed input instead of rejecting with 400 Bad Request.

## Attacker mindset
An attacker exploits differential HTTP parsing between proxy and backend server. By crafting requests with subtle RFC violations that some parsers accept while others reject, the attacker causes a desynchronization in request boundary interpretation, allowing them to smuggle malicious requests past security controls.

## Defensive takeaways
- Strictly enforce RFC 7230 Section 3.2.4: reject any HTTP request with whitespace between header field-name and colon with 400 Bad Request
- Implement HTTP parser validation tests that verify RFC compliance for edge cases and malformed headers
- Use consistent HTTP parsers across proxy and backend infrastructure to prevent differential parsing
- Deploy request smuggling detection mechanisms that identify requests with RFC violations
- Keep HTTP libraries and parsers updated to latest versions with security patches
- Conduct security testing specifically for HTTP parser edge cases and RFC compliance

## Variant hunting
Test other whitespace characters (tabs, multiple spaces) before/after header colons
Test whitespace in other header positions (after colon, in header value)
Test malformed Content-Length values with spaces
Test Transfer-Encoding header variants with whitespace
Test HTTP/2 frame parsing for similar issues
Test other HTTP parsers (nginx, Apache, IIS) for inconsistent whitespace handling
Test header folding (line continuations) combined with whitespace issues

## MITRE ATT&CK
- T1190
- T1199
- T1598

## Notes
RFC 7230 explicitly addresses this issue, noting that 'differences in the handling of such whitespace have led to security vulnerabilities in request routing and response handling.' This is a known attack vector that llhttp failed to properly mitigate. The vulnerability requires a proxy/backend mismatch to be exploitable, making it dependent on specific infrastructure configurations. The PoC demonstrates Node.js accepting the malformed header, proving non-compliance with standards.

## Full report
<details><summary>Expand</summary>

**Summary:**
The ``llhttp`` parser in the ``http``module in Node 16.3.0 accepts requests with a space (SP) right after the header name before the colon. This can lead to HTTP Request Smuggling (HRS).

**Description:**
When Node receives the following request:

```
GET / HTTP/1.1
Host: localhost:5000
Content-Length : 5

hello
```

It interprets the request as having the body `hello`. Here is the relevant section of the code: https://github.com/nodejs/llhttp/blob/master/src/llhttp/http.ts#L410-L415

How could this lead to HRS? Imagine that Node is placed behind a proxy which ignores the CL header with a space before the colon, but forwards it as is. Then the following attack can be performed:

```
GET / HTTP/1.1
Host: localhost:5000
Content-Length : 23

GET / HTTP/1.1
Dummy: GET /smuggled HTTP/1.1
Host: localhost:5000

```

The proxy would see the first and the second GET-request. But Node would see the first and the third GET-request.

## Steps To Reproduce:

We don't know of any proxy that behaves this way, but here is how to show that Node is behaving in the described way. Run the following code like this: `node app.js`

```js
const http = require('http');

// https://nodejs.org/en/docs/guides/anatomy-of-an-http-transaction/

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

    response.end("Body length: " + body.length.toString() + " Body: " + body);
  });
}).listen(5000);
```

Then send a request with a space between the CL header and the colon. This can be done with the following one-liner:

```sh
echo -en "GET / HTTP/1.1\r\nHost: localhost:5000\r\nContent-Length : 5\r\n\r\nhello" | nc localhost 5000
```

See that Node interpreted the body as `hello`.

# Supporting Material/References:

Relevant section of RFC 7230 (second paragraph of https://datatracker.ietf.org/doc/html/rfc7230#section-3.2.4):

```
   No whitespace is allowed between the header field-name and colon.  In
   the past, differences in the handling of such whitespace have led to
   security vulnerabilities in request routing and response handling.  A
   server MUST reject any received request message that contains
   whitespace between a header field-name and colon with a response code
   of 400 (Bad Request).  A proxy MUST remove any such whitespace from a
   response message before forwarding the message downstream.
```

## Impact

Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

</details>

---
*Analysed by Claude on 2026-05-24*
