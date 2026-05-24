# Subdomain Takeover of ████.jitsi.net via Abandoned AWS EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 1197013 | https://hackerone.com/reports/1197013
- **Submitted:** 2021-05-14
- **Reporter:** ian
- **Program:** Jitsi
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record, Cloud Infrastructure Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A subdomain of jitsi.net (████.jitsi.net) contained a DNS A record pointing to an AWS EC2 instance (18.195.93.116) that was no longer owned or managed by Jitsi. The researcher was able to launch their own EC2 instance at the same IP address, gaining control over the subdomain and ability to serve arbitrary content under the jitsi.net domain. This could be leveraged for serving malicious content to users, OAuth attacks, or session hijacking via domain-scoped cookies.

## Attack scenario
1. Researcher identifies that ████.jitsi.net DNS record resolves to AWS EC2 IP 18.195.93.116
2. Researcher determines that the EC2 instance at that IP address is no longer active or owned by Jitsi
3. Researcher launches their own EC2 instance in the same AWS region and obtains the same IP address
4. The subdomain now resolves to the attacker's controlled instance, allowing them to serve arbitrary content
5. Attacker obtains a valid TLS certificate for the subdomain using Let's Encrypt or similar service
6. Attacker can now intercept traffic from users/services pointing to the subdomain, perform OAuth attacks, steal cookies, or distribute malicious content

## Root cause
Jitsi failed to properly decommission or remove DNS records for subdomains after terminating the underlying AWS infrastructure. The dangling DNS record continued to point to an IP address in the public AWS IP pool that could be reassigned to other customers.

## Attacker mindset
An attacker would systematically scan for dangling DNS records across target organizations' subdomains, identify those pointing to cloud infrastructure, and attempt to acquire the same cloud resources (EC2 instances, storage buckets, etc.). The subdomain takeover provides a foothold for credential harvesting, malware distribution, or lateral movement if the domain has special trust relationships configured.

## Defensive takeaways
- Implement DNS auditing processes to identify and remove dangling DNS records when infrastructure is decommissioned
- Use DNS monitoring tools to alert on changes to DNS records or when records point to non-existent/unowned resources
- Maintain an inventory of all subdomains and their associated infrastructure, with regular reconciliation
- Consider using CNAME records to AWS-managed services (e.g., CloudFront, ALB DNS names) instead of direct IP addresses to prevent reassignment issues
- Implement DNSSEC to prevent DNS hijacking attacks
- Use AWS Shield and WAF to detect and block suspicious traffic from subdomain takeover attempts
- Monitor certificate transparency logs for unauthorized certificates issued for your domains
- Implement domain-level access controls and consider zone file integrity monitoring

## Variant hunting
Search for other subdomains of jitsi.net pointing to AWS EC2 instances; check for similar patterns in related domains; look for subdomains pointing to other cloud providers (Azure, GCP) with unowned resources; examine subdomains pointing to outdated S3 bucket names; investigate subdomains with CNAME records pointing to decommissioned services

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1589 - Gather Victim Identity Information
- T1598 - Phishing: Reconnaissance
- T1566 - Phishing
- T1583 - Acquire Infrastructure

## Notes
This is a classic dangling DNS record vulnerability common in organizations that rapidly scale infrastructure or fail to properly offboard services. The impact is amplified because Jitsi.net is a trusted domain, making users more likely to accept content served from its subdomains. The researcher responsibly disclosed through HackerOne rather than actively exploiting the vulnerability for malicious purposes.

## Full report
<details><summary>Expand</summary>

## Summary
█████.jitsi.net points to an AWS EC2 instance at 18.195.93.116 that no longer exists. I was able to take control of this IP address and run my own EC2 instance. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

```
% dig +short ██████.jitsi.net
18.195.93.116

% curl ██████████.jitsi.net
<!-- hackerone.com/ian -->
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
