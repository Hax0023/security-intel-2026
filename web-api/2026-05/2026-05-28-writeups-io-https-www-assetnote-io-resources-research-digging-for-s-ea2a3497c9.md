# SSRF Vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** General security research (not a specific bug bounty program)
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, XML External Entity (XXE), Cross-Site Scripting (XSS), Information Disclosure
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image component enables server-side image optimization that can be exploited for blind SSRF attacks when remotePatterns are misconfigured with overly permissive wildcard rules. The vulnerability allows attackers to make the server request arbitrary internal URLs, potentially combined with open redirects or SVG/XML handling to leak sensitive data or achieve RCE.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with wildcard remotePatterns configuration allowing https://** and http://**
2. Attacker crafts a malicious request to _next/image endpoint with url parameter pointing to internal service (e.g., localhost:2345/api/v1/admin)
3. NextJS server processes the request and makes internal HTTP request to the specified URL
4. If response is valid image, attacker receives it; if response is XML/SVG with dangerouslyAllowSVG enabled, full content is leaked
5. Attacker alternatively finds open redirect on whitelisted domain (e.g., third-party.com/redirect?to=localhost:6379) and chains it
6. Internal SSRF request bypasses network segmentation, potentially accessing databases, APIs, or cloud metadata services

## Root cause
The _next/image component performs server-side HTTP requests to fetch and resize images without proper validation of destination URLs when remotePatterns uses overly permissive wildcards. The feature follows redirects transparently and uses content-type sniffing that can leak XML/SVG responses. Default configuration does not restrict internal/private IP ranges.

## Attacker mindset
An attacker recognizes that NextJS's convenience features (image optimization) create an attractive SSRF vector, especially since developers may not understand the security implications of wildcard remotePatterns. They exploit the redirect-following behavior to bypass restrictions and leverage content-type sniffing to exfiltrate data from internal services.

## Defensive takeaways
- Explicitly whitelist only necessary remote domains in remotePatterns; avoid wildcard protocols and hostnames
- Implement URL validation to reject private/internal IP addresses (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 169.254.0.0/16, ::1, fc00::/7)
- Disable redirect following in the image optimization component or validate redirect targets
- Set dangerouslyAllowSVG to false and keep NextJS updated to latest versions for better SVG/XML filtering
- Implement Content-Type validation: reject responses that don't match expected image MIME types
- Use network segmentation and firewall rules to restrict outbound server connections
- Monitor and log all _next/image requests with full URL parameters for suspicious patterns
- Consider disabling the _next/image component if not needed and using external CDN/image optimization service instead

## Variant hunting
['Test other NextJS API routes for similar SSRF patterns (_next/data, API routes accepting URL parameters)', 'Examine custom middleware and API handlers that accept URL/URL-like parameters and perform requests', 'Look for similar image optimization features in other frameworks (Next.js API routes, Express image handlers)', 'Check for SSRF in media proxying endpoints, screenshot services, or document rendering features', 'Investigate webhook implementations that fetch remote content based on user input', 'Search for open redirects on any whitelisted domains in remotePatterns configuration', 'Test for XXE/billion laughs attacks if XML responses are processed without proper sanitization']

## MITRE ATT&CK
- T1190
- T1021
- T1200
- T1595
- T1530
- T1552

## Notes
This research highlights a fundamental security challenge in framework design: convenient features (like automatic image optimization) can become security liabilities if developers don't understand the underlying mechanisms. The vulnerability is not in NextJS code itself but in default configurations and developer misunderstandings. The chaining of SSRF with open redirects and content-sniffing demonstrates how multiple seemingly minor design decisions compound into exploitable vulnerabilities. The research emphasizes the importance of secure defaults and clear documentation of security implications.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
