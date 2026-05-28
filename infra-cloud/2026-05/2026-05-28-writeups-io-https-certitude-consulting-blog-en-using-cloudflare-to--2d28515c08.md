# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Control Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-28
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Closed as Informative (non-eligible for bounty)
- **Severity:** High
- **Vuln types:** Insufficient Access Control, Cross-Tenant Security Bypass, Weak Certificate Validation, Trust Boundary Violation, Inadequate Documentation
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare's documented origin server protection mechanisms contain critical gaps that allow attackers with their own Cloudflare accounts to bypass customer-configured security controls by routing malicious traffic through Cloudflare's infrastructure. Two primary mechanisms—Authenticated Origin Pulls using shared certificates and IP allowlisting—can be circumvented because they implicitly trust all Cloudflare tenant connections. This design flaw renders configured WAF, DDoS prevention, and Bot management protections ineffective against attackers who are themselves Cloudflare customers.

## Attack scenario (step by step)
1. Attacker registers a malicious domain and creates a Cloudflare tenant account
2. Attacker points their domain's DNS A record to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, etc.) on their Cloudflare tenant configuration
4. Attacker crafts malicious payloads and routes them through their Cloudflare account toward the victim's origin server
5. Victim's origin server accepts the connection because it originates from Cloudflare infrastructure (trusted source) and matches Cloudflare IP ranges or certificate
6. Attack bypasses all security mechanisms the victim configured in their Cloudflare tenant, directly impacting the origin server

## Root cause
Cloudflare's architecture implements per-design implicit trust between Cloudflare infrastructure and customer origin servers without tenant-specific authentication. The shared Cloudflare certificate used in Authenticated Origin Pulls does not differentiate between legitimate and malicious Cloudflare tenants. IP allowlisting trusts entire Cloudflare IP ranges without validating that traffic actually passed through the specific customer's Cloudflare account. Documentation does not adequately explain the security implications of these design choices, leading customers to adopt inherently bypassable configurations.

## Attacker mindset
An attacker with moderate technical knowledge recognizes that Cloudflare's trust model creates an exploitable pathway. By becoming a Cloudflare customer themselves, they gain legitimate access to Cloudflare infrastructure and can weaponize it against other customers. This approach is attractive because it appears legitimate (traffic comes from Cloudflare), requires minimal sophistication, and bypasses expensive security solutions that organizations paid for specifically to protect against external attacks.

## Defensive takeaways
- Mandate use of custom tenant-specific certificates for origin authentication rather than shared Cloudflare certificates; document this requirement prominently
- Implement per-tenant certificate validation that cryptographically proves traffic passed through a specific customer's Cloudflare account
- Replace IP allowlisting with cryptographic origin verification; IP ranges alone are insufficient for multi-tenant environments
- Add explicit security warnings in documentation highlighting that shared certificates trust all Cloudflare tenants
- Implement request signing or additional headers that prove traffic passed through the customer's specific Cloudflare account configuration
- Provide automation or simplified tooling for custom certificate management to reduce adoption friction
- Consider architectural changes to the reverse-proxy that enforce per-tenant security policy at the infrastructure level

## Variant hunting
Search for similar trust-boundary violations in other reverse-proxy or CDN services (Akamai, Cloudflare competitors, AWS CloudFront). Examine whether other 'origin authentication' mechanisms in Cloudflare (custom certificates, mTLS configurations) have similar tenant-confusion issues. Investigate if Cloudflare's API allows enumeration or manipulation of origin configurations. Check whether Cloudflare HTTP headers (CF-Connecting-IP, CF-Ray) can be spoofed to further bypass origin-level protections. Test whether customers using multiple Cloudflare zones with different protection levels can leak traffic between tenants.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1563 - Impair Defenses
- T1021 - Remote Services
- T1578 - Modify Cloud Compute Infrastructure
- T1562 - Impair Defenses

## Notes
Cloudflare's dismissal of this as 'Informative' rather than a security vulnerability is controversial given the impact on downstream customers. The researchers responsibly disclosed and publicly shared details after rejection, which is appropriate given the systemic nature affecting all customers using these mechanisms. The vulnerability highlights a fundamental architectural challenge in multi-tenant reverse-proxy services: implicit trust models do not scale securely. This is not a bug in traditional sense but a design limitation that requires customer awareness and workaround adoption.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-28*
