# Apache HTTP Server mod_proxy_ajp HTTP Request Smuggling

## Metadata
- **Source:** HackerOne
- **Report:** 1594627 | https://hackerone.com/reports/1594627
- **Submitted:** 2022-06-08
- **Reporter:** ricterz
- **Program:** Apache HTTP Server
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** HTTP Request Smuggling, Inconsistent Interpretation of HTTP Requests, CL.TE (Content-Length Transfer-Encoding), Protocol Desynchronization
- **CVEs:** CVE-2022-26377
- **Category:** uncategorised

## Summary
A request smuggling vulnerability in Apache HTTP Server's mod_proxy_ajp module (versions ≤2.4.53) allows attackers to inject malicious requests to backend AJP servers through inconsistent HTTP header interpretation. The vulnerability exploits differing parsing of Content-Length and Transfer-Encoding headers between the HTTP frontend and AJP backend, enabling information disclosure and remote code execution.

## Attack scenario
1. Attacker crafts an HTTP request with conflicting Content-Length and Transfer-Encoding headers
2. Apache HTTP Server's mod_proxy_ajp frontend interprets the request one way (e.g., by Content-Length)
3. The backend AJP server interprets the same request differently (e.g., by Transfer-Encoding)
4. Attacker's smuggled payload remains in the request buffer after processing
5. Smuggled payload is prepended to the next legitimate request from another user
6. Backend AJP server processes the injected malicious commands, leading to information disclosure or RCE

## Root cause
Inconsistent handling of HTTP header parsing between mod_proxy_ajp's interpretation and the backend AJP server's interpretation. The module fails to normalize or reject ambiguous header combinations before forwarding requests, allowing attackers to exploit differential parsing behavior.

## Attacker mindset
An attacker targets web applications using Apache HTTP Server with mod_proxy_ajp reverse proxy configurations. They exploit the protocol desynchronization to inject hidden requests that access sensitive data or execute commands on backend servers, particularly in environments where multiple users share connection pools.

## Defensive takeaways
- Upgrade Apache HTTP Server to version 2.4.54 or later with patched mod_proxy_ajp
- Implement strict HTTP request validation that rejects ambiguous Content-Length/Transfer-Encoding combinations
- Normalize all HTTP headers before forwarding to backend servers
- Disable Transfer-Encoding if not explicitly required by application logic
- Implement request smuggling detection through connection-level monitoring
- Use connection isolation or connection pooling per-user/per-request
- Monitor for HTTP/1.1 violations and malformed headers in reverse proxy logs
- Test reverse proxy configurations for request smuggling using tools like HTTP Request Smuggler

## Variant hunting
Check other mod_proxy variants (mod_proxy_http, mod_proxy_balancer) for similar header parsing inconsistencies
Audit other reverse proxy modules in Apache for CL.TE and TE.CL smuggling vectors
Examine mod_rewrite rules that might not properly sanitize headers before proxying
Investigate custom Apache modules that handle AJP or HTTP/2 to HTTP/1.1 downgrade scenarios
Search for CVEs in other reverse proxies (Nginx, HAProxy, IIS) with mod_proxy_ajp functionality

## MITRE ATT&CK
- T1190
- T1021
- T1555
- T1059

## Notes
This vulnerability is critical in environments using Apache as a reverse proxy to Tomcat or other AJP-based servers. The lack of request smuggling protections in older versions allows attackers to bypass security controls and interact directly with backend application logic. Organizations running versions 2.4.53 or earlier should prioritize immediate patching. The vulnerability demonstrates the importance of protocol-level validation in proxy servers, especially when forwarding between different protocols (HTTP to AJP).

## Full report
<details><summary>Expand</summary>

Inconsistent Interpretation of HTTP Requests ('HTTP Request Smuggling') vulnerability in mod_proxy_ajp of Apache HTTP Server allows an attacker to smuggle requests to the AJP server it forwards requests to.  This issue affects Apache HTTP Server Apache HTTP Server 2.4 version 2.4.53 and prior versions.

## Impact

Information disclosure, RCE

</details>

---
*Analysed by Claude on 2026-05-24*
