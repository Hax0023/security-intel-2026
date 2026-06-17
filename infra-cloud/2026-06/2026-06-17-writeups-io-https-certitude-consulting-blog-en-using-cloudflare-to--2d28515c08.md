# Using Cloudflare to Bypass Cloudflare - Cross-Tenant Security Gap in Origin Server Protection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-17
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Closed as 'Informative' - no monetary bounty awarded
- **Severity:** High
- **Vuln types:** Broken Access Control, Insufficient Cross-Tenant Isolation, Shared Certificate Abuse, Trust Boundary Violation
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' configured security mechanisms (WAF, DDoS protection) can be bypassed because Cloudflare shares authentication certificates and IP address ranges across all tenants. An attacker can register their own Cloudflare account, point it to a victim's origin server, and tunnel malicious traffic through Cloudflare's infrastructure to circumvent the victim's security controls. The vulnerability stems from design decisions that assume all traffic from Cloudflare is trustworthy without verifying which tenant initiated it.

## Attack scenario (step by step)
1. Attacker registers a Cloudflare account and creates a custom domain (attacker-domain.com)
2. Attacker modifies DNS A record for their domain to point to victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, Bot Management) on their Cloudflare tenant
4. Attacker sends malicious payload through their Cloudflare account, which routes traffic through Cloudflare's reverse proxy infrastructure
5. Victim's origin server receives the request with a shared Cloudflare certificate or from Cloudflare's IP ranges and trusts it implicitly
6. Victim's security controls are bypassed because the request appears to originate from Cloudflare, not the attacker

## Root cause
Cloudflare's origin server protection mechanisms rely on implicit trust of all traffic originating from Cloudflare infrastructure without implementing per-tenant verification. Two specific issues: (1) Shared SSL certificates across all Cloudflare tenants for 'Authenticated Origin Pulls' - any tenant can use the same certificate; (2) Allowlisting Cloudflare IP ranges without distinguishing which tenant the connection represents, combined with DNS resolution allowing any tenant to point domains to arbitrary IPs.

## Attacker mindset
An attacker recognizes that security vendors create trust relationships between their infrastructure and customers' systems. By becoming a customer of that same vendor, the attacker can abuse the per-design trust model. The attacker exploits poor documentation that doesn't clearly communicate security implications of convenient default options (shared certificates vs. custom certificates) and the lack of cross-tenant isolation verification in what should be isolated security perimeters.

## Defensive takeaways
- Always use tenant-specific or custom authentication credentials (custom origin pull certificates) rather than shared certificates, even if less convenient
- Do not rely solely on IP allowlisting as a security control - combine with additional authentication mechanisms
- Implement defense-in-depth at the origin server level: verify mutual TLS, implement rate limiting, monitor for suspicious patterns
- Clearly document security implications of configuration choices, explicitly warning about shared credentials
- Implement per-tenant isolation verification in security intermediaries
- Require origin servers to validate not just the source (Cloudflare IP), but also authenticate the legitimacy of the request
- Review all third-party security service integrations for implicit trust assumptions

## Variant hunting
['Similar trust-relationship bypasses in other reverse proxy/WAF providers (AWS WAF, Akamai, Imperva) - can attackers use competitor accounts to bypass protections?', 'Other Cloudflare services with shared infrastructure - do other products have similar cross-tenant isolation issues?', 'DNS-based bypasses in other CDN services - can attackers re-point domains to origin servers via competitor CDNs?', 'Shared authentication tokens or API keys across tenants in other security platforms', 'Certificate pinning bypass scenarios in reverse proxy architectures', 'Rate limiting bypasses through multi-tenant abuse of shared infrastructure quotas']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1562 - Impair Defenses
- T1021 - Remote Services
- T1056 - Adversary-in-the-Middle
- T1078 - Valid Accounts

## Notes
This vulnerability highlights a fundamental tension in multi-tenant security services: convenience vs. security. Cloudflare categorized this as 'Informative' rather than a critical vulnerability, possibly because it requires customer misconfiguration and doesn't directly compromise Cloudflare's infrastructure. However, the impact on Cloudflare customers is significant. The researcher responsibly disclosed and later published findings because the issue wasn't fixed and customers need to understand the risks. The vulnerability demonstrates that security controls can be circumvented by becoming a customer of the same security provider - a novel attack vector for practitioners to consider.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-17*
