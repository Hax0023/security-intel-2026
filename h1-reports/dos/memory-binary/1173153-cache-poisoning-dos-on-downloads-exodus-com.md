# Cache Poisoning Denial of Service on downloads.exodus.com

## Metadata
- **Source:** HackerOne
- **Report:** 1173153 | https://hackerone.com/reports/1173153
- **Submitted:** 2021-04-23
- **Reporter:** youstin
- **Program:** Exodus
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Cache Poisoning, Denial of Service, Insufficient Cache Key Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
The downloads.exodus.com subdomain, which hosts user-downloadable files on Cloudflare-cached Azure Storage, is vulnerable to cache poisoning via a crafted Authorization header that triggers a 403 response. An attacker can poison the cache with this malformed header, causing all subsequent users to receive the cached 403 error and denying access to critical software downloads.

## Attack scenario
1. Attacker crafts an HTTP request to downloads.exodus.com with a malformed SharedKeyLite Authorization header and a unique cache-buster parameter
2. Attacker sends the request to the target file (e.g., hashes-exodus-21.2.12.txt), which reaches the origin Azure Storage server
3. Azure Storage rejects the malformed authorization header and returns a 403 Forbidden response
4. Cloudflare caches the 403 response, associating it with the file path and cache-buster parameter
5. Attacker removes or modifies the cache-buster parameter in subsequent requests to the same file
6. All users requesting the file now receive the cached 403 response, causing a denial of service until cache expiration

## Root cause
Cloudflare's cache key does not properly validate or exclude the Authorization header from cache key generation, allowing poisoning via authentication credentials. The origin server's error response (403) is cached and served to all users regardless of their authentication status.

## Attacker mindset
An attacker seeking to disrupt service availability would recognize that distributing software through a CDN creates a single point of failure if cache poisoning is possible. By crafting a request that generates an error response and sending it just before cache expiration, the attacker can ensure maximum impact with minimal requests. The use of cache-busting parameters demonstrates understanding of CDN mechanics and the ability to circumvent simple caching strategies.

## Defensive takeaways
- Configure Cloudflare to exclude or normalize the Authorization header from cache key generation for authenticated requests
- Implement cache rules that prevent 4xx and 5xx error responses from being cached, or set very short TTLs for error responses
- Use separate cache keys for authenticated and unauthenticated requests
- Implement request validation on the origin server to reject malformed Authorization headers before returning cached errors
- Monitor cache hit ratios and error responses for anomalies indicating potential poisoning attempts
- Consider using Cloudflare's cache rules to whitelist only expected headers for critical file distribution endpoints
- Implement signed URLs or other time-limited authentication mechanisms instead of relying on Authorization headers for file access

## Variant hunting
Similar vulnerabilities likely exist on other CDN-fronted Azure Storage endpoints. Search for other Exodus subdomains and services that distribute files through Cloudflare. Test for cache poisoning via other header-based mechanisms (User-Agent, X-Forwarded-For, custom headers). Check if other error status codes (400, 401, 429) are also cached and can be weaponized for DoS.

## MITRE ATT&CK
- T1190
- T1561
- T1499

## Notes
The researcher responsibly disclosed this vulnerability and used cache-busters during testing to avoid impacting live users. The attack requires precise timing relative to cache expiration to achieve maximum impact on legitimate users. This is a critical vulnerability for any software distribution platform, as it directly impacts users' ability to download essential software.

## Full report
<details><summary>Expand</summary>

## Summary:
Hello,

The subdomain downloads.exodus.com hosts all files meant to be downloaded by exodus users. A few of the file I found are:

```
https://downloads.exodus.com/releases/exodus-linux-x64-21.4.9.zip
https://downloads.exodus.com/releases/hashes-exodus-21.2.12.txt
https://downloads.exodus.com/releases/exodus-macos-21.3.29.dmg
```

The files are hosted on a azure storage host and are cached by Cloudflare.
A crafted Authorization header causes a 403 on the azure storage host, which is cached by cloudflare and passed to all other users accessing the source. 

### Disclaimer:
No actual denial of service attack was caused troughout my testing. All the testing used cache-busters, meaning it did not affect the live website in any way.

## Steps To Reproduce:

1. Send the following request to poison the cache:
```http
GET /releases/hashes-exodus-21.2.12.txt?cachebuster=hackerone HTTP/1.1
Host: downloads.exodus.com
Authorization: SharedKeyLite myaccount:ctzMq410TV3wS7upTBcunJTDLEJwMAZuFPfr0mrrA08=  

```
Notice you will get a 403. 

2. The cache is now poisoned so sending a request without the header or visiting the poisoned url in a browser will show you the cached 403. 
```
```http
GET /releases/hashes-exodus-21.2.12.txt?cachebuster=hackerone HTTP/1.1
Host: downloads.exodus.com

```
Will show the same 403 response. 

## Supporting Material/References:

Video PoC:

████████

## Impact

The steps that were used to take down a reosurce including a random parameter as a cache-buster can also be reproduced on the actual files when their cache is about to expire.  This will cause a DoS, restricting users from downloading or accessing the files hosted on downloads.exodus.com.

</details>

---
*Analysed by Claude on 2026-05-24*
