# Subdomain Takeover via Dangling DNS CNAME Records

## Metadata
- **Source:** HackerOne
- **Report:** 180393 | https://hackerone.com/reports/180393
- **Submitted:** 2016-11-05
- **Reporter:** kholy
- **Program:** GitHub/Zomato
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME Records
- **CVEs:** None
- **Category:** web-api

## Summary
A subdomain (engineering.zomato.com) was configured with a CNAME record pointing to Tumblr's domain service (domains.tumblr.com), but the actual Tumblr service was no longer in use or claimed by the organization. An attacker could claim the orphaned Tumblr domain to gain control over the subdomain and serve malicious content.

## Attack scenario
1. Attacker discovers engineering.zomato.com resolves to domains.tumblr.com via DNS enumeration
2. Attacker verifies the Tumblr domain is unclaimed or no longer associated with the target organization
3. Attacker registers or claims the Tumblr domain through Tumblr's platform
4. Attacker gains DNS authority over domains.tumblr.com or configures hosting for the domain
5. Victims visiting engineering.zomato.com are served attacker-controlled content from the claimed Tumblr domain
6. Attacker can conduct phishing, malware distribution, or session hijacking campaigns using the trusted subdomain

## Root cause
Organization failed to clean up DNS records for subdomains pointing to external third-party services that were no longer actively used or maintained. The CNAME record remained in DNS while the corresponding external service either became orphaned or was made available for re-registration.

## Attacker mindset
Reconnaissance-focused attacker identifying infrastructure gaps. Looks for stale DNS configurations and unclaimed external services. Low effort, high impact attack requiring only DNS enumeration and claiming available third-party domains.

## Defensive takeaways
- Maintain comprehensive DNS audit logs and regularly scan for dangling CNAME records
- Implement automated monitoring to detect subdomains pointing to non-existent or unclaimed external services
- Establish DNS management policies requiring removal of records for discontinued third-party integrations
- Use CNAME flattening or ALIAS records where possible to reduce subdomain takeover surface
- Implement CAA (Certification Authority Authorization) records to restrict certificate issuance for subdomains
- Regularly verify that all subdomains resolve to services actually controlled by the organization
- Include DNS hygiene checks in security scanning and infrastructure reviews
- Consider using subdomain protection services that monitor for takeover attempts

## Variant hunting
Scan for CNAME records pointing to GitHub Pages, Heroku, AWS S3, or other common PaaS providers that may be unclaimed
Check for CNAME records pointing to Desk.com, Zendesk, or other customer support platforms no longer in use
Identify A/AAAA records pointing to IP addresses no longer owned by the organization
Search for MX, NS, or TXT records pointing to external services that may have been discontinued
Look for subdomains with CNAME records to CDN providers where the origin is no longer configured
Hunt for abandoned analytics, monitoring, or logging service DNS entries

## MITRE ATT&CK
- T1583.001
- T1566.002
- T1589.001
- T1583.005

## Notes
The report contains some formatting inconsistencies (mixing GitHub and Zomato examples) but the core vulnerability is clear. The reporter provided NSLookup proof-of-concept showing the CNAME resolution chain. This is a relatively simple but critical vulnerability that can lead to account compromise, data theft, or malware distribution. The Detectify advisory referenced provides additional context on hostile subdomain takeover techniques across multiple platforms.

## Full report
<details><summary>Expand</summary>

Hello,

Your Subdomain engineering.github.com/paragonie is Pointing to Tumblr.com

You should immediately remove the DNS-entry for engineering.zomato.com is Pointing to Tumblr.com.. Any One Can Claim That Domain , Please Read The Advisory Below.

Remediation
Please make sure you're always going through your DNS-entries so no subdomains are pointing to external services you do not use.

We've written an advisory about this at Detectify:
http://blog.detectify.com/post/100600514143/hostile-subdomain-takeover-using-heroku-github-desk

Where you can read more about this sort of attack.

I Have Done NSLookup For POC :-

nslookup github.com/paragonie
Server: 192.168.188.1
Address: 192.168.188.2#53

Non-authoritative answer:
engineering.zomato.com canonical name = domains.tumblr.com.
Name: domains.tumblr.com
Address: 66.6.42.22
Name: domains.tumblr.com
Address: 66.6.43.22




</details>

---
*Analysed by Claude on 2026-05-24*
