# Subdomain Takeover on s3.shopify.com via Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 207576 | https://hackerone.com/reports/207576
- **Submitted:** 2017-02-20
- **Reporter:** avlidienbrunn
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Improper Resource Lifecycle Management
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain s3.shopify.com was configured with a CNAME pointing to an unclaimed Amazon S3 bucket, allowing an attacker to register and control the bucket. This enabled arbitrary content delivery, stored XSS attacks, and phishing through a trusted Shopify domain.

## Attack scenario
1. Attacker discovers s3.shopify.com resolves via CNAME to shopify-assets.s3.amazonaws.com
2. Attacker verifies the S3 bucket does not exist or is not owned by Shopify
3. Attacker creates an AWS account and claims the bucket 'shopify-assets'
4. Attacker uploads malicious HTML/JavaScript content to the bucket
5. Users visiting s3.shopify.com receive attacker-controlled content, bypassing same-origin policy protections
6. Attacker leverages Shopify's trusted domain for XSS, credential harvesting, or malware distribution

## Root cause
Shopify configured DNS CNAME records pointing to S3 buckets without ensuring bucket ownership/registration and ongoing lifecycle management. The dangling DNS record remained after the bucket was deprovisioned or never properly established.

## Attacker mindset
An opportunistic attacker scans for subdomain takeover opportunities by identifying CNAME records pointing to unclaimed cloud resources. S3 bucket registration requires minimal verification, making it an attractive target. The attacker exploits the trusted domain reputation to conduct XSS, phishing, or data exfiltration attacks with minimal detection.

## Defensive takeaways
- Implement DNS validation and monitoring to detect dangling CNAME/NS records pointing to unclaimed resources
- Enforce bucket naming conventions and maintain inventory of all DNS records with corresponding cloud resource ownership
- Use DNS CAA records and restrict S3 bucket creation policies to prevent unauthorized claims
- Monitor cloud resource lifecycle events and immediately remove DNS records when resources are deprovisioned
- Implement Content Security Policy (CSP) headers to mitigate XSS impact even if subdomain takeover occurs
- Regularly audit all subdomains and validate that they resolve to expected, controlled resources
- Consider using SSL/TLS certificate pinning or certificate transparency monitoring to detect unauthorized certificate issuance

## Variant hunting
Identify other Shopify subdomains with CNAME records to unclaimed cloud resources (AWS, Azure, GCP, Cloudflare, etc.)
Search for A/AAAA records pointing to IP addresses no longer controlled by Shopify or cloud providers
Check for NS records delegating subdomains to nameservers that accept arbitrary domain registration
Scan for GitHub Pages, Heroku, or other PaaS takeover opportunities via similar dangling records
Enumerate third-party integrations and webhooks that might reference takeover-vulnerable subdomains

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566.002 - Phishing: Spearphishing Link
- T1589 - Gather Victim Identity Information
- T1598 - Phishing for Information
- T1021 - Remote Services

## Notes
The researcher responsibly took control of the bucket to prevent exploitation by others, then disclosed to Shopify. This is a classic subdomain takeover vulnerability affecting a high-trust domain. The impact extends beyond XSS to include phishing, data interception, and application trust violations. The fix is straightforward: either remove the DNS record or ensure bucket ownership and access controls are properly configured.

## Full report
<details><summary>Expand</summary>

**Preword**
I know that this is not explicitly in scope, but I still felt it was serious enough to justify a report and let you decide the potential impact.

**Description**
The subdomain s3.shopify.com was pointed using CNAME to Amazon S3, but no bucket with that name was registered. This meant that anyone could sign up for Amazon S3, claim the bucket as their own and then serve content on s3.shopify.com.

DNS record:
```
s3.shopify.com.		3599	IN	CNAME	shopify-assets.s3.amazonaws.com.
shopify-assets.s3.amazonaws.com. 7518 IN CNAME	s3-directional-w.amazonaws.com.
s3-directional-w.amazonaws.com.	7218 IN	CNAME	s3-1-w.amazonaws.com.
s3-1-w.amazonaws.com.	4	IN	A	52.216.80.56
```


**Impact**
This could be used as stored XSS by uploading a HTML page.

Given that the attacker could control all the content (even at /), it could also make for a pretty convincing phishing page.

Last, if any of your application relies on s3.shopify.com any of the data sent/fetched there could be controlled by an attacker.

**Mitigation/PoC**
I have claimed the bucket on my account and disabled use except for the following URL:
http://s3.shopify.com/xss_unguessable3211231232.html

This means that nobody else can claim the bucket and add content.

**Fix**
Remove the s3.shopify.com DNS entry. Alternatively, if you wish to use s3.shopify.com with S3, tell me in a comment and I will remove the bucket from my Amazon account.

</details>

---
*Analysed by Claude on 2026-05-24*
