# Cache Poisoning Denial of Service (CPDoS) Attack on npm Registry

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** npm Registry (npmjs.org)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Header Manipulation, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service vulnerability in the npm registry that could render JavaScript packages inaccessible to millions of developers. By sending specially crafted HTTP requests with specific header combinations, an attacker could poison the registry's cache to serve 404 responses for legitimate packages. This supply chain attack could disrupt the entire JavaScript ecosystem, affecting 17+ million developers relying on 2.1+ million packages.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP GET request to a target package on registry.npmjs.org with specific header combinations and a unique cache-busting parameter
2. The specially crafted headers trigger a vulnerability in the backend caching system, causing it to generate and cache an erroneous 404 'Not Found' response
3. Attacker sends a follow-up request without the malicious headers but using the same cache key to retrieve the poisoned cached response
4. The npm registry's cache serves the poisoned 404 response to legitimate users attempting to download the targeted package
5. Developers worldwide experience installation failures when attempting to install the affected package via npm install
6. The poisoned cache persists for several minutes, allowing widespread disruption before expiration and natural cache invalidation

## Root cause
The npm registry's caching system (likely Cloudflare) fails to properly validate and differentiate HTTP requests containing specific header combinations, allowing attackers to manipulate cache key generation and poison the cache with error responses that are then served to legitimate requests.

## Attacker mindset
A sophisticated attacker could leverage this vulnerability for widespread supply chain disruption by targeting popular packages, causing denial of service to dependent projects and potentially creating cascading failures across the JavaScript ecosystem. The attack requires minimal resources and can be automated to target multiple packages simultaneously.

## Defensive takeaways
- Implement strict cache key validation that properly normalizes and validates all HTTP headers to prevent header-based cache key manipulation
- Segregate cache entries based on request legitimacy indicators and implement secondary validation before serving cached error responses
- Deploy request signing or authentication mechanisms for package registry access to prevent untrusted header injection
- Implement cache response sanitization to ensure error responses cannot be cached or have very short TTLs
- Monitor for unusual header combinations and cache poisoning patterns in real-time
- Establish multi-layer caching with validation at each tier to prevent single-point failures
- Consider implementing Vary headers more strictly to isolate cache entries from potentially malicious request variations
- Regular security audits of caching logic, particularly around edge cases in HTTP header handling

## Variant hunting
['Test other package registries (PyPI, Maven Central, RubyGems, Cargo) for similar CPDoS vulnerabilities using variant header combinations', 'Investigate HTTP/2 and HTTP/3 specific header handling and multiplexing to identify cache poisoning vectors', 'Research cache key normalization in different CDN providers (Cloudflare, Akamai, AWS CloudFront) for similar flaws', 'Test combining multiple HTTP headers with different encoding schemes to bypass cache key validation', 'Explore using Content-Range headers, Accept-Encoding variants, and other rarely-normalized headers for cache manipulation', 'Investigate private registry solutions built on similar caching architectures', 'Test conditional request headers (If-Match, If-Modified-Since) for cache poisoning potential']

## MITRE ATT&CK
- T1195.003 - Supply Chain Compromise: Compromise Software Repository
- T1499.004 - Denial of Service: HTTP Flood
- T1190 - Exploit Public-Facing Application
- T1557 - Adversary-in-the-Middle
- T1200 - Traffic Signaling

## Notes
The researchers responsibly withheld the exact header combination details to prevent immediate exploitation. The vulnerability was discovered during development of 'Depi', a supply chain security testing tool. The temporary nature of cache poisoning (minutes duration) suggests possible TTL-based cache invalidation but still allows significant disruption window. The attack is trivial to automate and scale across multiple packages. The researchers note this vulnerability highlights critical fragility in the JavaScript ecosystem's supply chain infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
