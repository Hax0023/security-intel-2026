# HTTP Request Smuggling on my.stripo.email

## Metadata
- **Source:** HackerOne
- **Report:** 777651 | https://hackerone.com/reports/777651
- **Submitted:** 2020-01-18
- **Reporter:** codeslayer1337
- **Program:** Stripo
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length / Transfer-Encoding) desynchronization, Request/Response desynchronization
- **CVEs:** None
- **Category:** uncategorised

## Summary
HTTP request smuggling vulnerability discovered on my.stripo.email caused by inconsistent parsing of Content-Length and Transfer-Encoding headers between front-end and back-end servers. An attacker can craft malformed requests with conflicting content length indicators to poison the TCP/TLS connection and inject arbitrary data into subsequent requests.

## Attack scenario
1. Attacker crafts HTTP POST request with both Content-Length and Transfer-Encoding: chunked headers with conflicting values
2. Front-end server processes request using Content-Length header and forwards request to back-end
3. Back-end server interprets the same request using Transfer-Encoding: chunked, causing desynchronization
4. Back-end server consumes fewer bytes than front-end expects, leaving additional payload in the TCP buffer
5. Next legitimate user request from another client gets prepended with attacker's injected payload
6. Attacker can poison cache, bypass security controls, steal session data, or perform phishing attacks on subsequent users

## Root cause
Inconsistent HTTP parsing between front-end and back-end servers when handling conflicting Content-Length and Transfer-Encoding headers. The servers prioritize different headers, causing request boundaries to be interpreted differently.

## Attacker mindset
Exploiting infrastructure misconfigurations to achieve request/response poisoning at the TCP level, enabling cache poisoning and session hijacking without authentication.

## Defensive takeaways
- Normalize and validate HTTP headers: reject requests with both Content-Length and Transfer-Encoding headers
- Ensure consistent HTTP parsing logic across all servers in the request chain
- Implement strict request validation: reject ambiguous or malformed requests at the earliest point
- Use HTTP/2 or HTTP/3 which have stricter parsing requirements and are less susceptible to smuggling
- Apply defense-in-depth: use WAF rules to detect and block smuggling attempts
- Regular security audits of reverse proxy and load balancer configurations
- Monitor for request smuggling indicators: unusual header combinations, chunked encoding anomalies

## Variant hunting
Test CL.TE variants: Content-Length with conflicting Transfer-Encoding values
Test TE.CL variants: Transfer-Encoding prioritized over Content-Length
Test TE.TE variants: multiple Transfer-Encoding headers with conflicting values
Check for header folding/line wrapping bypasses
Test with obfuscated Transfer-Encoding headers (spaces, tabs, case variations)
Examine other Stripo infrastructure endpoints for similar desynchronization issues
Test reverse proxy and CDN configurations that may introduce parsing differences

## MITRE ATT&CK
- T1190
- T1021
- T1040
- T1557

## Notes
Report contains proof-of-concept using Burp Suite Turbo Intruder with malformed headers. The attack demonstrates socket poisoning leading to 301 redirect to attacker-controlled domain. Report references PortSwigger research on HTTP desync attacks. Actual bounty amount not disclosed in writeup. Technical details suggest CL.TE desynchronization where front-end uses Content-Length while back-end uses Transfer-Encoding: chunked.

## Full report
<details><summary>Expand</summary>

## Summary:
HTTP request smuggling vulnerabilities arise when websites route HTTP requests through webservers with inconsistent HTTP parsing.
By supplying a request that gets interpreted as being different lengths by different servers, an attacker can poison the back-end TCP/TLS socket and prepend arbitrary data to the next request. Depending on the website's functionality, this can be used to bypass front-end security rules, access internal systems, poison web caches, and launch assorted attacks on users who are actively browsing the site.

## Steps To Reproduce:
I use BurpSuite with the help of the HTTP Smuggler Request plugin to provide POC
1.Run the burp suite turbo intruder on the following request
POST /?aeRg=2056729135 HTTP/1.1
Host: my.stripo.email
Accept-Encoding: gzip, deflate
Accept: */*
Accept-Language: en-US,en-GB;q=0.9,en;q=0.8
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding : chunked
Content-Len%s keep-alive

f
ubvhq=x&e3t5b=x
0


2.The script for the turbo intruder is attached with the name poc.txt
3.301 object responses OK for the post request needed to provide a header response to Location: https://codeslayer137.000webhostapp.com/indeks. php Please see the attached screenshot. (2.png).

## Impact

Impact
an attacker can poison the TCP / TLS socket and add arbitrary data to the next request. Depending on the functionality of the website, this can be used to bypass front-end security rules, internal system access, poison the web cache, and launch various attacks on users who actively activate the site.

Reference: https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn

Best regards

CodeSlayer13

</details>

---
*Analysed by Claude on 2026-05-24*
