# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** General Security Research / Bug Bounty Programs
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, XML External Entity (XXE), Cross-Site Scripting (XSS)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS applications expose a `_next/image` endpoint for image optimization that can be exploited for SSRF attacks when misconfigured with overly permissive `remotePatterns` settings. The vulnerability allows attackers to make requests to internal services and, under certain conditions, escalate to XXE or XSS through SVG handling or content-type sniffing.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with `remotePatterns` configured to allow all hostnames using wildcard syntax (https://** and http://)
2. Attacker crafts a malicious URL targeting the `_next/image` endpoint with a localhost or internal service URL: `https://example.com/_next/image?url=https://localhost:2345/api/v1/x&w=256&q=75`
3. The NextJS image optimization service makes a server-side request to the internal URL, bypassing network-level access controls
4. If the internal response is a valid image format, attacker receives the response; if not, attacker still confirms service availability (blind SSRF)
5. Attacker escalates by chaining with open redirects on whitelisted domains to pivot to non-whitelisted internal hosts
6. If SVG handling is enabled or using older NextJS versions, attacker can exfiltrate XML data or inject malicious SVG content for XSS

## Root cause
The `_next/image` endpoint lacks sufficient validation of the `url` parameter and respects overly permissive `remotePatterns` configurations. Developers often whitelist all domains (`**`) without understanding the security implications, and the endpoint follows redirects without proper validation, enabling SSRF chains.

## Attacker mindset
An attacker would systematically identify NextJS applications, probe the `_next/image` endpoint for misconfiguration, enumerate internal services on common ports (8080, 5000, 3000, etc.), and attempt to extract sensitive data from internal APIs or services. The attacker would leverage open redirects on whitelisted domains to bypass intended restrictions.

## Defensive takeaways
- Never use wildcard patterns (`**`) in `remotePatterns`; explicitly whitelist only necessary domains
- Implement strict URL validation and parsing to prevent open redirect chaining
- Disable `dangerouslyAllowSVG` unless absolutely required; keep NextJS updated to the latest version
- Monitor and block requests to internal/private IP ranges (10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16, 127.0.0.0/8, localhost)
- Implement rate limiting and logging on the `_next/image` endpoint to detect probing behavior
- Use a allowlist of Content-Types that are acceptable for image responses; reject XML and other unexpected types
- Disable redirect following in the image optimization service or strictly validate redirect targets
- Implement network segmentation to isolate internal services from application servers

## Variant hunting
['Test other NextJS image optimization configurations (quality, width, height parameters) for injection vulnerabilities', 'Probe for similar SSRF issues in other auto-optimization endpoints (videos, PDFs, documents)', 'Investigate if `remotePatterns` configuration can be bypassed via URL encoding, case variation, or IPv6 formats', 'Check if `_next/data` or GraphQL endpoints have similar issues with user-controlled URL parameters', 'Test for SSRF in custom image loaders or external CDN integrations', 'Analyze whether other static site generators (Nuxt, Gatsby, Hugo) with server-side features have similar vulnerabilities']

## MITRE ATT&CK
- T1190
- T1557
- T1021
- T1550
- T1552
- T1040

## Notes
This research highlights a common pattern in modern web frameworks: convenient default features that introduce security risks when misconfigured. The vulnerability is particularly dangerous because many developers may not be aware that `remotePatterns: [{protocol: 'https', hostname: '**'}]` creates an SSRF vector. The ability to chain with open redirects significantly expands the attack surface. Assetnote likely encountered this in real bug bounty assessments, making it a high-impact finding in the wild.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
