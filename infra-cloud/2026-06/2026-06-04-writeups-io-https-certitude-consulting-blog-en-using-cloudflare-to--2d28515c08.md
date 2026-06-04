# Using Cloudflare to bypass Cloudflare: Cross-Tenant Security Control Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-04
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** No bounty awarded (closed as 'Informative' before public disclosure)
- **Severity:** high
- **Vuln types:** Cross-Tenant Security Bypass, Insufficient Isolation, Shared Certificate Abuse, Trust Model Exploitation, Inadequate Documentation
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' configured protection mechanisms (WAF, DDoS prevention) can be bypassed because Cloudflare's origin server protection relies on trusting all traffic originating from Cloudflare infrastructure. Attackers with their own Cloudflare accounts can abuse this trust model by pointing their domain's DNS to a victim's origin server and tunneling attacks through Cloudflare, completely bypassing the victim's security configurations. The vulnerability stems from using shared authentication mechanisms (certificates and IP ranges) across all Cloudflare tenants without proper isolation.

## Attack scenario (step by step)
1. Attacker creates a legitimate Cloudflare account and registers a malicious domain
2. Attacker modifies the domain's DNS A record to point to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS, Bot Management) on their Cloudflare account for this domain
4. Attacker crafts malicious requests targeting the victim's origin server and sends them through their Cloudflare infrastructure
5. The victim's origin server receives the attack traffic directly from Cloudflare's legitimate IP ranges and accepts the shared certificate/certificate-less connection
6. Victim's configured Cloudflare protections are completely bypassed because the traffic appears to originate legitimately from Cloudflare

## Root cause
The protection mechanisms documented by Cloudflare operate on the assumption that all traffic from Cloudflare infrastructure can be trusted implicitly. However, Cloudflare uses shared authentication credentials (shared SSL certificates) and shared IP address ranges across all customer tenants without enforcing per-tenant validation. The documentation fails to explain that using 'Cloudflare certificates' (rather than custom certificates) creates a cross-tenant trust vulnerability. Additionally, IP allowlisting Cloudflare's ranges provides no granularity between benign and malicious tenants within Cloudflare.

## Attacker mindset
An attacker recognizes that defenders may rely on Cloudflare as their primary security boundary and that origin servers are often configured to trust Cloudflare implicitly. By exploiting the shared nature of Cloudflare's infrastructure, the attacker can weaponize Cloudflare's own services against its customers—achieving an ironic 'Cloudflare bypasses Cloudflare' attack. The attacker understands that many organizations follow official documentation without deep security analysis, making them vulnerable to implicit trust assumptions.

## Defensive takeaways
- Use custom origin pull certificates instead of shared Cloudflare certificates to enforce per-tenant authentication
- Implement additional authentication/validation layers beyond just IP allowlisting (e.g., custom tokens, request signing)
- Never rely solely on reverse-proxy/CDN security; implement defense-in-depth with origin server hardening
- Validate that origin server access controls are explicit about which Cloudflare tenant connections are permitted, not just which IPs
- Implement origin server-level WAF or request validation rules that are not dependent on upstream security controls
- Monitor for suspicious traffic patterns that appear to originate from legitimate Cloudflare ranges but target origin directly
- Review and maintain awareness of third-party shared infrastructure assumptions in your security architecture
- Enable per-request logging and analysis at the origin to detect anomalies in Cloudflare-routed traffic

## Variant hunting
Search for similar vulnerabilities in other reverse-proxy/CDN services that rely on implicit trust of their infrastructure (e.g., Akamai, AWS CloudFront, Fastly). Investigate whether other Cloudflare authentication mechanisms exhibit similar cross-tenant leakage. Examine whether Cloudflare's load balancing, SSL/TLS proxying, or page caching features can be similarly abused. Look for other Cloudflare documentation recommending security controls based on 'trusted Cloudflare origin' assumptions.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1021 - Remote Services (via Cloudflare proxy)
- T1526 - Reconnaissance via Cloud Infrastructure
- T1562 - Impair Defenses (bypass WAF/DDoS)

## Notes
Cloudflare closed this report as 'Informative' rather than addressing the underlying architectural gap, suggesting the vendor may view this as expected behavior or acceptable risk. The researchers proceeded with responsible public disclosure to inform customers. The vulnerability demonstrates a critical insight: security mechanisms cannot rely on implicit trust of shared infrastructure controlled by multiple parties. This is particularly relevant for organizations treating their CDN/reverse-proxy provider as a security boundary rather than one layer in defense-in-depth. The gap persists because documentation does not adequately communicate the security implications of configuration choices.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-04*
