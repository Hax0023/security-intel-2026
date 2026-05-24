# HTTP Request Smuggling Due to Flawed Transfer-Encoding Header Parsing in Node.js llhttp

## Metadata
- **Source:** HackerOne
- **Report:** 1524555 | https://hackerone.com/reports/1524555
- **Submitted:** 2022-03-28
- **Reporter:** zeyu2001
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Input Validation Flaw, Parser Logic Error
- **CVEs:** CVE-2022-32213
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js v17.8.0 incorrectly validates Transfer-Encoding headers, accepting malformed values like 'chunkedchunked' while processing only the last occurrence of 'chunked'. This allows HTTP Request Smuggling attacks where malicious requests are misinterpreted, potentially bypassing security layers and enabling cache poisoning.

## Attack scenario
1. Attacker crafts an HTTP request with a malformed Transfer-Encoding header (e.g., 'chunkedchunked')
2. The flawed llhttp parser accepts the malformed header and processes the request body as chunked encoding based on the last 'chunked' match
3. The attacker's payload is split across multiple requests where the second request is interpreted as part of the first request's body
4. If a frontend proxy/cache uses different parsing logic, it may interpret request boundaries differently than the backend server
5. The attacker's second request reaches an intended target (cached or processed by backend), while the frontend/proxy sees different content
6. Consequences include cache poisoning, credential theft, session hijacking, or bypassing of WAF/security filters

## Root cause
The Transfer-Encoding header parser in llhttp matches 'chunked' and then expects CRLF. If CRLF is missing, the parser attempts to match 'chunked' again instead of rejecting the invalid header. This allows malformed values like 'chunkedchunked' to be treated as valid, with only the last match being processed.

## Attacker mindset
An attacker would exploit inconsistencies between how different HTTP parsers interpret malformed headers. By using non-canonical but technically parseable Transfer-Encoding values, they can desynchronize request interpretation between frontend proxies and backend servers, enabling request smuggling attacks.

## Defensive takeaways
- Implement strict RFC 7230 compliance for Transfer-Encoding header validation - reject headers that don't match expected format exactly
- Ensure HTTP parsers reject malformed headers rather than attempting to recover via fallback matching logic
- Use the same HTTP parsing library across frontend proxies and backend servers to prevent desynchronization
- Add validation that Transfer-Encoding values must be a single 'chunked' token optionally preceded by other valid transfer codings, not repeated tokens
- Implement request/response logging to detect suspicious Transfer-Encoding patterns
- Test HTTP parsing with fuzzing and malformed header injection to catch parser inconsistencies

## Variant hunting
Search for similar parser flaws in other HTTP libraries (nginx, Apache, IIS, etc.) where transfer encoding validation may accept malformed values. Test for other double-value patterns in headers like 'Content-Length: 1313', 'Expect: 100-continue100-continue', or combinations of conflicting headers.

## MITRE ATT&CK
- T1190
- T1021
- T1071

## Notes
This vulnerability is part of a broader class of HTTP Desynchronization attacks (HRS/HTTP smuggling). The root cause stems from lenient parsing that attempts recovery rather than strict validation. The bug was discovered after a prior related issue (#1501679), suggesting the parser had multiple weaknesses in Transfer-Encoding handling. Node.js v17.8.0+ should be patched; users should upgrade to patched versions and audit HTTP parsing configurations.

## Full report
<details><summary>Expand</summary>

**Summary:** 

The `llhttp` parser in the `http` module in Node v17.8.0 does not correctly parse and validate `Transfer-Encoding` headers. This can lead to HTTP Request Smuggling (HRS).

**Description:** 

After #1501679, I did a bit more digging into the issue, and found that there were more flaws in the parsing of `Transfer-Encoding` headers. Relevant code [here](https://github.com/nodejs/llhttp/blob/master/src/llhttp/http.ts#L483).

After matching `"chunked"`, the parser attempts to match the CRLF sequence, failing which it matches `chunked` again. As a result, the following forms a valid request for the parser, despite the `Transfer-Encoding` value, `chunkedchunked`, being invalid.

```http
GET / HTTP/1.1
Host: localhost
Transfer-Encoding: chunkedchunked

1
a
0

```

Node will process the `Transfer-Encoding` value as `chunked`, only seeing the last-match of the string `"chunked"`.

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
         "Headers": request.headers,
         "Length": body.length,
         "Body": body,
      }) + "\n");
   });
}).listen(80);
```

Request:

```http
GET / HTTP/1.1
Host: localhost
Transfer-Encoding: chunkedchunked

1
a
0


```

Response:

```http
HTTP/1.1 200 OK
Date: Mon, 28 Mar 2022 15:02:31 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 92

{"Headers":{"host":"localhost","transfer-encoding":"chunkedchunked"},"Length":1,"Body":"a"}
```

## Supporting Material/References:

Payloads and outputs:
{F1671151}

## Impact

Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

</details>

---
*Analysed by Claude on 2026-05-24*
