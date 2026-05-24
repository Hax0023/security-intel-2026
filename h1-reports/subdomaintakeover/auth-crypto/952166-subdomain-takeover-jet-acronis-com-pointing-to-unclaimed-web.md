# Subdomain Takeover – jet.acronis.com pointing to unclaimed Webflow service

## Metadata
- **Source:** HackerOne
- **Report:** 952166 | https://hackerone.com/reports/952166
- **Submitted:** 2020-08-06
- **Reporter:** sumgr0
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Dangling DNS Record
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain jet.acronis.com was configured with a CNAME record pointing to proxy-ssl.webflow.com, but the corresponding Webflow service was unclaimed/expired. This allowed an attacker to register the same custom domain in Webflow and gain full control over the subdomain, enabling hosting of malicious content or phishing campaigns under the legitimate Acronis domain.

## Attack scenario
1. Attacker discovers that jet.acronis.com resolves to an unclaimed Webflow service by visiting the domain and observing the default Webflow 404 page
2. Attacker creates a Webflow account and upgrades to a paid plan to enable custom domain configuration
3. Attacker navigates to Project Settings > Hosting > Custom Domains section in Webflow portal
4. Attacker adds jet.acronis.com as a custom domain for their malicious Webflow site and completes domain verification
5. Attacker gains full control over jet.acronis.com and hosts phishing pages, malware, or redirects to malicious sites
6. Victims visiting jet.acronis.com are presented with attacker-controlled content, potentially leading to credential theft, malware infection, or social engineering attacks

## Root cause
Acronis created a CNAME DNS record pointing jet.acronis.com to proxy-ssl.webflow.com but failed to claim/register the corresponding custom domain in the Webflow service. When the Webflow project was abandoned or domain registration lapsed, the DNS record became a dangling pointer that any Webflow user could claim by registering the same custom domain.

## Attacker mindset
An opportunistic attacker scanning for subdomain takeover vulnerabilities would recognize this as an easy target since Webflow explicitly allows users to claim unclaimed domains. The attacker can leverage the legitimate Acronis brand authority to conduct phishing campaigns, distribute malware, or steal credentials with minimal effort and high credibility.

## Defensive takeaways
- Regularly audit all DNS records (CNAME, A, MX, etc.) to identify and remediate dangling records pointing to external services
- Implement a process to claim/verify all custom domains in third-party services (Webflow, Heroku, GitHub Pages, etc.) to prevent takeover
- Use DNS monitoring and alerting tools to detect unauthorized changes or unclaimed external service pointers
- Establish a subdomain inventory and lifecycle management system to track which subdomains are in use and which can be decommissioned
- Consider implementing CAA (Certification Authority Authorization) DNS records to restrict SSL certificate issuance for your domains
- Periodically test subdomains for takeover vulnerabilities using automated scanning tools
- Require domain claim/verification steps before allowing DNS delegation to external services in your deployment processes

## Variant hunting
Search for similar patterns: other subdomains pointing to Webflow (proxy-ssl.webflow.com, webflow.io), GitHub Pages (github.io), Heroku (herokuapp.com), AWS CloudFront, Azure services, Firebase hosting, Vercel, Netlify, or other PaaS/SaaS platforms. Examine CNAME records for all subdomains to identify those pointing to external services that may not be claimed by the organization.

## MITRE ATT&CK
- T1190
- T1583.001
- T1588.003
- T1608.004
- T1598.003
- T1566.002

## Notes
The researcher demonstrated responsible disclosure by claiming the domain themselves to prevent malicious actors from exploiting it while waiting for Acronis to remediate. The impact assessment correctly identifies multiple attack vectors including phishing, malware distribution, XSS, and SSL certificate abuse. This vulnerability exemplifies why DNS hygiene and external service management are critical for organizations using distributed hosting platforms.

## Full report
<details><summary>Expand</summary>

Hi Team,

Greetings!

I've come across **jet.acronis.com** of **acronis.com** pointing to an unclaimed Webflow service. Visiting the jet.acronis.com returned the default 404 page for Webflow service, thereby making it potential for subdomain takeover.
F937948


**jet.acronis.com** CNAME pointed to **proxy-ssl.webflow.com**. On checking at Webflow Portal using a basic paid plan, the **jet.acronis.com** was discovered to be currently unclaimed/expired and hence allowing anyone to register the same. On completion of the setup process on Amazon using the same sub-domain name, the person shall have full control over the content of the sub-domain of **acronis.com**. The attacker may then host malicious content on the website or may redirect the visitor to another malicious website to spread a malware/virus.


### PoC

- Visit https://jet.acronis.com
- You'll come a page with brand logo (to ensure visibility to the visitors)
- Check sources for the PoC message

F937949

### Steps to Reproduce:

1. Create webflow account
2. Upgrade to basic paid option to enable custom domain setup
3. Create a site
4. Go to Project Settings > Hosting
5. Scroll down to custom domains section and add jet.acronis.com to setup


### See also

- https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/  
- https://0xpatrik.com/subdomain-takeover/
- https://medium.com/@ajdumanhug/subdomain-takeover-through-external-services-f0f7ee2b93bd  
- http://yassineaboukir.com/blog/neglected-dns-records-exploited-to-takeover-subdomains/  


### Additional note

- I've claimed the resource to prevent a bad actor from doing so in the meantime.


### Mitigation

- Claim the custom domain in Webflow portal, after confirmation of releasing the same by myself

Best,
@sumgr0

## Impact

Sub-domain Takeover may lead to below consequences:

- Phishing / Spear Phishing
- Malware distribution
- XSS
- Authentication bypass and more
- Credential stealing

Sub-domain Takeover may also allow for SSL certificate be generated with ease, since few certificate authorities like Let's Encrypt requires only domain verification.

</details>

---
*Analysed by Claude on 2026-05-24*
