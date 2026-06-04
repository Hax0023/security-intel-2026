# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** npm/npmjs.com
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Header Manipulation, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry's caching infrastructure, allowing attackers to poison the cache with malicious 404 responses for legitimate packages. By crafting specially designed HTTP requests with specific headers, attackers could render packages temporarily inaccessible to millions of developers, potentially disrupting the entire JavaScript supply chain.

## Attack scenario (step by step)
1. Attacker develops a CPDoS module as part of security research to test cache poisoning vulnerabilities in artifact repositories
2. Attacker discovers npm registry (registry.npmjs.org) is vulnerable to cache poisoning through improper header handling
3. Attacker crafts a malicious HTTP GET request containing specific headers and cache-busting parameters targeting a legitimate package like 'safe-regex-1.1.0.tgz'
4. The specially crafted request triggers an error in npm's backend caching system, causing it to cache a 404 'Not Found' response for the package
5. Attacker sends follow-up requests without the malicious headers but with the same cache key, retrieving the poisoned 404 response from cache
6. Subsequent legitimate user requests for the package receive the cached 404 response, making the package unavailable despite it existing on the registry

## Root cause
Improper HTTP cache key generation in npm's caching infrastructure. The registry's backend systems failed to properly differentiate requests based on specific HTTP headers, allowing attackers to manipulate cache entries. The caching layer did not properly validate or segregate responses based on request headers, enabling poisoned 'Not Found' responses to be cached and served to legitimate users.

## Attacker mindset
An attacker would recognize the npm registry as a high-value target due to its critical role in the JavaScript ecosystem. With 2.1 million packages and 17 million developers relying on it, poisoning a single package's cache creates widespread disruption. The attack requires minimal effort once the vulnerability is identified—simply crafting specific HTTP headers—making it an attractive denial-of-service vector. The temporary nature of poisoning (minutes-long TTL) could enable repeated attacks causing persistent availability issues. Targeting widely-used packages could maximize impact across the supply chain.

## Defensive takeaways
- Implement strict HTTP cache key generation that properly includes all relevant headers and parameters to prevent cache poisoning
- Validate and sanitize all HTTP headers before using them in cache operations
- Use cache versioning and content integrity checks (e.g., ETags, checksums) to detect poisoned responses
- Implement rate limiting and monitoring for unusual request patterns targeting package endpoints
- Add comprehensive logging of cache operations to detect poisoning attempts
- Conduct regular security audits of caching infrastructure, specifically testing CPDoS vectors as described in PortSwigger research
- Implement fallback mechanisms to verify package availability if cache hits fail
- Consider short TTLs for package metadata and artifacts, and implement automatic cache invalidation for critical packages
- Establish incident response procedures for detected cache poisoning attempts
- Monitor for simultaneous access failures of the same package across regions as an indicator of cache poisoning

## Variant hunting
Security researchers should test other package registries (Artifactory, Nexus, PyPI, RubyGems, Maven Central) for similar CPDoS vulnerabilities in their caching layers. Look for variations exploiting different HTTP headers (Accept-Encoding, Accept-Language, X-Forwarded-* headers) that might be cached improperly. Test cache poisoning against npm's metadata endpoints, package.json files, and registry search functionality. Investigate whether attackers could poison caches to serve malicious package content rather than just 404 responses. Research whether CDN-level caching (Cloudflare) can be exploited differently than the origin cache.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1195 - Supply Chain Compromise
- T1195.001 - Compromise Software Dependencies and Development Tools
- T1498 - Network Denial of Service
- T1556 - Modify Authentication Process

## Notes
The researchers responsibly withheld specific header details to prevent active exploitation while the vulnerability remained unfixed. The temporary cache poisoning (minutes-long TTL) suggests the vulnerability may require repeated attacks for sustained disruption. The discovery was made during development of 'Depi', a supply chain security testing tool, indicating value of proactive vulnerability research frameworks. The writeup lacks information on whether npm was notified, patching timeline, or whether the vulnerability has been remediated. The use of cache-busting parameters ('lupin_E7A812DE-E09A-4906-A9E3-530E54AAEB41=cpdos_test') during testing demonstrates responsible disclosure practices to avoid poisoning production caches during research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
