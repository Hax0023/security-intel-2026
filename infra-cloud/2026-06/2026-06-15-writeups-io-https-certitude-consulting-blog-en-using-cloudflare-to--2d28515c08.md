# Using Cloudflare to Bypass Cloudflare - Cross-Tenant Security Control Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-15
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Disclosed as 'Informative' - Amount not specified
- **Severity:** High
- **Vuln types:** Cross-Tenant Security Bypass, Insufficient Access Controls, Trust Relationship Abuse, Shared Certificate Misuse, Inadequate Documentation
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers relying on platform-recommended origin server protection mechanisms can be bypassed by attackers using their own Cloudflare accounts to abuse the implicit trust relationship between Cloudflare and customer origins. Two key mechanisms—Authenticated Origin Pulls using shared Cloudflare certificates and IP allowlisting—are vulnerable to bypass attacks that render configured WAF and DDoS protections ineffective.

## Attack scenario (step by step)
1. Attacker registers a domain with Cloudflare and creates a Cloudflare account/tenant
2. Attacker points their domain's DNS A record to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS prevention) on their Cloudflare zone
4. Attacker crafts malicious requests (e.g., SQL injection, DDoS) and sends them through their Cloudflare account
5. Victim's origin server receives requests authenticated as legitimate Cloudflare traffic due to shared certificate or Cloudflare IP ranges
6. Victim's configured protections are bypassed because the traffic passed through Cloudflare infrastructure, bypassing their security controls

## Root cause
Cloudflare uses shared/global certificates and IP ranges for authenticating origin connections from all tenants. The trust model assumes all Cloudflare-sourced traffic is legitimate, without tenant isolation controls. Documentation fails to warn customers about the security implications of using shared certificates versus custom tenant-specific certificates. The per-design trust relationship between Cloudflare and customer origins is exploitable by any Cloudflare tenant.

## Attacker mindset
Opportunistic attacker seeking to evade WAF and DDoS protections by leveraging legitimate infrastructure relationships. Recognizes that cloud platform shared resources can be weaponized by insiders or competing tenants. Exploits the gap between documented security levels ('very secure') and actual implementation, targeting low-friction origin discovery and attack delivery.

## Defensive takeaways
- Use custom tenant-specific origin pull certificates instead of shared Cloudflare certificates; do not rely on convenience defaults for security-critical configurations
- Implement defense-in-depth at origin servers: multi-factor origin authentication, rate limiting, and request signing beyond IP-based allowlists
- Validate that origin server protection relies on mechanisms independent of Cloudflare's trust model (e.g., custom client certificates, cryptographic request signing)
- Review and harden origin server configurations to reject or rate-limit requests lacking additional authentication signals beyond Cloudflare IP ranges
- Adopt WAF rules at the origin server level as a redundant control independent of Cloudflare filtering
- Clearly document security implications and threat models for each protection mechanism, especially shared vs. custom configurations
- Consider origin server location/visibility restrictions and geographic IP filtering independent of Cloudflare IP ranges
- Implement per-request cryptographic validation (HMAC, signatures) that proves traffic passed through the legitimate Cloudflare tenant

## Variant hunting
['Test other CDN providers (Akamai, AWS CloudFront) for similar cross-tenant certificate sharing vulnerabilities', "Investigate whether Cloudflare's IP ranges can be enumerated and spoofed via compromised BGP/routing attacks", 'Examine if custom Cloudflare Worker scripts can be used to further obfuscate attack origins while transiting Cloudflare', "Check if Cloudflare's HTTP/2 Server Push or other protocol features can bypass origin authentication mechanisms", "Research whether Cloudflare's paid features (Advanced DDoS, Enterprise) implement stronger tenant isolation for certificate management", "Test if Cloudflare's API allows dynamic certificate rotation or tenant-specific certificate provisioning as mitigation", 'Analyze whether origin server logs can distinguish traffic from different Cloudflare tenants (likely cannot without custom headers)', 'Investigate other Cloudflare-adjacent services (Cloudflare Spectrum, Load Balancing) for similar tenant isolation gaps']

## MITRE ATT&CK
- T1190
- T1562.008
- T1021.001
- T1200
- T1557.002
- T1199

## Notes
Cloudflare closed this report as 'Informative' rather than actionable, suggesting the vendor considered this a customer configuration responsibility rather than a platform vulnerability. However, the documentation's rating of Authenticated Origin Pulls as 'very secure' without mentioning the shared certificate risk is misleading. This represents a documentation/design flaw in trust model communication. The researchers appropriately disclosed publicly after vendor rejection to enable customer remediation. This highlights the risk of implicit trust relationships in multi-tenant cloud platforms and the importance of defense-in-depth principles.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-15*
