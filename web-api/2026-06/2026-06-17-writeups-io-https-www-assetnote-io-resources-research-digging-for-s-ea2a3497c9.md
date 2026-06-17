# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** NextJS Framework (General Research)
- **Bounty:** Not specified (Research publication by Assetnote)
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, Information Disclosure, Cross-Site Scripting (XSS)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's `_next/image` endpoint is vulnerable to SSRF attacks when `remotePatterns` is misconfigured to allow wildcard hostnames. The image optimization component follows redirects and can be exploited to access internal services, leak XML content, or achieve XSS through SVG handling in older versions.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with wildcard remotePatterns configuration allowing all HTTPS/HTTP hosts
2. Attacker crafts malicious URL to `_next/image` endpoint targeting internal service: `https://example.com/_next/image?url=https://localhost:2345/api/v1/secret&w=256&q=75`
3. NextJS backend makes server-side request to internal host to fetch and resize the image
4. If response is valid image, attacker receives resized content; if XML/SVG, content leaks through response or error messages
5. Attacker finds open redirect on whitelisted domain and chains it to bypass restrictions and access internal resources
6. In older NextJS versions with dangerouslyAllowSVG enabled, attacker escalates to XSS by injecting SVG payloads

## Root cause
The `_next/image` endpoint's remotePatterns validation allows developers to configure wildcard hostname matching without security warnings. The endpoint follows HTTP redirects without re-validating against remotePatterns, and uses content-type sniffing to determine file types, enabling content leakage from internal endpoints.

## Attacker mindset
An attacker would recognize that image optimization endpoints are commonly exposed in modern web frameworks and often overlooked from a security perspective. By examining the NextJS documentation, they discover that permissive wildcard configurations are possible and not clearly documented as dangerous. The attacker understands that blind SSRF to internal services can leak information through error handling and content-type detection mechanisms, making this a practical attack vector against companies using NextJS for 'simple' static sites.

## Defensive takeaways
- Never use wildcard hostname patterns in remotePatterns; explicitly whitelist specific domains required for the application
- Restrict the `_next/image` endpoint to specific trusted external domains or disable it entirely if not needed
- Keep NextJS updated to latest version to benefit from security patches and improved default security posture
- Disable dangerouslyAllowSVG unless SVG image optimization is explicitly required
- Implement network segmentation to prevent server-side components from accessing internal APIs
- Monitor and audit requests to `_next/image` endpoint for suspicious patterns or internal domain access attempts
- Use allow-lists for redirect targets in image processing to prevent open redirect chaining attacks
- Ensure internal services respond with proper Content-Type headers and do not expose sensitive information in responses
- Implement rate limiting on the `_next/image` endpoint to mitigate blind SSRF enumeration attacks

## Variant hunting
['Check for similar image optimization endpoints in other frameworks (Nuxt, Gatsby, Remix) for equivalent vulnerabilities', 'Audit other `_next/*` endpoints for SSRF or similar request forgery vulnerabilities', 'Test remotePatterns bypass techniques using DNS rebinding or case-sensitivity tricks', 'Investigate if file upload endpoints accept URLs that could be exploited via the image optimizer', 'Search for applications using older NextJS versions where SVG handling is more permissive', 'Test for SSRF via other optimization features like font optimization or script optimization endpoints', 'Look for misconfigured API gateways or proxies that might not properly validate remotePatterns', 'Check for time-based information disclosure in image processing errors that could leak internal infrastructure details']

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1557.002
- T1046
- T1040
- T1016
- T1021
- T1133
- T1200

## Notes
This research identifies a framework-level architectural issue rather than a specific CVE. The vulnerability exists in default configurations and common developer misunderstandings about security implications. The chaining of SSRF with open redirects and content-type sniffing demonstrates how multiple seemingly minor design decisions compound into exploitable vulnerabilities. The research effectively demonstrates why static site generators should not be assumed to have minimal attack surface when server-side features are enabled by default.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
