# Using Cloudflare to bypass Cloudflare

## Metadata
- **Source:** writeups.io
- **Date:** 
- **Author:** Various
- **Program:** Cloudflare Bug Bounty Program
- **Bounty:** Not disclosed (classified as 'Informative' and closed)
- **Severity:** high
- **Vuln types:** Insufficient Cross-Tenant Security Controls, Shared Certificate Abuse, IP Allowlist Bypass, Trust Relationship Exploitation, Lack of Origin Server Isolation
- **Category:** infra-cloud
- **Writeup:** https://certitude.consulting/blog/en/using-cloudflare-to-bypass-cloudflare/

## Summary
Cloudflare customers' origin server protection mechanisms can be bypassed by attackers using their own Cloudflare accounts to exploit the inherent trust relationship between Cloudflare infrastructure and customer origin servers. Two key protection methods—Authenticated Origin Pulls using shared certificates and IP allowlisting of Cloudflare ranges—are vulnerable to abuse from within the Cloudflare platform itself.

## Attack scenario (step by step)
1. Attacker registers a domain with Cloudflare and obtains a Cloudflare account
2. Attacker disables all protection features (WAF, DDoS prevention) on their domain configuration
3. Attacker points their domain's DNS A record to the victim's origin server IP address
4. Attacker sends malicious requests through Cloudflare's infrastructure targeting the victim's origin
5. Victim's origin server authenticates the connection using the shared Cloudflare certificate or recognizes Cloudflare IP ranges
6. Malicious payload bypasses victim's configured security controls and reaches the unprotected origin server

## Root cause
Cloudflare's design assumes all connections originating from Cloudflare infrastructure are trustworthy. However, shared X.509 certificates and IP ranges are used across all tenants without tenant-specific isolation, allowing malicious tenants to impersonate legitimate Cloudflare connections. The documentation fails to highlight the security implications of using shared certificates versus custom certificates, and there is no cross-tenant validation mechanism.

## Attacker mindset
An attacker recognizes that Cloudflare's protection mechanisms create a false sense of security based on network/transport layer assumptions. By leveraging their own Cloudflare tenant, they exploit the platform's inherent trust model to legitimately route attacks through Cloudflare infrastructure, bypassing the very protections customers believe are in place. This requires understanding Cloudflare's architecture and configuration options.

## Defensive takeaways
- Do not rely solely on Cloudflare's shared certificate authentication; implement custom origin pull certificates with tenant-specific CAs
- IP allowlisting of Cloudflare ranges alone is insufficient; combine with additional origin server authentication mechanisms
- Implement mutual TLS (mTLS) with custom certificates on origin servers rather than relying on shared Cloudflare certificates
- Apply WAF and DDoS rules at the origin server level as a defense-in-depth measure, not just at the Cloudflare proxy
- Review and enhance documentation for origin server protection to explicitly warn against shared certificate risks
- Consider implementing rate limiting and request validation at the application layer independent of Cloudflare protections
- Validate the actual source of requests using additional contextual signals beyond certificate/IP verification

## Variant hunting
['Check if other reverse proxy services (Akamai, Cloudflare competitors) have similar shared credential issues', 'Investigate whether Cloudflare Workers or other Cloudflare services can be abused similarly', "Look for shared authentication mechanisms in other SaaS security vendors' origin protection schemes", 'Test whether custom nameservers configured with Cloudflare can be similarly abused', 'Examine if Page Rules or other Cloudflare features can bypass origin protections', 'Research whether different Cloudflare plan tiers have different certificate isolation']

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1557 - On-Path Attack
- T1021 - Remote Services
- T1566 - Phishing
- T1200 - Traffic Duplication
- T1040 - Traffic Redirection

## Notes
The researchers responsibly disclosed to Cloudflare, who categorized it as 'Informative' and closed the report without implementing fixes. Public disclosure was made to allow customers to self-remediate. The vulnerability is architectural rather than a code bug, affecting the design assumptions of the protection scheme. This highlights the risks of implicit trust models in multi-tenant cloud security infrastructure. Customers must implement defense-in-depth strategies and cannot rely solely on proxy-layer protections.

---
*Analysed by Claude (claude-haiku-4-5-20251001) on 2026-05-11*
