# Subdomain Takeover via Dangling CNAME Record - learnstormindia.khanacademy.org

## Metadata
- **Source:** HackerOne
- **Report:** 399165 | https://hackerone.com/reports/399165
- **Submitted:** 2018-08-24
- **Reporter:** avileox
- **Program:** Khan Academy
- **Bounty:** Not specified
- **Severity:** High
- **Vuln:** Subdomain Takeover, Dangling CNAME, DNS Misconfiguration
- **CVEs:** None
- **Category:** infra-cloud

## Summary
A subdomain (learnstormindia.khanacademy.org) contains a CNAME record pointing to an unclaimed Webflow proxy server, enabling potential subdomain takeover. An attacker can register the domain on Webflow and host malicious content under the Khan Academy subdomain, exploiting the legitimate domain for phishing and credential theft.

## Attack scenario
1. Attacker identifies that learnstormindia.khanacademy.org CNAME points to proxy-ssl.webflow.com which returns 404
2. Attacker creates a Webflow account and upgrades to paid tier to enable custom domain registration
3. Attacker adds learnstormindia.khanacademy.org as custom domain in Webflow account
4. Attacker creates fake Khan Academy login page or credential harvesting form on Webflow
5. Users receive phishing emails linking to learnstormindia.khanacademy.org (legitimate subdomain) and enter credentials
6. Attacker harvests credentials and sensitive user data, potentially escalating to XSS or authentication bypass attacks

## Root cause
Dangling CNAME record pointing to external service (Webflow) that was never claimed or has been abandoned. DNS configuration was not properly maintained when the original Webflow project was deleted or deprovisioned, leaving the CNAME record pointing to an available third-party service.

## Attacker mindset
Opportunistic attacker leveraging trust in legitimate domains. The attacker recognizes that a subdomain under khanacademy.org carries inherent trust and legitimacy. By taking over an abandoned CNAME record pointing to a cheap service, they can impersonate Khan Academy services, target users with phishing attacks, and steal credentials or sensitive information with minimal cost ($15 Webflow subscription).

## Defensive takeaways
- Audit all DNS records (A, AAAA, CNAME, MX) for dangling or abandoned entries
- Implement DNS monitoring and alerting for subdomain changes or unclaimed CNAME records
- Remove CNAME records that point to external services no longer in use
- Maintain an inventory of all subdomains and their purposes with ownership tracking
- Consider using DNS security tools that detect dangling DNS records and subdomain takeover risks
- Regularly validate that all DNS entries resolve to active, authorized services
- Implement DNSSEC to prevent DNS hijacking and unauthorized modifications
- Use CAA records to restrict certificate issuance for subdomains to authorized CAs only

## Variant hunting
Search for other dangling CNAME records across *.khanacademy.org namespace
Identify subdomains pointing to GitHub Pages, Heroku, AWS, or other third-party services that may be unclaimed
Check for MX records pointing to deprovisioned mail services
Look for NS records delegating to name servers no longer maintained by organization
Scan for subdomains with 404/NXDOMAIN responses that still have active DNS records
Test subdomains pointing to common platforms (Webflow, Wix, Wordpress, Shopify, etc.) for takeover feasibility

## MITRE ATT&CK
- T1584.001
- T1589.001
- T1598.003
- T1566.002
- T1190

## Notes
This is a straightforward subdomain takeover case. The reporter correctly identified the vulnerability but the writeup lacks depth in technical details. The impact assessment is accurate - subdomain takeover enables credential harvesting, phishing, XSS, and malware distribution. The attack requires minimal skill and investment ($15 Webflow account). Khan Academy should immediately audit all DNS records and remove dangling CNAME entries. The 404 response is a clear indicator the Webflow project is unclaimed and available for takeover.

## Full report
<details><summary>Expand</summary>

None of the weakness categories really fit this so I apologize for that.

The subdomain learnstormindia.khanacademy.org  points to 52.203.185.84 a webflow.io proxy server (proxy-ssl.webflow.com). The CNAME entry in the subdomain is pointing to an external page service (learnstormindia.khanacademy.org. 299 IN CNAME proxy-ssl.webflow.com)Because it 404s, this leads me to believe that a subdomain takeover is possible through the webflow service as whatever this is pointing to is unused.
IF it is possible to TAKEOVER 
therefore,by these steps the attacker should takeover this subdomian
1>Creat an account at webflow.io 
2>Creat a webpage(fake login page) to host and add you custom domian learnstormindia.khanacademy.org (for adding custom subdomian you need a paid account of webflow.io someabout $15)

## Impact

Subdomain takeover can be used for several purposes:
1>Malware
2>Phishing / Spear phishing
3>XSS
4>Authentication bypass

ex:-
An attacker can utilize this domain learnstormindia.khanacademy.org for targeting the organization by fake login khanacademy forms, or steal sensitive information of teams (credentials, credit card information, etc)

</details>

---
*Analysed by Claude on 2026-05-24*
