# Subdomain Takeover on delivery.yelp.com via Unclaimed S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 1715538 | https://hackerone.com/reports/1715538
- **Submitted:** 2022-09-28
- **Reporter:** racersaravanaa05
- **Program:** Yelp
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, S3 Bucket Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain delivery.yelp.com contained a dangling CNAME record pointing to an AWS S3 bucket endpoint that was not claimed by Yelp. An attacker could register/create the S3 bucket with the same name and host malicious content, impersonating Yelp's delivery service. This could lead to phishing, malware distribution, and severe reputational damage.

## Attack scenario
1. Attacker discovers that delivery.yelp.com resolves to an S3 bucket endpoint via DNS CNAME record
2. Attacker verifies the S3 bucket is unclaimed by attempting to access it and finding no content
3. Attacker creates an AWS S3 bucket with the name 'delivery.yelp.com'
4. Attacker uploads malicious HTML content (phishing page, malware payload) to the bucket
5. Attacker enables static website hosting on the S3 bucket
6. Users visiting delivery.yelp.com are redirected to attacker's malicious content, believing it's legitimate Yelp infrastructure

## Root cause
Yelp configured a CNAME record for delivery.yelp.com pointing to an AWS S3 bucket but failed to claim/reserve the bucket or remove the DNS record when the service was deprecated. This left a dangling DNS pointer that an attacker could abuse.

## Attacker mindset
An opportunistic attacker performing reconnaissance on organizational infrastructure, discovering forgotten/abandoned subdomains that still have active DNS records but unclaimed backend resources. The attacker exploits this configuration gap to impersonate a trusted service for phishing or malware distribution campaigns.

## Defensive takeaways
- Maintain an inventory of all subdomains and their associated services/endpoints
- Regularly audit DNS records for dangling CNAME pointers to external services
- When decommissioning services, either remove DNS records or claim/secure the backend resource
- For S3 buckets, verify ownership and implement bucket policies to prevent unauthorized access
- Monitor for unauthorized S3 bucket creation attempts matching your domain names
- Implement DNS CAA records to control certificate issuance for subdomains
- Use automated scanning tools to detect subdomain takeover vulnerabilities
- Implement alerts for DNS changes and new subdomain registrations

## Variant hunting
Scan all Yelp subdomains for dangling DNS records pointing to unclaimed cloud resources (S3, GitHub Pages, Heroku, Azure, etc.)
Check for similar patterns on related domains (yelp.com, yelp-owned properties)
Identify other subdomains pointing to S3 buckets that may not be claimed
Look for CNAME records pointing to deprecated or legacy services
Check subdomains for certificate transparency logs showing certificates for similar domains

## MITRE ATT&CK
- T1190
- T1583.001
- T1585.001
- T1598
- T1597

## Notes
The report quality is moderate with basic reproduction steps. The researcher correctly identified the vulnerability type and provided a working proof of concept. However, the writeup could be more detailed regarding DNS enumeration methodology. The typo in the title ('delivey' vs 'delivery') suggests this may have been a lower-tier submission. No specific bounty amount was disclosed, suggesting it may not have been high-priority despite the clear impact.

## Full report
<details><summary>Expand</summary>

## Summary:
[Subdomain takeover vulnerabilities occur when a subdomain (delivery.yelp.com) is pointing to a service]
Vulnerable url : delivery.yelp.com
This is an [verify Link](http://delivery.yelp.com.s3-website-us-east-1.amazonaws.com/).
{F1959331}

## Platform(s) Affected:
[website  ]


## Steps To Reproduce

  1. [Create the Amazon S3 Bucket on this Name : delivery.yelp.com]
{F1959320}
  1. [then Upload the Attacker HTML web page]
  1. [then using Static Web hosting ]

## Supporting Material/References:
{F1959332}

Remediation
Remove the cname entry or claim the subdomain delivey.yelp.com on amazon aws

## Impact

Risk
fake website
malicious code injection
users tricking
company impersonation
This issue can have really huge impact on the companies reputation someone could post malicious content on the compromised site and then your users will think it's official but it's not.

Best Regards, 
Racer Saravanaa 05

</details>

---
*Analysed by Claude on 2026-05-24*
