# npm Registry Cache Poisoning Attack (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** npm Registry (npmjs.com)
- **Bounty:** Not specified in writeup
- **Severity:** Critical
- **Vuln types:** Cache Poisoning, Denial of Service, Supply Chain Attack, HTTP Header Manipulation
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
Researchers discovered a Cache Poisoning Denial of Service (CPDoS) vulnerability in the npm registry that allows attackers to manipulate caching systems into serving 404 responses for legitimate packages. By crafting specially designed HTTP requests with specific headers, attackers could temporarily render packages inaccessible to millions of developers, disrupting the JavaScript ecosystem's software supply chain.

## Attack scenario (step by step)
1. Attacker identifies that npm registry's caching layer is vulnerable to header-based cache poisoning attacks
2. Attacker sends a specially crafted GET request to a specific package (e.g., safe-regex-1.1.0.tgz) containing malicious headers and a unique cache buster parameter
3. The backend caching system processes the request incorrectly and caches a 404 'Not Found' response associated with the package
4. Attacker sends a follow-up request without the malicious headers but with the same cache key
5. The poisoned cache serves the 404 response to legitimate users attempting to download the package
6. Package remains inaccessible for several minutes until the temporary cache expires, causing denial of service to dependent projects

## Root cause
The npm registry's caching infrastructure fails to properly handle or normalize HTTP headers when determining cache keys. Certain header combinations trigger backend errors that are incorrectly cached as legitimate 404 responses. The caching mechanism does not adequately distinguish between valid package requests and malformed requests containing manipulated headers, allowing attackers to pollute the cache with error responses.

## Attacker mindset
Adversary seeks to disrupt the JavaScript ecosystem by targeting critical infrastructure (npm registry). The attack demonstrates sophisticated understanding of web caching mechanics and HTTP protocol quirks. The attacker recognizes that poisoning a widely-used package repository could have cascading effects across millions of dependent projects, making this a high-impact supply chain attack vector. The temporary nature of the cache requires repeated exploitation but still provides significant disruption window.

## Defensive takeaways
- Implement strict cache key normalization that accounts for all request parameters and headers to prevent cache collision attacks
- Separate error responses from valid responses in caching logic with different cache durations and validation mechanisms
- Sanitize and validate HTTP headers before using them in cache key calculations
- Implement request integrity checks to detect and reject malformed header combinations
- Add monitoring for anomalous request patterns that could indicate cache poisoning attempts
- Use cache busting strategies that include request signature validation
- Implement per-package availability verification before serving cached responses
- Consider implementing rate limiting on package requests from suspicious user agents
- Establish clear separation between cache layers (CDN vs origin) with independent validation
- Conduct regular security audits of caching infrastructure using known CPDoS attack vectors

## Variant hunting
['Test other header combinations that might trigger similar backend errors in npm or other package registries', 'Investigate whether other package managers (PyPI, Maven Central, RubyGems) use similar caching patterns vulnerable to CPDoS', 'Examine if authentication headers can be manipulated to poison cached responses for private packages', 'Test whether query parameters in addition to headers can be combined to expand the attack surface', 'Research if different package versions or scoped packages (@scope/package) are equally vulnerable', 'Analyze whether the vulnerability can be extended to poison responses other than 404s (e.g., cached error pages with malicious content)', 'Test if the attack can be applied to registry metadata endpoints, not just package tarballs', 'Investigate whether CDN-specific headers (CloudFlare headers in response) can be leveraged for more persistent poisoning']

## MITRE ATT&CK
- T1190: Exploit Public-Facing Application
- T1195: Supply Chain Compromise
- T1195.003: Supply Chain Compromise - Compromised Software Dependencies
- T1499: Endpoint Denial of Service
- T1499.004: Denial of Service - Protocol Exploitation
- T1547: Abuse Elevation Control Mechanism

## Notes
This vulnerability was discovered during research into cache poisoning attacks on artifact repositories (Depi project). The researchers responsibly withheld the specific header combinations required to trigger the vulnerability at the time of publication. The attack has a temporary nature (few minutes) but could be repeated to maintain disruption. The write-up emphasizes the critical role of npm in the JavaScript ecosystem (2.1M packages, 17M developers) and demonstrates how a single vulnerability in core infrastructure can have cascading effects across the entire supply chain. The inclusion of example requests (with cache buster parameters to avoid collateral damage) shows responsible disclosure practices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
