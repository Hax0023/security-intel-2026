# Full Subdomain Takeover at s3.websummit.net via Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 173412 | https://hackerone.com/reports/173412
- **Submitted:** 2016-10-01
- **Reporter:** dhaval
- **Program:** Web Summit
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Cloud Infrastructure Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain s3.websummit.net was configured as a CNAME pointing to an AWS S3 website endpoint (dws-content.s3-website-eu-west-1.amazonaws.com) for a bucket that no longer exists. An attacker could register/claim the orphaned S3 bucket and serve malicious content under the legitimate websummit.net domain.

## Attack scenario
1. Attacker discovers s3.websummit.net resolves to a non-existent S3 bucket via DNS reconnaissance
2. Attacker identifies the target S3 bucket name from AWS error messages (dws-content)
3. Attacker attempts to create a new S3 bucket with the same name in the same region (eu-west-1)
4. If successful, attacker gains control of the bucket and can upload arbitrary content
5. Attacker's malicious content is now served at s3.websummit.net with full domain trust
6. Victims accessing the subdomain receive attacker-controlled content, enabling credential theft, malware distribution, or brand hijacking

## Root cause
The organization failed to remove DNS records (CNAME entries) after decommissioning the underlying S3 bucket. The dangling DNS record combined with AWS bucket naming uniqueness allows an attacker to claim the orphaned bucket and exploit the trust relationship with the parent domain.

## Attacker mindset
An attacker recognizes that legacy subdomains often point to defunct cloud resources. By systematically checking for 404 errors from cloud providers and identifying bucket names from error messages, they can claim valuable namespace real estate under trusted domains for phishing, malware hosting, or data theft campaigns.

## Defensive takeaways
- Maintain an inventory of all DNS records and cloud resources; remove CNAME records immediately when underlying resources are decommissioned
- Implement DNS monitoring to detect and alert on changes or orphaned records
- Regularly audit subdomain ownership and cloud service configurations
- Use predictable and domain-specific bucket names (avoid generic names that may be claimed by others)
- Consider using S3 bucket policies or IAM to restrict who can claim similarly-named buckets
- Implement DNS security practices like DNSSEC where applicable
- Conduct periodic subdomain enumeration and validation as part of security testing

## Variant hunting
Search for other subdomains in websummit.net DNS zone that may point to expired/unclaimed cloud services (S3, CloudFront, Azure, GCP)
Check for dangling CNAME records pointing to other AWS services (CloudFront distributions, API endpoints, load balancers)
Identify subdomains pointing to GitHub Pages, Heroku, Firebase or other PaaS platforms with unclaimed namespaces
Review organization's acquired companies or rebranded properties for DNS records pointing to deactivated infrastructure
Scan for historical DNS records (via VirusTotal, Wayback Machine) that may reveal forgotten subdomains

## MITRE ATT&CK
- T1566.002 - Phishing: Spearphishing Link (via hijacked subdomain)
- T1583.001 - Acquire Infrastructure: Domains (subdomain takeover)
- T1200 - Hardware Additions (cloud infrastructure misconfiguration)
- T1190 - Exploit Public-Facing Application (if used to distribute malware)

## Notes
This is a classic subdomain takeover vulnerability specific to cloud services. The vulnerability is particularly severe because: (1) it uses a legitimate organization domain, bypassing user trust filters, (2) AWS provides explicit error messages revealing the bucket name, and (3) the attack requires only creating a public S3 bucket. This report demonstrates the importance of DNS hygiene and infrastructure cleanup during decommissioning phases. The 'NoSuchBucket' error message was crucial reconnaissance that revealed both the vulnerability and the target bucket name.

## Full report
<details><summary>Expand</summary>

Hey

The sub domain at `s3.websummit.net` is pointing to `dws-content.s3-website-eu-west-1.amazonaws.com.`

> http://s3.websummit.net/

````
404 Not Found

    Code: NoSuchBucket
    Message: The specified bucket does not exist
    BucketName: s3.websummit.net
    RequestId: DB4C92F0D805D3F3
    HostId: NdSB/5EgNAiQz7B2pjzfBy5QwA6977cvAroA5vCyqfSsPR3nZLgdEyv4vQA4NCISzpILKP0WddM=
````

This means that the bucket has now expired and this  can now be claimed and content can be hosted on behalf of `http://s3.websummit.net/`

</details>

---
*Analysed by Claude on 2026-05-24*
