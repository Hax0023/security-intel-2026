# Subdomain Takeover of fr1.vpn.zomans.com via Unclaimed AWS EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 1182864 | https://hackerone.com/reports/1182864
- **Submitted:** 2021-05-03
- **Reporter:** ian
- **Program:** Zomans (via HackerOne)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Infrastructure Misconfiguration
- **CVEs:** None
- **Category:** business-logic

## Summary
The subdomain fr1.vpn.zomans.com contained a DNS A record pointing to an AWS EC2 instance (52.47.57.107) that was no longer under the organization's control. An attacker successfully registered and provisioned a new EC2 instance at the same IP address, gaining full control over the subdomain. This allowed serving arbitrary content, obtaining valid TLS certificates, and potentially intercepting traffic from clients or internal systems.

## Attack scenario
1. Attacker discovers fr1.vpn.zomans.com via DNS enumeration or passive reconnaissance
2. Attacker identifies the IP (52.47.57.107) no longer resolves to active Zomans infrastructure
3. Attacker provisions a new AWS EC2 instance and obtains the same public IP address
4. Attacker serves malicious content on the domain and obtains a valid TLS certificate
5. Attacker targets employees with phishing emails using the legitimate-looking subdomain
6. Attacker intercepts traffic from legacy clients or systems still configured to connect to this subdomain

## Root cause
The organization failed to maintain an inventory of active DNS records and their corresponding infrastructure. When the original EC2 instance was decommissioned, the DNS record was not cleaned up, leaving a dangling pointer to an IP that could be reclaimed by third parties.

## Attacker mindset
An attacker seeks to identify forgotten or orphaned infrastructure as a foothold for domain takeovers. The VPN-related subdomain is particularly valuable due to its apparent internal/security-critical nature, making it convincing for phishing campaigns targeting employees. The attacker recognizes that legacy systems or configurations may still trust this domain.

## Defensive takeaways
- Implement DNS record lifecycle management; audit and remove dangling DNS records regularly
- Maintain a centralized inventory of all subdomains and their corresponding infrastructure
- Implement monitoring for DNS changes and alert on modifications to critical subdomains
- Use DNS CAA records to restrict TLS certificate issuance for your domain
- Decommission infrastructure and DNS records in coordinated fashion with tracking
- Scan for dangling DNS records proactively using subdomain enumeration tools
- Implement name server monitoring to detect when IP addresses become available for reuse
- Use certificate transparency logs to detect unauthorized certificate issuance for your domains

## Variant hunting
Search for other orphaned subdomains pointing to AWS, Azure, or GCP resources. Check for dangling DNS records across all organizational subdomains, particularly those with security-sensitive names (vpn, api, auth, admin, internal). Verify CNAME records pointing to external services that may no longer exist. Investigate AWS/cloud provider IP space that may have been released and could be reclaimed.

## MITRE ATT&CK
- T1190
- T1584.001
- T1583.001
- T1598.003
- T1566.002

## Notes
This is a classic subdomain takeover vulnerability exploiting infrastructure drift. The report demonstrates both the technical feasibility (DNS resolution, certificate provisioning) and business impact (phishing credibility, potential data interception). The VPN context suggests this could be used to target employees with particularly convincing pretexting. The vulnerability required no authentication and had trivial exploitation difficulty, making it a valuable find.

## Full report
<details><summary>Expand</summary>

## Summary
fr1.vpn.zomans.com points to an AWS EC2 instance at 52.47.57.107 that no longer exists. I was able to take control of this IP address and run my own EC2 instance. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

Since the risk of employee phishing here is pretty high, along with the risk of existing clients connecting to this server, I think it qualifies as a High per your policy:
> Subdomain Takeover - on a domain that sees heavy traffic or would be a convincing candidate for a phishing attack

### PoC
```
% dig +short fr1.vpn.zomans.com
52.47.57.107

% curl fr1.vpn.zomans.com
<!-- hackerone.com/ian -->
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
