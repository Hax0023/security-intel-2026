# Using Cloudflare to Bypass Cloudflare: Cross-Tenant Security Control Gaps

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-09
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (categorized as 'Informative' and closed)
- **Severity:** high
- **Vuln types:** Broken Access Control, Insufficient Cross-Tenant Isolation, Shared Secrets/Credentials, Security Misconfiguration
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers can have their configured security protections (WAF, DDoS, Bot Management) bypassed because recommended origin server protection mechanisms trust all traffic from Cloudflare infrastructure without verifying which tenant initiated the connection. An attacker with their own Cloudflare account can point a malicious domain to a victim's origin server and tunnel attacks through Cloudflare's infrastructure, bypassing the victim's security controls.

## Attack scenario (step by step)
1. Attacker registers a domain and sets up a Cloudflare account with their own tenant
2. Attacker configures the A record to point to the victim's origin server IP address
3. Attacker disables all protection features (WAF, DDoS prevention, Bot Management) on their malicious domain
4. Victim has configured 'Authenticated Origin Pulls' using shared Cloudflare certificates, trusting all Cloudflare-originated traffic
5. Attacker tunnels malicious requests through their Cloudflare tenant, which passes through victim's origin with valid Cloudflare client certificate
6. Requests bypass victim's configured protections and reach the origin server unfiltered

## Root cause
The documented origin server protection mechanisms assume all traffic from Cloudflare infrastructure is trustworthy, but the shared Cloudflare certificate used for Authenticated Origin Pulls is available to all tenants, and Cloudflare IP ranges are used by all tenants. The architecture lacks per-tenant trust differentiation or cryptographic proof that traffic originated from the victim's own Cloudflare tenant specifically.

## Attacker mindset
An attacker recognizes that security controls are only effective if they protect the actual attack surface. By exploiting the trust boundary between Cloudflare and origin servers, the attacker bypasses security layers that the victim believed were protecting them. This represents an elegant example of turning a security provider's infrastructure against itself through misplaced architectural assumptions.

## Defensive takeaways
- Use custom tenant-specific certificates for Authenticated Origin Pulls instead of shared Cloudflare certificates, which requires maintaining separate certificate infrastructure
- Implement additional origin server validation beyond IP allowlisting or certificate validation, such as custom headers, API tokens, or request signing specific to your Cloudflare account
- Do not rely solely on 'Cloudflare certified' or built-in mechanisms; assume adversarial tenants have access to shared Cloudflare infrastructure
- Review and validate which protection mechanisms are actually enforced at the origin server versus relying on proxy-level filtering
- Implement defense-in-depth at the origin server level, treating Cloudflare as a helpful but not fully trustworthy intermediary
- Monitor origin server logs for suspicious patterns of requests that claim Cloudflare origin but don't match legitimate traffic patterns
- Consider using geographic restrictions or rate limiting at origin level to reduce blast radius of compromised proxies

## Variant hunting
['Test other CDN providers (Akamai, AWS CloudFront, Fastly) for similar cross-tenant bypasses of configured protections', "Investigate whether other Cloudflare mechanisms marked 'very secure' (e.g., specific headers, Bot Management tokens) are similarly bypassable through shared infrastructure", 'Check if Cloudflare allows customers to restrict origin pulls to specific source accounts or namespaces', 'Examine whether custom certificates can be validated with tenant-specific metadata to enable proper isolation', 'Research if IP allowlisting combined with custom headers provides adequate cross-tenant protection', "Test whether Cloudflare's newer security features (Authenticated Origin Pulls v2, mTLS validations) properly implement per-tenant trust"]

## MITRE ATT&CK
- T1190
- T1021
- T1566
- T1199
- T1578
- T1526

## Notes
This vulnerability highlights a critical architectural flaw where security controls are implemented at the wrong layer. The researcher responsibly disclosed to Cloudflare, but the vendor closed it as 'Informative' rather than fixing the underlying cross-tenant isolation issue. This suggests Cloudflare views this as a customer configuration problem rather than a platform issue. The writeup is valuable for security practitioners because it demonstrates how trust boundaries can be exploited even in professionally-managed security platforms. The lack of clear documentation about the security implications of shared certificates versus custom certificates represents a significant documentation gap that could lead to widespread misconfigurations.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-09*
