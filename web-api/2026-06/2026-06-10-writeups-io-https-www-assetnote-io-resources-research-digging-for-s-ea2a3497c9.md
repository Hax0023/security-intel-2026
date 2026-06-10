# Digging for SSRF in NextJS Apps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** General Security Research / Bug Bounty Programs
- **Bounty:** Not specified
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Open Redirect exploitation, XML External Entity (XXE) Information Disclosure, Cross-Site Scripting (XSS), Insecure Deserialization
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS applications commonly expose SSRF vulnerabilities through the built-in _next/image endpoint when overly permissive remotePatterns configurations are used. By whitelisting wildcard domains or exploiting open redirects on whitelisted domains, attackers can craft requests to internal services, leak XML responses, or achieve XSS through SVG handling.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application using the default _next/image endpoint with remotePatterns configured to accept wildcard hostnames (protocol: 'https', hostname: '**')
2. Attacker crafts a malicious URL: https://target.com/_next/image?url=http://localhost:2345/api/v1/internal&w=256&q=75 to probe internal services
3. If the internal endpoint returns image data, the response is passed through the image optimization pipeline and returned to the attacker (blind SSRF)
4. Attacker escalates by discovering an open redirect on a whitelisted domain and chains it with the SSRF: https://target.com/_next/image?url=https://whitelisted.com/redirect?to=http://localhost:admin
5. If dangerouslyAllowSVG is enabled or older NextJS versions are used, attacker exfiltrates XML/SVG content: https://target.com/_next/image?url=http://localhost/config.xml returns full file contents
6. For old NextJS versions without Content-Type headers, attacker leaks full response bodies from misconfigured internal services

## Root cause
The _next/image endpoint performs server-side image fetching based on user-supplied URL parameters without sufficient validation. When combined with overly permissive remotePatterns configurations (wildcard hostnames), the endpoint becomes an SSRF vector. Additionally, the image renderer follows HTTP redirects without restricting redirect targets, enabling chaining with open redirects. Content-type sniffing and SVG handling create secondary information disclosure channels.

## Attacker mindset
Attackers recognize that modern static site generators like NextJS are increasingly popular but often misconfigured. The _next/image endpoint is enabled by default, making it an easy reconnaissance target. Developers commonly use wildcard patterns without understanding security implications. Open redirects on third-party domains become valuable chaining primitives. Information disclosure through content-type sniffing represents low-hanging fruit for data exfiltration.

## Defensive takeaways
- Never use wildcard hostname patterns in remotePatterns; explicitly whitelist only required external domains with specific protocols
- Disable dangerouslyAllowSVG unless absolutely necessary, and verify SVG handling is secure in the NextJS version being used
- Keep NextJS updated to the latest version with security patches for image processing and content-type detection
- Implement network segmentation and firewall rules to restrict internal service access from application servers
- Monitor and log all _next/image requests to detect potential SSRF reconnaissance attempts (high volume of 4xx responses to localhost/internal IPs)
- Audit whitelisted domains for open redirects and other vulnerability chains that could be exploited with SSRF
- Validate that Content-Type headers match actual response content; implement strict content-type validation
- Set request timeouts and size limits on image optimization to prevent DoS and resource exhaustion
- Use HTTP client libraries with SSRF-resistant configurations (disable redirect following or validate redirect targets)

## Variant hunting
Hunt for similar SSRF patterns in other NextJS built-in features: _next/data (data fetching), getServerSideProps with user input, API routes with external data fetching. Check for similar vulnerabilities in other static site generators (Gatsby image optimization, Nuxt image modules). Look for custom image optimization endpoints in NextJS projects that replicate the vulnerable pattern. Investigate whether other framework components (video optimization, font optimization) follow similar patterns. Review third-party NextJS plugins for image/media handling that may expose SSRF endpoints.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (SSRF via _next/image)
- T1598 - Phishing for Information (blind SSRF for internal service reconnaissance)
- T1526 - Cloud Service Discovery (SSRF to probe internal cloud metadata services)
- T1552 - Unsecured Credentials (exfiltration of config files containing credentials via SSRF)
- T1021 - Remote Services (SSRF to access internal administrative interfaces)
- T1557 - Man-in-the-Middle (potential if combined with network position)
- T1005 - Data from Local System (XML/SVG content exfiltration)

## Notes
This research highlights how default-enabled features in modern frameworks become security liabilities when developers lack security context. The _next/image endpoint is particularly dangerous because: (1) it's enabled by default, (2) configuration guidance doesn't emphasize security, (3) the SSRF is 'blind' making it harder to detect. The chaining with open redirects demonstrates how SSRF becomes more exploitable when combined with other common web vulnerabilities. Content-type sniffing attacks represent an underappreciated information disclosure vector. Assetnote's research suggests encountering NextJS sites 'extremely often' in assessments, indicating widespread adoption without corresponding security hardening. Organizations should audit NextJS deployments for remotePatterns configuration and consider disabling _next/image if not needed. The vulnerability class affects statically-served sites commonly perceived as low-risk, creating a false sense of security.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
