# Subdomain Takeover on happymondays.starbucks.com via Unclaimed AWS S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 186766 | https://hackerone.com/reports/186766
- **Submitted:** 2016-11-30
- **Reporter:** dpgribkov
- **Program:** Starbucks
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record, Cloud Resource Takeover
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A DNS CNAME record for happymondays.starbucks.com pointed to a non-existent AWS S3 bucket, allowing an attacker to claim the S3 bucket and serve arbitrary content from the Starbucks subdomain. The attacker demonstrated the ability to publish files, obtain SSL certificates via Let's Encrypt, and potentially steal httpOnly cookies through this takeover.

## Attack scenario
1. Attacker performs DNS reconnaissance on Starbucks subdomains and identifies happymondays.starbucks.com CNAME record pointing to AWS S3
2. Attacker discovers the target S3 bucket no longer exists or is unclaimed
3. Attacker registers the same S3 bucket name in their AWS account with proper DNS configuration
4. Attacker uploads malicious files (phishing pages, credential theft forms) to the claimed S3 bucket
5. Attacker obtains valid SSL certificate for the subdomain via Let's Encrypt using DNS/file verification
6. Attacker launches phishing campaign or credential harvesting using legitimate Starbucks domain, bypassing user trust mechanisms

## Root cause
Starbucks failed to maintain ownership of DNS records pointing to cloud resources. The S3 bucket was decommissioned or deleted without removing the corresponding DNS CNAME record, creating a dangling DNS reference that could be claimed by any actor.

## Attacker mindset
Opportunistic reconnaissance-driven attack. The attacker systematically enumerated subdomains, identified orphaned cloud resources, and recognized the high-value target of claiming a Starbucks subdomain for phishing and credential theft purposes.

## Defensive takeaways
- Implement DNS record hygiene: regularly audit and remove DNS records pointing to decommissioned resources
- Establish lifecycle management: coordinate cloud resource deletion with DNS record removal
- Monitor for dangling DNS records using automated tools that detect CNAME records pointing to non-existent resources
- Implement subdomain monitoring and alerting for all organizational domains
- Consider using cloud-specific DNS validation with shorter TTLs for non-production resources
- Enforce DNS CAA records to restrict SSL certificate issuance to authorized CAs
- Regularly perform subdomain enumeration and validation from attacker perspective

## Variant hunting
Search for other Starbucks subdomains with dangling DNS records (staging.starbucks.com, test.starbucks.com, dev.starbucks.com)
Identify other AWS S3 buckets pointed to by Starbucks DNS records that may be unclaimed
Check for dangling records pointing to other cloud providers (Azure, GCP, Heroku, GitHub Pages)
Look for CNAME records pointing to CDN endpoints, load balancers, or other cloud services that may have been decommissioned
Enumerate related domains (starbuckscard.com, starbuckscorp.com) for similar misconfigurations

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1598.003 - Gather Victim Identity Information: Spearphishing Link
- T1589.001 - Gather Victim Identity Information: Credentials
- T1583.005 - Acquire Infrastructure: Domains

## Notes
This is a classic subdomain takeover vulnerability with high severity due to the legitimate Starbucks domain enabling advanced phishing and credential theft. The attacker demonstrated comprehensive understanding of the attack chain including SSL certificate procurement. The vulnerability is easily preventable through basic DNS hygiene but often overlooked during infrastructure decommissioning. The httpOnly cookie stealing capability is particularly dangerous for session hijacking.

## Full report
<details><summary>Expand</summary>

Hi,

I discovered that happymondays.starbucks.com DNS CNAME record is pointing to S3 AWS bucket which doesn't exist. Here's the screenshot of vulnerable domain: {F138556}

As happymondays.starbucks.com was free to register on AWS S3 service and DNS-setup is already correct set-up: {F138557} 
I was able to claim the domain for PoC using the following set-up:  {F138558}
Also I have placed a two files located under root directory for validation: {F138559}
For mitigation you should immediately remove the DNS-entry for this domain. 

As you might consider, the impact of this are pretty significant. I now can publish whatever I want on this domain, even fetching httpOnly cookies. I would also be able to register SSL certificate for this domain through Let's Encrypt (it is only need meta/file verification to issue the certificate) That would end up with the ability to read secure cookies as well.

In addition, there's no way at all for a visitor of this page to validate that the content on this domain is not served by Starbucks, making it extremely easy to utilize this for targeting the organization by fake login forms / spear phishing using your own domain to plant the attack.

Cheers,
Danil





</details>

---
*Analysed by Claude on 2026-05-24*
