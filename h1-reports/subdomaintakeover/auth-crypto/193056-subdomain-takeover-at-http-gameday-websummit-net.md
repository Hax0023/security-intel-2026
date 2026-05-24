# Subdomain Takeover at gameday.websummit.net via Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 193056 | https://hackerone.com/reports/193056
- **Submitted:** 2016-12-21
- **Reporter:** filedeletor1
- **Program:** Web Summit
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Cloud Infrastructure Misconfiguration, Dangling DNS Record, AWS S3 Bucket Hijacking
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A DNS CNAME record pointing to a non-existent AWS S3 bucket allowed an attacker to claim the subdomain by creating the corresponding S3 bucket. This enabled arbitrary content hosting and potential phishing attacks under the organization's domain.

## Attack scenario
1. Attacker discovers DNS CNAME record for gameday.websummit.net pointing to gameday.websummit.net.s3-website-eu-west-1.amazonaws.com
2. Attacker verifies the target S3 bucket does not exist by attempting to access it
3. Attacker creates an AWS S3 bucket with the exact name 'gameday.websummit.net' in eu-west-1 region
4. Attacker enables static website hosting on the newly created bucket
5. Attacker uploads malicious content (proof-of-concept) to the bucket
6. Attacker's content is now served under the legitimate websummit.net subdomain, bypassing origin validation

## Root cause
DNS record pointing to non-existent S3 bucket was not cleaned up when the original bucket was deleted or abandoned, combined with AWS S3's global namespace allowing any account holder to register unclaimed bucket names.

## Attacker mindset
An opportunistic security researcher performing reconnaissance discovered forgotten infrastructure. The low barrier to exploitation (simple bucket creation) made this a high-impact finding requiring minimal technical sophistication.

## Defensive takeaways
- Implement DNS hygiene practices: regularly audit and remove dangling DNS records pointing to cloud resources
- Establish infrastructure lifecycle management to track and decommission resources properly
- Use DNS validation and monitoring tools to detect CNAME records pointing to non-existent destinations
- For AWS: implement preventive measures like bucket naming conventions and consider using CloudFront with origin access identities instead of direct S3 website endpoints
- Enforce strict IAM policies limiting S3 bucket creation and require approval workflows
- Maintain an inventory of all subdomains and their corresponding cloud resource mappings
- Monitor for subdomain takeover attempts by alerting on unexpected content changes

## Variant hunting
Search for other abandoned CNAME records pointing to S3 buckets in the same organization's DNS
Scan for similar dangling DNS records pointing to other AWS services (CloudFront, ELB, API Gateway endpoints)
Check for subdomains pointing to non-existent Google Cloud Storage, Azure Blob Storage, or Heroku endpoints
Enumerate wildcard DNS entries that might not be validated
Review historical DNS records to identify patterns of resource churn

## MITRE ATT&CK
- T1190
- T1566
- T1583.001
- T1589.002

## Notes
This vulnerability demonstrates the risks of cloud infrastructure with global namespaces. The attack required minimal technical skill—merely creating a bucket and uploading files. The impact could be severe (phishing, credential harvesting, malware distribution) despite the simplicity. The report lacks detail on actual bounty amount and remediation timeline, suggesting this was reported early in HackerOne's platform adoption.

## Full report
<details><summary>Expand</summary>

As i said in the title i found a subdomain takeover vulnerability on the url http://gameday.websummit.net
The url was trying to find a bucket that didn't exist from a probably forgotten dns entry that was at
gameday.websummit.net.s3-website-eu-west-1.amazonaws.com

So i created a bucket with the specified name and uploaded a poc.
POC in the pictures

For more infos please ask...

</details>

---
*Analysed by Claude on 2026-05-24*
