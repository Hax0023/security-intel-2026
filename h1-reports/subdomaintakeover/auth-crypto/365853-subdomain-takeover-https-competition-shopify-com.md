# Subdomain Takeover - competition.shopify.com via Unclaimed Heroku Custom Domain

## Metadata
- **Source:** HackerOne
- **Report:** 365853 | https://hackerone.com/reports/365853
- **Submitted:** 2018-06-14
- **Reporter:** llt4l
- **Program:** Shopify
- **Bounty:** Not specified in report
- **Severity:** high
- **Vuln:** Subdomain Takeover, DNS Misconfiguration, Abandoned Third-Party Service
- **CVEs:** None
- **Category:** auth-crypto

## Summary
The subdomain competition.shopify.com was vulnerable to takeover as it contained a CNAME record pointing to an unclaimed Heroku custom domain (competition.shopify.com.herokudns.com). An attacker could claim the custom domain in Heroku and serve arbitrary content under the trusted Shopify domain, including malicious JavaScript, phishing pages, or malware.

## Attack scenario
1. Attacker discovers competition.shopify.com CNAME record resolves to competition.shopify.com.herokudns.com
2. Attacker verifies the custom domain is unclaimed in Heroku by attempting to add it to a Heroku application
3. Attacker successfully claims the custom domain and associates it with their Heroku application
4. Attacker deploys malicious content or phishing page to their Heroku app, now accessible via competition.shopify.com
5. Victims visit competition.shopify.com, trusting the Shopify domain and SSL certificate
6. Attacker harvests credentials, injects malware, steals cookies, or performs other attacks leveraging domain trust

## Root cause
Shopify maintained a DNS CNAME record pointing to a Heroku custom domain that was no longer in use or was never claimed, creating a dangling DNS reference. Shopify failed to remove or update the DNS record when the Heroku service association ended.

## Attacker mindset
Opportunistic reconnaissance identifying abandoned DNS configurations. The attacker demonstrated responsible disclosure by claiming the domain defensively and providing proof-of-concept rather than exploiting it maliciously. This shows white-hat intent to alert the company to a critical vulnerability before a malicious actor could exploit it.

## Defensive takeaways
- Maintain inventory of all DNS records and regularly audit CNAME entries pointing to third-party services
- Implement automated monitoring to detect dangling DNS records pointing to unclaimed external services
- Establish deprecation procedures that require removal of DNS records when retiring third-party service integrations
- Regularly scan subdomains against known hosting providers (Heroku, AWS, Azure, etc.) to identify unclaimed services
- Use DNS validation and DNSSEC where applicable to prevent unauthorized domain claims
- Implement certificate transparency monitoring to detect unauthorized certificates issued for company domains
- Conduct periodic security audits of all subdomains and their configurations

## Variant hunting
Scan all Shopify subdomains for similar CNAME records pointing to other hosting providers (AWS S3, GitHub Pages, Fastly, etc.)
Check for CNAME records pointing to other Heroku endpoints across Shopify's domain portfolio
Identify subdomains with MX or TXT records pointing to unclaimed email services (SendGrid, Mailgun, etc.)
Search for CNAME records with typos or partial configurations suggesting abandoned services
Check wildcard DNS entries that might include unclaimed subdomains

## MITRE ATT&CK
- T1190
- T1199
- T1566.002

## Notes
This report demonstrates responsible disclosure best practices. The researcher defensively claimed the domain to prevent malicious exploitation while providing Shopify with clear remediation steps. The vulnerability has significant impact potential given the trusted nature of Shopify's domain for customers and employees. The report effectively outlines multiple attack scenarios (credential theft, malware distribution, phishing, C2 infrastructure) that could result from successful exploitation. The fix is straightforward (remove CNAME record or reclaim Heroku service), indicating this was likely an oversight rather than a complex misconfiguration.

## Full report
<details><summary>Expand</summary>

Dear Shopify Security Team,

The Shopify.com subdomain competition.shopify.com was vulnerable to a subdomain takeover as it was pointing to an unclaimed Heroku service through the CNAME competition.shopify.com.herokudns.com, while the custom domain 'competition.shopify.com' was unclaimed in Heroku.

To prevent an attacker from claiming the domain and using it for malicious purposes, and also as a proof of concept, I have claimed the domain in Heroku and uploaded a proof of concept, which you can view here: https://competition.shopify.com/329a01fddb5a552265170b02c579c85f.html (I've also redirected visitors of the index page to https://shopify.com)

To fix the issue, there are two possible solutions. If you would like to re-start using Heroku with this domain, I can remove the custom domain from my Heroku app. Otherwise you may choose to delete the entry from your DNS servers, which will also fix the problem.

## Impact

I don't think I need to go into the security implications of a malicious attacker hijacking the domain, but here are a few possible attacks that could be performed if a malicious attacker were to hijack the domain:
* The ability for an attacker to execute JavaScript to steal user cookies and/or using the site as an endpoint for browser exploitation.
* Using the subdomain as a fool-proof phishing site (stealing Shopify customer/employee credentials). SSL has also been enabled, giving end users more trust of the site.
* Defacement of the website, or deployment of a fake site, such as a fake Shopify competition that harvests customer credit card details.
* Spreading of malware, or use of the domain as a C2 server.

I look forward to hearing back from your team.

Regards,
t4

</details>

---
*Analysed by Claude on 2026-05-24*
