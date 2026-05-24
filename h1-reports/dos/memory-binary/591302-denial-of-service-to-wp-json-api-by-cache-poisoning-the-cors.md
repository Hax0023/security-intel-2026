# Denial of Service via Cache Poisoning of CORS Allow-Origin Header in WP-JSON API

## Metadata
- **Source:** HackerOne
- **Report:** 591302 | https://hackerone.com/reports/591302
- **Submitted:** 2019-05-28
- **Reporter:** nathand
- **Program:** HackerOne (WordPress.com/Automattic)
- **Bounty:** Not specified in writeup
- **Severity:** Medium
- **Vuln:** Cache Poisoning, Denial of Service, CORS Misconfiguration, HTTP Response Splitting
- **CVEs:** None
- **Category:** memory-binary

## Summary
WordPress.com's WP-JSON API echoes back the Origin header in the Access-Control-Allow-Origin response header without validating it, and the response is cached without keying on the Origin value. An attacker can poison the cache by making requests from arbitrary origins, causing subsequent legitimate cross-origin requests from different origins to fail CORS validation and resulting in denial of service for dependent services.

## Attack scenario
1. Attacker identifies a WordPress.com website using WP-JSON API that has cached responses (indicated by X-Cache: hit header)
2. Attacker makes a fetch request to the target WP-JSON endpoint from their own domain (e.g., attacker.com) with a unique query string to ensure cache busting
3. The WP-JSON API responds with Access-Control-Allow-Origin: https://attacker.com, which gets cached on the CDN/edge cache
4. Victim website (e.g., foo.target.com) attempts to use WP-JSON API from target.com in a browser context, triggering a CORS request
5. The victim's browser receives the cached response with Access-Control-Allow-Origin: https://attacker.com instead of their origin
6. The CORS check fails in the browser, blocking the response and breaking functionality that depends on the WP-JSON API

