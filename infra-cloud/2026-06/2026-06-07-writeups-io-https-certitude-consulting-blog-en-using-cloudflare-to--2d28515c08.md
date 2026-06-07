# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Control Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-07
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (categorized as 'Informative' and closed)
- **Severity:** High
- **Vuln types:** Broken Access Control, Insufficient Cross-Tenant Isolation, Weak Origin Server Authentication, Trust Relationship Abuse
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare's recommended origin server protection mechanisms contain critical gaps in cross-tenant security controls that allow attackers with their own Cloudflare accounts to bypass customer-configured security protections (WAF, DDoS prevention) by tunneling malicious traffic through Cloudflare's infrastructure. The vulnerability exploits the implicit trust relationship between Cloudflare infrastructure and customer origin servers, rendering configured protection mechanisms ineffective.

## Attack scenario (step by step)
1. Attacker registers a malicious domain with Cloudflare and creates a new tenant account
2. Attacker modifies DNS A record to point their malicious domain to victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, rate limiting) on their malicious domain tenant
4. Attacker sends crafted malicious payloads through their Cloudflare tenant infrastructure to victim's origin server
5. Victim's origin server receives requests originating from Cloudflare IP ranges with valid Cloudflare certificates, bypassing victim's configured WAF and DDoS rules
6. Attack succeeds because victim's protections are configured to trust all Cloudflare infrastructure traffic indiscriminately

## Root cause
Cloudflare uses shared, tenant-agnostic certificates and IP address ranges for origin server authentication. The documentation recommends trusting 'all traffic from Cloudflare' without explaining that attackers can abuse their own Cloudflare accounts to route traffic through Cloudflare infrastructure, bypassing the victim's configured security policies. The design assumes benign actors only, without accounting for adversarial tenants on the same platform.

## Attacker mindset
A sophisticated attacker recognizes that security-conscious victims trust Cloudflare infrastructure implicitly and configure origin servers to accept any traffic bearing Cloudflare credentials. By obtaining a legitimate Cloudflare account and registioning a malicious domain pointing to the victim's infrastructure, the attacker converts the victim's trusted security provider into an attack vector, weaponizing the very infrastructure meant to protect against such attacks.

## Defensive takeaways
- Do not rely solely on shared Cloudflare certificates for origin authentication; implement custom, tenant-specific origin pull certificates
- Validate that origin server authentication mechanisms are tenant-specific, not infrastructure-wide
- Implement additional origin server-side verification beyond IP whitelisting and shared certificates
- Review and validate that all configured security policies (WAF rules, rate limiting, DDoS protection) are actually enforced before traffic reaches the origin
- Consider implementing mutual TLS with custom certificates even for Cloudflare connections
- Segment origin servers from direct internet access and limit authenticated origins to specific certificate fingerprints or custom CAs
- Monitor origin server logs for anomalous access patterns from expected Cloudflare IPs
- Document the security implications and limitations of origin protection mechanisms in customer-facing documentation

## Variant hunting
Review other cloud infrastructure providers (AWS CloudFront, Akamai, Fastly) for similar shared authentication mechanisms. Investigate other Cloudflare services that authenticate based on provider infrastructure rather than tenant identity (Argo Tunnel, Load Balancing, Cache). Examine whether other reverse proxy or CDN vendors implement per-tenant vs. infrastructure-wide authentication. Search for similar trust-relationship exploitation patterns in multi-tenant SaaS platforms providing security services.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship (abusing trust in Cloudflare provider)
- T1578 - Modify Cloud Compute Infrastructure (DNS manipulation)
- T1562 - Impair Defenses (bypassing WAF/DDoS controls)
- T1021 - Remote Services (leveraging legitimate Cloudflare infrastructure)
- T1565 - Data Manipulation (potential unauthorized access to origin servers)

## Notes
This vulnerability was responsibly disclosed to Cloudflare who categorized it as 'Informative' rather than a security issue, suggesting they view the documented origin protection mechanisms as sufficient guidance rather than guaranteed security. The researchers decided to publicly disclose due to Cloudflare's dismissal. This represents a significant gap between customer expectations of 'very secure' mechanisms and actual security guarantees. The vulnerability requires customer misconfiguration (trusting all Cloudflare traffic) but the official documentation appears to encourage this configuration without adequate security warnings. Mitigation requires customers to deviate from officially recommended simple approaches and implement custom certificate management, increasing operational complexity. This is a supply-chain security issue where the security vendor itself becomes a pivot point for attacks.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-07*
