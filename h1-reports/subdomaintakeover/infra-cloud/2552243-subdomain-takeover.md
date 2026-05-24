# Subdomain Takeover via Dangling CNAME Record Pointing to Unregistered Domain

## Metadata
- **Source:** HackerOne
- **Report:** 2552243 | https://hackerone.com/reports/2552243
- **Submitted:** 2024-06-14
- **Reporter:** martinvw
- **Program:** Unknown (Redacted HackerOne Report)
- **Bounty:** Unknown (Redacted)
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain maintained a CNAME record pointing to an ELB domain (open-elb-prod-277276106.us-east-1.elb-amazonaws.com) that was no longer registered or in use. An attacker could register the unowned domain and redirect the subdomain to malicious content. This enables hosting of arbitrary content under the target organization's domain with associated risks.

## Attack scenario
1. Attacker discovers the subdomain via DNS enumeration or certificate transparency logs
2. Attacker identifies the CNAME target (open-elb-prod-277276106.us-east-1.elb-amazonaws.com) is not actively registered or is orphaned
3. Attacker registers the orphaned domain or gains control of the AWS resources
4. Attacker configures the domain to serve malicious content, phishing pages, or perform XSS attacks
5. Victims visiting the subdomain under the organization's domain trust the content due to domain origin
6. Attacker harvests credentials, steals cookies, or executes client-side attacks against users

## Root cause
Stale CNAME DNS record pointing to a decommissioned or never-claimed AWS ELB endpoint. The organization failed to remove the DNS record when the underlying infrastructure was deprovisioned, creating a dangling pointer that allows external domain registration.

## Attacker mindset
Opportunistic domain registrant exploiting poor DNS hygiene. Low barrier to entry: identify orphaned domains via DNS queries, register them cheaply, and leverage the trusted parent domain for phishing/malware distribution without sophisticated exploitation.

## Defensive takeaways
- Implement DNS record inventory and audit processes; document purpose and owner of each CNAME/DNS record
- Establish automated monitoring to detect and alert on DNS records pointing to non-existent or decommissioned services
- Use DNSSEC and CNAME validation to ensure DNS records only point to owned infrastructure
- Implement a DNS decommissioning checklist requiring removal of all related records when infrastructure is removed
- Monitor certificate transparency logs and DNS datasets (e.g., Censys, SecurityTrails) for dangling subdomains
- Use subdomain takeover detection tools (e.g., can-i-take-over-xyz) as part of periodic security assessments
- Leverage CAA records and ACME account security to prevent fraudulent certificate issuance on takeover domains
- Implement Content Security Policy (CSP) headers to limit impact of compromised subdomains

## Variant hunting
Search for other CNAME records pointing to decommissioned AWS resources (ELB, CloudFront, S3, API Gateway endpoints)
Enumerate subdomains pointing to other cloud providers' orphaned infrastructure (Azure, GCP, Heroku, etc.)
Identify CNAME chains where intermediate targets are no longer active (recursive takeover potential)
Check for NS record delegations pointing to non-existent nameservers
Look for A/AAAA records pointing to unregistered or short-term parking IP addresses

## MITRE ATT&CK
- T1190
- T1589
- T1583
- T1583.1
- T1566.002
- T1598

## Notes
Severity assessment: HIGH due to multiple attack vectors (XSS, credential theft, phishing). This is a well-documented vulnerability class (CWE-404: Improper Resource Validation). The proof-of-concept hash (e7437329-ab61-4f22-a049-df5b3685313a.txt) suggests the report included working exploitation. Remediation is trivial (DNS record removal) but often overlooked due to lack of automated lifecycle management for DNS infrastructure.

## Full report
<details><summary>Expand</summary>

The subdomain `█████` is pointing to `open-elb-prod-277276106.us-east-1.elb-amazonaws.com.`, the domain `elb-amazonaws.com` was available for registration

## Impact

Using this vulnerability an attacker can:
- host unwanted/malicious content under your domain
- receive email on subdomains mentioned above
- effectively execute cross-site scripting attacks
- in some cases, steal cookie data
- in some cases, trick password managers into filling in passwords

## System Host(s)
█████████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Visit http://████████/proof.e7437329-ab61-4f22-a049-df5b3685313a.txt

## Suggested Mitigation/Remediation Actions
Remove CNAME record █████



</details>

---
*Analysed by Claude on 2026-05-24*
