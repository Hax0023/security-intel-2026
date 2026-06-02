# SSRF vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** NextJS Framework / General web applications
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect exploitation, XML External Entity (XXE) leakage, Cross-Site Scripting (XSS) via SVG, Misconfiguration
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's _next/image endpoint is vulnerable to SSRF attacks when remotePatterns is misconfigured with overly permissive wildcards. An attacker can exploit this to access internal services, leak XML responses, or chain with open redirects on whitelisted domains to bypass restrictions.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with wildcard remotePatterns configuration accepting all https:// and http:// hostnames
2. Attacker crafts a request to _next/image endpoint pointing to internal service: https://example.com/_next/image?url=http://localhost:2345/api/v1/internal&w=256&q=75
3. NextJS server makes internal request to the specified URL and returns response if it contains valid image data
4. If dangerouslyAllowSVG is enabled or using old NextJS version, attacker can request SVG resources for XSS payload injection
5. Attacker can alternatively find open redirect on whitelisted domain and chain it with image endpoint to reach arbitrary internal URLs
6. Attacker leverages XML content-type sniffing vulnerability to leak full XML/API responses from internal hosts

## Root cause
The _next/image component performs server-side image fetching without adequate validation of target URLs. When developers use wildcard patterns in remotePatterns, the endpoint allows requests to any host. The framework also follows redirects without re-validating against whitelist and performs content-type sniffing that can leak sensitive responses in certain configurations.

## Attacker mindset
An attacker recognizes that static site generators like NextJS are increasingly popular but may have security misconfigurations. They understand that image optimization features are enabled by default and that developers often misconfigure remotePatterns for convenience. They look for overly permissive patterns or chainable vulnerabilities (open redirects) on whitelisted domains to bypass restrictions.

## Defensive takeaways
- Never use wildcard patterns in remotePatterns configuration; explicitly whitelist only necessary domains
- Regularly audit next.config.js for overly permissive image optimization settings
- Keep NextJS updated to latest version to benefit from security patches and default-secure configurations
- Ensure dangerouslyAllowSVG is explicitly set to false unless SVG support is required
- Implement request validation to prevent redirect-chain attacks; re-validate URLs after redirects
- Configure internal services to require authentication and not expose sensitive data via content-type sniffing
- Use network segmentation to restrict outbound connections from application servers to internal APIs
- Monitor _next/image requests for suspicious patterns targeting internal hosts or localhost addresses

## Variant hunting
Hunt for similar image optimization vulnerabilities in other frameworks (Gatsby, Nuxt, etc.). Search for instances where image CDN endpoints follow redirects without re-validation. Look for XML response leakage via content-type sniffing in other image processing libraries. Investigate similar default-enabled features in frameworks that perform server-side resource fetching.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services (internal network access)
- T1552 - Unsecured Credentials (API exposure)
- T1598 - Phishing (via redirect chains)

## Notes
This research demonstrates how security-aware defaults in frameworks can be undermined by developer misconfiguration. The vulnerability is particularly impactful because image optimization is enabled by default and many developers may not understand the security implications of wildcard remotePatterns. The chaining potential with open redirects on whitelisted domains significantly expands the attack surface.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
