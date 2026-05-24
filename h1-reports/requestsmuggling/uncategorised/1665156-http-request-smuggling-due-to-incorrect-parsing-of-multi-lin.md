# HTTP Request Smuggling Due to Incorrect Parsing of Multi-line Transfer-Encoding (Improper Fix for CVE-2022-32215)

## Metadata
- **Source:** HackerOne
- **Report:** 1665156 | https://hackerone.com/reports/1665156
- **Submitted:** 2022-08-10
- **Reporter:** shacharm
- **Program:** Node.js
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Improper Input Validation, Parser Vulnerability, Incomplete Security Fix
- **CVEs:** CVE-2022-32215
- **Category:** uncategorised

## Summary
An incomplete fix for CVE-2022-32215 in Node.js versions 16.16.0 and 18.7.0 allows attackers to craft multi-line Transfer-Encoding headers that bypass validation, enabling HTTP Request Smuggling attacks. The llhttp parser incorrectly accepts malformed Transfer-Encoding headers like 'chunked , chunked-false', allowing attackers to inject arbitrary requests that are parsed as separate legitimate requests by the server.

## Attack scenario
1. Attacker crafts an HTTP request with a multi-line Transfer-Encoding header containing 'chunked' followed by a newline and ', chunked-false'
2. Attacker sends initial POST request body that the server parses as a single chunked request
3. Attacker includes a hidden second request (e.g., GET /flag) in the first request's payload that is not consumed by the initial request parsing
4. Server incorrectly treats the second request as a new legitimate request on the keep-alive connection
5. Attacker's injected GET request executes on the server, bypassing access controls and security layers
6. Attacker leverages this to perform cache poisoning, credential theft, or access restricted resources

## Root cause
The llhttp parser in Node.js http module does not properly validate multi-line Transfer-Encoding headers. The parser accepts headers split across multiple lines with leading spaces/commas, failing to reject malformed encodings. The original CVE-2022-32215 fix was incomplete and did not address all variations of the parsing bypass.

## Attacker mindset
An attacker recognizes that HTTP header parsing logic often has edge cases when handling folded headers (headers continued on next lines with leading whitespace). By injecting a newline and additional tokens after a valid Transfer-Encoding value, the attacker can trick the parser into accepting invalid syntax. This allows request smuggling where one logical request is parsed as two separate requests by the server, enabling downstream exploitation.

## Defensive takeaways
- Implement strict validation of Transfer-Encoding headers that rejects any multi-line or continuation sequences
- Properly handle and reject header folding in Transfer-Encoding specifically (RFC 7230 recommends deprecating obs-fold)
- Test security fixes against multiple variations and edge cases, not just the reported payload
- Consider rejecting requests with ambiguous or non-canonical header formatting
- Use a well-maintained HTTP parser library and keep it updated with the latest security patches
- Implement request smuggling detection at the application level (monitoring for unexpected request sequences)
- When fixing parser vulnerabilities, ensure comprehensive test coverage of related attack vectors

## Variant hunting
Search for similar incomplete fixes in other HTTP parsers (Python, Go, Java). Look for other Transfer-Encoding bypass techniques using different whitespace, null bytes, or encoding tricks. Test Content-Length header parsing for similar multi-line injection issues. Investigate whether other HTTP headers that accept multiple values (Accept, Accept-Encoding) have similar vulnerabilities. Check if the fix properly handles all RFC 7230 obs-fold variations.

## MITRE ATT&CK
- T1190
- T1090

## Notes
This is a regression vulnerability - the same basic vulnerability was reported in CVE-2022-32215 but the fix was incomplete. The payload exploits header line folding where continuation lines starting with whitespace are processed as part of the previous header. The vulnerability allows HTTP Request Smuggling which is a critical class of attacks affecting reverse proxies, load balancers, and cache systems. The report demonstrates actual exploitation showing two separate HTTP responses for what should be a single malformed request rejection.

## Full report
<details><summary>Expand</summary>

**Summary:**
Due to an incomplete fix for CVE-2022-32215, the `llhttp` parser in the `http` module in Node v16.16.0 and 18.7.0  still does not correctly handle multi-line Transfer-Encoding headers. This can lead to HTTP Request Smuggling (HRS).

**Description:** [add more details about this vulnerability]

We have identified that the root issue of CVE-2022-32215 (that was [reported here](https://hackerone.com/reports/1501679)) was seemingly not fixed at all. Running the same exploit produces the same unwanted result. For the sake of brevity, I won't repeat the description, it can be seen in the [original issue](https://hackerone.com/reports/1501679). 

## Steps To Reproduce:

The reproduction steps are the same from the original issue

#### Testing Server

Run the following server (`node server.js`):
```js
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

#### Payload

```
printf "POST / HTTP/1.1\r\n"\
"Host: 127.0.0.1\r\n"\
"Transfer-Encoding: chunked\r\n"\
" , chunked-false\r\n"\
"\r\n"\
"1\r\n"\
"A\r\n"\
"0\r\n"\
"\r\n"\
"GET /flag HTTP/1.1\r\n"\
"Host: 127.0.0.1\r\n"\
"foo: x\r\n"\
"\r\n"\
"\r\n" | nc localhost 80
```

#### Output

```
HTTP/1.1 200 OK
Date: Sun, 06 Mar 2022 03:34:05 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 101

{"Headers":{"transfer-encoding":"chunked , chunked-false"},"Length":1,"Body":"A"}
HTTP/1.1 200 OK
Date: Sun, 06 Mar 2022 03:34:05 GMT
Connection: keep-alive
Keep-Alive: timeout=5
Content-Length: 64

{"Headers":{"host":"127.0.0.1", "foo":"x"},"Length":0,"Body":""}
```

As you can see, the payload was parsed as two requests (POST to / , and GET to /flag) which is erroneous behavior (the first request was parsed as a chunked request, which is wrong)

The expected output should be -
```
HTTP/1.1 400 Bad Request
Connection: close
```

## Supporting Material/References:

Exploitation of the issue on Node 16.16.0 -
{F1861233}

## Credit

The vulnerability was discovered by Liav Gutman of the JFrog CSO Team

## Impact

Depending on the specific web application, HRS can lead to cache poisoning, bypassing of security layers, stealing of credentials and so on.

</details>

---
*Analysed by Claude on 2026-05-24*
