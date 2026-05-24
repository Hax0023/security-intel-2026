# GNIP Subdomain Takeover via Misconfigured CloudFront

## Metadata
- **Source:** HackerOne
- **Report:** 189548 | https://hackerone.com/reports/189548
- **Submitted:** 2016-12-08
- **Reporter:** hussein98d
- **Program:** Twitter (GNIP)
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, CloudFront Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain blog.gnipcentral.com was configured to point to an unowned CloudFront distribution backed by an S3 bucket, allowing an attacker to claim the S3 bucket and serve arbitrary content. This classic subdomain takeover vulnerability enabled the attacker to redirect users to attacker-controlled content.

## Attack scenario
1. Attacker identifies that blog.gnipcentral.com resolves to a CloudFront distribution
2. Attacker discovers the underlying S3 bucket origin is unclaimed/available
3. Attacker creates an S3 bucket matching the expected origin name (testcloudfrontbug.s3-us-west-2.amazonaws.com)
4. Attacker uploads malicious content (index.html) to the newly created bucket
5. When users visit blog.gnipcentral.com, the CloudFront distribution serves attacker-controlled content from the S3 bucket
6. Attacker can host phishing pages, malware, or defacement content

## Root cause
DNS records for blog.gnipcentral.com pointed to a CloudFront distribution whose origin S3 bucket was not claimed/secured by the organization. The S3 bucket name was predictable and available for registration by an attacker, creating a dangling DNS pointer vulnerability.

## Attacker mindset
Opportunistic reconnaissance attacker scanning for common subdomain patterns and misconfigured cloud infrastructure. Likely performed passive enumeration of DNS records and cloud service configurations to identify available takeover targets.

## Defensive takeaways
- Inventory all DNS records and ensure every CNAME/alias points to claimed and secured resources
- For CloudFront distributions, ensure origin S3 buckets are secured with bucket policies preventing unauthorized access
- Use private S3 bucket origins with Origin Access Identity (OAI) or Origin Access Control (OAC) rather than public access
- Implement DNS validation and certificate pinning to prevent subdomain hijacking
- Regularly audit cloud resource ownership and access controls for all subdomains
- Monitor for dangling DNS pointers using automated scanning tools
- Remove or secure DNS records for deprecated services and subdomains

## Variant hunting
Scan all company subdomains for CNAME records pointing to cloud providers (CloudFront, Azure CDN, Akamai)
Enumerate S3 buckets with predictable naming patterns derived from company domain names
Check for unclaimed GitHub Pages subdomains (*.github.io CNAMEs)
Identify Heroku apps with dangling DNS pointers
Look for misconfigured AWS/Azure/GCP load balancers with no backend targets
Test for zone transfer vulnerabilities that might reveal additional subdomains

## MITRE ATT&CK
- T1583.001
- T1190
- T1589.002

## Notes
This vulnerability references report #145224 which contains the detailed explanation. The PoC demonstrates the core issue by showing the CloudFront redirect to the attacker-controlled S3 bucket. This is a well-documented vulnerability class that affects organizations using AWS CloudFront without proper origin security controls. The fix involves either securing the S3 bucket with restrictive policies or removing/updating the DNS record.

## Full report
<details><summary>Expand</summary>

Hello,
Your subdomain at blog.gnipcentral.com is not well configured with allows subdomain take over as @fransoren explained in report #145224 .

PoC:
Go to http://blog.gnipcentral.com/ , you will be redirected to my domain http://testcloudfrontbug.s3-us-west-2.amazonaws.com/asd/index.html 


Please for more information visit the report made by @fransorosen, it's explained with all details possible.

Thanks,
Hussein

</details>

---
*Analysed by Claude on 2026-05-24*
