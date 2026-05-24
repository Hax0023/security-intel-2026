# Subdomain Takeover – www.jet.acronis.com pointing to unclaimed Webflow service

## Metadata
- **Source:** HackerOne
- **Report:** 953719 | https://hackerone.com/reports/953719
- **Submitted:** 2020-08-08
- **Reporter:** sumgr0
- **Program:** Acronis
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** subdomain takeover, dangling DNS record, unclaimed external service, insecure domain delegation
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain www.jet.acronis.com was pointing to an unclaimed Webflow service, allowing an attacker to claim the Webflow domain and take control of the subdomain. This classic subdomain takeover vulnerability could enable phishing, malware distribution, and credential theft attacks against Acronis users.

## Attack scenario
1. Attacker identifies www.jet.acronis.com resolves to Webflow's default 404 page
2. Attacker creates a Webflow account and upgrades to paid plan to enable custom domain configuration
3. Attacker navigates to Webflow portal and claims www.jet.acronis.com as a custom domain in their project settings
4. Attacker completes domain verification and gains full control over content served on www.jet.acronis.com
5. Attacker hosts phishing page, malware, or redirects traffic to malicious site to compromise Acronis users
6. Attacker obtains SSL certificate for the subdomain via Let's Encrypt for HTTPS legitimacy

## Root cause
Acronis created a DNS CNAME record pointing www.jet.acronis.com to Webflow infrastructure but failed to claim/maintain the corresponding Webflow project, leaving the subdomain in an unclaimed state. No periodic audit of DNS records and external service claims was performed to detect orphaned resources.

## Attacker mindset
Opportunistic attacker conducting reconnaissance on domain infrastructure, identifying low-hanging fruit in unclaimed external service delegations. Motivated by ability to conduct high-impact attacks (phishing, malware) against a trusted brand with minimal technical barriers.

## Defensive takeaways
- Maintain comprehensive inventory of all DNS records and external service delegations (Webflow, Heroku, GitHub Pages, etc.)
- Implement domain claim verification process: automatically verify all delegated services remain claimed and under organizational control
- Conduct regular subdomain enumeration and DNS audits to identify dangling records pointing to unclaimed external services
- Establish clear offboarding procedures: when discontinuing use of external services, immediately unconfigure DNS records
- Use DNS monitoring tools to alert on unexpected changes or unresolved/default responses from delegated subdomains
- Implement Content Security Policy (CSP) headers on primary domain to restrict framing/redirection attacks from compromised subdomains
- Require MFA and IP whitelisting on all third-party service accounts managing company subdomains
- Monitor certificate transparency logs for unauthorized SSL certificates issued for company domains/subdomains

## Variant hunting
Search for other Acronis subdomains pointing to unclaimed services: GitHub Pages (404 on domain not found), Heroku (Application Error page), Shopify (Oops page), Desk.com, Zendesk, and other SaaS platforms. Check for similar patterns across parent domain acronis.com and related acquisitions. Look for subdomains in DNS records that no longer resolve or return default service pages.

## MITRE ATT&CK
- T1199
- T1583.001
- T1583.002
- T1589.001
- T1598.002
- T1566.002
- T1190

## Notes
Reporter responsibly claimed the Webflow domain to prevent malicious actor exploitation prior to Acronis remediation. This represents a classic and well-documented class of vulnerabilities (detectify 2014+). The vulnerability is trivial to exploit once identified—requires only account creation on the external service. Webflow's paid-tier requirement for custom domains adds minor friction but does not prevent exploitation. Let's Encrypt auto-issuance of certificates for unverified domains amplifies impact by enabling HTTPS impersonation attacks.

## Full report
<details><summary>Expand</summary>

Hi Team,

Greetings!

I've come across another subdomain**www.jet.acronis.com** of **acronis.com** pointing to an unclaimed Webflow service. Visiting the www.jet.acronis.com returned the default 404 page for Webflow service, thereby making it potential for subdomain takeover.
F940499

Similar to the previous report #952166, on checking at Webflow Portal using a basic paid plan, the **www.jet.acronis.com** was discovered to be currently unclaimed/expired and hence allowing anyone to register the same. On completion of the setup process on Amazon using the same sub-domain name, the person shall have full control over the content of the sub-domain of **acronis.com**. The attacker may then host malicious content on the website or may redirect the visitor to another malicious website to spread a malware/virus.


### PoC

- Visit https://www.jet.acronis.com
- You'll come a page with a generic message
- Check sources for the PoC message

F940501


### Steps to Reproduce:

1. Create webflow account
2. Upgrade to basic paid option to enable custom domain setup
3. Create a site
4. Go to Project Settings > Hosting
5. Scroll down to custom domains section and add www.jet.acronis.com to setup


### See also

- https://labs.detectify.com/2014/10/21/hostile-subdomain-takeover-using-herokugithubdesk-more/  
- https://0xpatrik.com/subdomain-takeover/
- https://medium.com/@ajdumanhug/subdomain-takeover-through-external-services-f0f7ee2b93bd  
- http://yassineaboukir.com/blog/neglected-dns-records-exploited-to-takeover-subdomains/  


### Additional note

I've claimed the resource to prevent a bad actor from doing so in the meantime.


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
