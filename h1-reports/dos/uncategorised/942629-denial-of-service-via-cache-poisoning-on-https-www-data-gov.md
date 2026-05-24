# Denial of Service via Cache Poisoning on data.gov using Host Header Manipulation

## Metadata
- **Source:** HackerOne
- **Report:** 942629 | https://hackerone.com/reports/942629
- **Submitted:** 2020-07-25
- **Reporter:** kq8dq
- **Program:** data.gov
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Cache Poisoning, Host Header Injection, Denial of Service
- **CVEs:** None
- **Category:** uncategorised

## Summary
An attacker can poison the cache on data.gov by sending requests with a malicious Host header (h0st) that causes the backend to generate 502 responses, which are then cached and served to legitimate users. By using a cache buster parameter, the attacker can target specific URLs and persistently deny access to the application.

## Attack scenario
1. Attacker crafts HTTP request to https://www.data.gov/?xyzxyz=1 with a spoofed/invalid Host header (h0st: wrtqvavjigwdvoqk)
2. Backend server processes the malformed host header and generates a 502 Bad Gateway response
3. CDN/caching layer caches the 502 error response associated with the URL and cache key
4. Legitimate users requesting the same URL receive the cached 502 error instead of valid content
5. Attacker can repeat process with different cache buster parameters to poison multiple URL paths
6. Service remains unavailable to legitimate users until cache TTL expires

## Root cause
The web server or reverse proxy does not properly validate the Host header before processing the request and does not exclude error responses or Host header variations from cache key computation. This allows attackers to manipulate the cache key using a malformed host header to poison cached responses.

## Attacker mindset
Exploit misconfiguration in cache key normalization to achieve persistent denial of service without direct rate limiting or bot detection. The use of cache buster parameters allows targeting specific URLs while remaining stealthy. Low effort attack with high impact potential.

## Defensive takeaways
- Implement strict Host header validation - reject requests with invalid/unexpected Host headers before reaching backend
- Normalize Host header in cache key computation to prevent poisoning via header variations
- Do not cache error responses (4xx, 5xx) or implement very short TTLs for error pages
- Use allowlist approach for Host headers at CDN/WAF level
- Implement request rate limiting per Host header value to detect poisoning attempts
- Add monitoring for unusual Host header values in access logs
- Configure reverse proxy to sanitize and validate Host headers before forwarding to origin

## Variant hunting
Test other header injection vectors (X-Forwarded-Host, X-Original-Host) for cache poisoning
Attempt cache poisoning with malformed port numbers in Host header (e.g., Host: example.com:99999)
Test cache poisoning on different URL paths and query parameters
Try combining Host header injection with other headers (User-Agent, Accept-Language) to expand cache key variations
Test cache poisoning with internationalized domain names (IDN) in Host header
Attempt to poison specific content types by manipulating Accept headers alongside Host headers

## MITRE ATT&CK
- T1499.004 Application Layer DDoS (HTTP Floods/Cache Poisoning)
- T1190 Exploit Public-Facing Application

## Notes
Reporter referenced PortSwigger research on web cache poisoning and cited similar vulnerabilities. The attack demonstrates how improper cache key construction can lead to persistent DoS. The presence of similar prior reports (622122, 409370) suggests this was a known attack vector that data.gov may not have fully remediated.

## Full report
<details><summary>Expand</summary>

An attacker can persistently block access to any on https://www.data.gov/ by using cache poisoning with the h0st headers to cause
502 response code。

To replicate:
load https://www.data.gov/ in your browser.
look the burp ,  add ?xyzxyz=1 as cache buster , and add h0st headers h0st: wrtqvavjigwdvoqk in your burp.
load https://www.data.gov/?xyzxyz=1 in your browser. again.
and you win see 502 ERROR

{F922984}

To be more clearer, see my video
{F922983}

my http request：

```
GET /?xyzxyz=1 HTTP/1.1
Host: www.data.gov
Connection: close
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
h0st: wrtqvavjigwdvoqk
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate
Accept-Language: zh-CN,zh;q=0.9

```


For more information on the theory behind this attack, check out https://portswigger.net/research/responsible-denial-of-service-with-web-cache-poisoning

Similar report：
https://hackerone.com/reports/622122
https://hackerone.com/reports/409370

## Impact

An attacker can persistently block access to any on https://www.data.gov/

</details>

---
*Analysed by Claude on 2026-05-24*