## Root cause
The WP-JSON implementation reflects the Origin header from the request directly into the Access-Control-Allow-Origin response header without validation, and the caching layer (Automattic's CDN/edge cache) does not include the Origin header as part of the cache key. This allows a single poisoned response to affect all subsequent requests regardless of their origin.

## Attacker mindset
An attacker seeks to disrupt services that rely on cross-origin WP-JSON API calls by weaponizing the caching layer. The attack requires minimal effort (simple HTTP requests) and can be automated to poison multiple cache entries. The attacker may target competitors or high-profile WordPress.com customers whose services depend on WP-JSON for critical functionality.

## Defensive takeaways
- Always include request headers that vary the response (Origin, Host, etc.) in the cache key
- Implement an Origin whitelist instead of reflecting arbitrary Origin headers; validate against known trusted origins
- For CORS responses, either use specific allowed origins or use the wildcard '*' (which disables credential-based requests), but never reflect user-supplied values
- Add security headers like X-Content-Type-Options: nosniff and Vary: Origin to control caching behavior
- Monitor for suspicious CORS header variations in access logs that may indicate cache poisoning attempts
- Use CSP and other security controls to limit the impact of CORS misconfigurations
- Implement cache purging strategies and monitoring to detect when responses are being served with incorrect CORS headers

## Variant hunting
Test other WordPress hosting providers (Kinsta, WP Engine, etc.) for similar cache poisoning issues with WP-JSON
Check if other REST API implementations reflect Origin headers without validation
Investigate whether other response headers (Authorization, Set-Cookie, etc.) can be poisoned through similar cache key weaknesses
Test if the vulnerability extends to cached responses for authenticated endpoints
Examine whether query parameters or other request attributes are properly keyed in the cache

## MITRE ATT&CK
- T1190
- T1561
- T1499

## Notes
This vulnerability is a sophisticated example of how caching infrastructure can amplify security misconfigurations. The attack is particularly insidious because it affects legitimate users without requiring them to visit a malicious website. The researcher responsibly disclosed this to multiple WordPress SaaS providers, indicating this is a systemic issue in how some platforms handle WP-JSON caching. The proof of concept intentionally uses cache-busting to avoid poisoning production caches, demonstrating responsible security research.

## Full report
<details><summary>Expand</summary>

The WP-JSON implementation on some wordpress.com websites I've tested is vulnerable to denial of service where by an attacker can provide an arbitrary `Origin` header in the request, which is then echoed back in the response via the `Access-Control-Allow-Origin` header, which is cached and served to other requests.

This response header is used by browsers to determine whether the requesting origin (if it is a cross origin request) is allowed to read the response in the request. In the event the victim website had another origin that used the WP-JSON API to request data from their wordpress.com site (e.g. a sub domain), this cache poisoning would deny access to such requests due to failed a CORS access control check. It appears that this vulnerability is only a concern if the WP-JSON API responses are cached, which you can determine by the presence of a `X-Cache: hit` header in the response.

## Proof of concept

For this test, I'm going to target `█████████.com`, a wordpress.com site. I will be doing this with a cache busting technique that doesn't really poison the live site's cache (by supplying a bespoke query string value) so this should be safe to repeat verbatim.

  1. First, open a HTTPS website - it doesn't matter which website, as long as it isn't `https://█████████.com` (to trigger browser CORS). For my test, I used my own website https://nathandavison.com.
  1. Open the javascript console and execute the following 5-10 times (to make sure the cache is poisoned across backends): `fetch('https://██████████.com/wp-json/?dontreallypoison1').then(res => res.json()).then(json => console.log(json))`
  1. Now, open another HTTPS website - it also doesn't matter which site it is, as long as it too isn't `https://███████.com`. Execute the same fetch as above.
  1. You should now experience a CORS error in your browser, such as: `Cross-Origin Request Blocked: The Same Origin Policy disallows reading the remote resource at https://█████████.com/wp-json/?dontreallypoison1. (Reason: CORS header ‘Access-Control-Allow-Origin’ does not match ‘https://nathandavison.com’).`

What's going on here? because the WP-JSON response is CORS aware, it is responding with a `Access-Control-Allow-Origin` header value. Presumably to offer wide support for CORS, the `Origin` value in the request is being echoed back. So far, I believe this is standard Wordpress WP-JSON behavior. However, automattic/wordpress.com is caching this response and is not keying the cache based on the request `Origin` value (which is `https://nathandavison.com` in step 1 above), so therefore is serving the poisoned response in step 4, and because the other origin is not `https://nathandavison.com`, CORS in the browser blocks the response coming back into the DOM.

I believe any wordpress.com website that caches WP-JSON responses is vulnerable to this. A quick way, as an attacker, to find potential victims would be a query like this:

https://publicwww.com/websites/%22If%20you're%20reading%20this,%20you%20should%20visit%20automattic.com%22/

## Attach scenario

To attack this, a victim site would have to:

  1. Use WP-JSON is a meaningful way in a browser context (or any other context that respects CORS headers)
  1. Use it from an origin that triggers CORS. For example, if the WP-JSON API is used on "foo.████.com" to request the blog posts from "█████.com". Another example may be a "headless" Wordpress site (e.g. api.x.com is Wordpress and x.com is the frontend, which uses the WP-JSON plugin to interact with the WP backend).

Once a target is found that satisfies these conditions, an attacker would then simply poison the CORS response with regular requests to specific endpoints. This poisoning would result (in the example above) in visitors to "foo.██████.com" failing to load the WP-JSON API requests to "██████████.com" due to CORS failures, causing a DoS for whatever service relies on this functionality.

## Fix

I believe to fix this, automattic should make sure that edge caches for WP-JSON requests are using the `Origin` header in the request to key the cache, so one value can't affect the cache served to another value. Preventing the echoing back of the `Origin` into the `Access-Control-Allow-Origin` response header without first passing through a configurable whitelist would also be a potential solution, but this may be harder to implement. 

## More information

Please see the following blog post for more information on this:

https://nathandavison.com/blog/corsing-a-denial-of-service-via-cache-poisoning

I wrote this post in response to disclosing a very similar vulnerability to another Wordpress SaaS provider.

## Impact

The impact of this vulnerability depends on how and where a client uses the WP-JSON plugin. If a wordpress.com customer uses WP-JSON in a context that relies on CORS, this technique could deny service to the WP-JSON endpoints in use.

</details>

---
*Analysed by Claude on 2026-05-24*
