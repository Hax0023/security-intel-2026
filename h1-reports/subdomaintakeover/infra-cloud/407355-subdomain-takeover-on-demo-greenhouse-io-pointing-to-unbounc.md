# Subdomain Takeover on demo.greenhouse.io pointing to Unbounce

## Metadata
- **Source:** HackerOne
- **Report:** 407355 | https://hackerone.com/reports/407355
- **Submitted:** 2018-09-08
- **Reporter:** ninadmathpati
- **Program:** Greenhouse
- **Bounty:** Not specified
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** infra-cloud

## Summary
The subdomain demo.greenhouse.io contains a CNAME record pointing to unbouncepages.com, a service that appears to be no longer actively used by Greenhouse. An attacker with a paid Unbounce account could claim this subdomain and host malicious content impersonating Greenhouse. This enables phishing attacks, malware distribution, and brand reputation damage.

## Attack scenario
1. Attacker identifies demo.greenhouse.io CNAME pointing to unbouncepages.com via DNS enumeration
2. Attacker purchases an Unbounce paid subscription (approximately $150-200)
3. Attacker creates a new Unbounce page and adds CNAME record demo.greenhouse.io
4. Attacker claims ownership of the subdomain within Unbounce's platform
5. Attacker hosts a fake login page or malicious content on the claimed subdomain
6. Users attempting to access demo.greenhouse.io are redirected to attacker's malicious page, enabling credential theft or malware infection

## Root cause
Greenhouse maintains an active DNS CNAME record for demo.greenhouse.io pointing to Unbounce without actively hosting content on that Unbounce account. When the hosting service was deprioritized or account abandoned, the DNS record was not cleaned up, creating an orphaned subdomain vulnerable to takeover.

## Attacker mindset
An attacker with modest financial resources ($150-200) can claim this high-profile subdomain and leverage Greenhouse's brand trust to conduct sophisticated social engineering attacks, credential harvesting, or malware distribution. The demo subdomain, while appearing less critical than primary domains, still maintains significant user trust and accessibility.

## Defensive takeaways
- Implement regular DNS audits to identify and remove dangling CNAME records pointing to external services
- Establish a policy requiring DNS records to be deprovisioned when underlying services are discontinued or deprioritized
- Monitor for subdomain takeover vulnerabilities using automated tools (e.g., SubdomainTakeover, can-i-take-over-xyz)
- Claim all company subdomains on third-party hosting services even if not actively used, or remove the DNS records entirely
- Implement DNSSEC to prevent DNS hijacking attacks
- Use subdomain monitoring services to detect unauthorized changes to DNS configurations
- Establish incident response procedures for subdomain takeover scenarios

## Variant hunting
Search for other Greenhouse subdomains with CNAME records pointing to deprecated services (Heroku, GitHub Pages, Desk.com, Shopify, etc.). Check for similar patterns across dev, staging, api, and legacy subdomains. Examine WHOIS and DNS history for recently abandoned external service integrations.

## MITRE ATT&CK
- T1583.001
- T1589.001
- T1598.003
- T1566.002

## Notes
The reporter noted they could not afford the Unbounce subscription to provide a complete PoC but correctly identified the vulnerability chain. This report is marked as duplicate of report #38007, suggesting Greenhouse may have been previously notified of similar subdomain takeover issues. The demo.greenhouse.io subdomain appears to be a lower-priority target but still carries significant risk for credential harvesting given its association with the Greenhouse brand. Unbounce's service architecture inherently allows subdomain takeover if proper DNS cleanup is not performed by organizations using their platform.

## Full report
<details><summary>Expand</summary>

Actuall this report is same as of this one:- https://hackerone.com/reports/38007  


Subdomain takeover vulnerabilities occur when a subdomain (subdomain.example.com) is pointing to a service (e.g. GitHub pages, Heroku, etc.) that has been removed or deleted. This allows an attacker to set up a page on the service that was being used and point their page to that subdomain. For example, if subdomain.example.com was pointing to a GitHub page and the user decided to delete their GitHub page, an attacker can now create a GitHub page, add a CNAME file containing subdomain.example.com, and claim subdomain.example.com.

Here there is a greenhouse domain  (demo.greenhouse.io) which is pointing towards unbounce pages so  this domain can be taken over can can be used to do any type of attacks mostly i can make a fake login page on your behalf and spoof your users, this is a critical vulnerability and needs to be fixed .

Vulnerable url : demo.greenhouse.io

PoC
Snapshot of the vulnerable page(actually for taking over from unbounce i need to take a paid subscription hich is of higher cost neraly 150-200$ i cannot afford that so as a poc i m showing you a vulnerable page hoping this should work )

cname: unbouncepages.com
Name: demo.greenhouse.io
Type: CNAME
Class: IN

## Impact

Impact
Risk
fake website
malicious code injection
users tricking
company impersonation
This issue can have really huge impact on the companies reputation someone could post malicious content on the compromised site and then your users will think it's official but it's not.

Remediation
Remove the cname entry or claim the subdomain demo.greenhouse.io on unbounce.com

See also
https://github.com/EdOverflow/can-i-take-over-xyz#unbounce
https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/
https://0xpatrik.com/subdomain-takeover/
https://medium.com/@ajdumanhug/subdomain-takeover-through-external-services-f0f7ee2b93bd
http://yassineaboukir.com/blog/neglected-dns-records-exploited-to-takeover-subdomains/



Best regards,
Hacker2202

</details>

---
*Analysed by Claude on 2026-05-24*
