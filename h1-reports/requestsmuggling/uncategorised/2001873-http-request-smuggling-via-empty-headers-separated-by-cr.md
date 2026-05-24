# HTTP Request Smuggling via Empty headers separated by CR in Node.js llhttp

## Metadata
- **Source:** HackerOne
- **Report:** 2001873 | https://hackerone.com/reports/2001873
- **Submitted:** 2023-05-25
- **Reporter:** yadhukrishnam
- **Program:** Node.js/HackerOne
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Protocol Parsing Vulnerability, CL.TE (Content-Length/Transfer-Encoding) Desynchronization
- **CVEs:** CVE-2023-30589
- **Category:** uncategorised

## Summary
The llhttp HTTP parser in Node v20.2.0 accepts a carriage return (CR) without line feed (LF) as a valid header delimiter, violating RFC 7230 which mandates CRLF sequences. This deviation allows attackers to inject smuggled HTTP requests that are parsed differently by frontend proxies and backend servers, leading to request desynchronization and potential access control bypass.

## Attack scenario
1. Attacker identifies a Node.js backend using llhttp parser behind a frontend proxy with stricter HTTP parsing
2. Attacker crafts a request with a header value containing CR followed by a new header injection (e.g., 'X-Abc: [CR]xTransfer-Encoding: chunked')
3. Frontend proxy validates and forwards the entire header as a single value since it expects CRLF, not CR alone
4. Backend llhttp parser treats the CR as a header terminator, splits the payload into two headers, and recognizes 'Transfer-Encoding: chunked'
5. Request parsing desynchronization causes the backend to process subsequent requests incorrectly or smuggle content through the connection
6. Attacker gains ability to bypass authentication, poison caches, or execute unintended backend operations

## Root cause
The llhttp library's header field parsing logic accepts a single CR character as a valid header delimiter instead of strictly enforcing RFC 7230's requirement for CRLF (CR+LF) sequences. This lenient parsing creates divergence with stricter parsers in frontend proxies.

## Attacker mindset
An attacker would exploit this discrepancy between lenient backend parsing and strict frontend validation to cause request desynchronization. By injecting headers using CR-only delimiters, they can hide smuggled requests from frontend proxies while ensuring backend systems parse them as separate headers, enabling authentication bypass and lateral request manipulation.

## Defensive takeaways
- Enforce strict RFC 7230 compliance in HTTP parsers - only CRLF should terminate header fields, not CR or LF alone
- Implement consistent HTTP parsing across frontend proxies and backend servers to prevent desynchronization attacks
- Add comprehensive test coverage for malformed headers including CR-only delimiters, mixed CRLF/CR variations, and edge cases
- Use HTTP request smuggling detection mechanisms that check for parser discrepancies between layers
- Consider using stricter parsers by default and rejecting ambiguous HTTP formatting
- Monitor for suspicious header patterns and connection states that may indicate smuggling attempts
- Update to patched versions of llhttp and Node.js that strictly validate header delimiters

## Variant hunting
Test LF-only delimiters (without CR) for header termination
Probe mixed CRLF/CR combinations in different header positions
Inject null bytes or other control characters as potential delimiters
Test Content-Length header injection via CR delimiters to cause CL.TE attacks
Check if other HTTP implementations (nginx, Apache, Python http.server) accept CR-only delimiters
Examine other Node.js modules or older llhttp versions for similar parsing quirks
Test header folding techniques combined with CR delimiters (obsolete line wrapping)
Investigate if whitespace before CR affects parsing behavior

## MITRE ATT&CK
- T1190
- T1036

## Notes
This vulnerability is part of a class of HTTP request smuggling bugs that exploit parser divergence. The report references a similar issue (HackerOne #1888760), suggesting a pattern of insufficient validation in llhttp. The missing test case in the invalid.md test file indicates the vulnerability was not explicitly considered during development. The attack is particularly dangerous in microservices architectures and CDN setups where multiple HTTP parsers may be in the request path.

## Full report
<details><summary>Expand</summary>

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

HTTP Request Smuggling can lead to access control bypass.

</details>

---
*Analysed by Claude on 2026-05-24*
