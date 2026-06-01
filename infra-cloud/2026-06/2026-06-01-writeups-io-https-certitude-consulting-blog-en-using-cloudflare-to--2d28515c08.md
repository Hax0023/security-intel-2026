# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Gap in Origin Server Protection

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-01
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Disclosed as 'Informative' - No monetary bounty awarded
- **Severity:** High
- **Vuln types:** Broken Access Control, Improper Cross-Tenant Isolation, Insufficient Security Documentation, Trust Boundary Violation, Shared Credential Misuse
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' origin server protection mechanisms can be bypassed by attackers using their own Cloudflare accounts to tunnel malicious traffic through Cloudflare's infrastructure. The vulnerability stems from shared trust relationships and insufficient tenant isolation in Cloudflare's recommended protection strategies. This undermines the security value of protections like WAF, DDoS prevention, and bot management that customers rely upon.

## Attack scenario (step by step)
1. Attacker registers a domain with Cloudflare and creates a Cloudflare tenant account
2. Attacker points their domain's DNS A record to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, bot management) in their own Cloudflare configuration
4. Attacker crafts malicious payloads and sends them through Cloudflare's reverse proxy infrastructure targeting the victim's origin server
5. Victim's origin server receives requests appearing to originate from trusted Cloudflare infrastructure, bypassing victim's configured protections
6. Attack succeeds because origin server trusts all Cloudflare-originated traffic without validating the source tenant

## Root cause
Cloudflare's recommended origin server protection mechanisms rely on implicit trust of all traffic originating from Cloudflare infrastructure without enforcing tenant-specific authentication. The use of shared SSL certificates for 'Authenticated Origin Pulls' and broad Cloudflare IP allowlisting creates a trust boundary that can be abused by any Cloudflare tenant. Documentation fails to clearly communicate these security implications and tenant isolation limitations.

## Attacker mindset
A sophisticated attacker recognizes that Cloudflare's shared infrastructure creates a privilege escalation opportunity. By understanding the trust model between Cloudflare and customer origin servers, the attacker realizes they can leverage Cloudflare's own infrastructure as an attack vehicle. The attacker exploits the gap between security documentation (which implies per-tenant protection) and actual implementation (which trusts all Cloudflare tenants equally).

## Defensive takeaways
- Do not rely solely on Cloudflare IP allowlisting or shared certificate authentication for origin server protection
- Implement custom origin pull certificates with tenant-specific CAs instead of shared Cloudflare certificates
- Validate authentication at the origin server level with strict tenant-specific credentials or mutual TLS with custom certificates
- Add additional origin server protections independent of Cloudflare (rate limiting, request validation, geographic restrictions at origin)
- Implement defense-in-depth: layer multiple authentication mechanisms and do not trust implicit Cloudflare origination
- Review official Cloudflare documentation critically and understand the actual security implications of 'trust Cloudflare' recommendations
- Monitor for suspicious patterns of requests appearing to come from multiple Cloudflare zones but targeting the same origin
- Use custom API authentication or API keys for sensitive origin endpoints rather than relying on network-level protections
- Consider that any protection mechanism relying on 'trust Cloudflare' will fail if that trust can be abused by another tenant

## Variant hunting
['Investigate whether other CDN/WAF providers (Akamai, AWS CloudFront, Imperva) have similar cross-tenant trust issues', "Test whether Cloudflare's Page Rules, Transform Rules, or Workers can be configured to bypass origin protections", "Examine if Cloudflare's Logpush or other logging services expose tenant isolation weaknesses", "Analyze whether DNS takeover of subdomains pointing to victim's origin can abuse similar trust mechanisms", "Test if Cloudflare's Argo Tunnel or other connection-based services have similar bypass potential", 'Investigate whether rate limiting, caching, or other Cloudflare features can be configured to amplify attacks on protected origins', "Explore if attackers can abuse Cloudflare's IP reputation services or bot scoring to identify protected origins"]

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application (bypass of origin protections)
- T1021 - Remote Services (abuse of Cloudflare infrastructure as attack vector)
- T1199 - Trusted Relationship (exploitation of Cloudflare-to-customer trust)
- T1556 - Modify Authentication Process (bypass of authentication-like protections)
- T1578 - Modify Cloud Compute Infrastructure (attacker's Cloudflare configuration abuse)
- T1562 - Impair Defenses (bypass of WAF, DDoS protection)

## Notes
This vulnerability highlights a critical gap between security marketing (Cloudflare as origin protector) and security implementation (shared tenant trust). The fact that Cloudflare categorized this as 'Informative' rather than a security issue suggests a potential misunderstanding of the severity from the vendor's perspective. The public disclosure was necessary because the vulnerability cannot be fully mitigated by customers without implementing custom certificate infrastructure, which is not the default recommended approach. This represents a systemic issue affecting potentially thousands of Cloudflare customers using the documented 'very secure' or 'moderately secure' mechanisms without awareness of cross-tenant bypass potential.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-01*
