# Subdomain Takeover via Instapage CNAME Misconfiguration

## Metadata
- **Source:** HackerOne
- **Report:** 159156 | https://hackerone.com/reports/159156
- **Submitted:** 2016-08-14
- **Reporter:** geekboy
- **Program:** HackerOne
- **Bounty:** Not specified in report
- **Severity:** Critical
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, CNAME Dangling Pointer
- **CVEs:** None
- **Category:** infra-cloud

## Summary
HackerOne's main domain (hacker.one) was vulnerable to subdomain takeover through a dangling CNAME record pointing to Instapage. An attacker could claim the unclaimed Instapage account and serve arbitrary content on the primary domain, enabling phishing attacks, malware distribution, or complete brand compromise.

## Attack scenario
1. Attacker identifies that hacker.one has a CNAME record pointing to Instapage infrastructure
2. Attacker verifies the Instapage account/subdomain is unclaimed or orphaned
3. Attacker creates or takes over the Instapage account associated with the CNAME target
4. Attacker configures the Instapage account to serve malicious content (e.g., fake login page, phishing site)
5. Victim visits hacker.one and receives attacker-controlled content from the redirected Instapage domain
6. Attacker steals credentials, distributes malware, or damages HackerOne's reputation

## Root cause
HackerOne maintained a CNAME DNS record pointing to Instapage infrastructure without verifying the target domain remained active and claimed. When Instapage account was deprovisioned or became unclaimed, the CNAME became dangling, allowing any attacker to claim the orphaned Instapage account and hijack the DNS resolution.

## Attacker mindset
Opportunistic reconnaissance - discovered low-hanging fruit through DNS enumeration. Recognized that major companies often have legacy third-party service integrations with forgotten CNAME records. Exploited lack of DNS hygiene to gain control of a high-value domain for phishing, credential harvesting, or brand impersonation.

## Defensive takeaways
- Implement regular DNS audits to identify and remove unused CNAME records pointing to third-party services
- Maintain inventory of all external services and their DNS bindings with deprecation dates
- Use DNS monitoring tools to detect dangling DNS records and alert on suspicious changes
- Implement DNSSEC and CAA records to prevent unauthorized domain control
- Require verification that target domains are still active before maintaining CNAME records
- Use subdomain takeover scanning tools during security testing
- Implement stricter change control processes for DNS modifications
- Monitor third-party service status and remove CNAMEs when services are decommissioned

## Variant hunting
Search for dangling CNAME records pointing to: AWS CloudFront, GitHub Pages, Heroku, Shopify, Azure, Fastly, Firebase Hosting, Zendesk, Intercom, and other popular SaaS platforms. Scan wildcard CNAME records and subdomain patterns in scope.

## MITRE ATT&CK
- T1190
- T1587.001
- T1566.002
- T1583.001

## Notes
This is a classic subdomain takeover vulnerability. The reporter's remediation advice is sound - immediate removal of the dangling CNAME is appropriate while pursuing vendor patch. The vulnerability is trivial to verify and exploit once discovered. High-value target (main domain of security platform) amplifies impact. Report demonstrates responsible disclosure methodology.

## Full report
<details><summary>Expand</summary>

Hello 
HackerOne Sec Team,

####Description :
> This report is about domain takeover of __hacker.one__ via __instapage 0day__ issue which i just found .



####Step To Verify : 
+ Visit : https://www.hacker.one
+ You will see some html updated by me.

####Impact : 
+ as its one of offical website of hackerone , so attacker can serve anything like login page or etc as he have complete access to main domain ! 

####Possible Fix :
+ For now just remove the cname of instapage , till i try to contact them and get complete fix .


Please let me know if any more info needed !

-------------
**Regards**
*Geekboy !*

</details>

---
*Analysed by Claude on 2026-05-24*
