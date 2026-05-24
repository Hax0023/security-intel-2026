# Subdomain Takeover at course.oberlo.com via Kajabi

## Metadata
- **Source:** HackerOne
- **Report:** 1690951 | https://hackerone.com/reports/1690951
- **Submitted:** 2022-09-04
- **Reporter:** m7mdharoun
- **Program:** Oberlo
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Records, Service Misconfiguration
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain course.oberlo.com was vulnerable to takeover through the Kajabi service due to dangling DNS records pointing to an abandoned or unverified Kajabi account. An attacker could register or claim the associated Kajabi resource, gaining control of the subdomain and enabling malicious activities.

## Attack scenario
1. Attacker identifies that course.oberlo.com resolves via DNS to a Kajabi service endpoint
2. Attacker discovers the Kajabi account associated with the DNS record is unclaimed or abandoned
3. Attacker creates a new Kajabi account or claims the existing unclaimed resource
4. Attacker gains control of the subdomain and serves arbitrary content at course.oberlo.com
5. Attacker demonstrates proof-of-concept by hosting content visible via web archive snapshot
6. Attacker can now execute phishing, malware distribution, XSS, or other attacks leveraging the trusted domain

## Root cause
Dangling DNS records pointing to an external Kajabi service endpoint that was either never properly configured, abandoned, or the underlying Kajabi account was deactivated without cleaning up corresponding DNS entries. The organization failed to maintain an inventory of DNS records and validate their targets.

## Attacker mindset
Reconnaissance-focused attacker scanning for forgotten or misconfigured subdomains. Likely part of systematic subdomain enumeration identifying low-hanging fruit in cloud service integrations. Motivated by credential to demonstrate vulnerability or prepare infrastructure for follow-up attacks.

## Defensive takeaways
- Maintain a comprehensive inventory of all DNS records and their associated services
- Regularly audit DNS records to identify and remove dangling entries
- Implement DNS monitoring and alerting for unauthorized changes
- Use CNAME validation and verification mechanisms before pointing domains to external services
- Establish offboarding procedures that include DNS cleanup when third-party services are deactivated
- Monitor subdomains for takeover risk using tools like can-i-take-over-xyz or SubOver
- Implement DNSSEC to prevent DNS hijacking
- Use DNS CAA records to restrict certificate issuance on subdomains

## Variant hunting
Scan other Oberlo subdomains for similar dangling DNS records pointing to Kajabi or other services
Check for subdomains pointing to other abandoned SaaS platforms (Heroku, Netlify, GitHub Pages, AWS S3, etc.)
Look for CNAME records pointing to services without active accounts
Investigate wildcard DNS records that may expose multiple subdomains
Check for SSL certificate transparency logs revealing additional subdomains with similar misconfigurations

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing: Spearphishing Link
- T1656 - Impersonation

## Notes
This is a classic subdomain takeover vulnerability requiring minimal technical skill but high impact. The PoC is documented via web archive, confirming the takeover occurred. The reporter provided clear reproduction steps and impact scenarios. Response should prioritize immediate DNS cleanup and comprehensive subdomain audit across the organization.

## Full report
<details><summary>Expand</summary>

Hi,
I was able to takeover your subdomain `course.oberlo.com` via using `kajabi` services.

## `Poc :`

visit https://course.oberlo.com/ you will see my poc 

https://web.archive.org/web/20220904143512/https://course.oberlo.com/



## `Suggested Fix :`

Clear your subdomain DNS.

## Impact

Subdomains Takeovers can be use in many things :
Malware
Phishing / Spear phishing
XSS
Authentication bypass
Open Redirects
True access
.. etc


****************************************
Kind Regards,
Mohamed Haron.

</details>

---
*Analysed by Claude on 2026-05-24*
