# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Assetnote Security Research (General NextJS Ecosystem)
- **Bounty:** Not specified - Research publication
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Blind SSRF, Open Redirect Chaining, Information Disclosure, Cross-Site Scripting (XSS)
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS applications with overly permissive image optimization configurations expose a blind SSRF vulnerability through the _next/image endpoint. By whitelisting all hostnames via remotePatterns or exploiting open redirects on whitelisted domains, attackers can probe internal services and exfiltrate data. Additional escalation vectors exist through SVG handling and XML content leakage in older NextJS versions.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with remotePatterns configured to allow all hostnames using wildcard patterns (protocol: 'https/http', hostname: '**')
2. Attacker crafts a malicious _next/image request targeting internal services: https://target.com/_next/image?url=https://localhost:2345/api/v1/sensitive&w=256&q=75
3. The image optimization endpoint makes a server-side request to the internal URL and processes the response
4. If response is a valid image format, attacker receives blind confirmation of service availability; if content-sniffing is enabled, full response may leak
5. Attacker chains whitelisted domain open redirects to bypass hostname restrictions and access arbitrary internal endpoints
6. For older NextJS versions or dangerouslyAllowSVG=true, attacker exfiltrates XML/SVG responses or achieves reflected XSS via SVG injection

## Root cause
Default permissive image optimization configuration combined with insufficient validation of remotePatterns, content-type sniffing without proper restrictions, and failure to disable redirect following in server-side image fetching logic

## Attacker mindset
Reconnaissance and lateral movement focused - using the image optimization feature as a network scanner to discover internal services, map infrastructure, and locate API endpoints. Secondary interest in chaining with other vulnerabilities (open redirects, SVG handling) for data exfiltration and XSS exploitation.

## Defensive takeaways
- Explicitly whitelist only required domains in remotePatterns; avoid wildcard hostname patterns
- Disable SVG processing by default (ensure dangerouslyAllowSVG is false) and keep NextJS updated to versions with proper SVG filtering
- Disable HTTP redirect following in image optimization endpoint or validate redirect destinations against whitelist
- Implement strict Content-Type validation rather than relying on content-sniffing
- Enforce restrictive network policies to limit server-side request scope from application servers
- Monitor _next/image endpoint for suspicious patterns (localhost/internal IPs, unusual ports, repeated failures)
- Use network segmentation to isolate internal services from application server access

## Variant hunting
["Search for remotePatterns with hostname: '**' or similar wildcards across public GitHub repos and bug bounty targets", 'Check for open redirects on commonly whitelisted CDN domains (cdn.example.com, assets.example.com) that could chain with SSRF', 'Test for similar SSRF patterns in other image/media optimization endpoints (next/og, sharp-based processing)', 'Investigate if remotePatterns are inherited or merged from parent configurations in monorepo setups', 'Examine older NextJS versions (<12.0) for default dangerouslyAllowSVG behavior and SVG content-sniffing bypass techniques', 'Look for XXE vulnerabilities in XML response handling when SSRF retrieves XML endpoints', 'Test internal service discovery via timing differences or error message variations in image processing responses']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1046 - Network Service Discovery
- T1057 - Process Discovery
- T1016 - System Network Configuration Discovery
- T1087 - Account Discovery
- T1040 - Network Sniffing
- T1071.001 - Application Layer Protocol (HTTP)

## Notes
This is a research publication documenting common misconfigurations rather than a specific bug report. The vulnerability class (SSRF via image optimization) is framework-level rather than a zero-day. Severity elevated from Medium to High due to blind SSRF confirmation combined with data exfiltration potential and chaining vectors. The research emphasizes that 'static site generators' like NextJS have significant server-side attack surface that developers may underestimate. Practical exploitation requires application to have remotePatterns misconfigured or whitelisted domains with open redirects.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
