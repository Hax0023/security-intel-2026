# Subdomain Takeover on wfmnarptpc.starbucks.com via Unclaimed Azure CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 388622 | https://hackerone.com/reports/388622
- **Submitted:** 2018-07-30
- **Reporter:** 0xpatrik
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Record, Cloud Service Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A Starbucks subdomain (wfmnarptpc.starbucks.com) contained a CNAME record pointing to an unclaimed Azure Traffic Manager endpoint that could be registered by any attacker. This allowed complete takeover of the subdomain for hosting malicious content, phishing attacks, and SSL certificate generation.

## Attack scenario
1. Attacker identifies wfmnarptpc.starbucks.com DNS record pointing to s00149tmppcrpt.trafficmanager.net
2. Attacker verifies the Azure Traffic Manager profile is no longer claimed/active
3. Attacker registers the unclaimed Traffic Manager profile in Azure Portal
4. Attacker gains full control over the subdomain and serves malicious content
5. Attacker uses Let's Encrypt or other CAs to issue valid SSL certificates for the subdomain
6. Attacker leverages the trusted Starbucks domain for phishing, malware distribution, or XSS attacks

## Root cause
Starbucks failed to maintain ownership of cloud resources referenced in DNS records. When the Azure Traffic Manager profile was deprovisioned, the CNAME record was not removed from DNS, leaving a dangling reference that could be claimed by attackers.

## Attacker mindset
An opportunistic attacker performing reconnaissance on target domain infrastructure, discovering orphaned cloud resource references, and capitalizing on the lack of cleanup to gain control over a trusted subdomain for credential harvesting or malware distribution campaigns.

## Defensive takeaways
- Implement DNS record auditing to identify and remove dangling CNAME records pointing to unclaimed cloud services
- Establish change management procedures requiring DNS cleanup when cloud resources are deprovisioned
- Monitor all subdomains and their target endpoints for orphaned configurations
- Use CNAME flattening or ALIAS records where possible to reduce dangling reference risk
- Implement DNS monitoring and alerting for changes to external service endpoints
- Require certificate transparency log monitoring to detect unauthorized cert issuance
- Establish inventory of all DNS records and associated cloud service ownership

## Variant hunting
Scan all starbucks.com and owned subdomain CNAMEs for orphaned cloud service endpoints (AWS, GCP, Azure, Heroku, etc.)
Check for dangling NS records pointing to unclaimed nameservers
Identify MX records pointing to deprovisioned mail services
Review all CNAME chains for intermediate dead endpoints
Test other known Starbucks subdomains for similar misconfigurations

## MITRE ATT&CK
- T1190
- T1199
- T1583.001
- T1583.005
- T1566.002
- T1588.004

## Notes
This is a high-impact vulnerability class affecting many organizations. The report demonstrates responsible disclosure with a PoC and clear mitigation steps. The vulnerability is particularly dangerous because: (1) it affects a trusted brand domain, (2) it enables SSL certificate generation, (3) it requires minimal technical skill to exploit once discovered, and (4) it can persist for extended periods undetected. Starbucks likely has internal tracking/bounty amount but it's not disclosed in the public report.

## Full report
<details><summary>Expand</summary>

Hello,

this is pretty serious security issue in some context, so please act as fast as possible.

Overview:
One of the starbucks.com subdomains is pointing to Azure, which has unclaimed CNAME record. ANYONE is able to own starbucks.com subdomain at the moment.

This vulnerability is called subdomain takeover. You can read more about it here:

https://0xpatrik.com/subdomain-takeover-basics/

Details:
wfmnarptpc.starbucks.com has CNAME to s00149tmppcrpt.trafficmanager.net. However, s00149tmppcrpt.trafficmanager.net is not registered in Azure cloud anymore and thus can be registered by anyone. After registering the TrafficManager Profile in Azure portal, the person doing so has full control over content on wfmnarptpc.starbucks.com.

PoC:
http://wfmnarptpc.starbucks.com/poc.html

 Mitigation:
Remove the CNAME record from starbucks.com DNS zone completely.
Claim it back in Azure portal after I release it
Regards,

Patrik Hudak

## Impact

Subdomain takeover is abused for several purposes:

Malware distribution
Phishing / Spear phishing
XSS
Authentication bypass
...
List goes on and on. Since some certificate authorities (Let's Encrypt) require only domain verification, SSL certificate can be easily generated.

</details>

---
*Analysed by Claude on 2026-05-24*
