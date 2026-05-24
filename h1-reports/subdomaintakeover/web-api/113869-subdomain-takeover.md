# Subdomain Takeover via Dangling DNS CNAME to Tumblr

## Metadata
- **Source:** HackerOne
- **Report:** 113869 | https://hackerone.com/reports/113869
- **Submitted:** 2016-02-01
- **Reporter:** kiraak-boy
- **Program:** Zomato
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Records, DNS Misconfiguration
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain engineering.zomato.com contained a CNAME record pointing to domains.tumblr.com, which was not actively claimed by Zomato. An attacker could register or claim this Tumblr domain to hijack the subdomain and potentially impersonate Zomato services or perform phishing attacks. The DNS misconfiguration left the subdomain vulnerable to hostile takeover.

## Attack scenario
1. Attacker enumerates Zomato subdomains and identifies engineering.zomato.com
2. Attacker performs DNS lookup and discovers CNAME pointing to unclaimed domains.tumblr.com
3. Attacker creates a Tumblr account and claims the domains.tumblr.com domain
4. Attacker configures the claimed domain to serve malicious content (phishing page, malware, credential harvesting)
5. Legitimate users visiting engineering.zomato.com are redirected to attacker-controlled Tumblr domain
6. Attacker harvests credentials, distributes malware, or performs brand impersonation attacks

## Root cause
Zomato failed to maintain DNS hygiene by leaving a CNAME record pointing to an external service (Tumblr) that the organization no longer actively used or claimed. No periodic audit or cleanup of DNS records was performed to identify dangling or orphaned entries.

## Attacker mindset
Opportunistic reconnaissance-focused attacker scanning for low-hanging fruit in DNS configurations. These attackers leverage passive reconnaissance to identify abandoned external service registrations and exploit them for brand impersonation, phishing, or malware distribution campaigns.

## Defensive takeaways
- Maintain an inventory of all DNS records and external service integrations
- Implement periodic DNS audits to identify and remediate dangling CNAME records
- Establish a decommissioning process that includes DNS cleanup when services are retired
- Monitor for unclaimed external service accounts that your DNS records point to
- Use DNS security scanning tools to automatically detect subdomain takeover risks
- Implement DNSSEC and DNS monitoring to detect unauthorized changes
- Require approval workflows before creating CNAME records to external services
- Document the purpose and ownership of each DNS entry

## Variant hunting
Search for other Zomato subdomains with CNAME records pointing to external services (GitHub Pages, Heroku, AWS, etc.)
Check for other CNAME records pointing to Tumblr domains.tumblr.com across the organization
Identify subdomains with CNAME records to services that have been discontinued
Scan for MX records pointing to unclaimed mail service providers
Look for NS records delegating to external nameservers no longer in use
Check for A/AAAA records pointing to IP space of shutdown cloud services

## MITRE ATT&CK
- T1583.001
- T1598.003
- T1597.002
- T1589.001

## Notes
This is a classic subdomain takeover vulnerability that became widespread after 2014. The vulnerability is easily exploitable and has significant impact for phishing and brand impersonation. The reporter provided clear proof of concept with nslookup output. This type of vulnerability should be part of any standard bug bounty scope as it represents a common organizational oversight.

## Full report
<details><summary>Expand</summary>

Hello,

Your Subdomain engineering.zomato.com is Pointing to Tumblr.com


You should immediately remove the DNS-entry for engineering.zomato.com is Pointing to Tumblr.com.. Any One Can Claim That Domain , Please Read The Advisory Below.

Remediation
Please make sure you're always going through your DNS-entries so no subdomains are pointing to external services you do not use.

We've written an advisory about this at Detectify:
http://blog.detectify.com/post/100600514143/hostile-subdomain-takeover-using-heroku-github-desk

Where you can read more about this sort of attack.

I Have Done NSLookup For POC :-

nslookup engineering.zomato.com
Server:		192.168.188.2
Address:	192.168.188.2#53

Non-authoritative answer:
engineering.zomato.com	canonical name = domains.tumblr.com.
Name:	domains.tumblr.com
Address: 66.6.42.22
Name:	domains.tumblr.com
Address: 66.6.43.22


Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
