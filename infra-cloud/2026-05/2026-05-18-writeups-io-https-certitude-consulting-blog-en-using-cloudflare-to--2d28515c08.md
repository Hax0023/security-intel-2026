# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Control Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-18
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Disclosed as 'Informative' and closed by Cloudflare; no bounty awarded
- **Severity:** High
- **Vuln types:** Broken Access Control, Insufficient Cross-Tenant Isolation, Shared Authentication Credential Abuse, Firewall/WAF Bypass
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare's origin server protection mechanisms suffer from cross-tenant security gaps that allow attackers to bypass customer-configured protections by leveraging their own Cloudflare accounts. The vulnerability stems from shared infrastructure trust relationships and the use of shared SSL certificates for origin authentication, enabling attackers to tunnel malicious traffic through Cloudflare's own infrastructure while bypassing configured firewalls and WAF rules.

## Attack scenario (step by step)
1. Attacker registers a domain and configures it with their own Cloudflare account
2. Attacker points the domain's DNS A record to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, etc.) on their own Cloudflare tenant for this domain
4. Attacker sends malicious requests through their Cloudflare infrastructure, which authenticates using the shared Cloudflare certificate trusted by the victim
5. Victim's origin server receives requests that appear legitimate (originating from Cloudflare IP ranges) and bypass configured firewall/WAF rules
6. Attack succeeds because traffic passed through Cloudflare infrastructure but bypassed victim's security controls

## Root cause
Two design flaws: (1) Authenticated Origin Pulls uses a shared Cloudflare certificate trusted for all tenants instead of per-tenant certificates, and (2) IP allowlisting of Cloudflare ranges trusts all traffic from Cloudflare infrastructure without verifying the requesting tenant's legitimacy or security posture. Documentation fails to clearly articulate the security implications of using shared vs. custom certificates.

## Attacker mindset
Sophisticated attacker recognizes that Cloudflare's infrastructure, intended as a protective intermediary, can be weaponized when one has legitimate access to the platform. By understanding the implicit trust relationship between Cloudflare and protected origins, the attacker exploits the multi-tenant architecture to blend malicious traffic with legitimate Cloudflare traffic, rendering customer security controls ineffective.

## Defensive takeaways
- Implement per-tenant or customer-specific certificates for origin authentication rather than shared certificates
- Use custom origin pull certificates instead of the default shared Cloudflare certificate
- Layer multiple protection mechanisms; do not rely solely on IP allowlisting or shared certificate authentication
- Implement additional origin-level controls independent of Cloudflare (e.g., rate limiting, behavioral analysis)
- Validate the authenticity of origin requests beyond IP address and certificate origin
- Review and clearly document all security implications of multi-tenant shared infrastructure in public documentation
- Consider implementing request signing or per-customer authentication tokens in addition to certificates
- Monitor for suspicious traffic patterns from Cloudflare IPs that bypass configured protections

## Variant hunting
Search for similar bypasses in other reverse-proxy and CDN services (Akamai, AWS CloudFront, Fastly) that use shared infrastructure. Investigate whether other Cloudflare protection mechanisms rely on tenant-implicit trust. Test whether custom Cloudflare domain configurations can bypass rate limiting, bot management, or DDoS protection. Examine whether the bypass extends to Cloudflare Workers or other tenant-controlled services.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (bypassing WAF through shared infrastructure)
- T1562.008 - Impair Defenses: Disable or Modify Cloud Logs
- T1021.005 - Remote Services: Cloud Services
- T1578.002 - Modify Cloud Compute Infrastructure: Create Cloud Instance
- T1199 - Trusted Relationship (exploiting implicit trust between Cloudflare and origin)

## Notes
Cloudflare's dismissal of this as 'Informative' appears problematic given the severity of the vulnerability affecting all customers using the documented protection mechanisms. The researchers' responsible disclosure and subsequent public release is justified given the closed-out status. This represents a fundamental architectural trust problem rather than a simple configuration issue, requiring platform-level remediation rather than customer-side workarounds. The vulnerability demonstrates how shared multi-tenant infrastructure can create security gaps even in mature security platforms.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-18*
