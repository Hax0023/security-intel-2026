# Using Cloudflare to bypass Cloudflare - Cross-Tenant Security Controls Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-19
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** None (Closed as 'Informative')
- **Severity:** High
- **Vuln types:** Insufficient Access Controls, Shared Certificate Weakness, Cross-Tenant Trust Abuse, Bypass of WAF/DDoS Protection, Improper Documentation of Security Implications
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare's origin server protection mechanisms rely on a flawed trust model that assumes all traffic from Cloudflare infrastructure is legitimate. Attackers can abuse this by registering their own Cloudflare accounts, pointing custom domains to victim IPs, and tunneling malicious traffic through Cloudflare's infrastructure to bypass customer-configured protections like WAF and DDoS mitigation. The vulnerability stems from shared authentication certificates and inadequate cross-tenant isolation controls.

## Attack scenario (step by step)
1. Attacker registers a malicious domain with their own Cloudflare account
2. Attacker configures DNS A record pointing to victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, Bot Management) on their malicious domain in Cloudflare
4. Attacker sends crafted malicious traffic through Cloudflare's reverse proxy infrastructure targeting the victim's origin server
5. Victim's origin server receives traffic from Cloudflare IP ranges and permits it due to allowlisting or authenticated origin pull mechanisms
6. Malicious payload bypasses victim's configured Cloudflare protections and successfully compromises origin server

## Root cause
Cloudflare's security architecture relies on implicit trust of all connections originating from Cloudflare infrastructure. The 'Authenticated Origin Pulls' mechanism uses a shared, tenant-agnostic Cloudflare certificate by default rather than requiring tenant-specific custom certificates. Additionally, the 'Allowlist Cloudflare IP addresses' mechanism trusts all connections from Cloudflare IP ranges without verifying which tenant initiated them. The documentation fails to clearly articulate the security implications of these design choices, leading customers to unknowingly adopt vulnerable configurations.

## Attacker mindset
An attacker recognizes that major CDN/security providers like Cloudflare are universally trusted by their customers. By abusing the provider's own infrastructure, the attacker bypasses security controls that would normally detect and block direct attacks. The attacker leverages the assumption that traffic from the security provider is inherently safe, turning the protection mechanism into an attack vector. This represents sophisticated thinking about third-party trust relationships and shared infrastructure weaknesses.

## Defensive takeaways
- Implement mandatory tenant-specific authentication credentials rather than shared certificates for origin authentication
- Require explicit documentation of security trade-offs for all protection mechanisms, especially those relying on implicit trust models
- Provide opt-in enforcement for custom certificates with clear guidance on security implications of default options
- Implement per-tenant rate limiting and anomaly detection on reverse proxy infrastructure to detect abuse patterns
- Add origin server protection best practices: verify originating tenant ID alongside IP allowlisting, implement additional authentication layers, use custom certificates exclusively
- Consider implementing a Cloudflare Tenant ID header signed with tenant-specific keys that origin servers can validate
- Regularly audit and document cross-tenant trust boundaries in shared infrastructure services
- Provide clear warnings in documentation when security mechanisms rely on implicit trust assumptions

## Variant hunting
['Check for similar bypass mechanisms in other CDN providers (Akamai, AWS CloudFront, Fastly) that use shared certificates or implicit trust', 'Investigate if other Cloudflare authentication mechanisms (e.g., mTLS configurations) suffer from similar cross-tenant issues', 'Test whether Cloudflare Page Rules or Worker transformations can be abused to bypass origin protections through tenant-agnostic mechanisms', 'Examine if other cloud providers with reverse proxy offerings (AWS WAF, Azure Application Gateway) properly isolate tenant traffic', "Check if Cloudflare's custom certificate option properly prevents the described attack and if implementation is straightforward enough for adoption"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1218 - System Binary Proxy Execution (abusing legitimate Cloudflare infrastructure)
- T1199 - Trusted Relationship (abusing trust relationship between Cloudflare and origin servers)
- T1021 - Remote Services (leveraging Cloudflare proxy to reach restricted origin server)
- T1556 - Modify Authentication Process (exploiting weak authentication between Cloudflare and origin)

## Notes
The researchers conducted responsible disclosure but Cloudflare dismissed the report as 'Informative' without fixing the underlying architectural issue. This decision by Cloudflare to not address the vulnerability while the researchers publicly disclosed it highlights tension between vendor dismissal and researcher responsibility. The vulnerability is particularly serious because it affects a core security premise of Cloudflare's service offering. Organizations using Cloudflare for protection must implement custom origin certificates and additional authentication layers to compensate for this architectural gap. The bug demonstrates how implicit trust assumptions in multi-tenant shared infrastructure can become a critical vulnerability vector.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-19*
