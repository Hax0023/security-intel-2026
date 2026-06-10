# npm Registry Cache Poisoning Attack (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** npm/npmjs.com
- **Bounty:** Not explicitly stated
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service (DoS), Supply Chain Attack, HTTP Cache Manipulation, Caching Header Handling Flaw
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to manipulate caching headers to poison the cache with 404 responses, rendering packages temporarily inaccessible to legitimate users. By sending specially crafted HTTP requests with malicious headers, an attacker could prevent package downloads for the entire user base, potentially disrupting millions of developers and applications worldwide.

## Attack scenario (step by step)
1. Attacker identifies npm registry uses vulnerable caching mechanisms that don't properly validate header combinations
2. Attacker crafts malicious request with specific header series targeting a popular package (e.g., safe-regex-1.1.0.tgz)
3. Request is processed by backend systems which incorrectly cache a 404 Not Found response due to header manipulation
4. Attacker sends follow-up request without the malicious headers but with same cache key
5. Cloudflare caching layer serves the poisoned 404 response to all subsequent legitimate user requests
6. Package becomes inaccessible across npm ecosystem for several minutes until cache expires

## Root cause
Improper HTTP cache key computation and header validation in the npm registry's caching layer. The backend systems fail to properly distinguish between requests with different header combinations, allowing specially crafted headers to trigger 404 responses that get cached and served to legitimate users.

## Attacker mindset
Researcher mindset focused on supply chain security testing. They were developing a theoretical attack module (Depi) to test cache poisoning vulnerabilities in artifact repositories when they discovered the npm registry was vulnerable to the same attack vectors. This demonstrates that well-known security research techniques can expose flaws in critical infrastructure.

## Defensive takeaways
- Implement strict HTTP cache key validation that includes all request headers influencing response content
- Add header normalization and validation to reject requests with suspicious or malformed header combinations
- Configure shorter TTLs for error responses (404, 5xx) to minimize impact window of poisoned cache entries
- Implement request rate limiting per source IP to prevent rapid cache poisoning attempts
- Add monitoring for unusual header patterns and cache hit rates on error responses
- Use cache tags or versioning to allow rapid invalidation of poisoned entries
- Conduct regular cache poisoning penetration testing using CPDoS techniques
- Implement redundant caching layers with different validation logic to catch bypasses

## Variant hunting
Look for similar CPDoS vulnerabilities in other package registries (Maven Central, PyPI, RubyGems), container registries (Docker Hub, ECR), and CDN caching layers. Test header combinations with Vary header misconfigurations, X-Original-* headers, custom headers, and HTTP/2 pseudo-headers. Check for inconsistent header handling between origin servers and edge caches.

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise
- T1498: Network Denial of Service
- T1557: Man-in-the-Middle
- T1199: Trusted Relationship

## Notes
The vulnerability was disclosed responsibly with npm prior to publication. The exact header combination remains undisclosed to prevent active exploitation. The cached 404 responses were temporary (minutes-long TTL), limiting but not eliminating impact. This vulnerability is particularly severe due to npm's criticality in the JavaScript ecosystem (2.1M packages, 17M developers, millions of daily downloads). The researchers discovered this while developing security testing tools, highlighting the value of proactive supply chain security research.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
