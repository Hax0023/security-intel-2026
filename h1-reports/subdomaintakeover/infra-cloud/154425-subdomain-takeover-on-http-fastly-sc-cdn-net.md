# Subdomain Takeover on fastly.sc-cdn.net via Dangling DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 154425 | https://hackerone.com/reports/154425
- **Submitted:** 2016-07-27
- **Reporter:** ebrietas
- **Program:** Snapchat
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Third-party Service Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A Snapchat CDN subdomain (fastly.sc-cdn.net) retained a DNS CNAME record pointing to Fastly after the service was cancelled, allowing an attacker to register a Fastly instance and take control of the domain. While the domain appeared unused on Snapchat properties, it could be leveraged for credential theft, malware distribution, or session hijacking if referenced in cached content.

## Attack scenario
1. Attacker identifies fastly.sc-cdn.net as a Snapchat property through certificate enumeration (Censys)
2. Attacker discovers the domain has a CNAME record pointing to Fastly's nameservers despite the service being cancelled
3. Attacker registers a new Fastly account and claims the unclaimed fastly.sc-cdn.net subdomain
4. Attacker configures the Fastly instance to serve malicious content or perform man-in-the-middle attacks
5. If the domain is referenced in cached pages or client-side code, user requests are redirected to attacker-controlled infrastructure
6. Attacker could steal credentials, inject malware, or perform session fixation attacks on users accessing Snapchat services

## Root cause
Insufficient cleanup procedures when deprovisioning third-party CDN services. DNS records were not removed after the Fastly service was cancelled, leaving a dangling CNAME record that could be claimed by an attacker.

## Attacker mindset
Opportunistic reconnaissance approach: systematically enumerate organizational domains and third-party services, identify abandoned or misconfigured infrastructure, and exploit the window of opportunity before cleanup occurs. Low-hanging fruit targeting organizational sloppiness rather than sophisticated exploitation.

## Defensive takeaways
- Implement mandatory DNS record cleanup in service deprovisioning workflows
- Maintain an inventory of all third-party services and their associated DNS records
- Regularly audit DNS configurations for dangling CNAME records pointing to unclaimed services
- Use DNSSEC and CAA records to restrict certificate issuance on sensitive domains
- Monitor for subdomain takeover attempts by tracking DNS changes and unexpected service registrations
- Implement automated alerts when DNS records point to unclaimed third-party platforms
- Periodically scan for stale subdomains using tools like SubdomainTakeover or tko-subs

## Variant hunting
Search for other Snapchat subdomains with dangling records; enumerate all sc-cdn.net subdomains; identify other organizations using Fastly CDN with similar misconfiguration patterns; check for abandoned AWS CloudFront, Akamai, or other CDN provider integrations with orphaned DNS records

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1584 - Compromise Infrastructure
- T1583 - Acquire Infrastructure
- T1498 - Network Denial of Service

## Notes
Researcher responsibly validated the takeover risk and confirmed Snapchat ownership via certificate analysis. The minimal reported impact (domain unused in active properties) does not diminish the vulnerability class severity, as cached references or future reuse could activate the risk. This is a classic example of subdomain takeover via dangling DNS records—a well-documented but frequently overlooked vulnerability in organizational hygiene.

## Full report
<details><summary>Expand</summary>

Hey team,

I've found a snapchat cdn domain here which had a test instance of fastly setup but did not remove the dns record when the service was cancelled. This allowed me to create a Fastly instance to take it over. I've confirmed this is a snapchat property via Censys (https://censys.io/certificates/65ba2e172a1eb85eb1071c9fd7a4e8371ef12625409890507c89a54978305558) though the risk here seems minimal at best as this domain does not appear to be used anywhere on any snapchat properties.

Repro steps:

* Visit http://fastly.sc-cdn.net/takeover.html

Recommended fix:
Removal of this record is recommended.


</details>

---
*Analysed by Claude on 2026-05-24*
