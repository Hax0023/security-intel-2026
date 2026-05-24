# Subdomain Takeover via Unclaimed Nameserver Records at us-east4.37signals.com

## Metadata
- **Source:** HackerOne
- **Report:** 1342422 | https://hackerone.com/reports/1342422
- **Submitted:** 2021-09-17
- **Reporter:** nagli
- **Program:** 37signals (Basecamp)
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Nameserver Hijacking
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain us-east4.37signals.com was configured with nameserver records pointing to an unclaimed DNS zone that the researcher was able to register and claim. This allowed the attacker to host arbitrary content on the organization's subdomain, enabling multiple attack vectors including cookie theft, XSS, and phishing.

## Attack scenario
1. Attacker identifies us-east4.37signals.com through subdomain enumeration or scanning
2. Attacker discovers the subdomain's NS records point to an unclaimed/unregistered nameserver zone
3. Attacker registers or claims the orphaned nameserver zone in their own account
4. Attacker creates DNS A records for the target subdomain pointing to their malicious server
5. Attacker hosts phishing pages, malware, or XSS payloads on the compromised subdomain
6. Victims access the malicious content which executes with the legitimate 37signals domain, stealing credentials or session cookies

## Root cause
37signals configured subdomain delegations to nameserver records that were not properly registered, maintained, or transferred. The organization failed to either: (1) ensure nameservers remained under their control, (2) clean up unused subdomain DNS records, or (3) monitor for orphaned nameserver delegations.

## Attacker mindset
The attacker recognized that subdomain delegations to external nameservers represent a common misconfiguration weakness. By identifying an unclaimed nameserver zone, the attacker realized they could claim it and inject arbitrary DNS records, effectively hijacking the subdomain. This demonstrates opportunistic reconnaissance followed by exploitation of poor DNS hygiene.

## Defensive takeaways
- Maintain an inventory of all subdomains and their DNS configurations, including nameserver delegations
- Only delegate subdomains to nameservers fully controlled and managed by your organization
- Regularly audit DNS records to identify and remove orphaned or obsolete subdomain delegations
- Implement continuous subdomain monitoring and enumeration to detect unauthorized or misconfigured entries
- Use DNS CAA records to restrict certificate issuance on your domains
- Implement DNSSEC to prevent DNS spoofing and unauthorized zone modifications
- Establish a process for decommissioning subdomains, including removal of all associated DNS records

## Variant hunting
Search for other 37signals subdomains (*.37signals.com, *.basecamp.com, *.hey.com) with NS record delegations. Identify subdomains across the organization that may be delegated to third-party nameservers, particularly those no longer in active use. Check for patterns of incomplete subdomain cleanups during infrastructure migrations or service retirements.

## MITRE ATT&CK
- T1190
- T1583.001
- T1587.001
- T1589.001

## Notes
The report content was redacted by HackerOne (indicated by ████ symbols), suggesting sensitive details about the specific nameserver provider or domain were obscured. The POC link demonstrates proof of control over the subdomain. This is a classic subdomain takeover resulting from DNS delegation mismanagement rather than a web application vulnerability. The impact spans multiple attack scenarios (credential theft, XSS, phishing) making it a critical security issue despite being rooted in infrastructure configuration.

## Full report
<details><summary>Expand</summary>

## Description
 
 Hi!
 I have discovered that  us-east4.37signals.com was pointing to an unclaimed ████ NS zone and I've managed to claim it in my account.
 
 ##POC
 
 http://nagli.us-east4.37signals.com/takeover.html
 

{F1451587}


 ## Remediation
 Make sure to configure the DNS records under us-east4.37signals.com
 
Best regards,
@ nagli

## Impact

Subdomain takeovers can be used for
 Account takeovers (cookies set to .█████████ will be shared with this subdomain and can be obtained)
 Stored XSS (arbitrary javascript code can be executed in a users browser)
 Phishing
 Hosting malicious content

Since you cannot control the content hosted on the site, your brand is at risk of being damaged.
Additionally, the vulnerabilities in these sites, such as XSS, RCE, etc could put your sites/users at risk of attack, since they would occur on your domain.

</details>

---
*Analysed by Claude on 2026-05-24*
