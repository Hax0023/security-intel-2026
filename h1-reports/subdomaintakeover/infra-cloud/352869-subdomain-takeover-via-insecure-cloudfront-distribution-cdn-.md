# Subdomain Takeover Via Insecure CloudFront Distribution cdn.grab.com

## Metadata
- **Source:** HackerOne
- **Report:** 352869 | https://hackerone.com/reports/352869
- **Submitted:** 2018-05-16
- **Reporter:** todayisnew
- **Program:** Grab
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Insecure CloudFront Configuration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain cdn.grab.com was configured with a CNAME pointing to a CloudFront distribution that was not registered or claimed by Grab, allowing an attacker to register the CloudFront instance and take control of the subdomain. This enabled serving arbitrary content under Grab's trusted domain, facilitating phishing attacks and potential cookie theft from wildcard domain configurations.

## Attack scenario
1. Attacker discovers cdn.grab.com resolves via CNAME to an unclaimed *.cloudfront.net instance
2. Attacker creates an AWS CloudFront distribution matching the unclaimed endpoint
3. Attacker successfully registers/claims ownership of the CloudFront distribution
4. DNS resolution now routes cdn.grab.com traffic to attacker-controlled CloudFront distribution
5. Attacker hosts phishing content or malicious payloads at cdn.grab.com/index.html
6. Users visit the attacker's content believing it is served by legitimate Grab infrastructure

## Root cause
Grab created a CNAME DNS record pointing to a CloudFront distribution without registering or securing ownership of that distribution in AWS. The dangling DNS record combined with CloudFront's ability to be registered by any AWS account created an exploitable condition. Additionally, no validation mechanism existed to ensure only authorized parties could claim the distribution.

## Attacker mindset
Low-effort, high-impact attack requiring minimal technical sophistication. The attacker discovered an abandoned/forgotten subdomain configuration and recognized the opportunity for subdomain takeover. The approach demonstrates reconnaissance through DNS enumeration and understanding of cloud infrastructure weaknesses. The attacker responsibly disclosed the issue rather than exploiting it maliciously.

## Defensive takeaways
- Maintain inventory of all DNS records and verify corresponding cloud resources are registered and actively managed
- Implement DNS monitoring to detect orphaned or dangling CNAME records pointing to unclaimed resources
- Use AWS CloudFront security features: restrict distribution creation via IAM policies, require AWS account verification
- Regularly audit subdomains and their configurations; remove unused DNS records promptly
- Monitor for subdomain takeover using services that test for dangling DNS records
- Implement secure cookie flags: avoid wildcard domain cookies (*.example.com), use Secure and HttpOnly flags appropriately
- Use DNSSEC to prevent DNS hijacking and ensure integrity of DNS responses
- Establish a process for decommissioning subdomains that includes verifying all cloud resources are cleaned up

## Variant hunting
Search for other Grab subdomains pointing to unclaimed CloudFront distributions (cdn2.grab.com, static.grab.com, etc.)
Test other Grab subdomains for dangling DNS records pointing to AWS S3, Heroku, GitHub Pages, or other cloud services
Check if other services at Grab (API endpoints, internal tools) use similar patterns with unregistered cloud resources
Look for CNAME records pointing to other cloud providers' services that may also be claimable (Azure CDN, Fastly, etc.)
Enumerate Grab's DNS records via zone transfers, OSINT, or certificate transparency logs to identify additional targets

## MITRE ATT&CK
- T1190
- T1566.002
- T1583.001
- T1589.001

## Notes
This report demonstrates a classic subdomain takeover vulnerability. The responsible disclosure approach by the researcher (offering two remediation options) indicates good security community practices. The potential for chaining this vulnerability with cookie theft attacks using wildcard domain misconfiguration significantly increases impact. CloudFront's permissive registration model (allowing any AWS account to claim unregistered distributions) contributed to the vulnerability. This finding likely prompted Grab to implement stricter DNS and cloud resource management policies.

## Full report
<details><summary>Expand</summary>

Good day, I truly hope it treats you awesomely on your side of the screen :)


I have found that your website cdn.grab.com is pointed via a cname to a cloudfront instance

cdn.grab.com => *.cloudfront.net

This was not registered on Amazon Aws Cloudfront.

I was able to take over the domain:

See my POC (Pug of Concept)
http://cdn.grab.com/index.html



Options How to fix:

1) Remove the Cname record on cdn.grab.com to not point to cloudfront.net

2) Ask me to remove my registered cdn.grab.com on cloudfront, and you can re register yours :)

May you be well on your side of the screen :)

-Eric

## Impact

Impact:

Cyber attackers can launch a phishing campaign leveraging your established (soon to be impacted) brand reputation.

The victim has no way of telling, whether the content is served by the domain owner or the cyber attacker.

Attackers can also chain higher severity attacks to this. Many applications expose session cookies to a wildcard domain (*.example.com),
so any subdomain can access them. An attacker can take a forgotten subdomain, trick the user to visit it, and extract cookies 
(even those with secure flag). This can be seen as an advanced version of XSS.

</details>

---
*Analysed by Claude on 2026-05-24*
