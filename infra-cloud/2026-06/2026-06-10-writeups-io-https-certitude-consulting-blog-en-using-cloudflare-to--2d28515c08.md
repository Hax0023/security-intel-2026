# Using Cloudflare to Bypass Cloudflare - Cross-Tenant Security Control Gap

## Metadata
- **Source:** writeups.io
- **Date:** 2026-06-10
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (reported as 'Informative' and closed)
- **Severity:** High
- **Vuln types:** Insufficient Cross-Tenant Isolation, Shared Credential Abuse, Trust Boundary Bypass, Inadequate Documentation of Security Implications
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' security protections can be bypassed by attackers using their own Cloudflare accounts to abuse the implicit trust relationship between Cloudflare infrastructure and protected origin servers. The vulnerability exists in two recommended protection mechanisms: Authenticated Origin Pulls using shared Cloudflare certificates and IP allowlisting of Cloudflare ranges, both of which fail to validate tenant ownership.

## Attack scenario (step by step)
1. Attacker registers a domain and sets up a Cloudflare account as a legitimate customer
2. Attacker configures their domain's DNS A record to point to the victim's origin server IP address
3. Attacker disables all Cloudflare protection features (WAF, DDoS, Bot management) on their malicious domain
4. Attacker tunnels malicious requests through their Cloudflare tenant, leveraging the shared certificate or Cloudflare IP ranges
5. Victim's origin server accepts requests as legitimate Cloudflare traffic due to certificate trust or IP allowlisting
6. Bypass is complete: victim's configured protections (WAF rules, DDoS filters) are rendered ineffective

## Root cause
Cloudflare implements per-design trust relationships where all traffic from Cloudflare infrastructure is implicitly trusted, without validating that the traffic originates from the same tenant. Shared SSL certificates and publicly documented Cloudflare IP ranges create a false security boundary. Documentation fails to articulate the security implications of choosing shared certificates over tenant-specific certificates.

## Attacker mindset
An attacker recognizes that security controls are only effective if they cannot be circumvented through legitimate platform mechanisms. By understanding that Cloudflare customers trust all traffic from Cloudflare infrastructure, the attacker leverages their own legitimate Cloudflare account as a vector to reach protected origin servers. This represents a sophisticated abuse of platform design rather than exploitation of a software bug.

## Defensive takeaways
- Do not rely solely on shared infrastructure credentials; implement tenant-specific authentication mechanisms (custom origin pull certificates) instead of shared Cloudflare certificates
- Do not assume all traffic from a CDN/proxy provider is trustworthy without validating the originating tenant identity
- Implement additional origin server protection layers independent of the CDN provider (API keys, request signing, mutual TLS with tenant-specific certificates)
- Validate DNS and domain ownership before accepting requests, even from trusted proxy services
- Apply end-to-end security controls that validate request legitimacy beyond network/transport layer indicators
- Security documentation must explicitly warn of cross-tenant attack vectors and their impact
- Use rate limiting and behavioral analysis on origin servers to detect anomalous traffic patterns

## Variant hunting
['Investigate other CDN/proxy providers (Akamai, CloudFlare competitors) for similar cross-tenant trust boundary issues in their origin protection documentation and mechanisms', 'Examine shared credential systems in other security services (cloud WAFs, DDoS providers) where multiple tenants share infrastructure', 'Test whether other Cloudflare protection mechanisms (Bot Management, Rate Limiting) can be bypassed through attacker-controlled tenants', 'Investigate if Cloudflare Workers or other serverless offerings can be abused to generate authenticated traffic to customer origins', 'Review IP-based allowlisting mechanisms in other providers where attacker and victim both use the same infrastructure']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1199 - Trusted Relationship
- T1566 - Phishing (if combined with social engineering)
- T1021 - Remote Services
- T1578 - Modify Cloud Compute Infrastructure (creating malicious Cloudflare configuration)

## Notes
This vulnerability was responsibly disclosed but Cloudflare dismissed it as 'Informative', indicating they may not consider cross-tenant security a critical issue. The public disclosure is valuable as it educates customers on proper origin server protection strategies. The core issue is architectural: implicit trust in infrastructure cannot be considered security if multiple hostile tenants share that infrastructure. Customers using only Cloudflare-recommended protections without additional origin validation are vulnerable. The researcher emphasizes this is not a traditional bug but a design gap in security assumptions.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-06-10*
