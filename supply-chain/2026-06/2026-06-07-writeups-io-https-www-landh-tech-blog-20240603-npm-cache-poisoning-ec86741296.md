# NPM Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** NPM/npmjs.com
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Response Splitting, Cache Key Collision
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the caching system through specially crafted HTTP headers, causing legitimate package requests to return 404 errors. By manipulating web cache mechanisms, an attacker could render popular packages temporarily inaccessible to millions of developers, effectively disrupting the JavaScript supply chain. The vulnerability exploits subtle flaws in how caching headers interact with the registry's backend systems.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP request with a specific series of headers targeting a popular npm package (e.g., safe-regex-1.1.0.tgz)
2. The request is sent to registry.npmjs.org with a cache buster parameter and special header to trigger backend error handling
3. The registry's caching system incorrectly caches the error response (404 Not Found) using a cache key derived from the request
4. Attacker sends a follow-up request without the malicious header but with the same cache key parameters
5. The poisoned cache entry is retrieved and served to subsequent users requesting the legitimate package
6. Thousands of developers receive 404 errors when attempting to install the poisoned package, causing widespread supply chain disruption

## Root cause
The npm registry's caching layer (likely Cloudflare) fails to properly differentiate between requests with specific header combinations that trigger backend errors. The cache key generation logic does not account for certain header variations, allowing an attacker to create a cache collision where a 404 error response becomes associated with legitimate package requests. The backend error handling exposes the poisoning mechanism by caching error states that should not be cached.

## Attacker mindset
An adversary seeks to maximize supply chain disruption by targeting the most popular npm packages with the goal of causing widespread denial of service across the JavaScript ecosystem. By requiring only repeated requests with a rotating cache buster, the attacker can maintain the poisoning with minimal effort. The temporary nature of the cache suggests the attacker would need to continuously re-poison packages, making this suitable for targeted disruption campaigns rather than persistent attacks.

## Defensive takeaways
- Implement strict cache key generation that includes all request headers relevant to response variation, preventing header-based cache collisions
- Never cache error responses (4xx/5xx) in shared caches without explicit short TTLs and cache validation headers
- Use cache tags or surrogate keys to allow rapid invalidation of poisoned entries when abuse is detected
- Monitor cache hit ratios and 404 response patterns for anomalies indicating active poisoning attempts
- Implement request validation to reject or sanitize unusual header combinations before they reach backend systems
- Use Vary header correctly to account for all headers that influence the response, preventing cache key collisions
- Implement rate limiting on package requests to prevent repeated cache poisoning attempts from single IPs
- Add integrity verification mechanisms so package managers can validate downloaded content against manifest hashes

## Variant hunting
Look for similar CPDoS vulnerabilities in other registries: PyPI, Maven Central, RubyGems, Cargo, NuGet. Test for cache poisoning via: Content-Length discrepancies, Range request manipulation, Charset/Encoding header conflicts, X-Forwarded-* header variations, and HTTP version switching (HTTP/1.1 vs HTTP/2). Check if other header combinations can trigger different backend error states that are cached. Test whether authentication headers or API tokens influence cache behavior. Investigate if package version strings with special characters cause similar cache key collision issues.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (registry vulnerability exploitation)
- T1195 - Supply Chain Compromise (poisoning package distribution)
- T1499 - Endpoint Denial of Service (CPDoS attack)
- T1657 - Defacement (serving 404 instead of legitimate package)
- T1583 - Acquire Infrastructure (for requesting malicious package versions)

## Notes
The researchers explicitly withheld disclosure of the specific header combination to prevent immediate exploitation. The vulnerability was discovered during internal testing of Depi, a supply chain security testing tool. The cached 404 response was temporary (lasting minutes), requiring continuous re-poisoning. The attack uses a cache buster parameter (lupin_E7A812DE-E09A-4906-A9E3-530E54AAEB41) to avoid unintentionally poisoning legitimate user requests during testing. This represents a sophisticated understanding of cache mechanics and suggests the vulnerability likely affects the Cloudflare edge caching layer in front of npmjs.org. The potential impact is catastrophic given npm's centrality to the JavaScript ecosystem (2.1M packages, 17M developers).

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
