# Subdomain Takeover on svcgatewaydevus.starbucks.com and svcgatewayloadus.starbucks.com

## Metadata
- **Source:** HackerOne
- **Report:** 383564 | https://hackerone.com/reports/383564
- **Submitted:** 2018-07-19
- **Reporter:** blurbdust
- **Program:** Starbucks
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS CNAME, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
Two Starbucks subdomains (svcgatewaydevus.starbucks.com and svcgatewayloadus.starbucks.com) contained CNAME records pointing to unclaimed Azure Traffic Manager endpoints. An attacker could claim these Azure resources and serve malicious content to thousands of users accessing these subdomains.

## Attack scenario
1. Attacker discovers DNS CNAME records pointing to unregistered Azure Traffic Manager endpoints via DNS enumeration or passive reconnaissance
2. Attacker creates a new Azure Traffic Manager profile matching the target CNAME (e.g., s00197tmp0crdfulload0.trafficmanager.net)
3. Attacker configures the Traffic Manager to serve malicious content (phishing pages, malware, XSS payloads)
4. Users accessing the Starbucks subdomains are redirected to attacker's infrastructure due to valid DNS resolution
5. Attacker harvests credentials, delivers malware, or executes XSS attacks on thousands of unique IPs (341 in 45 minutes during PoC)
6. Attack persists until Starbucks removes the dangling CNAME or claims the Azure resource

## Root cause
Starbucks created CNAME records in their DNS zone pointing to Azure Traffic Manager endpoints but failed to claim/configure the corresponding Azure resources, leaving them available for takeover. The organization did not implement DNS hygiene practices to validate or remove orphaned CNAME records.

## Attacker mindset
An attacker exploits operational negligence and cloud resource management gaps. They recognize that legitimate company infrastructure pointing to unclaimed cloud services represents a low-risk, high-impact opportunity to compromise user trust and deliver attacks at scale through an authentic domain.

## Defensive takeaways
- Implement DNS auditing and validation: regularly scan for CNAME records and verify all target resources are claimed and configured
- Enforce cloud resource lifecycle management: ensure all created Azure resources are properly provisioned or explicitly removed
- Deploy monitoring for dangling DNS records using automated tools that detect CNAME targets without corresponding active resources
- Implement DNSSEC and CAA records to reduce attack surface
- Establish ownership verification: before creating DNS records, confirm the target cloud resource exists and is under organizational control
- Conduct regular DNS hygiene audits, particularly during decommissioning or infrastructure changes
- Use subdomain takeover detection services to identify vulnerable configurations before attackers

## Variant hunting
Search DNS records for CNAME entries pointing to AWS CloudFront distributions, S3 buckets, or ELB endpoints that may be unclaimed
Identify CNAME records targeting GitHub Pages, Heroku, or other PaaS providers without validation
Scan for dangling records pointing to Fastly, Akamai, or other CDN providers
Check for orphaned CNAME records from previous vendors or decommissioned services
Enumerate subdomains of competitor organizations and test for similar takeover vulnerabilities
Analyze subdomain patterns (svcgateway*, load*, dev*) to identify related infrastructure that may share the same misconfiguration

## MITRE ATT&CK
- T1190
- T1566
- T1598
- T1589
- T1590
- T1596

## Notes
This report references a previous similar vulnerability (HackerOne #325336) on different Starbucks subdomains, indicating systemic DNS management issues. The attacker demonstrated real-world impact by reaching 341 unique IPs in 45 minutes, proving the vulnerability was actively exploited. The subdomain names (svcgateway, load, dev) suggest these were gateway or load-balancing services, possibly legacy or experimental infrastructure. Azure Traffic Manager's namespace is publicly registrable, making this a common attack vector for Azure deployments. The PoC links provided indicate the researcher demonstrated working proof-of-concept access before disclosure.

## Full report
<details><summary>Expand</summary>

Hello,

This is fairly close to [this report](https://hackerone.com/reports/325336) however these are different subdomains than the one in the report.

This can be pretty serious since I can server virtually anything I want. In the 45 minutes I've held the domain I have served to 341 unique IP addresses. 

Two starbucks.com subdomains are pointed to Azure with an unclaimed CNAME record. Anyone would be able to serve content on these subdomains.

##svcgatewayloadus.starbucks.com
```
;; Server: 1.1.1.1:53
;; Size: 191
;; Unix time: 1531965036
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 3697
;; flags: qr rd ra ; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 0

;; QUESTION SECTION:
svcgatewayloadus.starbucks.com. IN A

;; ANSWER SECTION:
svcgatewayloadus.starbucks.com. 600 IN CNAME s00197tmp0crdfulload0.trafficmanager.net.

;; AUTHORITY SECTION:
trafficmanager.net. 30 IN SOA tm1.msft.net. hostmaster.trafficmanager.net. 2003080800 900 300 2419200 30

```

##svcgatewaydevus.starbucks.com
```
;; Server: 9.9.9.9:53
;; Size: 156
;; Unix time: 1531965036
;; ->>HEADER<<- opcode: QUERY, status: NXDOMAIN, id: 47788
;; flags: qr rd ra ; QUERY: 1, ANSWER: 1, AUTHORITY: 1, ADDITIONAL: 0

;; QUESTION SECTION:
svcgatewaydevus.starbucks.com. IN A                                                                                                                                                            

;; ANSWER SECTION:
svcgatewaydevus.starbucks.com. 600 IN CNAME s00197tmp0crdfuldev0.trafficmanager.net.                                                                                                           

;; AUTHORITY SECTION:
trafficmanager.net. 30 IN SOA tm1.msft.net. hostmaster.trafficmanager.net. 2003080800 900 300 2419200 30
```

#PoC:
http://svcgatewayloadus.starbucks.com/
http://svcgatewaydevus.starbucks.com/

##Mitigation:
Remove the CNAME record from the starbucks.com DNS zone
Claim it in Azure once I release it

## Impact

Subdomain takeover can be used for several purposes:

* Malware
* Phishing / Spear phishing
* XSS
* Authentication bypass

</details>

---
*Analysed by Claude on 2026-05-24*
