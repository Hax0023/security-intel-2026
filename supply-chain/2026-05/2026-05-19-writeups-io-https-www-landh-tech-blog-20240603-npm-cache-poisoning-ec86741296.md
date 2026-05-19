# npm Registry Cache Poisoning Attack (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Response Splitting, Cache Key Collision
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to manipulate HTTP caching headers to poison the cache with 404 responses for legitimate packages. By crafting specially designed requests with specific header combinations, attackers could render packages temporarily inaccessible to all users, affecting the entire JavaScript ecosystem of 17 million developers.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP GET request to npmjs.org for a target package with specially constructed headers designed to trigger backend caching errors
2. Attacker includes cache-busting parameters and malicious headers in the request to bypass normal cache validation mechanisms
3. The vulnerable caching system stores an erroneous 404 'Not Found' response in the cache using the poisoned request as the cache key
4. Subsequent legitimate requests from other users for the same package without the malicious headers hit the poisoned cache entry
5. Users receive 404 errors instead of the legitimate package tarball, effectively denying access to the package
6. The attack persists for several minutes until the temporary cache entry expires, during which all package downloads fail

## Root cause
The npm registry's caching infrastructure (likely Cloudflare-based) incorrectly handles HTTP headers when computing cache keys and validating responses. The vulnerability stems from inconsistent cache key generation where requests with malicious headers and requests without them are treated as the same cache entry, allowing poisoning. Additionally, the backend fails to properly validate requests before caching error responses, enabling attackers to cache negative responses that should never be cached.

## Attacker mindset
Supply chain saboteur seeking to maximize ecosystem disruption with minimal effort. The attacker recognizes that npm's centralized nature makes it a high-impact target. By repeatedly poisoning popular packages for short windows, they could cause widespread build failures across the JavaScript community without requiring account compromise or package modification capabilities.

## Defensive takeaways
- Implement strict cache key normalization that includes all request parameters and headers in consistent order to prevent key collision attacks
- Never cache error responses (4xx, 5xx) from backend systems without explicit cache-control headers
- Use cache-busting mechanisms that strip out suspicious or non-standard headers before cache key computation
- Implement rate limiting on requests to the same resource from single IP addresses to limit CPDoS attack window
- Monitor cache hit ratios and alert on sudden increases in 404 responses for specific packages
- Consider using separate caches for authenticated vs unauthenticated requests
- Implement cache validation logic that re-checks backend availability for error responses before serving from cache

## Variant hunting
['Test other package registries (yarn, Maven Central, PyPI) for similar cache poisoning via header manipulation', 'Investigate if CDN configuration at Cloudflare allows cache poisoning through other header combinations (Accept, Accept-Encoding, Authorization variations)', 'Test whether the vulnerability applies to scoped packages (@org/package) with different URL structures', 'Check if the attack works on registry.npmjs.org subdomain vs cdn.npmjs.org or other npm endpoints', 'Attempt cache poisoning with other HTTP methods (HEAD, OPTIONS) to bypass method-specific cache rules', 'Test if the vulnerability extends to package metadata endpoints (/package.json vs .tgz files)', 'Investigate whether conditional headers (If-Modified-Since, ETag) can be abused similarly']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1195.003 - Supply Chain Compromise: Compromised Software Dependencies
- T1499 - Endpoint Denial of Service
- T1499.004 - Endpoint Denial of Service: Application Exhaustion
- T1657 - Force Quitting Application

## Notes
This vulnerability was discovered during authorized security research into artifactory cache poisoning. The researchers responsibly disclosed findings and withheld specific header combinations to prevent immediate widespread exploitation. The temporary nature of the cache (minutes) limits real-world impact but allows for coordinated attacks on high-traffic package releases. The vulnerability demonstrates how infrastructure-level flaws can cascade to affect millions of developers. npm likely patched by improving cache key generation logic and response validation rules post-disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
