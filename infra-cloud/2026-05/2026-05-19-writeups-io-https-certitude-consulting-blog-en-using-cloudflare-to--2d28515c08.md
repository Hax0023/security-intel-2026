# Using Cloudflare to bypass Cloudflare

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-19
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Categorized as 'Informative' and closed without monetary award
- **Severity:** High
- **Vuln types:** Cross-tenant security bypass, Insufficient access control, Trust boundary violation, Shared certificate vulnerability, Weak origin server authentication
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers using official origin server protection mechanisms can have their security controls bypassed by attackers leveraging their own Cloudflare accounts. Attackers can tunnel malicious traffic through Cloudflare's infrastructure using shared certificates or IP ranges, circumventing WAF, DDoS, and bot management protections. The vulnerability stems from design flaws in origin authentication that treat all Cloudflare-originated traffic as trusted regardless of tenant isolation.

## Attack scenario (step by step)
1. Attacker registers a domain and creates a Cloudflare account, pointing their domain's DNS A record to the victim's origin server IP address
2. Attacker disables all Cloudflare protection features (WAF, DDoS, bot management) on their malicious domain
3. If victim uses 'Authenticated Origin Pulls' with shared Cloudflare certificates, attacker tunnels requests through their Cloudflare tenant using the same certificate chain
4. Victim's origin server accepts the connection because it originated from Cloudflare infrastructure (verified by shared certificate)
5. Attacker's malicious payload bypasses victim's configured protection mechanisms and reaches the origin server directly
6. Attack succeeds because victim's protections were designed to only protect against non-Cloudflare traffic

## Root cause
Design flaw in Cloudflare's origin authentication strategy: (1) Shared certificates used across all tenants create implicit cross-tenant trust; (2) Documentation recommends 'very secure' mechanisms without clearly stating security implications of using shared vs. custom certificates; (3) No tenant isolation enforced at the certificate or IP allowlist level; (4) The per-design trust relationship between Cloudflare and origin servers is abused by attackers who are also legitimate Cloudflare customers.

## Attacker mindset
An attacker thinks: 'Cloudflare customers trust all traffic from Cloudflare infrastructure. If I register my own Cloudflare account and point it to their origin server, I can piggyback on that trust relationship to bypass their security controls. They configured protection against external attackers, not against attacks coming through Cloudflare itself. This is a design assumption I can exploit.'

## Defensive takeaways
- Do not rely solely on shared certificate-based authentication; implement custom origin pull certificates with tenant-specific CAs
- IP allowlisting is insufficient; combine with additional origin server authentication mechanisms (mutual TLS with custom certificates, origin tokens, shared secrets)
- Review Cloudflare configuration to ensure origin server protection is not dependent on trust of the Cloudflare platform itself
- Implement defense-in-depth at the origin server level: rate limiting, request signing, custom authentication headers independent of Cloudflare
- Understand the security model: Cloudflare protections are designed for external threats, not for attacks leveraging Cloudflare's own infrastructure
- Explicitly configure origin server to reject requests that did not pass through your specific Cloudflare zone configuration
- Document and audit which protection mechanisms rely on implicit Cloudflare infrastructure trust

## Variant hunting
Look for similar trust-boundary bypasses in other CDN/reverse-proxy services (Akamai, Cloudfront, etc.) where shared certificates or IP ranges could be abused. Investigate whether WAF rules can detect traffic originating from attacker-controlled Cloudflare zones. Check if DNS-level controls (CNAME protection) or origin server IP pinning are viable mitigations. Research whether attackers can abuse other Cloudflare tenant features (Page Rules, Workers, Tunnels) to bypass origin protections.

## MITRE ATT&CK
- T1190
- T1598
- T1566
- T1021
- T1040
- T1557

## Notes
Cloudflare categorized this as 'Informative' rather than a security vulnerability, suggesting they view this as a configuration/documentation issue rather than a bug. However, the researchers responsibly disclosed publicly to allow customers to mitigate. The core issue is architectural: the shared infrastructure that makes Cloudflare convenient also creates a trust model that can be abused by other Cloudflare customers. Mitigation requires customers to implement compensating controls at the origin server level rather than relying on Cloudflare infrastructure isolation.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-19*
