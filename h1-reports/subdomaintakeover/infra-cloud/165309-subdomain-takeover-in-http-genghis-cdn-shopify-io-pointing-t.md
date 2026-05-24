# Subdomain Takeover in genghis-cdn.shopify.io pointing to Fastly

## Metadata
- **Source:** HackerOne
- **Report:** 165309 | https://hackerone.com/reports/165309
- **Submitted:** 2016-09-02
- **Reporter:** peroni
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, Dangling DNS Record, Service Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A Shopify CDN subdomain (genghis-cdn.shopify.io) had its DNS record pointing to Fastly but was not registered to any active Fastly service, allowing potential takeover. An attacker could claim the domain in Fastly and serve malicious content under Shopify's trusted domain.

## Attack scenario
1. Attacker discovers that genghis-cdn.shopify.io resolves to Fastly's nameservers (shopify-e.map.fastly.net) but returns 'unknown domain' error
2. Attacker recognizes this as a dangling DNS record where the domain points to a third-party service (Fastly) that no longer has it registered
3. Attacker creates a Fastly account and registers the genghis-cdn.shopify.io domain to their own Fastly service
4. Attacker configures their Fastly service to serve arbitrary content (phishing, malware, sensitive data) under the trusted Shopify domain
5. Victims access the subdomain believing it's legitimate Shopify infrastructure, trusting the domain and SSL certificate
6. Attacker exfiltrates credentials, injects malicious content, or performs phishing attacks leveraging Shopify's brand reputation

## Root cause
Shopify deprovisioned the Fastly service for genghis-cdn.shopify.io but failed to remove or update the corresponding DNS record pointing to Fastly's nameservers, creating a dangling DNS pointer.

## Attacker mindset
Reconnaissance-focused attacker identifying abandoned infrastructure. Once discovered, the takeover is trivial - simply registering the domain in Fastly's service console. The attack leverages trust in Shopify's domain and subdomain to deliver malicious content at scale. High-value target due to Shopify's brand recognition and potential customer traffic.

## Defensive takeaways
- Maintain an inventory of all subdomains and external services (CDN, DNS providers, etc.) they're delegated to
- Implement automated DNS monitoring to detect dangling records pointing to third-party services
- Establish a deprovisioning checklist requiring DNS record removal before service cancellation
- Use CNAME validation and service-specific monitoring to detect when external services no longer control subdomains
- Implement subdomain enumeration and validation in CI/CD pipelines to catch misconfigurations
- Monitor Fastly service registrations for your domain names
- Set up alerts for DNS changes affecting critical subdomains

## Variant hunting
Search for other Shopify subdomains pointing to Fastly/other CDNs that may be unclaimed
Check for similar patterns in other Shopify properties (*.shopify.com, *.shopifycdn.com, etc.)
Hunt for abandoned AWS CloudFront distributions, Azure CDN, or Cloudflare services with dangling DNS
Look for subdomains pointing to GitHub Pages, Heroku, or other common PaaS services without active registrations
Enumerate all *.shopify.io subdomains and check which ones return service-not-found errors
Cross-reference Shopify IP ranges against DNS records to find inconsistencies

## MITRE ATT&CK
- T1190
- T1583.001
- T1566.002
- T1589.001

## Notes
This is a classic subdomain takeover vulnerability resulting from inadequate infrastructure cleanup. The reporter demonstrates good methodology by using DNS queries to identify the Fastly delegation and the service-not-found error confirming non-registration. Similar to HackerOne report #32825 (likely another Shopify subdomain takeover). The attack surface is large for any organization using multiple CDN/external services with subdomains.

## Full report
<details><summary>Expand</summary>

Hi,

I've found a Shopifu cdn domain here which had an instance of fastly setup but did not remove the dns record when the service was cancelled. a subdomain takeover similar to that of https://hackerone.com/reports/32825 could be possible.

Vulnerable URL: http://genghis-cdn.shopify.io

Page Response: 
```
Fastly error: unknown domain: genghis-cdn.shopify.io. Please check that this domain has been added to a service.
```

Which indicate that this domain is point to fastly but there is no app in fastly with that name allowing anyone to claim it.
The subdomain "http://genghis-cdn.shopify.io/" is currently pointing to Fastly (shopify-e.map.fastly.net), but is not registered to a service. 

```
$ host genghis-cdn.shopify.io
genghis-cdn.shopify.io is an alias for shopify-e.map.fastly.net.
shopify-e.map.fastly.net is an alias for prod.shopify-e.map.fastlylb.net.
prod.shopify-e.map.fastlylb.net has address 151.101.60.108
```


Thanks!

</details>

---
*Analysed by Claude on 2026-05-24*
