# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln types:** Cache Poisoning, Denial of Service, Supply Chain Attack, HTTP Cache Manipulation
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to manipulate the caching system into serving 404 Not Found responses for legitimate packages. By crafting specialized HTTP requests with specific headers, attackers could render packages temporarily inaccessible to millions of developers worldwide, potentially disrupting the entire JavaScript ecosystem.

## Attack scenario (step by step)
1. Attacker identifies that npm registry's caching system improperly handles certain HTTP header combinations
2. Attacker crafts malicious request with specific header combination and query parameter targeting a popular package (e.g., safe-regex-1.1.0.tgz)
3. First request triggers backend error, causing cache to store '404 Not Found' response with poisoned state
4. Attacker sends follow-up request without the trigger headers but same cache key to retrieve poisoned response
5. Legitimate users requesting the same package receive cached 404 error instead of actual package content
6. Package remains inaccessible for several minutes until cache expires, disrupting downstream builds and deployments

## Root cause
The npm registry's caching layer (likely Cloudflare-based) incorrectly processes HTTP header combinations and cache key generation, allowing attackers to inject error responses into the cache that persist across different request variations. The cache does not properly validate or differentiate between requests with and without trigger headers when generating cache keys.

## Attacker mindset
Supply chain sabotage through denial of service targeting the most critical JavaScript package repository. Attacker seeks to demonstrate ecosystem fragility, potentially for research purposes, extortion, or competitive advantage. The use of query parameters as 'cache busters' suggests responsible disclosure awareness while still proving exploitability at scale.

## Defensive takeaways
- Implement strict cache key generation that accounts for all request variations and ignores attacker-controlled headers
- Validate error responses before caching, ensure 404s are only cached when definitively confirmed
- Add request rate limiting and anomaly detection for suspicious header combinations targeting multiple packages
- Implement cache poisoning detection by monitoring cache hit patterns and response consistency
- Use cache tags/purging mechanisms to quickly invalidate suspicious responses during active attack
- Separate caching policies for success vs error responses with shorter TTL for errors
- Implement request signing or validation to prevent header manipulation attacks
- Monitor for coordinated requests targeting multiple packages or unusual access patterns

## Variant hunting
['Test other package registries (PyPI, RubyGems, Composer, Maven Central) for similar CPDoS vulnerabilities in caching layers', 'Investigate whether similar header-based cache poisoning works on CDN providers (Cloudflare, Akamai, AWS CloudFront)', 'Explore other HTTP headers (Accept, Accept-Encoding, X-Forwarded-*, custom headers) for cache confusion attacks', 'Test if response header manipulation can poison caches differently (e.g., Cache-Control header injection)', 'Examine if the vulnerability extends to source archive URLs (.zip, .tar.gz variants) or metadata endpoints', "Probe for CPDoS on npm's package metadata endpoint (/package-name/latest vs specific versions)", 'Test whether the attack can be chained with other vulnerabilities (authentication bypass, path traversal) for amplification']

## MITRE ATT&CK
- T1190
- T1195
- T1195.003
- T1499.004
- T1657

## Notes
Researchers explicitly withheld technical details (exact header combinations) to prevent widespread exploitation during coordinated disclosure. The temporary cache duration (minutes) limits immediate impact but demonstrates proof of concept. The discovery was made during development of Depi, a supply chain security testing tool, suggesting this may be part of broader security research. Cloudflare infrastructure is involved as the caching layer. The vulnerability affects 2.1M packages and 17M developers, making this a critical ecosystem-wide risk despite seemingly targeted exploitation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
