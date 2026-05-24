# Subdomain Takeover of www2.growasyouplan.com via Abandoned AWS EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 1179193 | https://hackerone.com/reports/1179193
- **Submitted:** 2021-04-28
- **Reporter:** ian
- **Program:** Palo Alto Networks
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, IP Reuse Vulnerability
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain www2.growasyouplan.com contained a dangling DNS A record pointing to an AWS EC2 instance IP (67.202.62.93) that was no longer under the organization's control. An attacker was able to launch their own EC2 instance at the same IP address and serve arbitrary content under this domain.

## Attack scenario
1. Attacker identifies that www2.growasyouplan.com resolves to IP 67.202.62.93
2. Attacker determines the IP address is no longer in use by Palo Alto's infrastructure
3. Attacker launches a new AWS EC2 instance and obtains the same IP address through AWS's IP reuse pool
4. Attacker configures the instance to respond to requests for www2.growasyouplan.com
5. Attacker obtains a valid TLS certificate for the domain (via Let's Encrypt or similar)
6. Attacker serves malicious content to users/services attempting to reach the subdomain

## Root cause
Organization failed to properly decommission infrastructure and clean up associated DNS records. The subdomain DNS record was left pointing to an IP address after the original EC2 instance was terminated, allowing AWS to reassign the IP to a different customer.

## Attacker mindset
Opportunistic reconnaissance attacker scanning for dangling DNS records and abandoned infrastructure. The attack requires minimal effort once the vulnerability is discovered—simply requesting an EC2 instance with the same IP creates immediate trust exploitation opportunities.

## Defensive takeaways
- Implement DNS record lifecycle management: audit all DNS records quarterly and remove those pointing to decommissioned infrastructure
- Establish infrastructure decommissioning procedures that include synchronized DNS cleanup
- Monitor subdomain enumeration and validate that all subdomains point to active, owned infrastructure
- Use DNS CAA records to restrict certificate issuance to authorized CAs only
- Implement DNSSEC to prevent DNS hijacking
- For critical subdomains, consider using subdomain takeover monitoring services
- Review and restrict scope of domain-level cookies and OAuth configurations
- Implement content security policies and HSTS headers to mitigate some impacts of successful takeover

## Variant hunting
Scan all subdomains of growasyouplan.com and related domains for similar dangling records
Check for other Palo Alto properties that may have abandoned subdomains
Enumerate subdomains across all acquisitions/subsidiaries of Palo Alto
Look for subdomains pointing to deprecated hosting platforms (Heroku, GitHub Pages, Azure, etc.)
Check for CNAME records pointing to abandoned services (CloudFront, S3 buckets, etc.)
Investigate internal/staging subdomains that may have been forgotten

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1566 - Phishing (via malicious content served on trusted domain)
- T1200 - Traffic Redirection
- T1583.001 - Acquire Infrastructure: Domains

## Notes
This is a classic subdomain takeover resulting from infrastructure drift and poor DNS hygiene. The vulnerability is straightforward to exploit once discovered but has significant impact due to domain trust. The reporter demonstrated responsible disclosure by including a proof-of-concept identifier (hackerone.com/ian) in the response rather than serving truly malicious content.

## Full report
<details><summary>Expand</summary>

## Summary
www2.growasyouplan.com points to an AWS EC2 instance at 67.202.62.93 that no longer exists. I was able to take control of this IP address and run my own EC2 instance. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

### Proof of scope
`growasyouplan.com` is owned by the same company as `paloalto.com`.

```
% whois growasyouplan.com | grep Org
Registrant Organization: Palo Alto Software, Inc.
```

### PoC
```
% dig +short www2.growasyouplan.com
67.202.62.93

% curl www2.growasyouplan.com
<!-- hackerone.com/ian -->
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
