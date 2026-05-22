# SSRF in NextJS _next/image Component via Misconfigured Remote Patterns

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** NextJS Framework Security Research (Assetnote)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Blind SSRF, Open Redirect Exploitation, XML External Entity (XXE) Information Disclosure, Cross-Site Scripting (XSS) via SVG
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image optimization endpoint enables blind SSRF attacks when remotePatterns is configured with overly permissive wildcards (hostname: '**'). The image renderer follows redirects and performs content-type sniffing, allowing attackers to access internal services, leak XML responses, or achieve XSS through SVG handling in older versions.

## Attack scenario (step by step)
1. Attacker discovers a NextJS application with remotePatterns wildcard configuration enabling any hostname
2. Attacker crafts malicious request to _next/image endpoint targeting internal service: _next/image?url=https://localhost:2345/api/v1/internal&w=256&q=75
3. NextJS server makes SSRF request to internal URL and receives response, returning it if it passes image validation checks
4. If internal response is valid image format, attacker confirms service accessibility; if SVG allowed or old NextJS version, attacker leaks full XML content or injects XSS payload
5. Alternatively, if whitelisted external domain has open redirect, attacker chains it: _next/image?url=https://third-party.com/redirect?target=http://localhost:internal&w=256&q=75
6. Internal service response is returned through redirect chain, bypassing hostname restrictions

## Root cause
NextJS image optimization endpoint (_next/image) does not properly validate destination URLs when remotePatterns uses wildcards. The component follows HTTP redirects without re-validating the final destination against the whitelist, and performs content-type sniffing that trusts response body structure over headers, enabling information disclosure.

## Attacker mindset
Reconnaissance-focused: exploit default-enabled features in popular frameworks; target misconfigured security controls (overly permissive whitelists) that developers implement without understanding risk; chain multiple weaknesses (redirects + sniffing + SVG handling) for maximum impact; focus on blind SSRF scenarios where direct response leakage is limited.

## Defensive takeaways
- Never use wildcard hostname patterns (hostname: '**') in remotePatterns; explicitly whitelist only necessary external domains
- Validate final destination URLs after redirects against remotePatterns whitelist, not just initial URL
- Disable dangerouslyAllowSVG unless absolutely required; keep NextJS updated to versions with improved SVG/content-type validation
- Implement response content-type validation based on response headers, not body sniffing heuristics
- Use network segmentation and firewall rules to restrict outbound connections from application servers to internal services
- Audit third-party domains in whitelist for open redirects that could be chained with SSRF
- Monitor and log _next/image requests for anomalous patterns (unusual hostnames, localhost references, high frequency)

## Variant hunting
['Check for similar image optimization endpoints in other frameworks (Nuxt, Gatsby, custom implementations)', 'Hunt for overly permissive remotePatterns configurations in public GitHub repositories and npm packages', 'Test other NextJS API routes that accept URLs (OG image generation, thumbnails, PDF rendering) for similar SSRF vectors', 'Identify open redirects on common CDN/third-party domains that appear in whitelists across multiple NextJS apps', 'Research content-type sniffing bypasses in current NextJS versions for XML/SVG leakage', 'Test for SSRF via other image-related configurations (imageOptimizer, optimizedImages in older versions)']

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1567
- T1200
- T1526

## Notes
This research identifies a class of vulnerabilities rather than a single framework bug. The primary issue is developer misconfiguration (wildcard whitelisting), compounded by framework design choices (redirect following, sniffing). The cascading weaknesses (SVG+sniffing→XXE, redirects+whitelist bypass) demonstrate need for defense-in-depth. NextJS popularity and default-enabled image optimization make this a high-impact finding for penetration testers. The 'blind SSRF' aspect is particularly dangerous as internal service discovery may be possible without direct output.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
