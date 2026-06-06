# SSRF in NextJS Image Optimization Component (_next/image)

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** N/A - General Research
- **Bounty:** N/A - Research Publication
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect, Cross-Site Scripting (XSS), Information Disclosure, Misconfiguration
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint for image optimization can be exploited for SSRF attacks when remotePatterns are overly permissive (hostname: '**'). The image renderer follows redirects and performs content-type sniffing, allowing attackers to access internal services, exfiltrate XML responses, and potentially achieve XSS through SVG handling in older versions.

## Attack scenario (step by step)
1. Attacker discovers a NextJS application with remotePatterns configured to allow all hostnames using wildcard ('**')
2. Attacker crafts a request to _next/image endpoint with url parameter pointing to internal service: https://example.com/_next/image?url=http://localhost:2345/api/v1/internal&w=256&q=75
3. NextJS server makes server-side request to the internal service without proper validation
4. If response is valid image, attacker receives it; if XML/SVG with dangerouslyAllowSVG enabled, full content is leaked
5. Attacker can chain with open redirect on whitelisted domain to bypass hostname restrictions
6. In older NextJS versions or with SVG enabled, attacker can escalate to XSS by injecting malicious SVG content

## Root cause
NextJS _next/image endpoint performs server-side image fetching and manipulation without adequate URL validation. Root causes include: (1) Overly permissive remotePatterns configuration allowing all hosts, (2) Lack of SSRF-specific validation before making upstream requests, (3) Content-type sniffing that bypasses Content-Type headers, (4) Following redirects without proper destination validation, (5) SVG handling that can execute arbitrary code in older versions

## Attacker mindset
An attacker identifies that image optimization is a commonly enabled default feature in NextJS applications. They recognize that developers may not understand the security implications of wildcard hostname patterns and assume the feature is 'safe'. They exploit the redirect-following behavior and content-sniffing to access internal APIs and exfiltrate sensitive data. They specifically target misconfigured applications where either wildcard patterns are used or open redirects exist on whitelisted domains.

## Defensive takeaways
- Use explicit, narrowly-scoped remotePatterns - never use wildcard hostname ('**') configuration
- Implement strict URL validation for image sources before making requests
- Disable dangerouslyAllowSVG unless absolutely necessary and regularly audit its use
- Disable redirect following in the image optimization component or validate redirect destinations against whitelist
- Implement Content-Type validation based on response headers, not content sniffing
- Apply network-level controls to prevent server from accessing internal services
- Regularly audit and test image optimization endpoint configurations
- Keep NextJS updated to latest version to benefit from security patches
- Monitor _next/image endpoint for suspicious patterns (internal IPs, unusual ports, protocol mismatches)

## Variant hunting
['Check for similar SSRF in other NextJS features like _next/api routes with fetch-based handlers', 'Test next/font endpoints for SSRF vulnerabilities with font URL parameters', 'Audit getServerSideProps and getStaticProps functions that fetch external resources', 'Test API route handlers that use fetch without URL validation', 'Check for SSRF in webhook handlers that fetch content from user-supplied URLs', 'Investigate middleware functions that proxy requests', 'Test for SSRF in any image processing libraries integrated with Next.js applications', 'Hunt for open redirects on whitelisted domains in remotePatterns configuration']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1589 - Gather Victim Identity Information
- T1592 - Gather Victim Host Information
- T1526 - Passive Scanning
- T1557 - Adversary-in-the-Middle
- T1570 - Lateral Tool Transfer
- T1021 - Remote Services
- T1080 - Taint Shared Content

## Notes
This is foundational research on a framework-level vulnerability affecting numerous NextJS deployments. The vulnerability chain demonstrates how default configurations combined with redirect-following and content-sniffing can create exploitable SSRF. The research highlights the broader security problem of image optimization features in modern frameworks being enabled by default without clear security documentation. The blind SSRF aspect is particularly dangerous as it allows attackers to probe internal networks without direct response feedback. The escalation paths to XSS and full content exfiltration depend on version and configuration, making this a multi-faceted vulnerability with varying severity based on deployment specifics.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
