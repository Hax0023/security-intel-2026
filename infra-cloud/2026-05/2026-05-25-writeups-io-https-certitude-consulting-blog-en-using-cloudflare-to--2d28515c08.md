# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Control Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-05-25
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (categorized as 'Informative' and closed)
- **Severity:** High
- **Vuln types:** Cross-Tenant Security Bypass, Insufficient Access Controls, Shared Infrastructure Weakness, Authentication Bypass, Origin Server Protection Bypass
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' protection mechanisms (WAF, DDoS prevention, Firewall) can be bypassed by attackers using their own Cloudflare accounts to abuse the inherent trust relationship between Cloudflare and origin servers. The vulnerability stems from shared infrastructure and documented origin server protection mechanisms that rely on trusting all Cloudflare traffic without tenant isolation, allowing attackers to tunnel malicious payloads through Cloudflare's infrastructure while bypassing customer-configured security controls.

## Attack scenario (step by step)
1. Attacker creates a legitimate Cloudflare account and registers a custom domain under their control
2. Attacker configures the custom domain's DNS A record to point to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS prevention, Firewall) on their malicious Cloudflare tenant
4. Attacker sends crafted malicious requests through their Cloudflare tenant to the victim's origin server
5. The victim's origin server receives the request appearing to originate from trusted Cloudflare infrastructure, bypassing the victim's configured protection rules
6. Attack succeeds because origin server protection relies on shared Cloudflare certificates or IP allowlists that don't isolate between tenants

## Root cause
Cloudflare's origin server protection documentation recommends mechanisms that fundamentally assume all traffic originating from Cloudflare infrastructure is trustworthy. The shared 'Cloudflare certificate' used for Authenticated Origin Pulls is issued to all Cloudflare tenants, not specific customers. Similarly, allowlisting Cloudflare IP ranges doesn't differentiate between legitimate and malicious Cloudflare tenants. The documentation fails to adequately warn customers about the security implications of this shared trust model and the necessity of tenant-specific controls.

## Attacker mindset
An attacker recognizes that Cloudflare customers implicitly trust the Cloudflare platform as a security boundary and place faith in documented 'very secure' protection mechanisms. By leveraging the same Cloudflare infrastructure that victims rely on for protection, the attacker exploits the false assumption of tenant isolation. The attacker realizes they can abuse the victim's own security architecture by operating as a legitimate (but malicious) Cloudflare tenant, transforming the security provider into a pivot point for attacks.

## Defensive takeaways
- Do not rely solely on Cloudflare's shared certificate infrastructure for origin server authentication; implement custom tenant-specific certificates via API
- Understand that allowlisting Cloudflare IP ranges alone does not provide tenant isolation and should be combined with additional authentication mechanisms
- Implement additional origin server protections independent of Cloudflare (WAF, rate limiting, authentication) as defense-in-depth against bypass attacks
- Review and strengthen origin server authentication to verify not just that traffic came from Cloudflare, but from the legitimate Cloudflare tenant serving your domain
- Consider implementing request signing or cryptographic verification at the origin server level to authenticate legitimate Cloudflare proxy requests
- Carefully evaluate documented security recommendations from CDN/proxy providers and challenge implicit assumptions about trust boundaries
- Implement additional security controls such as origin server-level rate limiting, IP reputation checks, and behavioral analysis independent of proxy provider trust

## Variant hunting
['Check if other CDN providers (Akamai, AWS CloudFront, Fastly) have similar cross-tenant authentication bypass issues in their origin protection mechanisms', "Investigate whether Cloudflare's API-based custom certificate mechanism properly enforces tenant isolation and access controls", 'Test if other Cloudflare origin server protection features (e.g., IP allowlists with geographic restrictions) can be similarly bypassed by abusing shared infrastructure', 'Research whether attackers can manipulate DNS propagation timing to create race conditions during domain registration across multiple Cloudflare tenants', "Examine if Cloudflare's authenticated origin pulls can be bypassed by certificate pinning attacks or MITM scenarios within Cloudflare infrastructure", 'Investigate whether compromised Cloudflare tenant accounts could be used to systematically bypass protections across multiple victim domains']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1557 - On-Path Interception
- T1578 - Modify Cloud Compute Infrastructure
- T1526 - Reconnaissance Infrastructure
- T1598 - Phishing for Information
- T1199 - Trusted Relationship

## Notes
Cloudflare closed the report as 'Informative' rather than a security vulnerability, suggesting they may not view cross-tenant trust-based bypasses as a product defect but rather a customer configuration responsibility. The researchers disclosed publicly to educate Cloudflare customers about proper security configuration. This represents a significant gap between security mechanism documentation and actual security properties—customers following official guidance may unknowingly deploy ineffective protections. The vulnerability highlights the critical importance of understanding shared infrastructure risks when relying on third-party security providers and the necessity of implementing defense-in-depth strategies that don't solely depend on provider trust boundaries.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-25*
