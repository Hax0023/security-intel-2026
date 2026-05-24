# Subdomain Takeover of images.crossinstall.com via Unclaimed AWS S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 1406335 | https://hackerone.com/reports/1406335
- **Submitted:** 2021-11-21
- **Reporter:** ian
- **Program:** Twitter (HackerOne)
- **Bounty:** Not specified in provided content
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, AWS S3 Bucket Misconfiguration
- **CVEs:** None
- **Category:** business-logic

## Summary
The subdomain images.crossinstall.com contained a dangling DNS CNAME record pointing to a non-existent AWS S3 bucket (assets.crossinstall.com.s3.amazonaws.com). An attacker was able to create a new S3 bucket with the same name and take control of the subdomain, allowing arbitrary content delivery and potential OAuth/cookie-based attacks. This represents a complete compromise of the subdomain namespace.

## Attack scenario
1. Attacker discovers images.crossinstall.com via DNS enumeration and identifies the CNAME record pointing to assets.crossinstall.com.s3.amazonaws.com
2. Attacker verifies the S3 bucket no longer exists by attempting access (receiving 404 or similar)
3. Attacker creates a new AWS S3 bucket named 'assets.crossinstall.com' (S3 bucket names are globally unique)
4. Attacker uploads malicious content (HTML, JavaScript, etc.) to the newly created bucket
5. Content becomes accessible via images.crossinstall.com due to the DNS CNAME resolution
6. Attacker can obtain valid TLS certificate for the domain and exploit OAuth redirects or cookie-scoped trust relationships

## Root cause
Organization failed to decommission DNS records pointing to AWS S3 buckets that were deleted. S3 bucket deletion does not automatically remove associated DNS records, leaving dangling CNAME entries that become vulnerable to hijacking. No monitoring or regular audit of DNS records and their target validity was in place.

## Attacker mindset
Opportunistic reconnaissance attacker discovering stale infrastructure during subdomain enumeration. Recognized the high-impact potential of controlling an organization's domain-scoped asset, particularly for OAuth exploitation or content injection attacks targeting customers or internal services.

## Defensive takeaways
- Implement automated DNS record auditing to detect dangling/invalid records (CNAME pointing to non-existent resources)
- Establish a process to verify all DNS records have valid, accessible targets before resource deletion
- Use DNS monitoring tools that alert on resolution failures or changes to critical subdomains
- Maintain a centralized inventory of all DNS records and their corresponding infrastructure (S3 buckets, CDN origins, etc.)
- Implement preventive S3 bucket naming strategies or use Route53 alias records instead of CNAME where possible
- Regularly audit external-facing subdomains and their configurations as part of security assessments
- Consider using DNS zones or CAA records to restrict certificate issuance on critical domains
- Review OAuth redirect URI whitelists to prevent exploitation via takeover of whitelisted subdomains

## Variant hunting
Scan for other dangling DNS records across subdomains pointing to: CloudFront distributions, GitHub pages, Heroku, Firebase, other AWS services (S3, CloudFront, ALB), Azure services, Fastly, etc.
Enumerate subdomains of crossinstall.com and Twitter's other owned domains for similar patterns
Check for CNAME records where the target is inaccessible or returns 404/NoSuchBucket errors
Investigate subdomains that may have been part of acquisitions or internal projects subsequently abandoned
Look for dual-use subdomains that might be OAuth redirect URIs or trusted for cookie scoping

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1584.001 - Compromise Infrastructure: Domains
- T1556.004 - Modify Authentication Process: Modify OAuth Access Token

## Notes
This vulnerability class (subdomain takeover via dangling DNS) remains prevalent despite being well-documented. The attack succeeds because S3 bucket names are globally unique and cannot be reserved indefinitely. The victim (Twitter/X) is the registrant organization per WHOIS, confirming domain ownership but failure in DNS hygiene. Impact elevated because images.crossinstall.com likely served user-facing content, making it attractive for cookie theft, malware distribution, or OAuth attacks.

## Full report
<details><summary>Expand</summary>

## Summary
images.crossinstall.com points to an AWS S3 bucket that no longer exists. I was able to take control of this bucket and put my own content onto it. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

## PoC
Visit images.crossinstall.com/index.html; an HTML comment with my username is present.

```
% dig images.crossinstall.com +short
assets.crossinstall.com.s3.amazonaws.com.
s3-1-w.amazonaws.com.
s3-w.us-east-1.amazonaws.com.
52.217.103.180

% curl images.crossinstall.com/index.html
<!-- hackerone/ian bugcrowd/iangcarroll -->

% whois crossinstall.com | grep Org
Registrant Organization: Twitter, Inc.
Admin Organization: Twitter, Inc.
Tech Organization: Twitter, Inc.
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
