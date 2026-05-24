# Subdomain Takeover on media.vine.co due to Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 32825 | https://hackerone.com/reports/32825
- **Submitted:** 2014-10-25
- **Reporter:** fransrosen
- **Program:** Vine (HackerOne)
- **Bounty:** Not specified in report
- **Severity:** critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Cloud Service Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
Vine's subdomain media.vine.co was configured with a CNAME pointing to AWS S3 (vines.s3.amazonaws.com), but the corresponding bucket was never created or was deleted. An attacker could claim the unclaimed S3 bucket named 'media.vine.co' to serve arbitrary content on a trusted company domain, enabling phishing, malware distribution, and XSS attacks.

## Attack scenario
1. Attacker enumerates DNS records for Vine subdomains and discovers media.vine.co CNAME pointing to vines.s3.amazonaws.com
2. Attacker recognizes S3 CNAME misconfiguration where bucket name must match the CNAME hostname (media.vine.co)
3. Attacker creates an AWS S3 bucket named 'media.vine.co' in the appropriate region
4. Attacker uploads phishing HTML (e.g., fake login form) or malicious content to the S3 bucket
5. Attacker tricks users by directing them to http://media.vine.co/login, appearing as legitimate Vine domain
6. Users enter credentials or download malware, believing they're interacting with legitimate Vine infrastructure

## Root cause
Vine maintained a DNS CNAME record pointing to an S3 bucket that either never existed or was deleted without removing the corresponding DNS entry. Additionally, no monitoring or DNS hygiene process was in place to detect orphaned cloud service pointers.

## Attacker mindset
An attacker seeks to abuse trusted domain branding for credential theft and social engineering. The high trust users have in vine.co domain makes it an attractive target for phishing. The misconfiguration represents a low-effort, high-impact attack vector requiring only cloud service account creation.

## Defensive takeaways
- Regularly audit all DNS records (A, AAAA, CNAME, MX) and verify that external service pointers are actively used and owned
- Implement DNS monitoring and alerting for orphaned or misconfigured records pointing to cloud services
- Remove DNS entries immediately when decommissioning cloud resources or subdomains
- Establish subdomain takeover protection by monitoring unclaimed resources matching your domain patterns
- Use DNS validation and zone file version control to detect unauthorized changes
- Implement CAA records to restrict SSL certificate issuance for subdomains
- Document all external service integrations and maintain an inventory of active cloud resource bindings
- Enable AWS S3 bucket creation prevention by using SCPs and resource policies scoped to owned buckets

## Variant hunting
Search for other subdomains with CNAME records pointing to: GitHub Pages, Heroku, Shopify, Firebase, Azure Blob Storage, Fastly, Akamai, or any external CDN/cloud service. Check for similar misconfigured S3 bucket pointers where bucket name doesn't match hostname or points to deleted buckets.

## MITRE ATT&CK
- T1190
- T1566.002
- T1598.003
- T1589.002
- T1583.001

## Notes
This report was submitted in 2015 when subdomain takeover was a novel vulnerability class. The reporter references Detectify's advisory on hostile subdomain takeover, indicating this was part of early industry awareness. The vulnerability is particularly severe because it affects brand-trusted domains, making social engineering highly effective. The reporter noted a geographic limitation (bucket availability in specific AWS regions) that slightly mitigated impact but would not prevent attacks in correctly configured regions.

## Full report
<details><summary>Expand</summary>

Hi,
This is an urgent issue and I hope you will act on it likewise.
Your subdomain media.vine.co is pointing to AWS S3, but no bucket was connected to it. Actually, the reason to it is due to the CNAME of the meda.vine.co-DNS-entry:

```
media.vine.co
 -> media.vine.co is an alias for vines.s3.amazonaws.com.
```

This might have worked before, since there is a bucket with the name "vines". However, these are the rules for how CNAMEs to S3 are working currently:

> Customizing Amazon S3 URLs with CNAMEs
> 
> Depending on your needs, you might not want "s3.amazonaws.com" to appear on your website or service. For example, if you host your website images on Amazon S3, you might prefer http://images.johnsmith.net/ instead of http://johnsmith-images.s3.amazonaws.com/.
> 
> The bucket name must be the same as the CNAME. So http://images.johnsmith.net/filename would be the same as http://images.johnsmith.net.s3.amazonaws.com/filename if a CNAME were created to map images.johnsmith.net to images.johnsmith.net.s3.amazonaws.com.

So what happens here is actually that, since media.vine.co is pointing to S3, S3 is actually checking if there's a bucket with that name. Which in this case was not true. So I was able to claim the bucket media.vine.co and thus, can place content on this URL.

 _You should immediately remove the DNS-entry for media.vine.co pointing to AWS S3._ 

Since I have complete control over the subdomain I can do whatever I want on it. The restriction I have now is that I'm not able to serve anything on the root-URL ( http://media.vine.co/ ) – however – if I would have created the bucket in the correct region (West-1) in AWS, this would've worked.

Creating a login form that would fool anyone, since it's present on a Vine.co domain.

POC-link:
http://media.vine.co/login

POC-image attached.

This is really severe. Foolproof phishing. XSS on vine.co. Potential malware spread through a domain you – in this case – do not control. Extremely painful for the Company Brand.

Please make sure you're always going through your DNS-entries so no subdomains are pointing to external services you do not use.

We've written an advisory about this at Detectify:
http://blog.detectify.com/post/100600514143/hostile-subdomain-takeover-using-heroku-github-desk

Where you can read more about this sort of attack.

Regards,
Frans

</details>

---
*Analysed by Claude on 2026-05-24*
