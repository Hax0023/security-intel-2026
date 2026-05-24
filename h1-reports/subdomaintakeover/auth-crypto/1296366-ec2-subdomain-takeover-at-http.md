# EC2 Subdomain Takeover via Dangling DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 1296366 | https://hackerone.com/reports/1296366
- **Submitted:** 2021-08-09
- **Reporter:** dreyand_
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A dangling DNS A record pointed to an EC2 instance that was no longer in use, allowing an attacker to claim the instance and host arbitrary content under the victim's subdomain. This enabled bypassing security controls like CORS policies and potential phishing/redirect attacks.

## Attack scenario
1. Attacker discovers a subdomain through DNS enumeration or public records
2. Attacker identifies the subdomain has a dangling DNS A record pointing to an unclaimed EC2 instance IP
3. Attacker launches a new EC2 instance and obtains the same IP address (or identifies an available IP)
4. Attacker configures the EC2 instance with malicious content or scripts
5. Attacker hosts proof-of-concept demonstrating content delivery under victim's subdomain
6. Attacker leverages subdomain authority to bypass CORS restrictions or conduct phishing/redirects

## Root cause
Organization failed to decommission DNS records when corresponding cloud resources (EC2 instances) were terminated, leaving dangling pointers to IP addresses that could be reclaimed by attackers.

## Attacker mindset
Low-effort opportunistic attack requiring basic DNS reconnaissance and cloud infrastructure knowledge. Attacker seeks to exploit abandoned infrastructure for content injection, credential harvesting, or security control bypass.

## Defensive takeaways
- Implement DNS record lifecycle management with mandatory cleanup of records when associated resources are decommissioned
- Use DNS monitoring/alerting to detect changes or orphaned records
- Implement cloud resource tagging and automated cleanup policies for termination events
- Maintain comprehensive inventory of all DNS records and associated infrastructure
- Use CNAME records instead of A records where possible to reduce takeover surface
- Implement CAA records to restrict certificate issuance on subdomains
- Regularly audit DNS zones for dangling records pointing to non-existent or unclaimed resources
- Enable MFA and access controls on cloud infrastructure to prevent unauthorized resource claims

## Variant hunting
Scan for other dangling DNS records (CNAME, MX, NS) pointing to cloud resources (AWS, Azure, GCP)
Check for dangling load balancer records or CDN endpoints
Search for subdomains with stale CNAME records pointing to GitHub Pages, Heroku, or other PaaS
Enumerate all subdomains and verify associated resources still exist
Check for dangling SSL certificates that may indicate stale infrastructure

## MITRE ATT&CK
- T1190
- T1583.001
- T1199
- T1657

## Notes
Report content heavily redacted with █ characters. Attack demonstrates critical gap between DNS management and cloud infrastructure lifecycle management. EC2 instances can be rapidly reclaimed by different AWS account owners if IP addresses are reassigned, making this a particularly dangerous misconfiguration in shared cloud environments.

## Full report
<details><summary>Expand</summary>

There is a dangling DNS A record that points to an EC2 instance that no longer exists, I was able to claim the EC2 instance and host content on http://███████/.

## Steps To Reproduce:

  1. Visit http://█████████/██████████.html and view the PoC:  ██████


## Suggested Remediation Steps

  Remove the A record pointing to the current ec2 instance. 

## Impact

Hosting content on http://█████/ and potentionally fully bypassing web protections like CORS (in cases of `████████`) or redirecting users to malicious pages.

## Impact

Hosting content on http://██████/ and potentionally fully bypassing web protections like CORS (in cases of `██████████`) or redirecting users to malicious pages,

## System Host(s)
██████

## Affected Product(s) and Version(s)


## CVE Numbers


## Steps to Reproduce
Visit http://██████████/█████.html and view the PoC:  █████

## Suggested Mitigation/Remediation Actions
Remove the A record pointing to the current ec2 instance.



</details>

---
*Analysed by Claude on 2026-05-24*
