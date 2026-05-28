# NPM Registry Cache Poisoning Attack (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** npm/npmjs.com
- **Bounty:** Not specified
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, Supply Chain Attack, HTTP Request Smuggling, Cache Key Collision
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to poison the caching system by sending specially crafted HTTP requests with specific headers. An attacker can manipulate the cache to serve '404 Not Found' responses for legitimate packages, rendering them temporarily inaccessible to millions of developers worldwide. This represents a critical supply chain risk affecting the entire JavaScript ecosystem.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP request with specific header combinations targeting a popular npm package (e.g., safe-regex-1.1.0.tgz)
2. Request includes a cache buster parameter and custom headers that trigger backend cache processing errors
3. The npm registry's caching layer (Cloudflare or internal) stores an incorrect '404 Not Found' response associated with the package
4. Attacker sends follow-up requests without the malicious headers but with the same cache key, retrieving the poisoned cached response
5. Legitimate users requesting the same package receive cached '404 Not Found' responses instead of the actual package
6. Package becomes temporarily inaccessible, causing build failures and denying service to dependent projects

## Root cause
The npm registry's caching mechanism improperly handles HTTP header combinations in cache key generation. Specific headers trigger backend errors that result in '404 Not Found' responses being cached with incorrect TTL or cache key collision rules. The cache layer fails to differentiate between error responses caused by malicious requests and legitimate unavailability, allowing poisoned responses to be served to subsequent legitimate requests.

## Attacker mindset
Opportunistic researcher discovering a high-impact vulnerability during security testing of artifact repositories. The attacker recognizes the potential for widespread disruption across the JavaScript ecosystem given npm's critical role. The discovery appears somewhat accidental during module development, suggesting the attack vector wasn't well-known. The attacker demonstrates responsible disclosure by not releasing full technical details while the vulnerability remained exploitable.

## Defensive takeaways
- Implement strict cache key normalization that canonicalizes all variations of request headers before cache lookup
- Separate error responses (4xx, 5xx) from success responses with distinct TTL policies and cache segregation
- Add request validation and rate limiting on registry endpoints to detect patterns of malicious cache poisoning attempts
- Monitor cache hit rates and error response patterns for anomalies indicating active poisoning attacks
- Implement cache coherence mechanisms that validate cached responses match expected content hashes
- Add cryptographic signatures to package metadata to detect cache tampering
- Deploy WAF rules to block requests with suspicious header combinations known to trigger cache errors
- Establish redundant caching layers with independent validation to prevent single-point cache poisoning
- Implement request logging and forensic capabilities to identify and remediate poisoned cache entries
- Conduct regular security audits of caching infrastructure and HTTP header handling

## Variant hunting
Search for similar cache poisoning vulnerabilities in: other package registries (PyPI, RubyGems, Maven Central), CDN configurations, API gateways using shared caching layers, proxy servers, and load balancers. Test variations using different HTTP methods, content-type headers, range requests, and protocol version mismatches. Investigate whether the vulnerability extends to poisoning specific package versions or metadata endpoints. Check if attackers can poison download redirects or integrity hash endpoints.

## MITRE ATT&CK
- T1195 Supply Chain Compromise
- T1195.003 Supply Chain Compromise: Compromised Software Dependencies
- T1190 Exploit Public-Facing Application
- T1499 Endpoint Denial of Service
- T1499.004 Application Exhaustion Flood
- T1565 Data Manipulation
- T1565.002 Data from Information Repositories

## Notes
The vulnerability was discovered during development of Depi, a research tool for testing cache poisoning on artifact repositories. Researchers withheld specific header combinations to prevent active exploitation at time of publication. The attack requires repeated requests to maintain cache poisoning as responses were temporarily cached (minutes duration). The npm registry serves 2.1M+ packages to 17M+ developers, making this a critical supply chain risk. Cloudflare (CF-Ray header) appears to be handling caching, indicating the vulnerability may be in upstream configuration or Cloudflare's cache key derivation. The 'Vary: Accept-Encoding' header suggests the cache key generation is vulnerable to header manipulation. No explicit bounty amount mentioned; typically npm/GitHub would offer substantial rewards for such critical vulnerabilities.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
