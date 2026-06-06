# Using Cloudflare to bypass Cloudflare - Cross-Tenant Security Control Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-06
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (Cloudflare categorized as 'Informative' and closed)
- **Severity:** High
- **Vuln types:** Insufficient Access Control, Broken Authentication, Trust Boundary Violation, Cross-Tenant Security Weakness, Configuration Flaw
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers relying on origin server protection mechanisms can be bypassed by attackers who leverage their own Cloudflare accounts to exploit the implicit trust relationship between Cloudflare infrastructure and protected origin servers. Attackers can register a domain with Cloudflare, point it to victim's origin server, disable protections, and tunnel malicious traffic through Cloudflare's shared infrastructure, completely circumventing the victim's configured WAF, DDoS, and bot management protections.

## Attack scenario (step by step)
1. Attacker registers a domain and creates a Cloudflare account
2. Attacker configures the domain's DNS A record to point to victim's origin server IP address
3. Attacker disables all Cloudflare protection features (WAF, DDoS, Bot Management) for their attacker-controlled domain
4. Attacker tunnels malicious requests through their own Cloudflare tenant to reach victim's origin server
5. Victim's origin server receives requests with Cloudflare IP source (trusted) and shared Cloudflare certificate, bypassing victim's configured protections
6. Attack succeeds because victim's origin server implicitly trusts all traffic from Cloudflare infrastructure without tenant verification

## Root cause
Cloudflare's design uses shared infrastructure and shared certificates (Authenticated Origin Pulls) for all tenant traffic. The origin server protection mechanisms documented by Cloudflare assume implicit trust in all traffic originating from Cloudflare infrastructure, without implementing tenant-specific authentication or verification. This creates a cross-tenant security gap where one tenant can abuse Cloudflare's infrastructure to attack another tenant's protected resources.

## Attacker mindset
Cost-effective reconnaissance and attack delivery - attackers realize they can leverage Cloudflare's trusted relationship and shared infrastructure to bypass expensive protection mechanisms. This represents a 'living off the land' technique, weaponizing the victim's own chosen security provider against them. The attacker recognizes the implicit trust model creates a bypass opportunity with minimal detection risk since traffic appears legitimate.

## Defensive takeaways
- Implement tenant-specific or custom origin pull certificates instead of relying on Cloudflare's shared certificates
- Verify origin pull certificate chain includes tenant-specific identifiers or use mutual TLS with custom CAs
- Layer origin server protections beyond reverse-proxy trust: implement WAF/rate-limiting on origin server itself
- Use origin server-level authentication that validates specific Cloudflare zone/tenant identifiers, not just IP ranges or certificates
- Review Cloudflare documentation for unstated security implications of 'convenient' default options vs. 'secure' alternatives
- Monitor origin server logs for requests with unexpected Host headers or DNS mismatches
- Implement geographic/behavioral anomaly detection at origin server level independent of Cloudflare
- Regularly audit origin server access logs to identify traffic patterns inconsistent with expected Cloudflare behavior
- Document and enforce use of custom certificates in organizational Cloudflare policies

## Variant hunting
['Similar trust-based bypasses in other CDN providers (AWS CloudFront, Akamai, Fastly) where shared infrastructure may be abused', 'Other Cloudflare services using shared certificates or IP-based trust (e.g., API Shield, Workers, Load Balancing)', "DNS-level attacks leveraging Cloudflare's DNS service to redirect traffic for customers on other CDNs", "Abuse of Cloudflare's Page Rules or Workers to inject payloads into victim domains configured on attacker's account", 'Multi-tenant origin server scenarios where shared certificates could expose one customer to another', "Cloudflare's IP ranges used in corporate firewall allowlists without tenant verification - can be abused by attackers on Cloudflare"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (bypass of WAF protections)
- T1021 - Remote Services (abusing trusted reverse-proxy connection)
- T1578 - Modify Cloud Compute Infrastructure (misconfigured Cloudflare tenant setup)
- T1562 - Impair Defenses (disabling protections on attacker-controlled domain)
- T1199 - Trusted Relationship (exploiting Cloudflare-origin server trust)
- T1598 - Phishing (could deliver payloads bypassing victim's WAF)

## Notes
Cloudflare's categorization as 'Informative' rather than a security vulnerability is questionable - this represents a fundamental flaw in their multi-tenant architecture. The vulnerability requires customers to use undocumented/inconvenient mitigations (custom certificates, API configuration). The public disclosure is valuable for customers to understand their actual security posture. This demonstrates the risk of implicit trust models in shared infrastructure - each tenant must be individually verified, not trusted based on infrastructure source alone.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-06*
