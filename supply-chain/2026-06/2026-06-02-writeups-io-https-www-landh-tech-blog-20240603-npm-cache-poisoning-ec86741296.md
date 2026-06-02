# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** npm (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, Supply Chain Attack, HTTP Cache Manipulation
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the caching system by sending specially crafted HTTP requests with specific headers. This causes the registry to cache 404 Not Found responses for legitimate packages, rendering them temporarily inaccessible to all users and potentially disrupting the JavaScript ecosystem which serves 2.1 million packages to 17 million developers.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP GET request to registry.npmjs.org with specially designed headers that trigger backend caching errors
2. The malicious request targets a specific package file (e.g., safe-regex-1.1.0.tgz) and includes headers that cause the caching system to generate a 404 Not Found response
3. The npm registry caches this fraudulent 404 response with a cache key derived from the request
4. Attacker sends a follow-up request without the malicious headers but with the same cache key, retrieving the poisoned 404 response
5. All subsequent legitimate user requests for the targeted package receive the cached 404 response, making the package temporarily unavailable
6. Package becomes inaccessible for minutes until the temporary cache expires, causing build failures and deployment disruptions across dependent projects

## Root cause
The npm registry's caching infrastructure (likely Cloudflare-based) incorrectly processes specific HTTP header combinations, storing error responses in shared caches without proper cache key differentiation. The caching mechanism fails to distinguish between legitimate and maliciously-crafted requests, allowing attackers to manipulate how responses are cached and served to other users.

## Attacker mindset
Supply chain sabotage: An attacker seeking maximum disruption could target high-dependency packages used across thousands of projects. The low barrier to entry (simple HTTP requests) combined with ecosystem-wide impact makes this an attractive vector for motivated threat actors. The temporary nature of the cache poisoning allows repeated attacks with minimal detection risk.

## Defensive takeaways
- Implement strict header validation and normalization before caching decisions to prevent header-based cache poisoning
- Use separate cache keys for different request origins and exclude attacker-controllable headers from cache key generation
- Implement rate limiting and anomaly detection on cache-related endpoints to identify CPDoS attack patterns
- Add cache poisoning detection monitoring that alerts on unusual 404 patterns for previously available packages
- Consider implementing signed cache responses or integrity verification for critical package registry operations
- Segregate caches by user/request type to prevent cross-user cache poisoning attacks
- Regular security audits of caching layer configuration and HTTP header handling
- Implement request origin validation and filtering at the CDN/edge level

## Variant hunting
Search for similar CPDoS vulnerabilities in other major package registries (PyPI, Maven Central, RubyGems, NuGet). Test cache poisoning against header combinations in other npm endpoints (metadata endpoints, search APIs). Investigate whether the vulnerability extends to other HTTP methods (PUT, POST) or content types. Research whether malicious cache poisoning can redirect content rather than just deny it.

## MITRE ATT&CK
- T1195 - Supply Chain Compromise
- T1195.001 - Compromise Software Dependencies
- T1561 - Disk Wipe
- T1499 - Denial of Service
- T1499.004 - Application Exhaustion Flood
- T1557 - Adversary-in-the-Middle
- T1036 - Masquerading

## Notes
The researchers explicitly withheld the exact header combination that triggers the vulnerability to prevent exploitation during disclosure. The vulnerability was discovered during development of 'Depi', a supply chain security testing tool. The cache poisoning is temporary (lasts minutes) but repeatable, allowing continuous disruption. The npm registry serves as critical infrastructure for the JavaScript ecosystem, making this a systemic risk to the entire platform. The researchers disclosed this responsibly to npm/Cloudflare prior to public disclosure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
