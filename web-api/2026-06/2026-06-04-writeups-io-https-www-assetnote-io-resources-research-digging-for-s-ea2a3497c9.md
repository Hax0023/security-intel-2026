# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** NextJS Framework / General Bug Bounty Programs
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, Cross-Site Scripting (XSS), Information Disclosure, Configuration Vulnerability
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image component for image optimization can be exploited to perform blind SSRF attacks when remotePatterns are overly permissive (e.g., using wildcard hostname matching). The vulnerability allows attackers to access internal services, leak sensitive data, or chain with open redirects on whitelisted domains to bypass restrictions.

## Attack scenario (step by step)
1. Attacker discovers a NextJS application with remotePatterns configured to accept wildcard hostnames (protocol: 'https|http', hostname: '**')
2. Attacker crafts a request to the _next/image endpoint with a malicious URL pointing to internal services: https://example.com/_next/image?url=http://localhost:2345/api/v1/secret&w=256&q=75
3. NextJS backend makes a server-side request to the attacker-supplied URL to fetch and resize the image
4. If the response is a valid image format, attacker receives the response; if it's XML/SVG with dangerouslyAllowSVG enabled, full content is leaked
5. Attacker alternatively finds an open redirect on a whitelisted domain and chains it with the SSRF to bypass hostname validation
6. Attacker exfiltrates sensitive data, credentials, or internal API responses unavailable from the client perspective

## Root cause
1) Overly permissive remotePatterns configuration using wildcards without proper validation; 2) NextJS image optimizer follows redirects without sufficient security checks; 3) Content-type sniffing behavior and SVG handling that can leak full response bodies; 4) Default-enabled image optimization feature creates an unauthenticated SSRF gadget endpoint

## Attacker mindset
Reconnaissance-focused approach targeting modern static site generators; understanding that developers may not fully appreciate security implications of wildcard patterns; leveraging built-in features meant for convenience as an exploitation vector; chaining multiple weaknesses (open redirects + SSRF) for bypass

## Defensive takeaways
- Never use wildcard hostname patterns in remotePatterns - explicitly whitelist only required domains
- Validate and restrict URL schemes to https only when possible
- Implement hostname validation that prevents access to private IP ranges (127.0.0.1, 10.x.x.x, 172.16-31.x.x, 192.168.x.x)
- Disable image optimization or the _next/image endpoint if not required
- Avoid enabling dangerouslyAllowSVG unless absolutely necessary and implement additional content-type validation
- Audit open redirects on whitelisted domains and remediate them
- Monitor and log _next/image requests for suspicious internal URL access patterns
- Keep NextJS updated to patched versions with improved content-type validation
- Use allowlist approach rather than blocklist for remote pattern configuration

## Variant hunting
['Check for other NextJS optimization endpoints (_next/data, _next/static) with similar issues', 'Hunt for misconfigured remotePatterns across different NextJS deployments via search engines or content discovery', 'Test for SSRF via embedded image formats (JPEG, PNG) that may not be validated as strictly as SVG', 'Look for open redirects on commonly whitelisted third-party CDN domains (cloudinary, imgix, etc.)', 'Test if authentication bypass is possible by accessing _next/image without session tokens', 'Explore if query parameter manipulation (quality, width values) can trigger different code paths with weaker validation', 'Hunt for internal service discovery via timing attacks on the image resize operation']

## MITRE ATT&CK
- T1190
- T1105
- T1071
- T1046
- T1498
- T1530

## Notes
This is a systematic analysis of a common misconfiguration pattern in production NextJS deployments rather than a zero-day. The vulnerability class is well-known (SSRF), but the specific attack surface (image optimization endpoint) and exploitation patterns in NextJS ecosystem provide practical reconnaissance value. The research emphasizes that default-enabled features in modern frameworks create security implications developers may not fully consider. Content-type sniffing behavior compounds the issue, potentially allowing data exfiltration beyond typical image formats.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
