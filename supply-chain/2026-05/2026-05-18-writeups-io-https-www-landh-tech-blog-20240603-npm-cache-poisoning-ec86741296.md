# NPM Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** npm registry (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Cache Desynchronization, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the cache with specially crafted HTTP requests containing specific headers, causing legitimate package requests to return 404 errors. By manipulating the registry's caching system, an attacker could temporarily render packages inaccessible to millions of developers worldwide, with minimal effort required to re-poison the cache. This vulnerability exposes the fragility of the JavaScript software supply chain and affects over 2.1 million packages and 17 million developers.

## Attack scenario (step by step)
1. Attacker identifies that registry.npmjs.org uses a caching layer vulnerable to cache key manipulation through specific HTTP headers
2. Attacker crafts a malicious GET request to a popular package (e.g., /safe-regex/-/safe-regex-1.1.0.tgz) with specially crafted headers that trigger backend errors
3. The error response (404 Not Found) gets cached by the CDN/caching system with a cache key derived from the malicious headers
4. Attacker sends a follow-up request without the malicious headers but with the same cache parameters, retrieving the poisoned 404 response
5. Legitimate developers requesting the same package receive the cached 404 error, unable to download the dependency
6. Attacker can repeatedly re-poison the cache every few minutes to maintain the denial of service condition for critical packages

## Root cause
The npm registry's caching system fails to properly normalize HTTP headers when generating cache keys, allowing attackers to create multiple cache entries for the same resource. The backend system processes specially crafted headers in a way that generates error responses, which are then cached. The cache layer does not distinguish between legitimate requests and malicious ones, storing and serving poisoned content to subsequent users.

## Attacker mindset
A sophisticated supply chain attacker would recognize this vulnerability as an opportunity for mass disruption. Rather than poisoning specific packages for individual targets, they could systematically target popular packages (lodash, react, express, etc.) to cause widespread development disruption. The low effort-to-impact ratio makes this attractive for both destructive actors seeking to disrupt the JavaScript ecosystem and extortionists demanding payment to 'unpoisoned' packages.

## Defensive takeaways
- Implement strict HTTP header validation and normalization before cache key generation
- Use separate cache keys that exclude user-supplied headers or standardize header handling
- Implement cache key pinning to prevent cache poisoning from variant requests
- Add cache response validation to prevent caching of error responses from malformed requests
- Implement rate limiting and request fingerprinting to detect cache poisoning attempts
- Use cache busting tokens or version hashes that cannot be manipulated by attackers
- Monitor cache hit ratios and error response patterns for anomalies indicating poisoning attempts
- Implement security headers like Cache-Control: no-cache for sensitive resources
- Develop incident response procedures for rapid cache invalidation in case of poisoning
- Add redundancy and failover mechanisms to prevent single cache layer compromise from affecting all users

## Variant hunting
Hunt for similar CPDoS vulnerabilities in other major package registries (PyPI, RubyGems, Maven Central, NuGet). Test other CDN-fronted registries for cache key desynchronization. Investigate whether specific header combinations work across different caching layers (Cloudflare, Akamai, Varnish). Test for cache poisoning on package metadata endpoints, not just tarballs. Examine whether query parameters, custom headers, or HTTP methods can be abused to create alternate cache keys for legitimate packages.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise
- T1195.001: Compromise Software Dependencies and Development Tools
- T1499: Endpoint Denial of Service
- T1499.004: HTTP Flood
- T1556: Modify Authentication Process
- T1583: Acquire Infrastructure

## Notes
The researchers deliberately withheld the exact header combination needed to trigger the vulnerability, showing responsible disclosure. The temporary nature of the cache (minutes) means continuous re-poisoning would be required, but this is easily automatable. The use of a cache buster parameter in the proof-of-concept demonstrates the researchers' ethical approach to testing. npm's reliance on Cloudflare for caching may indicate the vulnerability lies in cache key handling at the CDN layer rather than npm's infrastructure. This vulnerability class (CPDoS) is relatively new and may affect other major infrastructure. The article's publication date (June 3, 2024) and note that it 'is still exploitable at the time of writing' suggests the vulnerability had not been fully patched when publicly disclosed.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
