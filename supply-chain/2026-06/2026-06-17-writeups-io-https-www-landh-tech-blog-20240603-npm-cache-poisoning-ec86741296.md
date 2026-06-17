# Cache Poisoning Denial of Service (CPDoS) Attack on npm Registry

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** CRITICAL
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Cache Desynchronization, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to manipulate caching headers and poison the cache with 404 responses, rendering packages temporarily inaccessible to millions of developers. By crafting specially-formed requests with specific headers, attackers can cause the registry to cache 'Not Found' responses that are served to subsequent legitimate requests, disrupting the JavaScript ecosystem's supply chain.

## Attack scenario (step by step)
1. Attacker identifies that npm registry's caching system is vulnerable to HTTP header manipulation
2. Attacker crafts a malicious HTTP GET request to a package URL (e.g., safe-regex-1.1.0.tgz) containing specially crafted headers that trigger backend cache errors
3. The request includes a unique cache-buster parameter to avoid affecting legitimate users during testing
4. npm's backend incorrectly processes the request and caches a 404 'Not Found' response with a specific cache key
5. Attacker sends a follow-up request without the malicious headers but with matching cache key parameters
6. Legitimate users attempting to download the package receive the poisoned 404 response from cache, causing package unavailability for minutes

## Root cause
npm registry's HTTP caching infrastructure fails to properly validate and differentiate between requests with malicious headers versus legitimate requests. The cache key generation logic does not account for request header variations, allowing attackers to poison cache entries by sending requests with specific header combinations that trigger 404 responses in the backend. The cache treats error responses identically to legitimate responses, storing and serving them to subsequent requests.

## Attacker mindset
Sophisticated supply chain attacker seeking to disrupt JavaScript ecosystem at scale. Researchers approached this systematically through theoretical attack vector testing during development of Depi security tool. Attacker recognizes that npm's centrality (2.1M packages, 17M developers, millions of daily downloads) makes it an ideal target for maximum ecosystem disruption. Temporary cache duration suggests attacker would need repeated requests to sustain DoS, indicating goal of broader service degradation rather than single-package disruption.

## Defensive takeaways
- Implement strict cache key generation that excludes request headers which should not affect cacheability of responses
- Validate and sanitize all HTTP headers before processing; reject requests with unexpected or malicious header combinations
- Implement separate cache layers for error responses with shorter TTLs and stricter validation
- Use cache-control directives properly to prevent caching of error responses or use private/no-cache for sensitive endpoints
- Monitor cache hit rates and 404 responses for anomalous patterns indicating poisoning attacks
- Implement request rate limiting and signature-based detection for repeated requests with abnormal header patterns
- Test caching behavior with security-focused tools and fuzzing against HTTP header variations
- Maintain detailed logging of cache poisoning attempts for forensic analysis and incident response

## Variant hunting
Hunt for similar cache poisoning vulnerabilities in other package registries (PyPI, Maven Central, RubyGems, NuGet). Test alternative header combinations (Accept-Encoding, X-Forwarded-For, Range, If-Modified-Since) against npm and other CDN-backed registries. Investigate whether the vulnerability affects metadata endpoints (.json files) in addition to package archives (.tgz files). Test if cache poisoning can be combined with header injection to serve malicious content instead of 404s. Examine whether CloudFlare's caching layer or origin server is the vulnerable component. Test for long-term cache key persistence or whether cache poisoning can achieve permanent poisoning through specific header sequences.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (npm registry)
- T1195 - Supply Chain Compromise
- T1195.001 - Compromise Software Repository
- T1496 - Resource Hijacking (availability impact)
- T1561 - Disk Wipe (functional equivalent via DoS)
- T1565.002 - Data from Information Repositories (integrity manipulation)

## Notes
Vulnerability was discovered during development of Depi security testing tool's cache poisoning research module. Authors deliberately withheld specific header sequences from public disclosure to prevent immediate exploitation. Researchers used cache-buster parameters during testing to avoid affecting legitimate users. Attack is temporary (minutes-long cache duration) requiring repeated requests to maintain DoS. Affects registry.npmjs.org which is fronted by Cloudflare (evident from CF-Ray response header). This represents a critical supply chain risk given npm's centrality to JavaScript development. Disclosure approach balanced public interest with ecosystem safety by alerting npm while not publishing exploitable details.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
