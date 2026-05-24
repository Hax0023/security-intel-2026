# Subdomain Takeover on usclsapipma.cv.ford.com via Unclaimed Azure CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 484420 | https://hackerone.com/reports/484420
- **Submitted:** 2019-01-23
- **Reporter:** march
- **Program:** Ford Motor Company
- **Bounty:** Not specified in report
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME, Cloud Resource Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain usclsapipma.cv.ford.com contains a CNAME pointing to an unclaimed Azure cloudapp virtual machine (feuscspma3fcvapi.eastus.cloudapp.azure.com) that is no longer registered. An attacker can claim this Azure resource and gain full control over the subdomain, enabling traffic interception, malware distribution, phishing, and authentication bypass attacks.

## Attack scenario
1. Attacker discovers through DNS enumeration that usclsapipma.cv.ford.com resolves to usclsapipma.trafficmanager.net, which points to feuscspma3fcvapi.eastus.cloudapp.azure.com
2. Attacker verifies the Azure FQDN is unclaimed by checking availability through Azure Portal API, confirming 'available: true' status
3. Attacker registers a new Azure VM in the eastus region with the same FQDN (feuscspma3fcvapi.eastus.cloudapp.azure.com)
4. Attacker configures the compromised Azure VM with malicious content (phishing pages, malware payload, rogue mail server)
5. Traffic targeting the Ford subdomain now resolves to attacker-controlled infrastructure, enabling credential theft, malware distribution, and email spoofing
6. Attacker exploits trust relationship to bypass authentication, distribute malware, or conduct targeted phishing against Ford employees and customers

## Root cause
Stale CNAME record pointing to decommissioned Azure cloud resource without proper cleanup. DNS zone contains reference to non-existent Azure VM that was never claimed/registered after creation attempt or was deleted without removing corresponding DNS records.

## Attacker mindset
Opportunistic subdomain enumeration targeting cloud-hosted subdomains. Attacker systematically identifies unclaimed cloud resources by checking DNS chains and leveraging cloud provider APIs to verify availability. Low effort, high-impact attack requiring only cloud account and technical knowledge of Azure services.

## Defensive takeaways
- Implement DNS audit process to identify and remove stale/dangling CNAME records pointing to cloud services
- Enforce lifecycle management: delete DNS records immediately when associated cloud resources are decommissioned
- Use CNAME record validation tools to detect dangling pointers to Azure, AWS, GitHub Pages, Heroku, etc.
- Monitor Azure portal for unclaimed FQDNs in organization's domain ranges
- Implement DNS security scanning as part of regular infrastructure audits
- Require change management approval before modifying DNS records pointing to cloud infrastructure
- Use subdomain takeover detection services to continuously monitor for vulnerable subdomains
- Implement CAA and DNSSEC records to add additional security layers

## Variant hunting
Scan all Ford subdomains for CNAME records pointing to AWS CloudFront, S3, ELB endpoints that may be unclaimed
Check for dangling GitHub Pages references (*.github.io) in Ford DNS zones
Identify subdomains pointing to Heroku, Shopify, WordPress.com, or other PaaS providers without active claims
Search for Azure Traffic Manager references with broken downstream resources
Test for similar misconfigured subdomains in parent domains and related properties
Monitor for new Azure VM registrations that could match Ford's IP space or domain patterns

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1071 - Application Layer Protocol
- T1583.001 - Acquire Infrastructure: Domains
- T1584.001 - Compromise Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598 - Phishing for Information
- T1566 - Phishing

## Notes
This is a classic example of infrastructure hygiene failure in cloud environments. The dangling CNAME represents a gap between DNS management and cloud resource lifecycle management. High impact due to ability to intercept all traffic for the subdomain including mail traffic. Report includes solid proof-of-concept evidence (Azure availability check and DNS dig results). No indication of actual exploitation, purely vulnerability disclosure.

## Full report
<details><summary>Expand</summary>

Hello Ford H1 team,

I want to report a Subdomain takeover vulnerability in this report, a pretty serious security issue in some context.

##Overview:
One of the ford.com subdomains is pointing to Azure, which has unclaimed CNAME record. ANYONE is able to own ford.com subdomain at the moment.

This vulnerability is called subdomain takeover. You can read more about it here:

https://blog.sweepatic.com/subdomain-takeover-principles/
https://labs.detectify.com/tag/hostile-subdomain-takeover/
https://hackerone.com/reports/325336

##Details:
usclsapipma.cv.ford.com has CNAME usclsapipma.trafficmanager.net wich has a CNAME to feuscspma3fcvapi.eastus.cloudapp.azure.com. However, feuscspma3fcvapi.eastus.cloudapp.azure.com is not registered in Azure cloudapp Virtual machine anymore and thus can be registered as FQDN for a easus VM by anyone. After registering the Cloud App Virtual Machine in Azure portal, the person doing so has full control over traffic on dynatraceppeast01.cf.ford.com (so, not only HTTP/HTTPS but also mails traffic, etc, since we have full control over the virtual machine and it's OS).

##Mitigation:
Remove the CNAME record from ford.com DNS zone completely.
OR
Claim it back in Azure portal

##Files : 
Azure-check-availability.png -> Screenshot of the Azure website api "check availability" for the "eastus" cloudapp virtual machine. on the link, you can see the location "eastus" part of the fqdn ad the DomainNameLabel "feuscspma3fcvapi" part of the FQDN, and the "available : true" response for this fqdn.
dns-proof.png -> Result of a "dig" command for this domains, showing the "NXDOMAIN" reponse for the CNAME entry of the ford subdomain.

Cheers,

March_42

## Impact

Subdomain takeover can be abused to do several things like :

Malware distribution
Phishing / Spear phishing
XSS
Authentication bypass
Legitimate mail sending and receiving on behalf of ford subdomain
...
List goes on and on.

</details>

---
*Analysed by Claude on 2026-05-24*
