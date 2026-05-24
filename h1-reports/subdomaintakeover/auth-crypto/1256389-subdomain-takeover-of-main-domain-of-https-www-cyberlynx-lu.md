# Subdomain Takeover of www.cyberlynx.lu via Unclaimed Wix DNS Record

## Metadata
- **Source:** HackerOne
- **Report:** 1256389 | https://hackerone.com/reports/1256389
- **Submitted:** 2021-07-09
- **Reporter:** 0xjackal
- **Program:** Acronis
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain www.cyberlynx.lu (acquired by Acronis) contains a CNAME record pointing to an unclaimed Wix DNS service (www118.wixdns.net). An attacker can register or claim this abandoned Wix resource and gain control of the subdomain, enabling them to serve malicious content under the victim's domain.

## Attack scenario
1. Attacker performs DNS enumeration and discovers www.cyberlynx.lu CNAME chain pointing to Wix infrastructure
2. Attacker verifies the subdomain returns HTTP 404 or connects to unclaimed Wix service
3. Attacker navigates to Wix's domain registration/claims process for the specific DNS endpoint
4. Attacker registers or claims the www118.wixdns.net resource in their own Wix account
5. Attacker configures the Wix resource to serve malicious content, phishing pages, or malware
6. Victims accessing www.cyberlynx.lu are redirected to attacker-controlled content via DNS resolution

## Root cause
Acronis acquired cyberlynx.lu but failed to properly decommission or remove DNS CNAME records pointing to third-party services. The Wix DNS endpoint was abandoned without being reclaimed or the DNS record being deleted, creating a dangling pointer vulnerability.

## Attacker mindset
An attacker would identify this as a low-effort, high-impact opportunity to compromise a corporate domain's subdomain. The ease of claiming abandoned third-party services combined with the trust users have in the parent domain makes this attractive for phishing, malware distribution, or brand damage campaigns.

## Defensive takeaways
- Maintain an inventory of all DNS records and subdomains across acquired companies
- Implement regular DNS audits to identify and remove dangling or orphaned CNAME records
- When decommissioning third-party services, remove corresponding DNS records immediately
- Monitor for unclaimed/dangling DNS pointers using automation tools
- Establish CNAME validation procedures during M&A integration
- Consider using DNS providers with features to alert on unused or misconfigured records
- Implement certificate transparency monitoring to detect unauthorized certificate issuance
- Use DNSSEC and CAA records to prevent DNS hijacking attacks

## Variant hunting
Scan other Acronis acquired company domains for similar dangling CNAME records
Search for other Acronis subdomains pointing to third-party CDNs (Akamai, CloudFlare, etc.)
Identify other companies with acquisitions and check their DNS for similar misconfigurations
Look for CNAME chains with multiple hops where intermediate services are unclaimed
Check for Wix DNS records across different organizations in the same industry
Hunt for NS records pointing to third-party nameservers that may be unmanaged

## MITRE ATT&CK
- T1190
- T1200
- T1583.001
- T1589.001

## Notes
This is a classic subdomain takeover vulnerability dependent on third-party service claim processes. The severity is high due to the main domain association and potential for brand damage. Similar report (H1 #1183296) indicates this is a known attack pattern. The fix is straightforward: remove the CNAME record or reclaim the Wix resource. The report lacks technical depth (no HTTP header analysis, no screenshot of actual takeover) but the vulnerability is clearly exploitable.

## Full report
<details><summary>Expand</summary>

## Summary
Hi Acronis Security Team , Hope you well.
I found one of your subdomains which is `www.cyberlynx.lu` (One of your Acquisition)  is pointing towards

`
www.cyberlynx.lu	canonical name = www118.wixdns.net.
www118.wixdns.net	canonical name = balancer.wixdns.net.
balancer.wixdns.net	canonical name = f7a0737a-balancer.wixdns.net.
f7a0737a-balancer.wixdns.net	canonical name = td-balancer-dc11-60-102.wixdns.net.
`
see the following:-

{F1371299}

{F1371300}

And it is unclaimed

##Steps To Reproduce:
    1. Go to http://site.therealreal.com , Gives 404
    2. the domain pointing towards to WIX cdn
    3. Anyone can claim this subdomain
 
##Similar report at H1:-
- https://hackerone.com/reports/1183296

Please let me know if need more info , OR need for poc video
Best Regards.
@doosec101

## Impact

An attacker can claim this subdomain by requesting a process of registering this abandoned subdomain to his name.
And attacker can fully take over this subdomain and do whatever he wants. this can cause huge damage to the website's main domain as well as to the company.

**I Recommend removing  the Cname and DNS connecting to it.**

</details>

---
*Analysed by Claude on 2026-05-24*
