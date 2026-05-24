# Subdomain Takeover in assets.goubiquiti.com

## Metadata
- **Source:** HackerOne
- **Report:** 109699 | https://hackerone.com/reports/109699
- **Submitted:** 2016-01-10
- **Reporter:** c12316651
- **Program:** Ubiquiti
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, AWS S3 Bucket Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain assets.goubiquiti.com contains a dangling DNS CNAME record pointing to an unclaimed AWS S3 bucket, allowing an attacker to register the S3 bucket and take control of the subdomain. This vulnerability could be leveraged to serve malicious content, perform phishing attacks, or damage the company's reputation.

## Attack scenario
1. Attacker discovers that assets.goubiquiti.com resolves to an AWS S3 endpoint via CNAME record
2. Attacker verifies that no S3 bucket with the expected name exists or is unclaimed
3. Attacker creates an AWS S3 bucket with the matching name to claim the dangling DNS record
4. Attacker uploads malicious content (malware, phishing page, exploit kit) to the S3 bucket
5. When users visit assets.goubiquiti.com, they receive attacker's malicious content with Ubiquiti's domain authority
6. Attacker leverages domain trust for credential theft, malware distribution, or brand damage

## Root cause
DNS CNAME record points to an AWS S3 bucket endpoint that either never existed or was deleted without removing the corresponding DNS record, creating a dangling reference.

## Attacker mindset
Opportunistic reconnaissance followed by exploitation of infrastructure inconsistencies. Attackers scan for dangling DNS records as low-effort, high-impact attack vectors that leverage existing domain trust.

## Defensive takeaways
- Implement DNS record auditing to identify and remove dangling CNAME records pointing to non-existent cloud resources
- Maintain inventory of all subdomains and their associated resources with regular reconciliation
- Monitor cloud infrastructure (S3 buckets, CloudFront distributions, etc.) and remove corresponding DNS records before deprovisioning
- Use subdomain enumeration tools regularly to discover unclaimed subdomains
- Consider CNAME cloaking or CAA records to restrict subdomain claims
- Implement automated checks in CI/CD to validate DNS records point to active resources
- Enable S3 bucket-specific protections like blocking public access by default

## Variant hunting
Scan other Ubiquiti subdomains (cdn.*, api.*, mail.*, etc.) for similar dangling records
Check for dangling records pointing to Heroku, Netlify, GitHub Pages, Cloudflare, and other PaaS providers
Identify subdomains in company acquisition/merger that may have inconsistent DNS configuration
Look for CNAME records pointing to decommissioned internal services or development infrastructure

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1583.006 - Acquire Infrastructure: Web Services
- T1657 - Financial Theft

## Notes
This is a classic subdomain takeover vulnerability demonstrating the importance of DNS hygiene. The reporter referenced Detectify's research on hostile subdomain takeover, which became a common bug bounty finding. This vulnerability type has significant real-world impact as demonstrated in later high-profile cases. The fix is straightforward: remove the CNAME record or ensure the S3 bucket exists and is properly secured.

## Full report
<details><summary>Expand</summary>

Hi there,

Its urgent issue about your subdomain http://assets.goubiquiti.com pointing to AWS S3 but no such website configuration is made. This unused subdomain can claim by anyone and fully take over it.

An attacker can fully takeover this subdomain and do whatever he wants. this can cause huge damage to the website's main domain as well as to the company.

I Recommend to remove the Cname and Dns connecting to it. 
PoC is attached to this report.

You can read about this sort of attacks here : http://labs.detectify.com/post/109964122636/hostile-subdomain-takeover-using

Please Consider my report to Support my study

cheers,

Karl


</details>

---
*Analysed by Claude on 2026-05-24*
