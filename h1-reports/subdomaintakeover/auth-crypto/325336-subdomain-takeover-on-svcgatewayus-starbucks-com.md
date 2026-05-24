# Subdomain Takeover on svcgatewayus.starbucks.com via Unclaimed Azure CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 325336 | https://hackerone.com/reports/325336
- **Submitted:** 2018-03-13
- **Reporter:** 0xpatrik
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Record, Cloud Resource Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A CNAME record for svcgatewayus.starbucks.com pointed to an unclaimed Azure Cloud App resource that could be registered by any attacker. This enabled full subdomain takeover allowing attackers to serve malicious content, phish users, or obtain SSL certificates under the starbucks.com domain.

## Attack scenario
1. Attacker discovers svcgatewayus.starbucks.com resolves to Azure CNAME s00197tmp0crdfulprod0.trafficmanager.net
2. Attacker identifies that the final Azure resource 1fd05821-7501-40de-9e44-17235e7ab48b.cloudapp.net is not registered
3. Attacker registers the unclaimed Cloud App resource in Azure Portal under their account
4. Attacker gains full DNS resolution control and serves malicious content at svcgatewayus.starbucks.com
5. Attacker obtains valid SSL certificate for the subdomain via ACME validation (Let's Encrypt)
6. Attacker conducts phishing, malware distribution, or XSS attacks leveraging Starbucks domain trust

## Root cause
Starbucks maintained DNS CNAME records pointing to Azure cloud resources that were deprovisioned or abandoned without removing the corresponding DNS entries. No monitoring or cleanup process existed for dangling cloud resource references.

## Attacker mindset
An attacker would recognize that abandoned cloud infrastructure references represent easy-to-takeover attack surface. The established domain reputation and HTTPS certificate issuance for starbucks.com subdomains make this extremely valuable for credential harvesting, malware distribution, or brand impersonation.

## Defensive takeaways
- Implement DNS record inventory and periodic audits to identify and remove dangling CNAME records
- Establish lifecycle management processes that synchronize DNS records with actual cloud resource provisioning/deprovisioning
- Use monitoring/alerting for DNS changes and unclaimed resource references
- Implement preventive controls in cloud platforms to block registration of resources matching known domain CNAME patterns
- Require CAA (Certification Authority Authorization) DNS records to prevent unauthorized certificate issuance
- Conduct regular subdomain enumeration and validation testing as part of security assessments
- Establish CNAME destination validation - verify cloud resources are actually claimed and configured

## Variant hunting
Look for other Starbucks subdomains with CNAME records pointing to: AWS CloudFront distributions, S3 buckets, GitHub Pages, Heroku apps, or other cloud providers. Search for patterns like *cdn*, *api*, *gateway*, *service* subdomains that commonly point to cloud infrastructure.

## MITRE ATT&CK
- T1583.001
- T1583.006
- T1190
- T1566.002
- T1071.001

## Notes
This report demonstrates the critical importance of DNS hygiene and cloud resource lifecycle management. The reporter responsibly disclosed and offered to release the claimed resource. Subdomain takeover is particularly dangerous because it bypasses trust relationships - users and security systems trust the parent domain, and the attacker inherits that trust through DNS resolution.

## Full report
<details><summary>Expand</summary>

Hello,

this is pretty serious security issue in some context, so please act as fast as possible.

### Overview:

One of the starbucks.com subdomains is pointing to Azure, which has unclaimed CNAME record. ANYONE is able to own starbucks.com subdomain at the moment.

This vulnerability is called subdomain takeover. You can read more about it here:

* https://blog.sweepatic.com/subdomain-takeover-principles/
* https://hackerone.com/reports/32825
* https://hackerone.com/reports/175070
* https://hackerone.com/reports/172137

### Details:

svcgatewayus.starbucks.com has CNAME to s00197tmp0crdfulprod0.trafficmanager.net which has CNAME to 1fd05821-7501-40de-9e44-17235e7ab48b.cloudapp.net. However, 1fd05821-7501-40de-9e44-17235e7ab48b.cloudapp.net is not registered in Azure cloud anymore and thus can be registered by anyone. After registering the Cloud App in Azure portal, the person doing so has full control over content on svcgatewayus.starbucks.com.

### PoC:

http://svcgatewayus.starbucks.com

### Mitigation:

* Remove the CNAME record from starbucks.com DNS zone completely.
* Claim it back in Azure portal after I release it

Regards,

Patrik Hudak

## Impact

Subdomain takeover is abused for several purposes:

* Malware distribution
* Phishing / Spear phishing
* XSS
* Authentication bypass
* ...

List goes on and on. Since some certificate authorities (Let's Encrypt) require only domain verification, SSL certificate can be easily generated.

</details>

---
*Analysed by Claude on 2026-05-24*
