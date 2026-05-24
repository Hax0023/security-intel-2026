# Subdomain Takeover on status.vimeo.com via Unclaimed StatusPage.io Domain

## Metadata
- **Source:** HackerOne
- **Report:** 49663 | https://hackerone.com/reports/49663
- **Submitted:** 2015-02-28
- **Reporter:** avlidienbrunn
- **Program:** Vimeo
- **Bounty:** Unknown (report from 2015, historical)
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** web-api

## Summary
Vimeo's subdomain status.vimeo.com was configured to point to hosted.statuspage.io via CNAME record, but no StatusPage.io service was actually provisioned or claimed. An attacker could register a StatusPage.io account and claim the status.vimeo.com subdomain, gaining full control over the domain and the ability to serve arbitrary content from a trusted Vimeo domain. This enabled cookie theft, phishing, same-origin policy abuse, and credential harvesting attacks.

## Attack scenario
1. Attacker discovers status.vimeo.com resolves to hosted.statuspage.io via DNS CNAME record
2. Attacker verifies the subdomain is unclaimed by attempting to access it and observing a default StatusPage.io placeholder or error page
3. Attacker registers a StatusPage.io account and creates a new status page, specifying 'status.vimeo.com' as the custom domain name
4. StatusPage.io accepts the domain claim, and attacker gains full control over status.vimeo.com content
5. Attacker creates phishing login form or malicious JavaScript on the claimed subdomain, leveraging the trusted vimeo.com domain origin
6. Attacker harvests Vimeo user credentials, manipulates cookies via same-origin access, or performs cross-site request forgery attacks against authenticated users

## Root cause
DNS CNAME record for status.vimeo.com pointed to statuspage.io infrastructure, but the corresponding StatusPage.io service was never provisioned, configured, or actively maintained. No process existed to audit and validate that external service integrations remained claimed and in-use. Dangling DNS records were left orphaned after service discontinuation or misconfiguration.

## Attacker mindset
Identify forgotten or misconfigured external service integrations by scanning for CNAME/A records pointing to third-party SaaS platforms. Check whether the target domain is actually claimed/configured on the external service. If unclaimed, register an account on that service and claim the subdomain to gain arbitrary code execution in the target organization's domain context.

## Defensive takeaways
- Maintain a comprehensive inventory of all DNS records and external service integrations
- Implement regular DNS audits to identify and remove dangling or orphaned records
- Establish a change management process requiring removal of DNS records when external services are decommissioned
- For third-party SaaS services, verify domain ownership and ensure services are actively provisioned before publishing DNS records
- Use DNS monitoring tools to alert on changes to critical subdomain configurations
- Implement DNSSEC to prevent DNS hijacking attacks
- Document the business purpose and ownership of each subdomain delegation
- Periodically verify that external service integrations are still in-use and properly claimed

## Variant hunting
Search for other dangling CNAME/NS records pointing to: Heroku, GitHub Pages, Azure Blob Storage, AWS S3, Firebase Hosting, Desk.com, Zendesk, Shopify, Fastly, Acquia, or other common SaaS platforms. Check subdomains like www, mail, api, dev, staging, cdn, assets, blog, shop, help, support, status, etc. Use DNS enumeration tools (dnsenum, fierce, sublist3r) combined with service-specific domain registration checks.

## MITRE ATT&CK
- T1583.001 - Acquire Infrastructure: Domains
- T1589.001 - Gather Victim Identity Information: Credentials
- T1598.003 - Phishing for Information: Spearphishing Link
- T1187 - Forced Authentication
- T1056.004 - Observation: Session Recording

## Notes
This report exemplifies the subdomain takeover vulnerability class that emerged prominently in 2015. The researcher (Mathias Karlsson) later founded Detectify, a security scanning platform. StatusPage.io and similar hosted services are particularly susceptible to this attack because they enable custom domain configuration without strong pre-verification of domain ownership. The criticality stems from the compromised subdomain inheriting the parent domain's trust relationship with users and browsers (same-origin policy, cookies, CSP whitelisting, etc.).

## Full report
<details><summary>Expand</summary>

Hi,

**Brief**
This is an urgent issue and I hope you will act on it likewise.
Your subdomain status.vimeo.com is pointing to hosted.statuspage.io, but no statuspage was connected to it. This means that anyone can claim the subdomain by setting up a statuspage.io site and using "status.vimeo.com" as the name!

*You should immediately remove the DNS-entry for statu.vimeo.com pointing to statuspage.io.*

Since I have complete control over the subdomain I can do whatever I want on it. Creating a login form that would fool anyone, since it's present on a vimeo.com domain, abuse same origin bugs, get/set vimeo cookies, you name it!

**PoC**
PoC-link:
http://status.vimeo.com

**Remediation**
Please make sure you're always going through your DNS-entries so no subdomains are pointing to external services you do not use.

We've written an advisory about this at Detectify:
http://blog.detectify.com/post/100600514143/hostile-subdomain-takeover-using-heroku-github-desk

Where you can read more about this sort of attack.

Best,
Mathias

</details>

---
*Analysed by Claude on 2026-05-24*
