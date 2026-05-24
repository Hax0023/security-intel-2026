# Subdomain Takeover of v.zego.com via Unclaimed AWS EC2 Instance

## Metadata
- **Source:** HackerOne
- **Report:** 1180697 | https://hackerone.com/reports/1180697
- **Submitted:** 2021-04-29
- **Reporter:** ian
- **Program:** Zego
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** memory-binary

## Summary
The subdomain v.zego.com was configured to point to an AWS EC2 instance (52.214.138.192) that was no longer owned or controlled by Zego. An attacker could claim this unallocated IP address by launching their own EC2 instance, gaining full control over the subdomain's content and HTTPS certificates. This could enable credential theft, malware distribution, or session hijacking if clients or integrations trust content served from this domain.

## Attack scenario
1. Attacker discovers v.zego.com resolves to 52.214.138.192, an orphaned AWS IP
2. Attacker launches a new AWS EC2 instance and obtains the same elastic IP address
3. Attacker serves malicious content on v.zego.com and obtains a valid TLS certificate
4. If OAuth whitelists *.zego.com, attacker can impersonate the service and steal credentials
5. Alternatively, attacker can serve malware or phishing content to customers expecting legitimate Zego resources
6. If cookies are scoped to .zego.com domain, attacker can steal session tokens from other subdomains

## Root cause
Zego decommissioned the EC2 instance backing v.zego.com but failed to remove or update the corresponding DNS record. The dangling DNS record pointed to an IP address that was released back to AWS's available pool, allowing any attacker to claim it by spinning up a new instance.

## Attacker mindset
An opportunistic attacker performing subdomain enumeration to identify dangling DNS records. The attacker recognized that unclaimed cloud infrastructure hosting subdomains of legitimate domains presents a low-effort, high-impact attack vector. The attacker leveraged the trust relationship between the domain owner and potential consumers to gain access to sensitive resources or credentials.

## Defensive takeaways
- Maintain an inventory of all DNS records and regularly audit for dangling or orphaned entries
- Implement automated checks to verify that DNS targets still resolve to active, owned infrastructure
- Use DNS validation tools (e.g., DNSdumpster, Censys) to identify stale records pointing to cloud resources
- When decommissioning cloud resources, immediately update or remove associated DNS records
- Consider using CNAME records pointing to CloudFront or API Gateway instead of directly to EC2 IPs to reduce takeover risk
- Scope cookies and OAuth redirects narrowly (specific subdomains) rather than wildcard domain scoping
- Monitor cloud provider IP allocation changes for your organization's IP ranges
- Implement certificate pinning or validation for critical subdomains to prevent SSL/TLS exploitation
- Use cloud provider resource tags and automated cleanup policies to track resource lifecycle

## Variant hunting
Search for other Zego subdomains pointing to orphaned cloud infrastructure (AWS, Azure, GCP). Check for other AWS elastic IPs associated with Zego's IP ranges that may have been released. Examine CNAME records pointing to non-existent cloud resources. Test other subdomains (api.zego.com, cdn.zego.com, etc.) for similar conditions. Review WHOIS and certificate transparency logs for historical IP allocations.

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1584.001 - Compromise Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing for Information: Spearphishing Link

## Notes
This is a classic subdomain takeover vulnerability that demonstrates the importance of DNS hygiene. The attacker provided clear PoC evidence (dig output and curl response). The severity depends on how v.zego.com is used—if it hosts sensitive APIs, OAuth endpoints, or serves content to high-value targets, the impact could be critical. AWS IP recycling makes this a persistent threat unless proactively remediated. The reporter successfully demonstrated control by serving recognizable content on the subdomain.

## Full report
<details><summary>Expand</summary>

## Summary
v.zego.com points to an AWS EC2 instance at 52.214.138.192 that no longer exists. I was able to take control of this IP address and run my own EC2 instance. I can now serve content on this domain, obtain a TLS certificate for this domain, etc.

If any customers or servers are pointing to anything within this domain, I could serve them arbitrary/malicious content. I could also use this in case your domain whitelists your own domain for OAuth, or if there are cookies scoped to the entire domain. Usually this can have a high impact.

### PoC
```
% dig +short v.zego.com
52.214.138.192

% curl v.zego.com
<!-- hackerone.com/ian -->
```

## Impact

Subdomain takeover

</details>

---
*Analysed by Claude on 2026-05-24*
