# npm Registry Cache Poisoning Vulnerability (CPDoS Attack)

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** npm Registry (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Cache Poisoning, Denial of Service (DoS), HTTP Response Splitting, Cache Key Manipulation, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to poison the caching system with crafted HTTP headers, causing legitimate package requests to return 404 Not Found responses. By manipulating cache keys through specially crafted headers, an attacker could temporarily render critical npm packages inaccessible to millions of developers worldwide, effectively disrupting the JavaScript supply chain.

## Attack scenario (step by step)
1. Attacker crafts malicious HTTP request with specially crafted headers targeting a specific npm package (e.g., safe-regex-1.1.0.tgz)
2. Request is sent to registry.npmjs.org with cache buster parameter and custom headers that trigger backend caching errors
3. npm's caching layer incorrectly stores a 404 Not Found response for the package in its cache with a vulnerable cache key
4. Attacker sends subsequent request without the malicious headers but using the same cache key
5. Cached 404 response is served to legitimate users requesting the same package, rendering it unavailable
6. Package remains inaccessible for several minutes until cache expires, causing widespread availability issues across dependent projects

## Root cause
The npm registry's HTTP caching mechanisms failed to properly differentiate between legitimate requests and malicious ones when processing certain header combinations. The cache key generation logic was vulnerable to manipulation, allowing attackers to poison cached responses by sending specially crafted HTTP headers that triggered backend errors. The system stored error responses (404) in cache without properly validating the request legitimacy, and subsequent requests using the same cache key would retrieve the poisoned response.

## Attacker mindset
A sophisticated supply chain attacker recognizing that npm is a critical infrastructure dependency for millions of developers. Rather than targeting individual packages, the attacker exploits caching infrastructure to create widespread denial of service. The attacker likely aims to maximize disruption by targeting popular packages, potentially causing cascading failures across the JavaScript ecosystem. The use of cache busters in initial reconnaissance suggests careful, methodical exploitation to avoid immediate detection.

## Defensive takeaways
- Implement strict cache key validation to prevent header-based cache key manipulation and ensure consistent cache behavior
- Add request validation logic to reject or sanitize HTTP headers that could trigger unexpected backend errors
- Implement cache poisoning detection mechanisms that monitor for unusual patterns of 404 responses on previously available packages
- Use separate cache keys for different request variants and validate header consistency
- Implement rate limiting on package retrieval requests to limit CPDoS attack effectiveness
- Add monitoring and alerting for sudden spikes in 404 responses for valid packages
- Conduct regular security audits of caching infrastructure and HTTP header handling logic
- Implement cache bypass mechanisms for critical packages or during detected attacks

## Variant hunting
['Test other header combinations (Accept-Encoding, User-Agent variations, custom headers) against caching mechanisms', 'Probe for similar vulnerabilities in other package registries (PyPI, Maven Central, crates.io, NuGet)', 'Investigate whether request smuggling techniques could be combined with cache poisoning for greater impact', 'Test if query parameter manipulation combined with headers creates additional cache key variations', 'Examine CDN caching behavior (Cloudflare in this case) for similar bypasses at edge level', 'Research whether authentication bypass could be combined with cache poisoning to affect private packages']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (npm registry vulnerability exploitation)
- T1195 - Supply Chain Compromise (npm package registry attack)
- T1195.003 - Supply Chain Compromise: Compromised Software Supply Chain (cache poisoning attack)
- T1499 - Endpoint Denial of Service (CPDoS rendering packages unavailable)
- T1557 - On-Path Attack (HTTP cache poisoning via header manipulation)
- T1047 - Windows Management Instrumentation (not directly applicable, but relevant for lateral movement post-compromise)

## Notes
This vulnerability represents a critical threat to the JavaScript ecosystem given npm's massive scale (2.1M packages, 17M developers, millions daily downloads). The attack is particularly insidious because it leverages infrastructure expected to be trustworthy. The temporary nature of cache poisoning (lasting minutes) makes detection challenging but also limits persistent damage. The researchers responsibly disclosed the vulnerability without publishing the exact header combination needed to exploit it. The vulnerability likely stems from improper handling of HTTP caching directives or edge case interactions between headers and cache key generation. This incident highlights how supply chain vulnerabilities often exist not in code itself but in distribution infrastructure.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
