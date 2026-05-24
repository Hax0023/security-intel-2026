# Subdomain Takeover via Webflow Proxy - sales.mixmax.com

## Metadata
- **Source:** HackerOne
- **Report:** 233402 | https://hackerone.com/reports/233402
- **Submitted:** 2017-05-30
- **Reporter:** z3t
- **Program:** Mixmax
- **Bounty:** Not specified
- **Severity:** medium
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Third-party Service Abuse
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain sales.mixmax.com resolves to a Webflow.io proxy server (151.101.16.229) that returns a 404 error, indicating the subdomain is unclaimed on Webflow and potentially available for takeover. An attacker could claim this subdomain on Webflow and serve arbitrary content under the Mixmax domain, leading to phishing, credential harvesting, or brand impersonation.

## Attack scenario
1. Attacker identifies that sales.mixmax.com resolves to Webflow's CDN IP (151.101.16.229) and returns 404
2. Attacker registers or claims a project on Webflow.io and configures a custom domain
3. Attacker points their Webflow project to sales.mixmax.com through Webflow's domain settings
4. Attacker creates a phishing page mimicking Mixmax's sales interface or login portal
5. Victims visit sales.mixmax.com believing it's legitimate Mixmax infrastructure and enter credentials
6. Attacker harvests credentials or delivers malware to compromise user accounts

## Root cause
Mixmax configured DNS to point sales.mixmax.com to Webflow's proxy server but never completed the Webflow project setup or claimed the subdomain. The subdomain remains dangling with no active service claiming it on the Webflow side, creating an unclaimed resource vulnerable to hijacking.

## Attacker mindset
An attacker would recognize the opportunity to claim a high-value subdomain under a legitimate company domain. The Webflow platform likely allows anyone to configure custom domains, making the takeover trivial once the unclaimed state is identified. The attacker would prioritize this target for phishing because sales.mixmax.com has inherent credibility.

## Defensive takeaways
- Audit all DNS records for dangling subdomains pointing to third-party services (CDNs, hosting platforms, email providers)
- Implement a subdomain inventory management process tracking which subdomains map to which services
- For each third-party service, verify that the subdomain is actively claimed/verified on that service
- Remove or update DNS records for subdomains no longer in use
- Monitor DNS configurations for changes and alert on new subdomain additions
- Consider using CNAME records that require explicit verification on the third-party service
- Regularly test subdomains for 404 responses or orphaned configurations

## Variant hunting
Check other Mixmax subdomains (api.*, support.*, mail.*, etc.) for similar dangling DNS records
Look for subdomains pointing to other CDNs or hosting services (AWS CloudFront, GitHub Pages, Heroku, etc.)
Search DNS historical records to identify when sales.mixmax.com was configured and if it was ever claimed on Webflow
Test for subdomain takeover on competitor domains in the productivity/sales software space
Identify other companies using Webflow and check for similar dangling subdomains across their domain portfolios

## MITRE ATT&CK
- T1190 - Exploit Public-Facing Application
- T1583.001 - Acquire Infrastructure: Domains
- T1583.006 - Acquire Infrastructure: Web Services
- T1598.003 - Phishing for Information: Spearphishing Link
- T1566.002 - Phishing: Phishing - Spearphishing Link

## Notes
The reporter acknowledges uncertainty about the DNS configuration and whether a takeover is definitively possible, indicating a lower confidence finding. However, the 404 response from a third-party CDN strongly suggests the subdomain is unclaimed and available for takeover. The researcher appropriately escalated despite incomplete certainty, which is appropriate for security findings. Mixmax should verify all third-party service integrations and remove or claim unused subdomains.

## Full report
<details><summary>Expand</summary>

None of the weakness categories really fit this so I apologize for that.

The subdomain `sales.mixmax.com` points to `151.101.16.229`, a `webflow.io` proxy server. Because it 404s, this leads me to believe that a subdomain takeover is possible through the webflow service as whatever this is pointing to is unused. 

Due to odd DNS configurations I'm not 100% sure on this but thought I'd make you aware just in case.

</details>

---
*Analysed by Claude on 2026-05-24*
