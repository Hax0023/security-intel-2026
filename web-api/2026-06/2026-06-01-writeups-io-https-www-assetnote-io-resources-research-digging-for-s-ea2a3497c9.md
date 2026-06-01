# SSRF Vulnerabilities in NextJS Image Optimization Component

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Assetnote Security Research
- **Bounty:** Not specified - research publication
- **Severity:** High
- **Vuln types:** Server-Side Request Forgery (SSRF), Cross-Site Scripting (XSS), Information Disclosure, Open Redirect Chaining
- **Category:** web-api
- **Writeup:** https://www.assetnote.io/resources/research/digging-for-ssrf-in-nextjs-apps

## Summary
NextJS's built-in _next/image endpoint is vulnerable to SSRF attacks when remotePatterns are overly permissive (e.g., wildcard configurations). The image optimization component follows redirects and performs content-type sniffing, allowing attackers to access internal services, leak sensitive data, or achieve XSS through SVG handling.

## Attack scenario (step by step)
1. Attacker identifies a NextJS application with wildcard remotePatterns configured (e.g., hostname: '**')
2. Attacker crafts a malicious URL targeting the _next/image endpoint with an internal service URL (e.g., localhost:2345/api/v1/x)
3. The image optimizer makes a server-side request to the internal endpoint, bypassing network-level protections
4. If the response is a valid image format or XML/SVG, attacker receives the response or exploits content-type sniffing to leak data
5. In older NextJS versions or with dangerouslyAllowSVG enabled, attacker chains XSS via SVG responses or escalates to full response leakage
6. Alternatively, attacker finds an open redirect on a whitelisted domain and chains it to access arbitrary internal URLs

## Root cause
The _next/image endpoint performs server-side image fetching and resizing without sufficient validation of the target URL. The framework trusts remotePatterns configuration but developers often misconfigure it with wildcards. Additionally, the component follows HTTP redirects and performs content-type sniffing (checking for <?xml header) rather than strictly respecting Content-Type headers, enabling information disclosure.

## Attacker mindset
An attacker recognizes that NextJS is widely deployed for modern web applications and that developers often use convenient-but-dangerous wildcard configurations without understanding the security implications. They understand that image optimization endpoints are often overlooked during security reviews and that the SSRF can be blind (no direct response exfiltration) but still valuable for probing internal services or chaining with other vulnerabilities.

## Defensive takeaways
- Never use wildcard patterns in remotePatterns configuration; explicitly whitelist only trusted, necessary domains
- Avoid enabling dangerouslyAllowSVG unless absolutely required, as it enables XSS and XML leakage attacks
- Implement strict URL validation and reject localhost/private IP ranges (127.0.0.1, 10.0.0.0/8, 172.16.0.0/12, 192.168.0.0/16)
- Disable HTTP redirect following in the image optimization component or validate redirect targets against the whitelist
- Use network segmentation to isolate internal services from image optimization processes
- Regularly update NextJS to benefit from security fixes related to content-type handling and SSRF mitigations
- Monitor _next/image endpoint requests for suspicious patterns (internal IPs, repeated 4xx responses, non-image responses)
- Implement rate limiting on the _next/image endpoint to prevent reconnaissance and automated attacks

## Variant hunting
['Search for NextJS applications with _next/image endpoints and analyze next.config.js for remotePatterns configurations', "Identify instances where remotePatterns use broad wildcards or protocol-only matching (e.g., protocol: 'https' without hostname restrictions)", 'Test for open redirects on whitelisted domains that could be chained with the image optimizer', 'Probe internal service discovery by attempting requests to common internal endpoints (metadata services, admin panels, health checks)', 'Test content-type sniffing behavior with XML/SVG responses from internal services to determine data leakage potential', 'Check for combinations of other NextJS misconfigurations (e.g., disabled authentication on internal routes) that amplify SSRF impact', 'Analyze error messages and response timing from failed image optimization requests to map internal infrastructure']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1552 - Unsecured Credentials
- T1537 - Transfer Data to Cloud Account
- T1530 - Data from Cloud Storage
- T1548 - Abuse Elevation Control Mechanism
- T1557 - Adversary-in-the-Middle
- T1200 - Hardware Additions

## Notes
This research highlights the danger of default-enabled features in modern frameworks and the gap between developer intent and security reality. The wildcard remotePatterns misconfiguration is particularly insidious because it appears to be a reasonable shortcut for 'enable external images' without developers understanding the SSRF implications. The chaining with open redirects on whitelisted domains is a sophisticated escalation technique. The content-type sniffing behavior, while intended for compatibility, creates an information disclosure vector that bypasses typical SSRF mitigation assumptions. The research underscores the importance of secure-by-default configurations and explicit security documentation in framework design.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
