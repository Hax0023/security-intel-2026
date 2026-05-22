# Using Cloudflare to bypass Cloudflare - Cross-Tenant Security Control Bypass

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-22
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not specified (classified as 'Informative' and closed by Cloudflare)
- **Severity:** High
- **Vuln types:** Insufficient Access Control, Shared Credential Weakness, Cross-Tenant Security Bypass, Broken Trust Boundary, Improper Authentication
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare's origin server protection mechanisms contain gaps in cross-tenant security controls that allow attackers with their own Cloudflare accounts to bypass WAF, DDoS prevention, and firewall protections. Attackers can tunnel malicious traffic through Cloudflare infrastructure using shared certificates or spoofed origins, rendering customer protections ineffective. The vulnerability stems from implicit trust in all traffic originating from Cloudflare infrastructure regardless of the tenant initiating it.

## Attack scenario (step by step)
1. Attacker registers a domain and creates a Cloudflare account, gaining access to shared infrastructure
2. Attacker points their domain's DNS A record to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, etc.) on their own Cloudflare tenant
4. Attacker crafts malicious payloads and routes them through Cloudflare's reverse proxy servers
5. Victim's origin server receives traffic from trusted Cloudflare IP ranges with shared authentication certificates
6. Victim's configured protections are bypassed because traffic appears legitimate, originating from Cloudflare infrastructure

## Root cause
Cloudflare's documentation recommends using shared certificates for 'Authenticated Origin Pulls' without adequately disclosing that these certificates are shared across all tenants. The trust model implicitly assumes all traffic from Cloudflare infrastructure is trustworthy, failing to distinguish between different Cloudflare tenants. Custom tenant-specific certificates are relegated to API-only configuration without prominence in documentation, making the insecure shared certificate the default choice.

## Attacker mindset
An attacker recognizes that Cloudflare is widely trusted as a security provider and that customers naturally trust traffic originating from Cloudflare infrastructure. By abusing this trust relationship through their own Cloudflare account, they can bypass the very protections customers deployed. The attacker leverages the shared nature of cloud infrastructure and the principle that defenders often trust infrastructure providers more than they trust direct threats.

## Defensive takeaways
- Use tenant-specific custom certificates for 'Authenticated Origin Pulls' rather than shared Cloudflare certificates
- Implement additional origin server protections independent of Cloudflare (layered security approach)
- Configure strict origin validation logic that goes beyond IP allowlisting of infrastructure providers
- Review and understand the implicit trust assumptions in documented protection mechanisms
- Implement additional authentication or challenge-response mechanisms at the origin server layer
- Monitor for suspicious patterns in traffic originating from trusted infrastructure providers
- Document and prominently highlight security trade-offs and implications of shared vs. custom credentials
- Consider implementing cryptographic origin verification that cannot be spoofed through legitimate CDN paths

## Variant hunting
['Other CDN/proxy providers (Akamai, Cloudflare, AWS CloudFront, etc.) using shared authentication mechanisms', 'WAF bypass techniques through legitimate infrastructure provider trust relationships', 'Multi-tenant SaaS platforms where tenants can route traffic through shared infrastructure', 'API gateway protection mechanisms relying on shared certificates across tenants', 'Load balancer authentication where shared credentials authenticate multiple tenants', 'Reverse proxy implementations in containerized/Kubernetes environments with shared certificates']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1021 - Remote Services
- T1199 - Trusted Relationship
- T1566 - Phishing
- T1561 - Disk Wipe
- T1498 - Network Denial of Service

## Notes
This vulnerability was responsibly disclosed to Cloudflare but dismissed as 'Informative' with no fix implemented, prompting public disclosure. The core issue represents a fundamental architectural weakness where legitimate infrastructure trust is weaponized by malicious actors within the same ecosystem. The vulnerability highlights the critical importance of tenant isolation in multi-tenant security platforms and the dangers of relying solely on infrastructure-level protections. Cloudflare customers using shared certificates remain vulnerable; migration to custom certificates is the primary mitigation but requires API knowledge and certificate management overhead.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-22*
