# Subdomain Takeover via Unclaimed DNS CNAME

## Metadata
- **Source:** HackerOne
- **Report:** 119220 | https://hackerone.com/reports/119220
- **Submitted:** 2016-02-28
- **Reporter:** bugdisclose
- **Program:** MoPub
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling CNAME
- **CVEs:** None
- **Category:** uncategorised

## Summary
The subdomain web.mopub.com was configured with a CNAME pointing to DYN's DNS service, but the corresponding host was never claimed/configured on the DYN platform. This allowed an attacker to register the unclaimed host on DYN and assume control of the subdomain. The attacker could then serve arbitrary content from web.mopub.com, enabling phishing, malware distribution, or credential harvesting.

## Attack scenario
1. Attacker discovers that web.mopub.com CNAME points to a DYN hostname
2. Attacker verifies the hostname is not claimed on DYN's platform
3. Attacker registers/claims the unclaimed hostname on DYN
4. Attacker gains DNS resolution control for web.mopub.com
5. Attacker hosts malicious content at web.mopub.com (phishing page, malware, etc.)
6. Users trusting MoPub domain are compromised via the attacker-controlled subdomain

## Root cause
MoPub created a DNS CNAME record pointing to DYN without ensuring the target hostname was properly claimed and configured on the DYN platform, leaving it in an orphaned state that could be claimed by any DYN user.

## Attacker mindset
Opportunistic reconnaissance followed by quick claim of unregistered infrastructure. Attackers systematically scan for dangling CNAINEs pointing to popular DNS/hosting providers and attempt to claim unconfigured hosts to compromise trusted domains.

## Defensive takeaways
- Audit all DNS CNAME records and verify corresponding hosts are claimed on target platforms
- Implement monitoring to detect dangling DNS records pointing to third-party services
- Remove DNS entries for subdomains no longer in use or not properly configured
- Regularly scan for subdomain takeover vulnerabilities using automated tools
- Coordinate DNS infrastructure changes with third-party platform teams
- Maintain inventory of all DNS records and their corresponding configurations

## Variant hunting
Search for other unclaimed subdomains pointing to common DNS providers (Route53, Cloudflare, Heroku, GitHub Pages, Azure, AWS S3). Check for CNAME records pointing to: dyn.com, dnsmadeeasy.com, cloudflare.com, route53.amazonaws.com, github.io, herokuapp.com, azurewebsites.net

## MITRE ATT&CK
- T1584.001 - Acquire Infrastructure: Domains
- T1583.001 - Acquire Infrastructure: Domains
- T1190 - Exploit Public-Facing Application

## Notes
Reporter references issue #32825 suggesting similar subdomain takeover issues existed previously. This indicates systemic DNS management problems at MoPub. Dangling CNAME records are one of the most common and easily exploitable infrastructure vulnerabilities.

## Full report
<details><summary>Expand</summary>

Hey !

Your subdomain web.mopub.com is pointing to DYN but you have not claimed it on DYN end.

So what happens here is actually that, since web.mopub.com is pointing to DYN, DYNis actually checking if there's a host with that name. Which in this case was not true. So I was able to claim the domain for my own host, and thus, can place content on this URL.

You should immediately remove the DNS-entry for web.mopub.com pointing to DYN

The issue is bit on same concept of #32825

</details>

---
*Analysed by Claude on 2026-05-24*
