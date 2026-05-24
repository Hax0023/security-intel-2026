# Subdomain Takeover at test.www.midigator.com via Abandoned AWS S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 1718371 | https://hackerone.com/reports/1718371
- **Submitted:** 2022-09-30
- **Reporter:** valluvarsploit_h1
- **Program:** Midigator
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A CNAME DNS record for test.www.midigator.com pointed to a deleted AWS S3 bucket endpoint (test.www.midigator.com.s3-website-us-west-1.amazonaws.com), allowing an attacker to register the abandoned bucket and serve arbitrary content. This classic subdomain takeover vulnerability could enable phishing, malware distribution, and credential theft under the target domain.

## Attack scenario
1. Attacker performs DNS enumeration and discovers test.www.midigator.com resolves to an S3 bucket CNAME
2. Attacker attempts to access the S3 bucket and confirms it no longer exists (404/NoSuchBucket error)
3. Attacker creates a new AWS S3 bucket with the identical name in the same region (us-west-1)
4. Attacker uploads malicious content (phishing page, malware, etc.) to the newly created bucket
5. Users visiting test.www.midigator.com are served attacker-controlled content under the legitimate domain
6. Attacker harvests credentials, spreads malware, or damages brand reputation

## Root cause
DNS CNAME record was not cleaned up after the associated S3 bucket was deleted. The dangling DNS record remained pointing to the orphaned S3 endpoint, creating a window for bucket claim-jacking. No DNS validation or monitoring was in place to detect stale cloud resource references.

## Attacker mindset
Systematic subdomain enumeration to find dangling DNS records pointing to cloud services. Recognition that deleted AWS resources can be re-registered by anyone, combined with DNS resolution still pointing to the service endpoint. Low barrier to exploit - simply requires AWS account and bucket creation.

## Defensive takeaways
- Implement DNS record lifecycle management: audit and remove CNAME entries when associated cloud resources are decommissioned
- Use cloud provider-specific subdomain takeover prevention (e.g., AWS S3 bucket name verification, Azure App Service domain validation)
- Maintain inventory of all DNS records and their corresponding cloud resources with regular reconciliation
- Monitor for dangling DNS records using automated tools (e.g., Can I Take Over XYZ, SubdomainTakeover scanners)
- Implement stricter IAM policies to prevent unauthorized S3 bucket creation matching organization domains
- Use DNS CNAME flattening or ALIAS records where applicable to reduce takeover surface
- Implement certificate transparency monitoring to detect SSL/TLS issuance for subdomains
- Include subdomain takeover scanning in CI/CD and security testing pipelines

## Variant hunting
Scan all DNS records (A, AAAA, CNAME, MX, NS) for cloud service endpoints (AWS CloudFront, Azure CDN, Heroku, Vercel, GitHub Pages)
Test subdomains at different hierarchy levels (*.midigator.com, *.www.midigator.com, *.test.midigator.com)
Check for services beyond S3: CloudFront distributions, API Gateway endpoints, Load Balancers, ELBs
Test other cloud providers: Azure App Service, GCP Cloud Storage, Digitalocean Spaces, Netlify
Identify newly registered subdomains in certificate logs that may indicate takeovered domains

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1598 - Phishing for Information
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1583.006 - Acquire Infrastructure: Web Services

## Notes
This is a well-documented, reproducible subdomain takeover via dangling CNAME record. The fix is straightforward (remove DNS entry) but the vulnerability was present long enough to be exploited. The reporter correctly demonstrated the issue through DNS resolution proof. No evidence of actual malicious content hosting provided in report. AWS has rate-limiting on bucket creation by account, but determined attackers can still register names. The redundant CNAME chain (test.www.midigator.com -> test.www.midigator.com.s3-website-us-west-1.amazonaws.com -> s3-website-us-west-1.amazonaws.com) is unusual and suggests either misconfiguration or leftover test infrastructure.

## Full report
<details><summary>Expand</summary>

## Vulnerability
Subdomain test.www.midigator.com points to an AWS S3 bucket that no longer exists. I was able to take control of this bucket and serve my own content on it.

## Proof Of Concept
```code
$ dig test.www.midigator.com
[snipped]
;; ANSWER SECTION:
test.www.midigator.com.	60	IN	CNAME	test.www.midigator.com.s3-website-us-west-1.amazonaws.com.
test.www.midigator.com.s3-website-us-west-1.amazonaws.com. 59 IN CNAME s3-website-us-west-1.amazonaws.com.
s3-website-us-west-1.amazonaws.com. 4 IN A	52.219.193.3
```

{F1963195}

## Remediation
Remove the CNAME entry for the `test.www.midigator.com`

## Impact

Subdomain Takeover

</details>

---
*Analysed by Claude on 2026-05-24*
