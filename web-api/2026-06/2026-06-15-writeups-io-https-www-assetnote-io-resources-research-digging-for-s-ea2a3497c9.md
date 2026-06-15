# SSRF Vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Assetnote Security Research
- **Bounty:** Not specified (research disclosure)
- **Severity:** HIGH
- **Vuln types:** Server-Side Request Forgery (SSRF), Cross-Site Scripting (XSS), Information Disclosure, Open Redirect Chaining
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint can be exploited for blind SSRF attacks when remotePatterns are overly permissive (e.g., wildcard hostnames). Attackers can probe internal services, exfiltrate XML/SVG content, or chain open redirects on whitelisted domains to bypass restrictions and access arbitrary internal endpoints.

## Attack scenario (step by step)
1. Attacker identifies NextJS application with overly permissive remotePatterns configuration allowing any protocol/hostname (e.g., '**' wildcard)
2. Attacker crafts _next/image request targeting internal service: https://example.com/_next/image?url=https://localhost:2345/api/v1/internal&w=256&q=75
3. If response is valid image, attacker receives image-processed response; if not, attacker receives error indicating service existence (blind SSRF confirmation)
4. Attacker exploits dangerouslyAllowSVG setting to leak full XML content via content-type sniffing bypass, or exfiltrates data from responses lacking Content-Type headers
5. Alternatively, attacker finds open redirect on whitelisted domain (e.g., third-party.com) and chains it to redirect to internal service, bypassing hostname whitelist
6. Attacker leverages successful SSRF to enumerate internal network topology, access metadata services, or trigger internal API actions

## Root cause
NextJS image optimization endpoint does not properly validate remotePatterns configuration, allowing developers to inadvertently expose SSRF via wildcard hostname allowlists. Content-type detection via sniffing and redirect following further amplify the vulnerability. Legacy versions and dangerouslyAllowSVG flag compound the issue by enabling XSS and full content exfiltration.

## Attacker mindset
Reconnaissance-focused attacker exploiting developer misconfiguration of modern frameworks. Targets 'static' site generators assumed to have minimal server-side attack surface. Uses SSRF as pivot point for internal network reconnaissance, data exfiltration, and lateral movement.

## Defensive takeaways
- Never use wildcard ('**') hostname patterns in remotePatterns; explicitly whitelist only necessary domains
- Disable dangerouslyAllowSVG unless absolutely required; SVG content-type detection via sniffing is inherently unsafe
- Implement strict input validation and URL parsing to block localhost/127.0.0.1/private IP ranges regardless of remotePatterns
- Disable redirect following in image optimization endpoint or limit redirects to whitelisted domains only
- Ensure Content-Type headers are properly set on all internal services to prevent sniffing-based exfiltration
- Regularly audit NextJS configuration files (next.config.js) in security reviews; static generators are not static if misconfigured
- Consider disabling _next/image endpoint entirely if image optimization is not needed
- Monitor _next/image requests for suspicious patterns (localhost URLs, private IP ranges, XML/SVG responses)

## Variant hunting
['Other framework image optimization endpoints (Gatsby Image API, Nuxt Image, Remix resources) for similar SSRF patterns', 'NextJS API routes and getServerSideProps using user-controlled URLs without proper validation', 'Open redirects on whitelisted third-party domains accessible via _next/image', 'NextJS rewrite/redirect rules that could chain with image endpoint', 'File upload endpoints that accept URLs and process them server-side', 'NextJS ISR (Incremental Static Regeneration) endpoints exploitable via URL parameters', 'Misconfigured remotePatterns in other NextJS projects discovered via GitHub/public code repositories']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (NextJS framework exploitation)
- T1498 - Network Denial of Service (potential amplification via SSRF)
- T1557 - Adversary-in-the-Middle (SSRF response interception)
- T1021 - Remote Services (SSRF to internal services)
- T1040 - Traffic Signaling (URL redirect chaining)
- T1005 - Data from Local System (SSRF exfiltration of local files/services)
- T1526 - Passive Scanning (blind SSRF for service enumeration)

## Notes
Research demonstrates that modern 'lightweight' frameworks can introduce significant security risks when default features are not properly understood. The _next/image component is enabled by default, making this a high-prevalence vulnerability. The whitelist bypass via open redirects is particularly dangerous as it requires only finding a single open redirect on any whitelisted domain. Content-type sniffing for SVG/XML detection is a design flaw that violates defense-in-depth principles. Assetnote identifies this as common in production NextJS deployments they encounter.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
