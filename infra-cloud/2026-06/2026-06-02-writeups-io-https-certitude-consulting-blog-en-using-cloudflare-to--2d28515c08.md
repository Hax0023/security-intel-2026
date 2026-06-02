# Using Cloudflare to Bypass Cloudflare - Cross-Tenant Security Control Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-02
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Closed as Informative (no bounty awarded)
- **Severity:** High
- **Vuln types:** Insufficient Access Control, Trust Boundary Violation, Cross-Tenant Security Bypass, Shared Infrastructure Abuse
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers can have their configured protection mechanisms (WAF, DDoS prevention, firewall rules) bypassed by attackers who abuse the inherent trust relationship between Cloudflare infrastructure and customer origin servers. Attackers can register their own Cloudflare accounts, configure malicious domains pointing to victim infrastructure, and tunnel attack traffic through Cloudflare's shared infrastructure to evade customer-configured protections. This gap exists due to undocumented security implications of using shared Cloudflare certificates and overly broad IP allowlisting strategies.

## Attack scenario (step by step)
1. Attacker identifies a target website protected by Cloudflare with customer-configured WAF, DDoS, or firewall rules
2. Attacker registers their own Cloudflare account and creates a new domain under their control
3. Attacker configures DNS A record for their domain to point to victim's origin server IP address
4. Attacker disables all protection features on their domain to allow unfiltered traffic transmission
5. Attacker crafts malicious payloads (SQL injection, XSS, DDoS, etc.) and sends them through their Cloudflare tenant
6. Victim's origin server accepts the traffic as legitimate since it originated from Cloudflare infrastructure, bypassing all configured protections

## Root cause
Cloudflare's design uses shared certificates and shared IP address ranges across all tenants without enforcing per-tenant trust boundaries. The documentation fails to clearly communicate that using shared Cloudflare certificates or IP allowlisting creates a vulnerability where any Cloudflare tenant can act as a proxy to the victim's origin server. The security model assumes all Cloudflare traffic is trustworthy, but does not account for malicious Cloudflare customers.

## Attacker mindset
An attacker recognizes that Cloudflare customers implicitly trust traffic originating from Cloudflare infrastructure as pre-filtered and safe. By becoming a Cloudflare customer themselves, they can leverage this trust relationship to tunnel attacks through legitimate infrastructure, transforming Cloudflare from a protection mechanism into an attack vector. The attacker exploits the documentation gap and convenience-over-security default configuration to achieve impact with minimal detection risk.

## Defensive takeaways
- Use custom tenant-specific certificates for Authenticated Origin Pulls instead of shared Cloudflare certificates
- Implement origin server IP filtering at the firewall level, not just DNS/WAF level, to prevent origin discovery
- Use additional authentication mechanisms beyond IP allowlisting (e.g., custom headers, mutual TLS with customer-controlled certificates)
- Implement rate limiting and request anomaly detection at the origin server level independent of Cloudflare
- Review and strengthen origin server security posture as if it were internet-facing, regardless of Cloudflare protection
- Monitor for unexpected traffic patterns originating from Cloudflare IP ranges
- Implement request header validation and ensure custom headers are required from legitimate proxies
- Consider using Cloudflare's custom hostname features with stricter isolation controls if available

## Variant hunting
Similar bypass techniques likely exist in other CDN/reverse-proxy shared infrastructure platforms (Akamai, Fastly, AWS CloudFront) where multi-tenant architectures trust all traffic from the service. Look for scenarios where: (1) shared certificates are used across tenants, (2) IP allowlisting assumes infrastructure-level filtering, (3) documentation obscures security implications, (4) convenience defaults override security, (5) trust boundaries between tenants are not explicitly enforced. Test whether other proxy services allow registering arbitrary origin IPs and disabling protections per-domain.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1016 - System Network Configuration Discovery
- T1557 - Man-in-the-Middle (Network Relay)
- T1578 - Modify Cloud Compute Infrastructure (Domain Registration)
- T1562 - Impair Defenses (Disable Protection Features)

## Notes
The disclosure was categorized as 'Informative' by Cloudflare and not treated as a security vulnerability, likely due to the argument that this is a customer misconfiguration issue rather than a platform flaw. However, the undocumented nature of the risk and convenient-but-insecure defaults make this a design flaw. The researchers responsibly disclosed despite the dismissal, which is commendable for customer awareness. This represents a fundamental trust model problem in multi-tenant CDN architectures where shared resources must be protected against abuse by other tenants.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-02*
