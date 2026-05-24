# Subdomain Takeover via Expired Hubspot Service - blog.greenhouse.io

## Metadata
- **Source:** HackerOne
- **Report:** 38007 | https://hackerone.com/reports/38007
- **Submitted:** 2014-12-01
- **Reporter:** fransrosen
- **Program:** Greenhouse
- **Bounty:** Not specified
- **Severity:** critical
- **Vuln:** subdomain_takeover, dns_misconfiguration, dangling_dns_pointer
- **CVEs:** None
- **Category:** web-api

## Summary
The subdomain blog.greenhouse.io pointed to an expired/cancelled Hubspot account via CNAME records, allowing attackers to claim the subdomain and serve malicious content. This enabled phishing attacks and arbitrary JavaScript execution on a trusted company domain without any verification needed.

## Attack scenario
1. Attacker discovers blog.greenhouse.io CNAME record points to san.secure001.hubspot.com.edgekey.net
2. Attacker verifies the Hubspot account associated with this CNAME has been cancelled or expired
3. Attacker creates a new Hubspot account or claims the abandoned service endpoint
4. Attacker gains ability to serve content at blog.greenhouse.io including malicious login forms or XSS payloads
5. Attacker executes JavaScript in the context of greenhouse.io domain, bypassing SOP and phishing protections
6. Users are phished or compromised without suspecting the trusted Greenhouse domain

## Root cause
Greenhouse failed to remove or update DNS CNAME records after discontinuing their Hubspot service, leaving a dangling pointer to an unclaimed external service. No ownership validation was performed by the third-party service provider before allowing takeover.

## Attacker mindset
Opportunistic reconnaissance of DNS records for external service integrations followed by verification of service abandonment. Low-effort exploitation requiring only DNS enumeration tools and ability to provision a new account on the target service.

## Defensive takeaways
- Maintain comprehensive inventory of all DNS records including CNAME/alias entries pointing to external services
- Regularly audit DNS records and retire entries when services are discontinued or migrated
- Implement monitoring/alerting for DNS changes and unused subdomain/service pointer detection
- Use DNS providers that support CNAME flattening or ALIAS records to reduce takeover surface
- Require subdomain validation or HTTP/TLS certificate pinning for critical services
- Implement Content Security Policy and X-Frame-Options headers to limit phishing effectiveness
- Establish offboarding checklists that include DNS cleanup when third-party services are cancelled
- Periodically scan for dangling DNS pointers using tools that verify service endpoint accessibility

## Variant hunting
Search DNS records for CNAME/MX/TXT records pointing to: Heroku, GitHub Pages, AWS S3, Firebase, Zendesk, Shopify, Fastly, Akamai, and other commonly abandoned SaaS endpoints. Verify each endpoint for takeover potential by attempting service signup.

## MITRE ATT&CK
- T1190
- T1598
- T1593
- T1583.001

## Notes
Early subdomain takeover report (2015) that became foundational in the bug bounty community. Reporter properly disclosed via HackerOne and included PoC. This vulnerability type directly enabled phishing due to domain reputation inheritance. The attached Detectify advisory became industry standard reference for this class of vulnerability.

## Full report
<details><summary>Expand</summary>

Hi,

Your subdomain blog.greenhouse.io is pointing to the service called Hubspot. However, your account at Hubspot has expired or has been cancelled. This basically means that anyone can claim your subdomain pointing to Hubspot and create their own site at this URL. This is EXTREMELY dangerous as whatever the attacker want can be placed on this domain. This is also a foolproof phishing attack since no one would be able to verify that this is not a legit greenhouse.io-login form.

I have temporarily claimed this domain for PoC. You should immediately remove the DNS-entry for blog.greenhouse.io pointing to Hubspot.

And since I'm able to run javascript at Hubspot, I'm able to do whatever I like on that domain. Creating a login form that would fool anyone, since it's present on a greenhouse.io domain.

```
$ host blog.greenhouse.io
blog.greenhouse.io is an alias for san.secure001.hubspot.com.edgekey.net.
san.secure001.hubspot.com.edgekey.net is an alias for e1395.b.akamaiedge.net.
```

PoC-link: 
http://blog.greenhouse.io/

PoC-images attached.

As you might understand, this is really bad. Foolproof phishing. XSS on greenhouse.io. Potential malware spread through a domain you - in this case - do not control. Extremely painful for the company brand.

Please make sure you're always going through your DNS-entries so no subdomains are pointing to external services you do not use.

We've written an advisory about this at Detectify: 
http://blog.detectify.com/post/100600514143/hostile-subdomain-takeover-using-heroku-github-desk

Where you can read more about this sort of attack.

Regards,
Frans Rosén

</details>

---
*Analysed by Claude on 2026-05-24*
