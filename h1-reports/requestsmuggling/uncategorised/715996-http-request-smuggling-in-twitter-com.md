# HTTP Request Smuggling in twitter.com

## Metadata
- **Source:** HackerOne
- **Report:** 715996 | https://hackerone.com/reports/715996
- **Submitted:** 2019-10-16
- **Reporter:** protostar0
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length/Transfer-Encoding) Desynchronization, Request Queue Poisoning
- **CVEs:** None
- **Category:** uncategorised

## Summary
HTTP request smuggling vulnerability was discovered in Twitter.com subdomains, allowing attackers to desynchronize HTTP requests between frontend and backend servers by leveraging Transfer-Encoding: chunked headers. An attacker could inject malicious requests (such as tweet composition) that would be processed by the backend server as separate legitimate requests, potentially leading to unauthorized actions.

## Attack scenario
1. Attacker identifies a valid POST request from twitter.com and sends it to Burp Suite repeater
2. Attacker removes restrictive headers (Connection: close, Accept-Encoding: gzip/deflate) that would prevent smuggling
3. Attacker adds 'Transfer-Encoding: chunked' header to indicate chunked transfer encoding
4. Attacker adds a second malicious request payload (e.g., tweet composition request) after the first request body with improper chunked encoding
5. Attacker sends the combined request; frontend server processes first request while backend interprets the smuggled second request
6. Smuggled request executes on backend server in context of legitimate user session, performing unauthorized action (composing tweet)

## Root cause
Backend server accepts and processes Transfer-Encoding: chunked encoding while frontend server does not properly validate or synchronize chunked encoding boundaries. Discrepancy between how frontend and backend parse the HTTP request body allows request injection. Insufficient removal of Transfer-Encoding headers and lack of request validation enable the smuggle.

## Attacker mindset
Attacker seeks to bypass request filtering and perform unauthorized actions on behalf of authenticated users. By exploiting HTTP protocol ambiguities between frontend/backend servers, attacker can inject requests that appear legitimate to backend systems. This allows account takeover capabilities, tweet posting, or other account actions without direct user interaction.

## Defensive takeaways
- Strictly validate and normalize HTTP request headers; reject requests with conflicting Content-Length and Transfer-Encoding headers
- Implement HTTP/2 or ensure frontend and backend use identical HTTP parsing logic and request normalization
- Disable Transfer-Encoding: chunked if not required; explicitly remove or reject such headers
- Use a Web Application Firewall to detect and block HTTP request smuggling attempts
- Implement request queue isolation between frontend and backend; avoid connection reuse without full request/response cycle completion
- Monitor for unusual request patterns, delayed responses, or multiple requests in single connection
- Conduct regular HTTP desync testing across all proxy/load-balancer/server combinations

## Variant hunting
Search for HTTP request smuggling vulnerabilities in other subdomains or endpoints accepting POST/PUT requests. Test CL.TE (Content-Length vs Transfer-Encoding), TE.CL, and TE.TE variants. Look for proxy servers, load balancers, or WAF bypasses. Test with HTTP/1.1 keep-alive connections. Examine edge cases with multiple Transfer-Encoding values or obfuscation (e.g., 'chunked', 'CHUNKED', with spaces).

## MITRE ATT&CK
- T1190
- T1552
- T1071.001

## Notes
Report references duplicate finding in report #713285 suggesting widespread exposure across Twitter infrastructure. POC demonstrates practical exploitation through tweet creation endpoint. Vulnerability requires understanding of HTTP protocol internals and proper tool usage (Burp Suite). PortSwigger references provide comprehensive technical background on request smuggling mechanics and exploitation scenarios.

## Full report
<details><summary>Expand</summary>

**Summary:**
the same vulnerability reported in other domain , see this report [here](https://hackerone.com/reports/713285) 
**Description:** 
the Description of HTTP request smuggling attacks : [here](https://portswigger.net/web-security/request-smuggling)

##Detect HTTP request smuggling attack (subdomains vulnerable):
-to detect HTTP request smuggling attack with add header `Transfer-Encoding: chunked` 
and encode the body of request with chunked encode.
1. send request with a valid chunked encode and you will get response means that the **back-end server accept chunked encode**
2. send a large value in hex of chunked encode , if get ** delay of response**  means its vulnerable. 
resource: https://portswigger.net/web-security/request-smuggling/finding

## CONFIRMATION:

##POC:

in this POC i will use TWEET request as second request (payload) ,means that if the HTTP request smuggling attack success,
will get a new TWEET in my account 

F609847


## Steps To Reproduce:


ps : i use chrome browser,with burp
1- choose any valid POST request (or change GET to POST) from twitter.com and send it to repeater
2- delete this header (Connection: close  ,Accept-Encoding: gzip, deflate)
3- add this header <Transfer-Encoding: chunked>

4- add chunked encode    put a valid chunked code or   [ put just 0 with two CRLFs]
5-put the second request  [i use a TWEET request ]
6- send the attacker request

## Impact

impact of http request smuggling 
- https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
- https://portswigger.net/web-security/request-smuggling/exploiting

</details>

---
*Analysed by Claude on 2026-05-24*
