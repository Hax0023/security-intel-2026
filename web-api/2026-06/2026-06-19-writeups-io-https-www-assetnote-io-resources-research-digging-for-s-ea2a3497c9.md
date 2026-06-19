# SSRF Vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** General NextJS Security Research
- **Bounty:** Not specified (Research disclosure)
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect Chaining, XML External Entity (XXE) Information Disclosure, Cross-Site Scripting (XSS)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint performs server-side image optimization and can be exploited for SSRF attacks when remotePatterns are overly permissive or when combined with open redirects on whitelisted domains. The vulnerability is further amplified by content-type sniffing behavior that can leak XML/SVG content and lead to XSS in older versions.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with overly permissive remotePatterns configuration using wildcard hostname matching
2. Attacker crafts a malicious URL to the _next/image endpoint requesting an internal service like https://example.com/_next/image?url=https://localhost:2345/api/v1/sensitive&w=256&q=75
3. NextJS backend makes the SSRF request to the internal endpoint and processes the response
4. If response is a valid image, attacker receives success; if XML/SVG content-type sniffing is enabled, full response body is leaked
5. Attacker alternatively finds an open redirect on a whitelisted domain and chains it to bypass whitelist restrictions
6. Attacker escalates to XSS if dangerouslyAllowSVG flag is enabled, injecting malicious SVG payloads

## Root cause
The image optimization component trusts the url parameter without proper validation when remotePatterns whitelist is overly permissive, does not sanitize content-type headers, and follows redirects without verifying final destination against whitelist policy

## Attacker mindset
An attacker recognizes that image optimization is a commonly enabled default feature in modern frameworks and that developers often misconfigure whitelist policies by using wildcards for convenience. The attacker probes for internal services, exploits content-type sniffing flaws, and chains open redirects to bypass security controls.

## Defensive takeaways
- Use explicit, specific hostname whitelisting in remotePatterns rather than wildcards or overly broad patterns
- Disable dangerouslyAllowSVG unless absolutely necessary and understand the XSS implications
- Do not allow the image optimizer to follow redirects, or validate the final destination against whitelist
- Implement strict Content-Type validation rather than relying on content sniffing
- Audit internal service exposure and implement network segmentation to prevent SSRF impact
- Keep NextJS framework updated to latest versions with security patches
- Monitor _next/image requests for suspicious patterns like localhost, private IP ranges, or unusual hosts

## Variant hunting
['Check for similar image optimization endpoints in other frameworks (Nuxt, Gatsby, Remix) and their SSRF attack surface', 'Investigate whether other _next/* endpoints have similar parameter injection vulnerabilities', 'Search for open redirects on commonly whitelisted third-party CDN domains', 'Test for blind SSRF detection using out-of-band callbacks and timing-based inference', 'Examine XML/XXE processing in other file type handlers (SVG, PDF metadata, etc.)', 'Review dangerouslyAllowSVG adoption rate in public repositories for prevalence assessment']

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1040
- T1567

## Notes
This is a framework-level vulnerability research article demonstrating multiple attack vectors against NextJS defaults. The severity escalates based on configuration choices (remotePatterns breadth, dangerouslyAllowSVG flag, version age). The chaining of open redirects on whitelisted domains is a particularly practical exploitation path. Content-type sniffing for SVG detection is a critical flaw that enables information disclosure. The research emphasizes secure-by-default configuration risks in popular modern web frameworks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
