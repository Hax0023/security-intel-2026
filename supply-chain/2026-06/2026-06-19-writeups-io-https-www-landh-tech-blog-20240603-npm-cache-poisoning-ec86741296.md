# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Header Manipulation, Cache Key Collision
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to manipulate HTTP caching mechanisms via specially crafted headers to poison cache entries, causing legitimate package requests to return 404 errors. The attack exploits subtle flaws in how the registry's caching infrastructure handles conflicting headers, potentially rendering packages temporarily inaccessible to millions of developers relying on the npm ecosystem.

## Attack scenario (step by step)
1. Attacker identifies vulnerable cache handling behavior in registry.npmjs.org by analyzing HTTP header processing
2. Attacker crafts malicious HTTP request containing specially designed headers that trigger backend caching errors
3. Request is sent with cache buster parameter containing unique identifier (e.g., lupin_E7A812DE-E09A-4906-A9E3-530E54AAEB41)
4. Backend incorrectly caches a 404 'Not Found' response instead of the legitimate package content
5. Attacker follows up with subsequent requests matching the same cache key but without malicious headers
6. Legitimate users receive cached 404 responses, unable to download the targeted package for several minutes

## Root cause
The npm registry's caching layer (likely Cloudflare-based CDN) fails to properly validate and differentiate requests with conflicting or anomalous HTTP headers when computing cache keys. The vulnerability stems from improper cache key generation that either ignores certain headers or processes them inconsistently, allowing an attacker to create a collision between a malicious request and subsequent legitimate requests.

## Attacker mindset
Supply chain sabotage motivated by ecosystem disruption. Attacker demonstrates research-oriented thinking by discovering vulnerability during defensive tool development rather than through opportunistic exploitation. Selective exploitation using cache busters shows sophistication and awareness of collateral damage. Intent appears to be proving ecosystem fragility rather than personal gain.

## Defensive takeaways
- Implement strict cache key generation that includes all relevant request headers in a canonical form to prevent header-based cache collisions
- Validate HTTP headers against a whitelist and reject requests with malformed or suspicious header combinations before caching
- Implement per-package rate limiting and anomaly detection to identify suspicious access patterns targeting specific versions
- Use cache versioning and integrity checks (e.g., cryptographic signatures) to detect poisoned cache entries
- Deploy cache poisoning detection mechanisms that identify when error responses are cached for content that should be cacheable
- Implement comprehensive logging and monitoring of cache operations with alerting for unusual cache key patterns
- Consider cache isolation strategies where critical package downloads bypass standard caching or use separate cache layers
- Establish incident response procedures specifically for supply chain cache poisoning scenarios

## Variant hunting
['Test other package registries (PyPI, Maven Central, RubyGems, NuGet) for similar cache poisoning vulnerabilities using HTTP header manipulation', 'Explore different HTTP header combinations (Accept-Encoding, Accept-Language, X-Forwarded-*, custom headers) to find alternative cache key collisions', 'Investigate whether cache poisoning can be weaponized to serve malicious package content instead of just 404 errors', 'Test if the vulnerability affects other npm endpoints (metadata queries, search functionality) beyond package downloads', "Examine whether cache poisoning duration can be extended beyond the reported 'few minutes' through header manipulation", 'Research if concurrent requests with varying headers can create race conditions in cache validation logic', 'Test CDN-specific behaviors when multiple cache poisoning requests target the same package simultaneously']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise
- T1499: Endpoint Denial of Service
- T1071: Application Layer Protocol

## Notes
Writeup deliberately omits exact header payloads to prevent immediate exploitation while the vulnerability remains unpatched. Discovery occurred during research tool development (Depi module testing), suggesting defensive research maturity. Vulnerability represents critical risk due to npm's central role in JavaScript ecosystem (2.1M packages, 17M developers, millions daily downloads). Temporary nature of poisoning (few minutes) suggests time-based cache TTL rather than permanent compromise. npm/Cloudflare's response and patch timeline not mentioned in article; responsible disclosure appears to have been followed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
