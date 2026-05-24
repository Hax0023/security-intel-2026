# Subdomain Takeover via Abandoned Fastly Configuration on registry.nodejs.org

## Metadata
- **Source:** HackerOne
- **Report:** 340580 | https://hackerone.com/reports/340580
- **Submitted:** 2018-04-19
- **Reporter:** dade
- **Program:** Node.js/npm
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Improper CDN Configuration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
An abandoned CNAME record pointing registry.nodejs.org to registry.npmjs.org was not properly registered with Fastly, allowing an attacker to register the subdomain on Fastly and intercept traffic. This could enable delivery of malicious npm packages to users misconfiguring their registry settings. The researcher received 300+ requests for npm packages during testing.

## Attack scenario
1. Attacker discovers registry.nodejs.org CNAME pointing to registry.npmjs.org via DNS enumeration
2. Attacker verifies the subdomain is not registered in the target Fastly service
3. Attacker registers registry.nodejs.org as a new domain in their own Fastly account without needing proof of DNS ownership
4. Attacker configures malicious backend or intercepts requests to serve backdoored npm packages
5. Users with misconfigured npm settings pointing to registry.nodejs.org receive attacker-controlled packages
6. Attacker could distribute supply chain compromises at scale via npm ecosystem

## Root cause
Stale CNAME DNS record pointing to a CDN service where the domain was never registered, combined with Fastly's lack of DNS ownership verification allowing any account to claim arbitrary domains. DNS records were not cleaned up when the subdomain fell out of use.

## Attacker mindset
Opportunistic supply chain attacker seeking high-impact attack surface. The npm registry is an attractive target because misconfigured clients automatically pull from alternate registries. The researcher responsibly disclosed after confirming the takeover was possible and received live requests, demonstrating real-world exploitability.

## Defensive takeaways
- Regularly audit all CNAME records and verify they point to actively managed services
- Delete or repurpose abandoned DNS records to prevent dangling pointer attacks
- For critical subdomains, implement CDN-level domain verification or use CAA records
- Coordinate with CDN providers to add additional ownership verification before domain activation
- Monitor DNS for unauthorized changes and implement alerting on subdomain creation
- Use HSTS headers and certificate pinning to defend against MITM attacks from subdomain takeovers
- Implement response header validation and signature verification in package managers

## Variant hunting
Hunt for other nodejs.org subdomains with similar CNAME misconfigurations. Search npm ecosystem for other package registries with dangling DNS records. Check npm-ecosystem mirrors and caching layers for similar Fastly takeover possibilities. Enumerate all first-party subdomains pointing to third-party CDNs without verification.

## MITRE ATT&CK
- T1190 Exploit Public-Facing Application
- T1584 Compromise Infrastructure
- T1589 Gather Victim Identity Information
- T1566 Phishing
- T1195 Supply Chain Compromise
- T1200 Traffic Redirection

## Notes
This is a classic subdomain takeover exploiting the gap between DNS configuration and CDN service registration. The npm registry context makes this especially dangerous as it could compromise thousands of developers. The researcher's responsible disclosure included offering to coordinate remediation, showing good faith. Fastly's lack of DNS CNAME validation is a systemic issue affecting all their customers with similar misconfigurations.

## Full report
<details><summary>Expand</summary>

I recently found an abandoned and/or overlooked nodejs.org subdomain that was indirectly pointing to Fastly. Fastly doesn't require any proof of DNS ownership to register new distributions that use a given domain, so I was able to effectively take it over.

Vulnerability: Subdomain Takeover via Fastly
Host: http://registry.nodejs.org

Solution:
There are two possible solutions to remediate this issue:

1.) If you no longer wish to use registry.nodejs.org, you can simply delete the registry.nodejs.org CNAME record that is currently pointing to registry.npmjs.org.

2.) Alternatively, if you would like to continue using and/or supporting registry.nodejs.org, you can coordinate with me, I will delete my Fastly service so that someone from nodejs.org can add the registry.nodejs.org domain to the "Domains" field in the related Fastly service.  This should be done in a timely and coordinated fashion to prevent another researcher (or less savory type) from registering it before you are able to.

## Impact

Since discovering this vulnerability I have received more than 300 requests for various npm packages. A malicious attacker could have used this access to begin delivering backdoored (or otherwise malicious) packages to users who were not using the correct registry setting of registry.npmjs.org.

</details>

---
*Analysed by Claude on 2026-05-24*
