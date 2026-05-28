# SSRF Bypass via HTTP Redirect to Extract AWS Metadata Through Cloudflare

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Redacted (Confidential)
- **Bounty:** Not disclosed
- **Severity:** Critical
- **Vuln types:** Server-Side Request Forgery (SSRF), Insufficient Input Validation, Metadata Exposure, IAM Credential Leakage
- **Category:** infra-cloud
- **Writeup:** https://infosecwriteups.com/an-exciting-journey-to-find-ssrf-bypass-cloudflare-and-extract-aws-metadata-fdb8be0b5f79

## Summary
A critical SSRF vulnerability in a PDF download endpoint allowed an attacker to bypass localhost/AWS metadata IP restrictions and Cloudflare filtering through HTTP 302 redirect chaining. By redirecting requests through a controlled server, the attacker extracted AWS IAM security credentials from the instance metadata service (169.254.169.254), gaining access to production AWS resources.

## Attack scenario (step by step)
1. Attacker discovers a PDF download endpoint accepting arbitrary URLs: /api/download-pdf?url=
2. Direct access to localhost and 169.254.169.254 is blocked by server-side filters and Cloudflare WAF
3. Attacker creates a malicious Django server configured to respond with HTTP 302 redirects
4. Attacker sends a request to the vulnerable endpoint pointing to their attacker-controlled server
5. Server follows the 302 redirect to 169.254.169.254/latest/meta-data/iam/security-credentials/, bypassing filters
6. AWS metadata and IAM role credentials are extracted and returned to the attacker

## Root cause
The application implemented input validation/filtering on the initial request URL but failed to validate or restrict redirect targets. The server blindly followed HTTP 3xx redirects without re-applying the same security controls, allowing bypass of IP-based restrictions. Cloudflare filtering was also circumvented through the redirect chain.

## Attacker mindset
Persistent reconnaissance and enumeration of bypass techniques. When direct exploitation failed, the attacker researched alternative SSRF vectors (different localhost representations, protocols) and studied redirect-based bypass documentation. Upon discovering redirect chains could bypass filters, the attacker quickly weaponized this with a simple Django server to achieve credential extraction.

## Defensive takeaways
- Implement SSRF protections on all redirect targets, not just initial requests
- Disable or strictly control HTTP redirects (3xx responses) in server-side request contexts
- Implement allowlist-based validation for URLs rather than blacklist approaches
- Block known metadata service IPs (169.254.169.254) at the application layer
- Use AWS IMDSv2 with session tokens instead of IMDSv1 to prevent SSRF metadata extraction
- Implement request signing and mutual TLS for internal service-to-service communication
- Monitor outbound requests to unusual destinations and AWS metadata endpoints
- Apply consistent security controls across the entire request chain (initial + redirects)

## Variant hunting
['Test for redirect chaining through multiple intermediate servers to evade multi-layer filtering', 'Explore DNS rebinding attacks combined with SSRF to bypass IP whitelists', 'Investigate if other redirect codes (301, 307, 308) behave differently than 302', 'Test for SSRF in other endpoints accepting URLs: image proxies, webhook handlers, URL shorteners', 'Attempt to extract credentials from other cloud metadata services (Azure IMDS, GCP metadata)', 'Check if alternative AWS credential endpoints or paths are accessible via SSRF', 'Research if Cloudflare can be bypassed through HTTP/2 push, CONNECT tunneling, or header injection']

## MITRE ATT&CK
- T1190
- T1552.005
- T1589.001
- T1538
- T1496

## Notes
This writeup demonstrates the critical risk of AWS IMDSv1 exposure combined with SSRF vulnerabilities. The redirect-based bypass is a well-known technique but highly effective against simplistic blacklist filters. The attacker's iterative approach (direct attempts → protocol variants → redirect chains) is representative of real-world SSRF exploitation. The confidential nature of the target program prevents validation of the actual impact and bounty awarded.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
