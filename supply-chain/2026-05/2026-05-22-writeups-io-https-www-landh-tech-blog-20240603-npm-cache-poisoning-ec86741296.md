# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Request Smuggling, Cache Key Manipulation
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the cache with specially crafted HTTP requests containing specific headers, causing legitimate package requests to return 404 errors. By manipulating the caching mechanism, attackers could render packages temporarily inaccessible to developers worldwide, potentially disrupting the JavaScript ecosystem's dependency resolution. The attack exploits subtle flaws in how the registry's caching systems (including Cloudflare) handle conflicting headers and cache key generation.

## Attack scenario (step by step)
1. Attacker identifies that npm registry's caching layer is vulnerable to header-based cache key confusion
2. Attacker crafts a malicious HTTP request with specific header combinations targeting a popular package (e.g., safe-regex-1.1.0.tgz)
3. The specialized headers trigger an error in the backend, causing the cache to store a 404 'Not Found' response with the poisoned cache key
4. Attacker makes a follow-up request without the malicious headers but with the same cache key parameter
5. The poisoned 404 response is served from cache to legitimate users requesting the package
6. Package becomes temporarily unavailable (lasting minutes to hours depending on cache TTL), disrupting builds and installations ecosystem-wide

## Root cause
The npm registry's caching infrastructure (Cloudflare/backend) fails to properly normalize or validate HTTP request headers when generating cache keys. Attackers can inject specific header combinations that cause the backend to generate error responses, which are then cached using a predictable cache key. The cache validation mechanism does not properly differentiate between legitimate requests and poisoned entries, allowing the malicious cached response to be served to subsequent requests.

## Attacker mindset
A sophisticated supply chain attacker could weaponize this vulnerability for maximum ecosystem disruption by poisoning caches of high-dependency packages at peak usage times, forcing widespread build failures. The attacker recognizes that npm is a critical infrastructure point and that temporary cache poisoning of even minutes can cascade into significant operational chaos across millions of dependent projects. The use of cache buster parameters demonstrates tactical awareness of avoiding unintended collateral damage while testing.

## Defensive takeaways
- Implement strict HTTP request validation and normalization for cache key generation to prevent header injection attacks
- Use whitelisting for headers that can influence cache behavior, rejecting or ignoring non-standard headers
- Add cache key diversification strategies that don't rely solely on URL parameters
- Implement cache response validation to ensure 404s and error responses undergo additional integrity checks before being cached
- Set aggressive cache TTLs for error responses (much shorter than success responses)
- Add monitoring and alerting for anomalous cache hit patterns, multiple 404s for the same package in short timeframes
- Conduct regular cache poisoning penetration tests using fuzzing techniques on header combinations
- Implement cache tags or secondary validation layers that verify package existence at cache retrieval time
- Document all headers that influence caching behavior and their expected values
- Consider implementing request signing or HMAC validation for package requests

## Variant hunting
Search for similar CPDoS vulnerabilities in other package registries (PyPI, Maven Central, RubyGems, Cargo, NuGet) using the same header-based cache key manipulation techniques. Test content delivery networks and caching layers (Cloudflare, Akamai, AWS CloudFront) for header normalization flaws. Investigate whether the vulnerability extends to metadata endpoints (/package.json) or if it's limited to tarball distribution. Examine if query parameters can be used similarly to headers for cache poisoning. Test for second-order effects where poisoned metadata could cause cascading failures.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1195.003 - Supply Chain Compromise: Compromised Software Dependencies
- T1561 - Disk Wipe
- T1499 - Service Exhaustion Denial of Service
- T1499.001 - Service Exhaustion Denial of Service: Direct Network Flood

## Notes
The writeup explicitly states the exact header combination was not disclosed at publication time due to active exploitability. The vulnerability affects not just npm but demonstrates systemic weakness in how package registries handle caching in CDN/reverse proxy layers. The temporary nature of the cache poisoning (minutes) suggests relatively short TTLs but still sufficient for disruption at scale. This vulnerability represents a critical supply chain risk affecting 17 million developers and 2.1 million packages. The research was conducted as part of Depi tool development during supply chain security assessment activities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
