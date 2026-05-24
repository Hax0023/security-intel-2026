# Subdomain Takeover via Dangling DNS Record on Azure CloudApp

## Metadata
- **Source:** HackerOne
- **Report:** 380158 | https://hackerone.com/reports/380158
- **Submitted:** 2018-07-10
- **Reporter:** txt3rob
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** uncategorised

## Summary
A DNS record for svcardproxydevus.starbucks.com pointed to a dead Azure CloudApp VM (s00307dpipsvcardproxy00.eastus.cloudapp.azure.com) that was no longer in use, allowing an attacker to claim the orphaned Azure resource and takeover the subdomain. This could enable credential harvesting attacks against internal staff and phishing campaigns leveraging the trusted Starbucks domain.

## Attack scenario
1. Attacker identifies the dangling DNS record pointing to a dead Azure CloudApp instance using DNS enumeration
2. Attacker provisions a new Azure VM with the same hostname to claim the orphaned Azure resource
3. Attacker hosts malicious content on the captured subdomain (pornographic content, phishing pages, etc.)
4. Attacker sends notification to Starbucks support claiming inappropriate content on their domain
5. When support visits the compromised subdomain, attacker's payload (UNC path image) triggers Windows authentication dialog via Responder
6. Attacker captures the NTLM hash from support staff and cracks it to gain credentials for VPN/internal network access

## Root cause
Starbucks failed to decommission DNS records when the corresponding Azure CloudApp resources were terminated, leaving the Azure resource namespace available for claim by external attackers. No monitoring existed to detect dangling DNS records pointing to deallocated cloud resources.

## Attacker mindset
An attacker recognizing that cloud resource takeovers combined with social engineering create a multi-stage attack chain. The attacker leverages the trusted corporate domain to lower victim suspicion and uses support staff's natural inclination to investigate reported issues as an exploitation vector. Credential theft through hash capture enables lateral movement rather than direct external impact.

## Defensive takeaways
- Implement DNS record audit processes to identify and remove dangling records pointing to deallocated/terminated cloud resources
- Use cloud provider native tools (Azure DNS zones scanning, AWS Route53 validation) to validate all DNS records periodically
- Prevent Azure resource name squatting by deleting/retiring cloud resources simultaneously with DNS record removal
- Deploy monitoring to alert on subdomain takeover attempts or unexpected resource claims in cloud environments
- Disable UNC path resolution in browsers or enforce NTLM authentication security controls to prevent hash harvesting
- Implement DNSSEC and DNS monitoring to detect unexpected changes to critical domain records
- Train support staff on phishing and social engineering risks when investigating user reports
- Maintain inventory of all DNS records mapped to cloud resources with clear lifecycle documentation

## Variant hunting
Search for other *.starbucks.com subdomains using dnsenum/Sublist3r and check which point to dead Azure/AWS/GCP resources
Check for dangling records pointing to: S3 buckets (bucket not found errors), GitHub pages (404 pages), Heroku apps, Firebase hosting
Identify CNAME records pointing to traffic managers, CDNs, or load balancers that may have underlying dead resources
Look for SSL certificates issued for subdomains that differ from currently active DNS records
Enumerate Azure resource names to find publicly accessible cloud app instances that may be unclaimed

## MITRE ATT&CK
- T1190
- T1583.001
- T1589.001
- T1598.003
- T1187
- T1557.001

## Notes
The reporter demonstrated sophisticated understanding of the attack chain combining cloud takeover, social engineering, credential harvesting (NTLM via Responder), and internal network pivoting. This represents a real threat as support staff are high-value targets. The vulnerability affects brand reputation and internal security. Azure-specific: verify that deleted CloudApp instances cannot be reclaimed by external subscribers and implement reservation holds on critical resource names.

## Full report
<details><summary>Expand</summary>

You have left a dns record pointing to a dead cloudapp vm.

```
svcardproxydevus.starbucks.com -> s00307ntmp0svcardproxydev0.trafficmanager.net -> s00307dpipsvcardproxy00.eastus.cloudapp.azure.com = Dead
```

## Impact

```
1) Attacker takes over subdomain and then puts something like porn or something that shouldn't be on the domain.
2) hacker then contacts support pretending to be a concerned user.
3) support click on it to check what is going on
4) attacker has put responder on the page via a image file using a UNC path (https://github.com/SpiderLabs/Responder)
5) attacker is then sent supports hash for their windows login.
6) attacker then cracks hash and uses the VPN to pivot 
```

They can also use it to phish and other bad activitys

</details>

---
*Analysed by Claude on 2026-05-24*
