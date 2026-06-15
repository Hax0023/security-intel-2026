# NPM Registry Cache Poisoning Attack (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** npm/npmjs.com
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Cache Poisoning, Denial of Service (DoS), HTTP Response Splitting, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the cache with specially crafted HTTP requests containing specific headers, causing legitimate package requests to return 404 errors. The attack manipulates how web caches store and serve content by exploiting flaws in cache key generation and response handling, potentially rendering packages inaccessible to millions of developers worldwide.

## Attack scenario (step by step)
1. Attacker identifies that npm registry uses vulnerable caching mechanisms that can be manipulated via specific HTTP headers
2. Attacker crafts a malicious request with specially crafted headers and a cache buster parameter targeting a specific package version (e.g., safe-regex-1.1.0.tgz)
3. The vulnerable backend caches an error response (404 Not Found) using a cache key that doesn't properly account for the malicious headers
4. Attacker sends a follow-up request without the special headers but with the same cache key to retrieve the poisoned cached response
5. Subsequent legitimate user requests for the same package receive the cached 404 response, unable to download the package
6. The attack requires repetition every few minutes as cached responses are temporary, creating sustained denial of service

## Root cause
The npm registry's caching system (likely Cloudflare) fails to properly differentiate cache keys when processing requests with non-standard headers. The backend generates error responses that are cached with insufficient cache key variation, allowing attackers to associate error responses with legitimate package requests. The vulnerability stems from improper HTTP header handling and cache key generation that doesn't account for all request variations.

## Attacker mindset
An attacker would recognize this as a high-impact supply chain attack vector affecting millions of developers. The motivation would be to cause widespread disruption, demand ransom, conduct competitive sabotage, or demonstrate ecosystem fragility. The attacker would appreciate that repeated exploitation is straightforward due to the temporary cache nature, allowing sustained attacks with minimal effort.

## Defensive takeaways
- Implement strict cache key generation that includes all potentially security-relevant HTTP headers
- Add request validation to reject or normalize non-standard headers before processing
- Implement cache poisoning detection mechanisms that identify sudden spikes in 404 responses for previously available packages
- Use cache headers (Cache-Control, Vary) explicitly to control what variations are cached
- Implement rate limiting on requests from single sources targeting package downloads
- Establish monitoring for cache hit ratios and error rate anomalies that could indicate poisoning
- Add cryptographic verification of cached responses before serving them
- Implement separate caching strategies for error responses vs. successful responses
- Conduct regular security audits of caching infrastructure with focus on HTTP protocol edge cases
- Establish incident response procedures for cache poisoning attacks affecting critical infrastructure

## Variant hunting
Search for similar cache poisoning vulnerabilities in: other package registries (PyPI, RubyGems, Maven Central, Cargo), CDN configurations, API gateways, reverse proxies (nginx, Apache), and edge caching services. Test cache key generation with varied header combinations (Host, X-Forwarded-*, Accept-Encoding, User-Agent variations). Check for CPDoS on other npm endpoints (package metadata, tarball downloads). Investigate whether the vulnerability affects package.json metadata responses differently than tarball responses.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1195.001 - Compromise Software Repository
- T1499 - Endpoint Denial of Service
- T1499.004 - HTTP Flood
- T1047 - Windows Management Instrumentation

## Notes
The researchers responsibly disclosed but did not reveal the exact header combination needed to trigger the vulnerability. The attack has temporary effect (cached responses expire in minutes), suggesting the registry has some mitigation in place but not complete. This demonstrates that even the most critical infrastructure in major ecosystems can have fundamental security flaws. The vulnerability was discovered during security research rather than in-the-wild exploitation, highlighting the importance of proactive supply chain security testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
