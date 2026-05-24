# Subdomain Takeover on users.tweetdeck.com via Unclaimed AWS S3 Bucket

## Metadata
- **Source:** HackerOne
- **Report:** 42236 | https://hackerone.com/reports/42236
- **Submitted:** 2014-12-31
- **Reporter:** missoum1307
- **Program:** Twitter
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, AWS S3 Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain users.tweetdeck.com was pointing to an AWS S3 endpoint without an actual S3 bucket being configured or claimed. An attacker could register or claim the corresponding S3 bucket to assume control of the subdomain and serve arbitrary content under the legitimate domain.

## Attack scenario
1. Attacker discovers that users.tweetdeck.com resolves to an AWS S3 endpoint via DNS enumeration or CNAME analysis
2. Attacker identifies that no S3 bucket is currently configured for that endpoint
3. Attacker creates or claims an AWS S3 bucket matching the dangling CNAME record
4. Attacker uploads malicious content (phishing pages, malware, defacement) to the bucket
5. Legitimate users access users.tweetdeck.com and are served attacker-controlled content from the compromised S3 bucket
6. Attacker can conduct phishing attacks, distribute malware, or deface the service with full domain trust

## Root cause
DNS CNAME record pointing to AWS S3 was not cleaned up after the S3 bucket was deleted, deprovisioned, or never properly configured. No validation mechanism ensured the S3 bucket remained claimed and controlled by Twitter.

## Attacker mindset
An attacker would systematically scan for dangling DNS records pointing to cloud services. The presence of a legitimate domain (tweetdeck.com) with weak subdomain management presents an easy takeover opportunity. The attacker prioritizes high-trust domains where users would implicitly trust the subdomain.

## Defensive takeaways
- Implement DNS auditing to identify and remediate dangling CNAME records pointing to cloud services
- Establish a process to remove DNS records when corresponding cloud resources are deprovisioned
- Use cloud provider features like S3 bucket policies to prevent unauthorized bucket creation matching specific patterns
- Monitor for unclaimed subdomains pointing to AWS, Azure, GCP, and other cloud providers
- Implement DNSSEC and domain validation checks as part of infrastructure lifecycle management
- Maintain an inventory of all subdomains and their corresponding cloud resources
- Periodically verify that all DNS records resolve to active, authorized services

## Variant hunting
Search for other dangling CNAME records across Twitter's subdomain portfolio (cdn.*, api.*, static.*, etc.)
Check for similar unclaimed S3 buckets across other Twitter-owned domains (twitter.com, tweetdeck.com, periscope.com, vine.co)
Investigate other cloud providers (Azure blob storage, Google Cloud Storage, Heroku) for dangling records
Look for subdomains pointing to deprecated CDN endpoints, cloud storage, or hosting services
Test for takeover potential on subdomains with older or legacy CNAME records that may predate current ownership changes

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1584.004 - Compromise Infrastructure: DNS Records
- T1200 - Hardware Additions
- T1557 - Man-in-the-Middle

## Notes
This is a duplicate of report #32825, indicating the vulnerability was reported previously. The simplicity of the report and lack of technical detail suggests the researcher may not have fully exploited the vulnerability, but the impact is critical due to the ability to serve content under a trusted domain. AWS provides tools to prevent this via bucket name reservation and DNS validation, but only if properly configured by the domain owner.

## Full report
<details><summary>Expand</summary>

hi twitter security team .

This is an urgent issue  the same of report #32825
Your subdomain users.tweetdeck.com  is pointing to AWS S3, but no bucket was connected to it. an attacker can claim the domain and takeover the full subdomain. 

Please fix it as soon as possible , and let me know if you need any further information .

missoum 
best regards 




</details>

---
*Analysed by Claude on 2026-05-24*
