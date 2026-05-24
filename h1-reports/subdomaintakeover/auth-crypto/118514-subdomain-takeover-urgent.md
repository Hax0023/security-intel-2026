# Subdomain Takeover via Expired Freshdesk Service

## Metadata
- **Source:** HackerOne
- **Report:** 118514 | https://hackerone.com/reports/118514
- **Submitted:** 2016-02-24
- **Reporter:** paresh_parmar
- **Program:** Kiwi.ki
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
A subdomain (service.kiwi.ki) was configured to point to an expired Freshdesk service instance, allowing an attacker to claim and control the subdomain. This dangling DNS record creates a direct path for subdomain takeover and potential credential theft or phishing attacks.

## Attack scenario
1. Attacker discovers that service.kiwi.ki resolves to a Freshdesk CNAME record
2. Attacker checks Freshdesk account availability and finds the service instance has been deleted/expired
3. Attacker registers or claims a new Freshdesk account using the expired subdomain reference
4. Attacker gains control of service.kiwi.ki through the Freshdesk platform
5. Attacker hosts malicious content, phishing pages, or credential harvesting forms on the claimed subdomain
6. Users visiting service.kiwi.ki trust the domain and interact with attacker-controlled content

## Root cause
The organization failed to remove or update DNS CNAME records pointing to Freshdesk after deprovisioning the service instance. No monitoring or validation mechanism existed to detect dangling DNS records.

## Attacker mindset
An opportunistic attacker scanning for common subdomain patterns (service, support, help, etc.) identifies expired third-party service integrations and exploits the trust users place in the parent domain.

## Defensive takeaways
- Maintain a comprehensive inventory of all DNS records and third-party service integrations
- Implement automated monitoring to detect dangling DNS records and CNAME chains to non-existent services
- Establish a decommissioning checklist that includes DNS cleanup for all services
- Regularly audit DNS records against active services using DNS enumeration tools
- Use DNSSEC and CAA records to prevent unauthorized certificate issuance
- Implement certificate transparency monitoring for all subdomains
- Consider CNAME flattening or removing unused subdomains entirely

## Variant hunting
Scan for other dangling CNAME records pointing to common platforms (Heroku, GitHub Pages, S3, Zendesk, etc.)
Check wildcard DNS entries that might reference expired services
Identify subdomains pointing to acquired/shutdown services that haven't been migrated
Look for CNAME records in TXT records or SRV records that might be forgotten
Test for subdomain takeover on any CDN, hosting, or SaaS integrations

## MITRE ATT&CK
- T1583.001
- T1583.002
- T1589.001
- T1598.003
- T1566.002

## Notes
This is a straightforward subdomain takeover case. The report lacks technical depth and actionable details (specific CNAME target, response codes, proof of control), but the vulnerability is clear and critical. The urgency indicated in the title appropriately reflects the severity - active exploitation is trivial once DNS misconfiguration is known. This is a common issue in organizations with poor infrastructure hygiene and lack of DNS auditing practices.

## Full report
<details><summary>Expand</summary>

hi,

one of your subdomain is pointing to FRESHDESK but servicce is expire there,
so i can claim this http://service.kiwi.ki/  subdomain.

Fix: remove dns entry of  this subdomain asap




Thanks

</details>

---
*Analysed by Claude on 2026-05-24*
