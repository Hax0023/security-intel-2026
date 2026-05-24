# Subdomain Takeover via Unclaimed AWS CloudFront Distribution

## Metadata
- **Source:** HackerOne
- **Report:** 317005 | https://hackerone.com/reports/317005
- **Submitted:** 2018-02-17
- **Reporter:** zephrfish
- **Program:** data.gov (GSA)
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain (18f.domains.api.data.gov) was configured with a CNAME record pointing to an AWS CloudFront distribution that was no longer claimed by the organization. An attacker was able to register a new CloudFront distribution and claim the subdomain, achieving complete subdomain takeover and enabling credential harvesting and phishing attacks.

## Attack scenario
1. Attacker performs DNS enumeration and identifies the subdomain 18f.domains.api.data.gov pointing to dn9rrjaiux2m0.cloudfront.net
2. Attacker visits the subdomain and observes an unclaimed CloudFront error page, indicating the distribution is no longer owned
3. Attacker creates a new AWS CloudFront distribution under their control
4. Attacker claims the hostname 18f.domains.api.data.gov in the new CloudFront distribution (AWS allows this since no current owner exists)
5. Attacker configures the CloudFront distribution to serve malicious content (phishing page, credential harvester, or malware)
6. Victims accessing the subdomain are now directed to attacker-controlled infrastructure, enabling credential theft and brand impersonation

## Root cause
Organization created a DNS CNAME record pointing to a third-party AWS CloudFront distribution but failed to remove or maintain the DNS entry after discontinuing use of the service. AWS CloudFront allowed the attacker to claim the hostname without additional verification checks, assuming the subdomain owner had relinquished control.

## Attacker mindset
Opportunistic attacker identifying forgotten infrastructure as an easy path to domain takeover. The attacker recognized that dangling DNS records pointing to unclaimed cloud services represent quick wins requiring minimal effort. By simply registering a new CloudFront distribution and claiming the hostname, the attacker bypassed all authentication barriers and gained legitimate-looking infrastructure for phishing or malware distribution.

## Defensive takeaways
- Implement a comprehensive DNS audit process to identify and remediate dangling DNS records pointing to third-party services
- Establish a service lifecycle management process that explicitly requires removal of DNS records when external services are decommissioned
- Use DNS monitoring and alerting tools to detect changes to DNS records and identify orphaned CNAME entries
- Maintain an inventory of all DNS records and their associated services/owners with regular reviews
- Replace dangling records with redirects to a canonical domain or error page rather than leaving them completely unresolved
- Implement nameserver monitoring to detect unauthorized claim attempts on cloud services
- Use DNS CAA records to control which CAs can issue certificates for subdomains
- Require MFA and verification steps for claiming subdomains/hostnames in cloud provider consoles
- Conduct regular security assessments of subdomain infrastructure across the organization

## Variant hunting
Search for other subdomains of data.gov pointing to AWS CloudFront, S3, or other cloud services that may be unclaimed
Scan for dangling CNAME records pointing to Heroku, Azure App Service, GitHub Pages, Shopify, and other common platforms
Use SubdomainFinder/Amass to enumerate all subdomains and check CNAME targets for unclaimed status
Monitor CloudFront/AWS for new distributions claiming government domain hostnames
Identify other GSA services with similar infrastructure management patterns that may have orphaned records
Check for CNAME records in DNS that resolve to service error pages indicating unclaimed resources
Audit all first-level subdomains of data.gov for external service dependencies

## MITRE ATT&CK
- T1589.001 - Gather Victim Identity Information (Credentials)
- T1598.003 - Phishing - Spearphishing Link
- T1187 - Forced Authentication
- T1566.002 - Phishing - Spearphishing Link

## Notes
This vulnerability was reported on an out-of-scope domain but the researcher correctly identified it as a valid security issue affecting data.gov. The report demonstrates excellent attack scenario documentation. The CVSS score of 7.7 reflects the high impact (credential theft, phishing potential) against low attack complexity. AWS's lack of verification when claiming hostnames on CloudFront distributions significantly increases risk. The reporter includes proof-of-concept screenshots showing successful takeover. This is a classic example of infrastructure debt in government systems where services are spun up but not properly decommissioned.

## Full report
<details><summary>Expand</summary>

**Note: I know this is on an out of scope domain, however felt it should still be raised as it was the only subdomain of data.gov to be vulnerable.**

## Issue Details

The consultant identified that subdomain `https://18f.domains.api.data.gov/` is pointing to `dn9rrjaiux2m0.cloudfront.net` via a DNS CNAME record. When browsing to the subdomain an AWS cloudflare error is displayed.

The subdomain "https://18f.domains.api.data.gov/" was (and still is) a CNAME pointing to a AWS Cloudfront CDN server (depending on your location, the latter will resolve differently):

```
 nslookup  18f.domains.api.data.gov
Server:         213.186.33.99
Address:        213.186.33.99#53

Non-authoritative answer:
18f.domains.api.data.gov        canonical name = dn9rrjaiux2m0.cloudfront.net.
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.116
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.87
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.105
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.202
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.145
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.21
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.64
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 52.85.89.161
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:d000:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:6600:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:6400:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:5000:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:be00:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:c400:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:4400:3:f914:5e00:93a1
Name:   dn9rrjaiux2m0.cloudfront.net
Address: 2600:9000:2045:7000:3:f914:5e00:93a1

```

However, the hostname  was not claimed any more on Cloudfront, resulting in a Cloudfront error page when visiting the subdomain before the takeover.

Subsequently, a new Amazon Cloudfront CDN endpoint was created and linked to an attacker-controlled origin server. For the new Cloudfront CDN endpoint, `18f.domains.api.data.gov` was designated as hostname successfully:

{F264221}

This concluded the subdomain takeover:

{F264222}

## Risk Breakdown
- Risk: High
- Difficulty to Exploit: Medium
- CVSS3 Score: 7.7 AV:N/AC:L/PR:N/UI:N/S:C/C:L/I:L/A:L/E:P/RL:O/RC:R

## Affected URLs

- 18f.domains.api.data.gov

## Attack Scenario

1. TTS starts using a new service, eg an external Support Ticketing-service, in this case aws.
2. TTS points a subdomain to the Support Ticketing-service, eg 18f.domains.api.data.gov
3. TTS stops using this service but does not remove the subdomain redirection pointing to the ticketing system.
4. Attacker signs up for the Service and claims the domain as theirs. No verification is done by the Service Provider, and the DNS-setup is already correctly setup.
5. Attacker can now build a complete clone of the real site, add a login form, redirect the user, steal credentials (e.g. admin accounts), cookies and/or completely destroy business credibility for your company.

## Recommendation
The most effective way to remediate this issue would be to remove the DNS entry entirely however if this is not possible, consider pointing the DNS entry at a redirect of some description to prevent potential hostile take over.

## Impact

Sub-domain take over attacks can happen when a company creates a dns entry that points to a third party service, however forgets about the third party application leaving it vulnerable to be hijacked by another party. Hackers can claim subdomains with the help of external services. This attack is practically non-traceable.

</details>

---
*Analysed by Claude on 2026-05-24*
