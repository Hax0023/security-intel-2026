# Subdomain Takeover on dev-admin.periscope.tv

## Metadata
- **Source:** HackerOne
- **Report:** 531890 | https://hackerone.com/reports/531890
- **Submitted:** 2019-04-08
- **Reporter:** h1ch3ro
- **Program:** Periscope
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Improper Resource Configuration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A dangling DNS record pointing to an unclaimed AWS S3 bucket allowed an attacker to register the S3 bucket and take control of the dev-admin.periscope.tv subdomain. The attacker demonstrated takeover by uploading an index.html file accessible at the subdomain, proving full control over the endpoint.

## Attack scenario
1. Attacker identifies that dev-admin.periscope.tv resolves to an AWS S3 website endpoint
2. Attacker discovers the S3 bucket corresponding to that endpoint is unclaimed and available for registration
3. Attacker creates an AWS account and registers the exact S3 bucket name (dev-admin.periscope.tv or equivalent)
4. Attacker configures the bucket as a website-enabled S3 bucket matching the expected endpoint
5. Attacker uploads malicious or test files (index.html) to the bucket
6. Attacker verifies content is accessible via http://dev-admin.periscope.tv and the S3 direct URL

## Root cause
Periscope created a DNS CNAME record pointing to an AWS S3 bucket but failed to maintain ownership of the bucket. The bucket was either deleted, the DNS record was orphaned without bucket ownership verification, or AWS bucket naming practices allowed re-registration by third parties. No bucket policy or ownership verification mechanism was in place.

## Attacker mindset
Opportunistic reconnaissance - attacker identified low-hanging fruit through DNS enumeration and recognized the subdomain pointed to an unclaimed cloud resource. Exploitation was straightforward once the bucket name was known, demonstrating minimal effort required for maximum impact.

## Defensive takeaways
- Implement DNS record monitoring and automated alerts for dangling DNS records pointing to cloud services
- Establish mandatory cleanup procedures: remove DNS records before deprovisioning cloud resources
- Use cloud provider DNS delegation (e.g., Route53 for AWS) instead of CNAME records where possible to maintain tighter control
- Implement S3 bucket policies and access controls to prevent unauthorized uploads even if bucket is compromised
- Conduct regular subdomain enumeration and DNS audits to identify orphaned records
- Use S3 bucket naming conventions that include domain ownership verification or are sufficiently unique
- Implement bucket versioning and access logging to detect unauthorized access
- Disable S3 website endpoints for buckets that don't require public access

## Variant hunting
Search for other Periscope subdomains pointing to AWS, Azure, or GCP endpoints; check if other services use similar S3 bucket naming patterns; identify other organizations with CNAME records to public cloud storage without corresponding resource ownership

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1583.006 - Acquire Infrastructure: Web Services
- T1190 - Exploit Public-Facing Application
- T1657 - Force Cloud Service Account Logoff

## Notes
Report shows proof-of-concept with file upload but lacks detail on DNS configuration and AWS bucket details. The vulnerability is a classic subdomain takeover via abandoned cloud resource. Severity depends on what sensitive functionality the dev-admin subdomain provided - if it was truly a development/admin endpoint, exposure could be critical. Report date suggests this was from early 2019 when subdomain takeover vulnerabilities were less commonly mitigated.

## Full report
<details><summary>Expand</summary>

Subdomain takeover on dev-admin.periscope.tv
I takeover the subdomain and upload the index file : index.html

## Impact

Subdomain takeover on dev-admin.periscope.tv
Subdomain takeover on dev-admin.periscope.tv/index.html
http://dev-admin.periscope.tv.s3-website-us-west-2.amazonaws.com/index.html

</details>

---
*Analysed by Claude on 2026-05-24*
