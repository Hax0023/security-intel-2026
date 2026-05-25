# npm Registry Cache Poisoning Denial of Service (CPDoS)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** npm (npmjs.org)
- **Bounty:** Not specified in writeup
- **Severity:** critical
- **Vuln types:** Cache Poisoning, Denial of Service, HTTP Cache Poisoning, Supply Chain Attack
- **Category:** supply-chain
- **Writeup:** https://www.landh.tech/blog/20240603-npm-cache-poisoning/

## Summary
A Cache Poisoning Denial of Service (CPDoS) vulnerability was discovered in the npm registry that allows attackers to poison the caching system by sending specially crafted HTTP requests with specific headers, causing the registry to serve cached '404 Not Found' responses for legitimate packages. This attack could render packages temporarily inaccessible to millions of developers worldwide, potentially disrupting the entire JavaScript ecosystem.

## Attack scenario (step by step)
1. Attacker crafts a malicious HTTP request containing specific header combinations designed to trigger backend caching errors against registry.npmjs.org
2. Request targets a popular npm package (e.g., safe-regex-1.1.0.tgz) with a unique cache buster parameter to avoid affecting legitimate users initially
3. The vulnerable caching system interprets the crafted headers incorrectly and stores a '404 Not Found' response in its cache for that package
4. Attacker sends a follow-up request without the malicious headers but using the same cache key to retrieve the poisoned cached response
5. The registry serves the cached '404 Not Found' response to subsequent legitimate requests from other developers
6. Package becomes unavailable for several minutes until the temporary cache entry expires, causing DoS to dependent projects

## Root cause
The npm registry's HTTP caching layer contains a vulnerability in how it processes and caches responses when presented with specific header combinations. The caching system fails to properly validate requests or differentiate between legitimate and malicious cache keys, allowing attackers to manipulate which responses get cached and served. The vulnerability exploits subtle flaws in the interaction between HTTP protocols, caching headers, and the backend systems.

## Attacker mindset
A sophisticated supply chain attacker recognizes that disrupting package availability on npm—the central repository for 2.1 million packages used by 17 million developers—would cause cascading failures across the JavaScript ecosystem. Rather than attempting costly direct compromises, the attacker exploits caching mechanics to achieve denial of service with minimal effort. The use of cache busters and targeted timing suggests research-oriented reconnaissance before large-scale exploitation.

## Defensive takeaways
- Implement strict HTTP cache key validation that normalizes headers and prevents header-based cache poisoning (e.g., whitelist safe headers for caching decisions)
- Enforce separate cache keys for different request variations and validate that response status codes match the request intent
- Add cache poisoning detection mechanisms that flag unusual patterns (e.g., 404 responses from atypical requests)
- Implement rate limiting on package download endpoints to prevent rapid cache poisoning attempts
- Monitor cache hit rates and error patterns for anomalies indicating active poisoning attacks
- Use cache control headers conservatively for error responses and reduce TTL for 404s from registries
- Conduct regular security audits of caching layer configuration and HTTP handling logic
- Implement request signature validation or authentication for package downloads to prevent header manipulation

## Variant hunting
Test other package registries (PyPI, RubyGems, Maven Central, Cargo) for similar CPDoS vulnerabilities by sending crafted header combinations. Investigate whether CDN providers (Cloudflare, Fastly) are vulnerable to similar attacks. Test internal artifact repositories (Nexus, Artifactory) commonly used by enterprises. Explore cache poisoning via other HTTP header injection vectors (X-Forwarded-*, Accept-*, Range headers). Examine whether the vulnerability can be exploited with permanent caching to affect users beyond minutes.

## MITRE ATT&CK
- T1195.003 - Supply Chain Compromise: Compromised Software Dependencies
- T1190 - Exploit Public-Facing Application
- T1561.002 - Disk Wipe: Disk Structure Wipe (functional equivalent via availability)
- T1499.004 - Endpoint Denial of Service: Application-Layer DDoS

## Notes
The researchers did not disclose the exact header combinations to prevent immediate mass exploitation while the vulnerability remained unpatched. The attack requires repeated requests for each package target and has a limited time window (minutes) before cache expiry. The discovery came from proactive research during development of 'Depi', a supply chain security testing tool. The npm registry's reliance on Cloudflare CDN means the vulnerability exists at the edge caching layer, affecting all users globally. This represents a critical fragility in the JavaScript ecosystem's trust model and highlights the importance of supply chain security testing.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
