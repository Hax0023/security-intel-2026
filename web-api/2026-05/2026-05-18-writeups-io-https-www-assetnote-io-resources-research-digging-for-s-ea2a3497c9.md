# SSRF Vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Assetnote Research
- **Bounty:** N/A - Security Research Publication
- **Severity:** HIGH
- **Vuln types:** Server-Side Request Forgery (SSRF), XML External Entity (XXE), Cross-Site Scripting (XSS), Information Disclosure, Open Redirect
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint is vulnerable to SSRF attacks when remotePatterns is misconfigured with overly permissive wildcard hostname matching. The image optimization component can be abused to access internal services, leak sensitive data through SVG/XML responses, and chain with open redirects on whitelisted domains.

## Attack scenario (step by step)
1. Attacker identifies NextJS application with remotePatterns configured to allow all hostnames using wildcard ('**') pattern
2. Attacker crafts malicious _next/image URL targeting internal services: https://example.com/_next/image?url=https://localhost:2345/api/v1/sensitive&w=256&q=75
3. NextJS image optimizer makes backend request to internal endpoint and retrieves response
4. If response is valid image or SVG, attacker receives content; if XML/SVG allowed, full response body is leaked via content sniffing
5. Attacker alternatively discovers open redirect on whitelisted domain and chains it with image endpoint to bypass whitelist restrictions
6. Attacker escalates to XSS if dangerouslyAllowSVG is enabled, or data exfiltration if internal services return non-image content

## Root cause
Overly permissive remotePatterns configuration combined with the image optimizer's behavior of following redirects and content-sniffing without strict validation. The framework's convenience features (wildcard patterns, redirect following, SVG content detection) create security gaps when not carefully configured.

## Attacker mindset
Recognizing that modern static site generators like NextJS are often perceived as low-risk compared to traditional CMS platforms, attackers target the misconfigurations that developers introduce when trying to maximize flexibility. The attacker exploits the disconnect between security implications and ease-of-use by weaponizing default features meant for convenience.

## Defensive takeaways
- Never use wildcard hostname patterns ('**') in remotePatterns - explicitly whitelist only required domains
- Disable SVG handling by ensuring dangerouslyAllowSVG remains false (default) to prevent content-type confusion attacks
- Implement strict Content-Type validation on responses before processing as images
- Audit and restrict Content-Type header sniffing behavior in image processing pipelines
- Apply least privilege to internal service accessibility - block image optimizer from accessing localhost/internal IPs
- Monitor _next/image requests for suspicious patterns (localhost, internal IPs, port numbers)
- Ensure whitelisted domains implement proper redirect validation and avoid open redirects
- Use network segmentation to restrict what the application server can reach
- Review NextJS version for known image optimization vulnerabilities and apply patches

## Variant hunting
Look for similar image optimization components in other frameworks (Gatsby, Nuxt, Hugo). Test for SSRF in other _next/* endpoints beyond image handling. Search for XML processing endpoints that might not validate content-types. Examine any user-controlled URL parameters in image/media handling across different frameworks. Test for variations using data: URIs, file: protocol handlers, and unicode/encoding bypasses.

## MITRE ATT&CK
- T1190
- T1498
- T1557
- T1090
- T1040
- T1005

## Notes
This research highlights how modern convenience features in frameworks can introduce security risks when not properly understood by developers. The _next/image component is enabled by default and the remotePatterns configuration is not obviously security-sensitive, making this a common misconfiguration. The ability to chain SSRF with open redirects on whitelisted domains demonstrates the importance of comprehensive security reviews beyond just the application code itself. The content-sniffing behavior combined with SVG/XML handling represents a multi-stage exploitation path.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
