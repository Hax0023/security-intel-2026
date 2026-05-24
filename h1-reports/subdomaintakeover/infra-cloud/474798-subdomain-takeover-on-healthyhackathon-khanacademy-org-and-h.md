# Subdomain Takeover via Unclaimed S3 Bucket - healthyhackathon.khanacademy.org and hackweek.khanacademy.org

## Metadata
- **Source:** HackerOne
- **Report:** 474798 | https://hackerone.com/reports/474798
- **Submitted:** 2019-01-04
- **Reporter:** katsuragicsl
- **Program:** Khan Academy
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Records, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
Two Khan Academy subdomains (healthyhackathon.khanacademy.org and hackweek.khanacademy.org) had DNS records pointing to non-existent S3 buckets, allowing an attacker to claim the buckets and serve arbitrary content. This enabled phishing attacks and information collection from users expecting legitimate hackathon content.

## Attack scenario
1. Attacker discovers subdomains via subdomain enumeration or SSL certificate transparency logs
2. Attacker performs DNS resolution and determines the domains point to S3 endpoints
3. Attacker verifies the target S3 bucket does not exist by attempting access
4. Attacker creates an S3 bucket with the same name in their AWS account
5. Attacker uploads phishing content mimicking legitimate Khan Academy hackathon pages
6. Attacker collects credentials/information from users visiting the compromised subdomain

## Root cause
Dangling DNS records pointing to S3 buckets that were deleted or never provisioned, combined with lack of DNS record cleanup after S3 bucket decommissioning. No verification that backend resources exist before DNS delegation.

## Attacker mindset
Low-effort, high-impact attack targeting brand trust. Attacker recognizes that users will trust content served on official Khan Academy subdomains without verifying the actual hosting provider. Phishing via trusted domain is more effective than direct phishing emails.

## Defensive takeaways
- Implement DNS record auditing to identify and remove dangling records pointing to non-existent cloud resources
- Establish process for simultaneous removal of DNS records and cloud resource decommissioning
- Use cloud provider solutions like S3 bucket naming restrictions or domain verification to prevent unauthorized bucket claims
- Monitor for subdomain takeovers using tools like can-i-takeover-xyz or internal scanning
- Implement CAA records and DNSSEC to reduce DNS hijacking surface
- Require verification of resource existence before accepting DNS delegation
- Maintain inventory of all subdomains and their corresponding backend resources

## Variant hunting
Check other Khan Academy subdomains for similar dangling DNS records
Scan for Heroku, GitHub Pages, Firebase, Fastly, or other platform-specific takeovers on subdomains
Look for CNAME records pointing to services that support arbitrary domain attachment
Review AWS CloudFront, API Gateway, and ALB configurations for accessible subdomains
Check CNAME records that may point to acquired/merged services with different ownership
Investigate subdomains referenced in historical SSL certificates no longer in use

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing
- T1598 - Phishing for Information
- T1583.001 - Acquire Infrastructure: Domains

## Notes
This is a classic subdomain takeover vulnerability often overlooked because DNS infrastructure is managed separately from application infrastructure. The reporter provided good context with reference to the can-i-takeover-xyz project. The impact statement correctly identifies the phishing/spoofing angle as the primary threat. Khan Academy's reputation with users makes this particularly dangerous for social engineering.

## Full report
<details><summary>Expand</summary>

#Summary :
healthyhackathon.khanacademy.org can be took over, since it points to a bucket in S3 but that bucket does not exists.

I know this domain is used to host information of healthyhackathon which is held by khanacademy, but you will not be able to do this anymore if someone is going to claim that bucket. 

#Reference :
[S3_takeover](https://github.com/EdOverflow/can-i-take-over-xyz/issues/36)

## Impact

Taking control of healthyhackathon.khanacademy.org and spoof khanacademy users that healthyhackathon is reopened/"archived for you to challenge" and collect their information.

</details>

---
*Analysed by Claude on 2026-05-24*
