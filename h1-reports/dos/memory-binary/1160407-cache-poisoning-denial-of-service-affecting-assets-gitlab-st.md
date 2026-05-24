# Cache Poisoning Denial of Service on assets.gitlab-static.net via x-http-method-override Header

## Metadata
- **Source:** HackerOne
- **Report:** 1160407 | https://hackerone.com/reports/1160407
- **Submitted:** 2021-04-10
- **Reporter:** youstin
- **Program:** GitLab
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Cache Poisoning, Denial of Service, HTTP Request Smuggling, Improper Input Validation
- **CVEs:** None
- **Category:** memory-binary

## Summary
GitLab's CDN at assets.gitlab-static.net uses Varnish caching and is hosted on GCP infrastructure that accepts the x-http-method-override header. An attacker can poison the cache by sending a GET request with x-http-method-override: HEAD, causing Varnish to cache an empty response that is then served to all users, resulting in denial of service by missing CSS/JS files.

## Attack scenario
1. Attacker identifies that assets.gitlab-static.net hosts critical JS/CSS files for gitlab.com using Varnish CDN
2. Attacker discovers GCP accepts x-http-method-override header and Varnish does not normalize it in cache keys
3. Attacker sends GET request with x-http-method-override: HEAD header and cache-busting query parameter to a critical asset file
4. GCP backend processes request as HEAD request and returns empty response body
5. Varnish caches the empty response without considering the x-http-method-override header as part of cache key
6. Subsequent legitimate user requests for the same file receive the poisoned empty response, breaking website functionality

## Root cause
Varnish CDN configuration does not include x-http-method-override header in cache key normalization, allowing the same cache entry to be used for different HTTP methods. Combined with GCP's default acceptance of x-http-method-override header, this enables cache poisoning.

## Attacker mindset
Attacker recognizes infrastructure-specific behaviors (GCP header handling) and caching layer weaknesses (Varnish cache key construction) to amplify impact through poisoned cache serving to all users without rate limiting.

## Defensive takeaways
- Normalize all headers that affect response semantics in CDN cache keys, including x-http-method-override
- Disable or restrict HTTP method override headers at CDN/reverse proxy level if not required
- Implement strict access controls on cache invalidation methods (PURGE); restrict to authenticated/authorized users only
- Configure origin servers to reject suspicious headers like x-http-method-override
- Implement cache key whitelisting - only vary cache on specific, known headers
- Monitor for cache poisoning patterns such as requests with unusual header combinations
- Implement request validation at CDN layer to reject conflicting headers before reaching origin

## Variant hunting
Test other HTTP method override headers (X-Original-Method, X-Method-Override, etc.) on Varnish-cached assets
Check if other GitLab CDN endpoints use similar vulnerable caching patterns
Probe for cache poisoning via Content-Type manipulation combined with method overrides
Test PURGE method access controls on other static asset CDNs within GitLab infrastructure
Investigate if Range request headers can be poisoned similarly in cache
Check Accept-Encoding header normalization to identify compression-based poisoning vectors

## MITRE ATT&CK
- T1190
- T1499

## Notes
Researcher responsibly avoided actual DoS by using cache-busting query parameters during testing. PURGE method authorization weakness is a secondary vector that amplifies impact by allowing cache invalidation before poisoning. The vulnerability chain demonstrates importance of defense-in-depth: both the cache key normalization AND access controls failed.

## Full report
<details><summary>Expand</summary>

# Summary

Hi,

Gitlab.com is hosting JS and CSS on `https://assets.gitlab-static.net/` and uses them on gitlab.com/*
The static files seem to be stored on a gcp host, which by default accepts the `x-http-method-override` header. Since the CDN is using Varnish to cache files, I was able to combine the GCP behaviour and poison the cache into returning an empty resource, inherenetly causing a denial of service on gitlab.com and all gitlab assets that use the specific cdn. 

###  Disclaimer

No actual denial of service attack was caused troughout my testing. All the testing used cache-busters, meaning it did not affect the live website in any way.
 
# Steps to reproduce

1. Sending a request such as:

```http
GET /assets/webpack/commons-pages.admin.sessions-pages.groups.omniauth_callbacks-pages.ldap.omniauth_callbacks-pages.omn-c3aaf8c4.3f9d44ba.chunk.js HTTP/1.1
Host: assets.gitlab-static.net
User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:87.0) Gecko/20100101 Firefox/87.0
Connection: close
```
will return the expected js file. 
By taking a quick look at the response headers, we can see the file is currently cached by varnish because of the following headers:
```http
Age: 498
X-Served-By: cache-dca17752-DCA, cache-osl6520-OSL
X-Cache: HIT, HIT
X-Cache-Hits: 1, 1
```
2. In order to test cache poisoning without affecting the live website, we can add random query parameters that will act as cache busters. In order to poison a resource, an attacker would send the following request:

```http
GET /assets/webpack/commons-pages.admin.sessions-pages.groups.omniauth_callbacks-pages.ldap.omniauth_callbacks-pages.omn-c3aaf8c4.3f9d44ba.chunk.js?cb=youstin-xyz HTTP/1.1
Host: assets.gitlab-static.net
x-http-method-override: HEAD
```

This will return an empty response, as it is expected from a `HEAD` request. However since the `x-http-method-override` header is not included in the cache key and the varnish configuration used does not proccess the `x-http-method-override`, this empty response will also be forwarded to all other users requesting the file, with normal GET requests. 

{F1260892}

You can also confirm the cache can be poisoned by visiting the file in your browser, making sure to include the parameter used as a cachebuster. You should notice the empty repsonse, typical to a HEAD request.

This vulnerability can be used on files used by the live site even if they are already cached, by making use of the PURGE http method, which clears the cache, allowing for an easily reproducible DoS attack.

## Impact

Since Gitlab does not forbid unauthorized users from using the PURGE http method, which clears the cache, it is possible for an attacker to clear the cache for actual JS or CSS files used on gitlab.com and poison it with an empty response. Doing so will lead to missing JS and CSS files, making gitlab completely unuseable. 
This vulnerability affects all instances of gitlab where the cdn is used for JS and CSS files.

</details>

---
*Analysed by Claude on 2026-05-24*
