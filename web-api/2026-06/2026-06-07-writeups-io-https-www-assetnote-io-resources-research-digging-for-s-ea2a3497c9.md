# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** General NextJS Applications
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, XML External Entity (XXE), Cross-Site Scripting (XSS), Information Disclosure
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS applications with overly permissive image optimization configurations are vulnerable to blind SSRF attacks through the _next/image endpoint. Attackers can craft malicious URLs to access internal services and APIs. When combined with dangerouslyAllowSVG enabled or open redirects on whitelisted domains, attackers can escalate to information disclosure or XSS.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with remotePatterns configured to accept wildcard hostnames (hostname: '**')
2. Attacker crafts a URL targeting the _next/image endpoint with an internal service: https://example.com/_next/image?url=https://localhost:2345/api/v1/x&w=256&q=75
3. If internal response is a valid image, server processes and returns it, confirming blind SSRF
4. Attacker escalates by discovering open redirects on whitelisted domains to bypass hostname restrictions
5. If dangerouslyAllowSVG is enabled or NextJS version is old, attacker can leak full XML/SVG content or inject malicious SVG for XSS
6. Attacker exfiltrates sensitive data from internal APIs, configuration endpoints, or metadata services (e.g., AWS EC2 metadata)

## Root cause
NextJS _next/image optimization endpoint trusts remotePatterns configuration without proper validation of internal/private IP ranges. Developers often use overly permissive wildcard patterns (hostname: '**') to simplify configuration, unaware of SSRF implications. Image renderer follows redirects and performs content-type sniffing, enabling attackers to bypass protections.

## Attacker mindset
Reconnaissance-focused: scan for NextJS apps using _next/image endpoint exposure. Exploitation is opportunistic - any permissive image config or whitelisted domain with open redirects becomes a lever for blind SSRF. Content-type sniffing and SVG handling represent additional attack surfaces to escalate information disclosure into RCE or data exfiltration.

## Defensive takeaways
- Never use wildcard hostname patterns (hostname: '**') in remotePatterns; explicitly whitelist only trusted domains
- Block private/internal IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, localhost, ::1) in image URL validation
- Disable dangerouslyAllowSVG unless absolutely necessary; update to latest NextJS version with SVG handling improvements
- Implement URL validation before passing to image optimizer; use allowlist rather than denylist approach
- Audit whitelisted domains for open redirects and SSRF vectors; consider using URL parsing to prevent redirect chain exploitation
- Monitor _next/image requests for unusual patterns (internal IPs, localhost, private domains, XML/SVG responses from image endpoints)
- Set response content-type validation to reject non-image MIME types before processing
- Enforce network segmentation to limit damage if internal APIs are accessed via SSRF

## Variant hunting
Search for other dynamic resource loading endpoints in NextJS (API routes, getServerSideProps, Image component usage). Check for similar SSRF in other frameworks with image optimization (Vercel, Gatsby image plugins). Hunt for SVG upload features combined with image optimization. Test for SSRF in file proxy/CDN features. Examine other URL parameters in _next endpoints for injection points. Look for remotePatterns misconfigurations in public GitHub repositories and code samples.

## MITRE ATT&CK
- T1190
- T1498
- T1057
- T1552
- T1105
- T1601

## Notes
This is foundational research on a common real-world vulnerability class in modern JavaScript frameworks. The vulnerability chain from misconfiguration to information disclosure is practical and exploitable. The research highlights framework-level defaults that appear secure but contain logical flaws. Critical for security assessment of NextJS applications in production. Assetnote's research represents reconnaissance methodology applicable to large-scale bug bounty hunting of modern web applications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
