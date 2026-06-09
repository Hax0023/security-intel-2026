# Digging for SSRF in NextJS Apps - _next/image Component Vulnerabilities

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** General security research (Assetnote)
- **Bounty:** Not specified - research disclosure
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Cross-Site Scripting (XSS), Information Disclosure, Open Redirect
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint for image optimization can be exploited for SSRF attacks when remotePatterns is misconfigured with wildcard hostnames. The vulnerability allows attackers to request internal URLs and potentially leak sensitive data or chain with SVG/XML processing or open redirects to escalate impact.

## Attack scenario (step by step)
1. Attacker identifies NextJS application with _next/image endpoint enabled
2. Attacker discovers remotePatterns configured with wildcard hostname (e.g., '**') allowing any domain
3. Attacker crafts malicious URL: https://example.com/_next/image?url=https://localhost:internal-port/api/endpoint&w=256&q=75
4. NextJS backend makes server-side request to internal URL attempting to fetch and resize as image
5. Attacker analyzes response: if valid image returned, SSRF confirmed; if SVG allowed, can escalate to XSS or XML content leak
6. Attacker chains with open redirect on whitelisted domain to bypass hostname restrictions

## Root cause
Default enablement of _next/image optimization combined with developer misconfiguration of remotePatterns using overly permissive wildcards, failing to restrict which domains can be fetched. The endpoint follows redirects without proper validation and uses content-type sniffing vulnerable to SVG/XML exploitation.

## Attacker mindset
Reconnaissance-focused: identify NextJS apps, check for image optimization endpoint, test remotePatterns configuration. If wildcard found, perform blind SSRF probing of common internal ports/services. If restrictions exist, search for open redirects on whitelisted domains. Escalate from blind SSRF to information disclosure via SVG/XML content leakage or XSS.

## Defensive takeaways
- Never use wildcard patterns in remotePatterns; explicitly whitelist specific trusted domains only
- Keep NextJS updated to patch dangerous SVG handling and content-type sniffing vulnerabilities
- Disable dangerouslyAllowSVG unless absolutely necessary; if required, use separate isolated endpoint
- Implement strict Content-Type validation rather than relying on sniffing
- Disable redirect following in the image optimization pipeline or validate redirect targets against whitelist
- Network segmentation: isolate application servers from internal APIs and metadata services
- Monitor _next/image requests for suspicious patterns (localhost, internal IPs, unusual ports)
- Document security implications of remotePatterns configuration in developer onboarding

## Variant hunting
Hunt for: (1) NextJS apps with overly permissive image patterns, (2) Open redirects on whitelisted image CDN domains, (3) Outdated NextJS versions with SVG sanitization bypasses, (4) Services returning XML/JSON without Content-Type headers, (5) Chaining image SSRF with other vulnerabilities like XXE via XML responses, (6) Similar frameworks (Nuxt, Next-compatible servers) with identical image optimization logic

## MITRE ATT&CK
- T1190
- T1020
- T1557
- T1200
- T1498

## Notes
This is foundational SSRF research rather than a single CVE report. The vulnerability class affects many NextJS deployments due to default enablement of the feature. Real-world impact varies: blind SSRF with image filtering is common; escalation to full content leak requires older versions or dangerous configurations. The redirect-following behavior is particularly dangerous when combined with open redirects on trusted domains. Critical for security teams to audit their NextJS deployments' image configuration.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
